"""Baseline benchmark plugins for PyBatGym.

Implements classic HPC scheduling heuristics (FCFS, SJF, EASY) as reference baselines
for comparing RL agent performance.
"""

from __future__ import annotations

import time
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from pybatgym.envs import PyBatGymEnv

from pybatgym.plugins.registry import Plugin
from .fcfs_policy import fcfs_policy
from .sjf_policy import sjf_policy
from .easy_backfilling_policy import easy_backfilling_policy


def run_baseline(
    env: PyBatGymEnv,
    policy_fn: Callable[[PyBatGymEnv], int],
    num_episodes: int = 10,
) -> dict[str, float]:
    """Run a baseline policy and collect aggregate metrics."""
    total_reward = 0.0
    total_util = 0.0
    total_wait = 0.0
    total_slowdown = 0.0

    for ep in range(num_episodes):
        obs, info = env.reset(seed=42 + ep)
        done = False
        ep_reward = 0.0

        while not done:
            action = policy_fn(env)
            action = min(action, env.action_space.n - 1)
            
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            ep_reward += reward

        total_reward += ep_reward

        completed = env._adapter.get_completed_jobs()
        if completed:
            makespan = env._adapter.get_current_time()
            total_cores = env._state.get("resource").total_cores
            
            wait_sum = sum(j.waiting_time for j in completed)
            slowdown_sum = sum(j.bounded_slowdown for j in completed)
            busy_time_sum = sum(j.actual_runtime * j.requested_resources for j in completed)

            total_wait += wait_sum / len(completed)
            total_slowdown += slowdown_sum / len(completed)
            if makespan > 0 and total_cores > 0:
                total_util += min(1.0, busy_time_sum / (makespan * total_cores))

    n = max(num_episodes, 1)
    return {
        "avg_reward": total_reward / n,
        "avg_utilization": total_util / n,
        "avg_waiting_time": total_wait / n,
        "avg_slowdown": total_slowdown / n,
    }


class BenchmarkPlugin(Plugin):
    """Plugin to automatically run heuristics and compare with RL agent logs."""

    @property
    def name(self) -> str:
        return "benchmark"

    def __init__(self, run_on_close: bool = True):
        self.run_on_close = run_on_close
        
    def on_close(self) -> None:
        if self.run_on_close:
            print("[BenchmarkPlugin] Environment closed. Run `run_baseline()` manually for comparisons.")
