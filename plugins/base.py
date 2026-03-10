import gymnasium as gym
from typing import Any, Tuple

class PyBatGymPlugin:
    """
    Base class for environment plugins that can hook into the lifecycle
    of a PyBatGym Env. Useful for logging, recording metrics, or
    adding customized behaviors without modifying the core Env object.
    """
    
    def on_init(self, env: gym.Env) -> None:
        """Called when the plugin is attached to the environment."""
        pass
        
    def on_reset(self, env: gym.Env, obs: Any, info: dict) -> None:
        """Called after the environment is reset."""
        pass
        
    def on_step(self, env: gym.Env, action: Any, obs: Any, reward: float, terminated: bool, truncated: bool, info: dict) -> None:
        """Called after an environment step."""
        pass
        
    def on_episode_end(self, env: gym.Env) -> None:
        """Called when an episode terminates (terminated or truncated)."""
        pass
        
    def on_close(self, env: gym.Env) -> None:
        """Called when the environment is closed."""
        pass

class PluginManager:
    """Manages tracking and dispatching events to a list of plugins."""
    
    def __init__(self, plugins: list[PyBatGymPlugin] = None):
        self.plugins = plugins or []
        
    def add_plugin(self, plugin: PyBatGymPlugin, env: gym.Env):
        self.plugins.append(plugin)
        plugin.on_init(env)
        
    def dispatch_reset(self, env: gym.Env, obs: Any, info: dict):
        for plugin in self.plugins:
            plugin.on_reset(env, obs, info)
            
    def dispatch_step(self, env: gym.Env, action: Any, obs: Any, reward: float, terminated: bool, truncated: bool, info: dict):
        for plugin in self.plugins:
            plugin.on_step(env, action, obs, reward, terminated, truncated, info)
            if terminated or truncated:
                plugin.on_episode_end(env)
                
    def dispatch_close(self, env: gym.Env):
        for plugin in self.plugins:
            plugin.on_close(env)
