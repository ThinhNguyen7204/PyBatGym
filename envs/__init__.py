"""
Environment Layer for PyBatGym

1. Design Review:
This module contains `PyBatGymEnv`, which is the core `gymnasium.Env` implementation.
It handles bridging the RL training loop (reset, step) with the `BatSimAdapter`.
It uses dependency injection for observation building, action mapping, and reward calculation to ensure maximum flexibility and modularity. 

2. Code:
Implemented in `pybatgym_env.py`.

3. Usage Example:
```python
from pybatgym.envs import PyBatGymEnv

env = PyBatGymEnv(
    batsim_command=["batsim", "-p", "platform.xml", "-w", "workload.json"],
    # observation_builder=MyObsBuilder(),
    # action_mapper=MyActionMapper(),
    # reward_calculator=MyRewardCalc()
)
obs, info = env.reset()
done = False
while not done:
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
env.close()
```

4. Testing Snippet:
See `tests/test_envs_module.py` for ensuring the gymnasium API is respected.
"""

from .pybatgym_env import PyBatGymEnv

__all__ = ["PyBatGymEnv"]
