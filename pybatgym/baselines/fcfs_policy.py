from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pybatgym.envs import PyBatGymEnv

def fcfs_policy(env: PyBatGymEnv) -> int:
    """First-Come-First-Served: schedule the oldest pending job."""
    state = env._state
    pending_jobs = state.get("pending_jobs", [])
    if not pending_jobs:
        return env.action_space.n - 1  # WAIT

    sorted_jobs = sorted(pending_jobs, key=lambda j: j.submit_time)
    resource = state.get("resource")
    
    for i, job in enumerate(sorted_jobs):
        if resource.can_allocate(job.requested_resources):
            return i

    return len(sorted_jobs)  # WAIT
