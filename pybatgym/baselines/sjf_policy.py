from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pybatgym.envs import PyBatGymEnv

def sjf_policy(env: PyBatGymEnv) -> int:
    """Shortest-Job-First: schedule the job with smallest requested walltime."""
    state = env._state
    pending_jobs = state.get("pending_jobs", [])
    if not pending_jobs:
        return env.action_space.n - 1

    resource = state.get("resource")
    sorted_by_submit = sorted(pending_jobs, key=lambda j: j.submit_time)
    
    candidates = [
        (i, job) for i, job in enumerate(sorted_by_submit)
        if resource.can_allocate(job.requested_resources)
    ]

    if not candidates:
        return len(sorted_by_submit)

    best_idx, _ = min(candidates, key=lambda pair: pair[1].requested_walltime)
    return best_idx
