import unittest
from pybatgym.plugins import PyBatGymPlugin, PluginManager

class MockEnv:
    pass

class MockPlugin(PyBatGymPlugin):
    def __init__(self):
        self.reset_called = False
        self.step_called = False
        self.episode_end_called = False
        
    def on_reset(self, env, obs, info):
        self.reset_called = True
        
    def on_step(self, env, action, obs, reward, terminated, truncated, info):
        self.step_called = True
        
    def on_episode_end(self, env):
        self.episode_end_called = True

class TestPlugins(unittest.TestCase):
    def test_plugin_dispatch(self):
        env = MockEnv()
        plugin = MockPlugin()
        manager = PluginManager([plugin])
        
        manager.dispatch_reset(env, None, {})
        self.assertTrue(plugin.reset_called)
        
        manager.dispatch_step(env, 0, None, 1.0, False, False, {})
        self.assertTrue(plugin.step_called)
        self.assertFalse(plugin.episode_end_called)
        
        manager.dispatch_step(env, 0, None, 1.0, True, False, {})
        self.assertTrue(plugin.episode_end_called)

if __name__ == "__main__":
    unittest.main()
