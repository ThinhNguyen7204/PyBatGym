from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pybatgym.envs import PyBatGymEnv

def easy_backfilling_policy(env: PyBatGymEnv) -> int:
    """EASY Backfilling heuristic policy.

    1. Try to schedule the first (oldest) pending job.
    2. If it doesn't fit, estimate when resources will free up (shadow time).
    3. Backfill smaller jobs that finish before the shadow time.
    """
    state = env._state
    pending_jobs = state.get("pending_jobs", [])
    if not pending_jobs:
        return env.action_space.n - 1

    resource = state.get("resource")
    sorted_jobs = sorted(pending_jobs, key=lambda j: j.submit_time)
    first_job = sorted_jobs[0]

    if resource.can_allocate(first_job.requested_resources):
        return 0  # Schedule the first job

    # --- Estimate shadow time from running jobs ---
    sim_time = env._adapter.get_current_time()
    # Attempting to access internal adapter state for shadow time estimation
    running_jobs_raw = getattr(env._adapter, "_running_jobs", [])
    if not running_jobs_raw:
        return len(sorted_jobs)  # WAIT — nothing running, can't backfill

    # Build (expected_completion_time, cores_freed) list.
    expected_completions = []
    for rj in running_jobs_raw:
        if hasattr(rj, "finish_time") and hasattr(rj, "cores"):
            # MockAdapter _RunningJob
            expected_completions.append((rj.finish_time, rj.cores))
        elif hasattr(rj, "requested_walltime"):
            # Fallback: raw Job object (e.g. RealBatsimAdapter)
            est_finish = sim_time + rj.requested_walltime
            expected_completions.append((est_finish, rj.requested_resources))
    expected_completions.sort()

    freed_cores = resource.free_cores
    shadow_time = sim_time

    for comp_time, cores in expected_completions:
        shadow_time = comp_time
        freed_cores += cores
        if freed_cores >= first_job.requested_resources:
            break

    # Backfill: try smaller jobs that finish before the shadow time
    for i in range(1, len(sorted_jobs)):
        job = sorted_jobs[i]
        if job.requested_resources <= resource.free_cores:
            expected_finish = sim_time + job.requested_walltime
            if expected_finish <= shadow_time:
                return i

    return len(sorted_jobs)
