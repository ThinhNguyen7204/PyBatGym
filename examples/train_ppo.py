"""
Example script for Training Proximal Policy Optimization (PPO) using Stable-Baselines3.
"""
import gymnasium as gym
from stable_baselines3 import PPO

# from pybatgym.envs import PyBatGymEnv
# from pybatgym.observation.simple import SimpleObservationBuilder
# from pybatgym.action.discrete import DiscreteActionMapper
# from pybatgym.reward.metrics import UtilizationRewardCalculator
# from pybatgym.wrappers import TimeLimitWrapper

def main():
    print("Setting up PyBatGym Environment...")
    # NOTE: This requires BatSim to be correctly installed and your PATH to include `batsim`.
    
    # env = PyBatGymEnv(
    #     batsim_command=["batsim", "-p", "platform.xml", "-w", "workload.json", "-e", "/tmp/batsim_export"],
    #     observation_builder=SimpleObservationBuilder(max_jobs=100),
    #     action_mapper=DiscreteActionMapper(max_queue_size=100),
    #     reward_calculator=UtilizationRewardCalculator(max_resources=128)
    # )
    
    # Wrap environment
    # env = TimeLimitWrapper(env, max_sim_time=3600*24) # 1 day simulated time

    print("Initializing PPO Model...")
    # model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_tensorboard/")
    
    print("Starting Training...")
    # model.learn(total_timesteps=100000)
    
    print("Saving Model...")
    # model.save("ppo_pybatgym_model")
    
    print("Done!")

if __name__ == "__main__":
    main()
