"""
Plugin Layer for PyBatGym

1. Design Review:
Allows cleanly injecting loggers, visualizers, or extra metric trackers into the RL loop without tangling the core Gym environment code.
An env subclass or a wrapper can utilize `PluginManager` to dispatch events to these hooks.

2. Code:
Implemented in:
- `base.py`: Defines the `PyBatGymPlugin` interface containing `on_init`, `on_reset`, `on_step`, `on_episode_end`, `on_close` hooks and the `PluginManager` singleton tracking them.

3. Usage Example:
```python
from pybatgym.plugins import PyBatGymPlugin, PluginManager

class LoggingPlugin(PyBatGymPlugin):
    def on_step(self, env, action, obs, rew, term, trunc, info):
        print(f"Step taken: rew={rew}")

manager = PluginManager([LoggingPlugin()])
# env could call manager.dispatch_step(...) during its step function.
```
"""

from .base import PyBatGymPlugin, PluginManager

__all__ = ["PyBatGymPlugin", "PluginManager"]
