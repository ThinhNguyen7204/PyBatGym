import gymnasium as gym
from gymnasium import spaces
import numpy as np

from pybatgym.observation.base import ObservationBuilder
from pybatgym.batsim.events import BatSimEvent, EventType, JobSubmittedEvent, JobCompletedEvent

class SimpleObservationBuilder(ObservationBuilder):
    """
    A simple observation builder that tracks the number of waiting jobs,
    running jobs, and completed jobs.
    
    Observation Space shape: (3,)
    - [0]: Number of jobs in queue (waiting)
    - [1]: Number of running jobs
    - [2]: Number of completed jobs
    """
    
    def __init__(self, max_jobs: int = 1000):
        self.max_jobs = max_jobs
        self.waiting_jobs = 0
        self.running_jobs = 0
        self.completed_jobs = 0

    def reset(self) -> None:
        self.waiting_jobs = 0
        self.running_jobs = 0
        self.completed_jobs = 0

    def update(self, event: BatSimEvent) -> None:
        if event.type == EventType.JOB_SUBMITTED:
            self.waiting_jobs += 1
        elif event.type == EventType.REQUESTED_CALL:
            # BatSim execute commands (processed via action mapper) 
            # should idealy be tracked to decrement waiting and increment running.
            # Here we assume a simple tracking via dedicated events if BatSim emitted them
            # or we rely on ActionMapper to sync state. 
            pass
        elif event.type == EventType.JOB_COMPLETED:
            self.running_jobs = max(0, self.running_jobs - 1)
            self.completed_jobs += 1
            
    # Need a method to be called by ActionMapper or Env to sync job starts
    def notify_job_started(self) -> None:
        self.waiting_jobs = max(0, self.waiting_jobs - 1)
        self.running_jobs += 1

    def get_observation(self) -> np.ndarray:
        return np.array([
            self.waiting_jobs, 
            self.running_jobs, 
            self.completed_jobs
        ], dtype=np.float32)

    def get_space(self) -> gym.Space:
        return spaces.Box(
            low=0.0, 
            high=float(self.max_jobs), 
            shape=(3,), 
            dtype=np.float32
        )
