import gymnasium as gym
from typing import Any, Tuple
import numpy as np

class TimeLimitWrapper(gym.Wrapper):
    """
    Terminates the environment if the simulated time exceeds a limit.
    This works on the simulated 'current_time' rather than step count.
    """
    def __init__(self, env: gym.Env, max_sim_time: float):
        super().__init__(env)
        self.max_sim_time = max_sim_time
        
    def step(self, action: Any) -> Tuple[Any, float, bool, bool, dict]:
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        current_time = info.get("current_time", 0.0)
        if current_time >= self.max_sim_time:
            truncated = True
            
        return obs, reward, terminated, truncated, info


class ActionMaskWrapper(gym.Wrapper):
    """
    Appends a valid action mask to the observation.
    Useful for masking out empty queue slots in Discrete Action spaces.
    Requires the underlying environment or mapper to expose `get_action_mask`.
    """
    def __init__(self, env: gym.Env):
        super().__init__(env)
        original_obs_space = self.env.observation_space
        # Assume observation space is a Dict or we convert Box to Dict
        # For simplicity, if it's already a dict, we add "action_mask"
        # If not, we wrap it in a dict.
        
        if isinstance(original_obs_space, gym.spaces.Dict):
            spaces = dict(original_obs_space.spaces)
            spaces["action_mask"] = gym.spaces.Box(
                low=0, high=1, 
                shape=(self.env.action_space.n,), 
                dtype=np.int8
            )
            self.observation_space = gym.spaces.Dict(spaces)
        else:
            self.observation_space = gym.spaces.Dict({
                "observation": original_obs_space,
                "action_mask": gym.spaces.Box(
                    low=0, high=1, 
                    shape=(self.env.action_space.n,), 
                    dtype=np.int8
                )
            })

    def _get_mask(self) -> np.ndarray:
        # Check if action_mapper exposes waiting jobs to mask them
        if hasattr(self.env, "action_mapper") and hasattr(self.env.action_mapper, "waiting_job_ids"):
            n_jobs = len(self.env.action_mapper.waiting_job_ids)
            n_actions = self.env.action_space.n
            mask = np.zeros(n_actions, dtype=np.int8)
            mask[:n_jobs] = 1
            mask[-1] = 1 # The 'wait' action is always valid
            return mask
        return np.ones(self.env.action_space.n, dtype=np.int8)

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        mask = self._get_mask()
        
        if isinstance(self.env.observation_space, gym.spaces.Dict):
            obs["action_mask"] = mask
            return obs, info
        else:
            return {"observation": obs, "action_mask": mask}, info

    def step(self, action: Any):
        obs, rew, term, trunc, info = self.env.step(action)
        mask = self._get_mask()
        
        if isinstance(self.env.observation_space, gym.spaces.Dict):
            obs["action_mask"] = mask
            return obs, rew, term, trunc, info
        else:
            return {"observation": obs, "action_mask": mask}, rew, term, trunc, info

