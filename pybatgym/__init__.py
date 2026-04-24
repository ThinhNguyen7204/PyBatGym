
__version__ = "0.1.0"

from pybatgym.env import PyBatGymEnv

from gymnasium.envs.registration import register

register(
    id="PyBatGym-v0",
    entry_point="pybatgym.env:PyBatGymEnv",
    kwargs={"config_path": None},
)