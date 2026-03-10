import unittest
import numpy as np
import gymnasium as gym
from gymnasium.utils.env_checker import check_env
from unittest.mock import MagicMock, patch

from pybatgym.envs import PyBatGymEnv
from pybatgym.batsim.events import EventType

class TestPyBatGymEnv(unittest.TestCase):
    
    @patch('pybatgym.envs.pybatgym_env.BatSimAdapter')
    def test_env_initialization(self, mock_adapter_class):
        env = PyBatGymEnv(batsim_command=["dummy"])
        self.assertIsInstance(env.observation_space, gym.spaces.Box)
        self.assertIsInstance(env.action_space, gym.spaces.Discrete)
        
    @patch('pybatgym.envs.pybatgym_env.BatSimAdapter')
    def test_env_reset(self, mock_adapter_class):
        # Setup mock behavior
        mock_adapter = mock_adapter_class.return_value
        # When waiting for SIMULATION_BEGIN:
        mock_adapter.recv_message.return_value = {
            "now": 0.0, "events": [{"timestamp": 0.0, "type": "SIMULATION_BEGIN"}]
        }
        
        env = PyBatGymEnv(batsim_command=["dummy"])
        obs, info = env.reset()
        
        self.assertEqual(info["current_time"], 0.0)
        self.assertFalse(env.simulation_ended)
        mock_adapter.launch_batsim.assert_called_once()
        
    @patch('pybatgym.envs.pybatgym_env.BatSimAdapter')
    def test_env_step(self, mock_adapter_class):
        mock_adapter = mock_adapter_class.return_value
        
        # initial reset
        mock_adapter.recv_message.return_value = {
            "now": 0.0, "events": [{"timestamp": 0.0, "type": "SIMULATION_BEGIN"}]
        }
        
        env = PyBatGymEnv(batsim_command=["dummy"])
        env.reset()
        
        # Prepare mock for step where simulation ends
        mock_adapter.recv_message.return_value = {
            "now": 10.0, "events": [{"timestamp": 10.0, "type": "SIMULATION_ENDS"}]
        }
        
        obs, reward, terminated, truncated, info = env.step(0)
        
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertEqual(info["current_time"], 10.0)
        
if __name__ == "__main__":
    unittest.main()
