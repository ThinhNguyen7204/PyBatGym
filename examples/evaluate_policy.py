"""
Example script for Evaluating a trained RL policy using Stable-Baselines3.
"""
from stable_baselines3 import PPO

def main():
    print("Setting up PyBatGym Environment for Evaluation...")
    # env = PyBatGymEnv(...)
    
    print("Loading Model...")
    # model = PPO.load("ppo_pybatgym_model")
    
    print("Evaluating Policy...")
    # obs, info = env.reset()
    # done = False
    # total_reward = 0
    # while not done:
    #     action, _states = model.predict(obs, deterministic=True)
    #     obs, reward, terminated, truncated, info = env.step(action)
    #     total_reward += reward
    #     done = terminated or truncated
        
    # print(f"Episode finished with Total Reward: {total_reward}")

if __name__ == "__main__":
    main()
