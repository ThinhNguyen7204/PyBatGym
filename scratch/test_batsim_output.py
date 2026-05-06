
from pybatgym.env import PyBatGymEnv
from pybatgym.config.loader import load_preset
import time
import os

print("--- Manual BatSim Output Test ---")
config = load_preset('medium_batsim')
config.mode = 'real'
# Ensure prefix is clean
prefix = "/workspace/data/test_out"
os.system("rm -f c:\\Users\\ASUS\\Desktop\\PyBatGym\\data\\test_out*")

env = PyBatGymEnv(config=config)
print("Resetting env...")
obs, _ = env.reset(seed=42)
print("Connected to BatSim.")

done = False
steps = 0
while not done:
    # Always WAIT to see if jobs finish on their own
    obs, reward, terminated, truncated, info = env.step(0) 
    done = terminated or truncated
    steps += 1
    if steps % 10 == 0:
        print(f"Step {steps}...")

print(f"Simulation finished in {steps} steps.")
print("Waiting 5 seconds for BatSim to flush files...")
time.sleep(5)
env.close()
print("Env closed.")
