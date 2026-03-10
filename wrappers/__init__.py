"""
Wrappers Layer for PyBatGym

1. Design Review:
Compatible with standard Gymnasium pipelines and `Stable-Baselines3`.
Provides utilities to restrict simulation time duration properly (via BatSim's internal time) and allows Action Masking.

2. Code:
Implemented in:
- `wrappers.py`: `TimeLimitWrapper` and `ActionMaskWrapper`.

3. Usage Example:
```python
from pybatgym.envs import PyBatGymEnv
from pybatgym.wrappers import TimeLimitWrapper, ActionMaskWrapper

env = PyBatGymEnv(...)
env = TimeLimitWrapper(env, max_sim_time=3600*24)
env = ActionMaskWrapper(env)
```
"""

from .wrappers import TimeLimitWrapper, ActionMaskWrapper

__all__ = ["TimeLimitWrapper", "ActionMaskWrapper"]
