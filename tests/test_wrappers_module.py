import unittest
import gymnasium as gym
import numpy as np

from pybatgym.wrappers import TimeLimitWrapper, ActionMaskWrapper

class DummyEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(1,))
        self.action_space = gym.spaces.Discrete(5)
        self.current_time = 0.0
        
    def reset(self, seed=None, options=None):
        self.current_time = 0.0
        return np.array([0.0]), {"current_time": self.current_time}
        
    def step(self, action):
        self.current_time += 10.0
        return np.array([0.0]), 1.0, False, False, {"current_time": self.current_time}

class TestWrappersModule(unittest.TestCase):
    def test_time_limit(self):
        env = DummyEnv()
        env = TimeLimitWrapper(env, max_sim_time=25.0)
        
        env.reset()
        _, _, term, trunc, info = env.step(0)
        self.assertFalse(trunc) # time = 10
        
        _, _, term, trunc, info = env.step(0)
        self.assertFalse(trunc) # time = 20
        
        _, _, term, trunc, info = env.step(0)
        self.assertTrue(trunc) # time = 30 >= 25
        
    def test_action_mask(self):
        env = DummyEnv()
        # Mock action mapper state
        class DummyMapper:
            waiting_job_ids = ["j1", "j2"]
        env.action_mapper = DummyMapper()
        
        env = ActionMaskWrapper(env)
        
        obs, _ = env.reset()
        self.assertIn("observation", obs)
        self.assertIn("action_mask", obs)
        # 2 jobs + 1 'wait' action -> [1, 1, 0, 0, 1] for space.n=5
        expected_mask = np.array([1, 1, 0, 0, 1], dtype=np.int8)
        self.assertTrue(np.array_equal(obs["action_mask"], expected_mask))
        

if __name__ == "__main__":
    unittest.main()
