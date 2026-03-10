import gymnasium as gym
from gymnasium import spaces
from typing import Any, List, Dict

from pybatgym.action.base import ActionMapper
from pybatgym.batsim.protocol import BatSimProtocol

class DiscreteActionMapper(ActionMapper):
    """
    A simple action mapper that maps a discrete action integer 
    to a specific job ID waiting in the queue.
    
    This is a naive implementation assuming the environment passes the ordered
    list of job IDs currently waiting. E.g., action `0` maps to the first job.
    """
    
    def __init__(self, max_queue_size: int = 100):
        self.max_queue_size = max_queue_size
        self.waiting_job_ids = []
        
    def reset(self) -> None:
        self.waiting_job_ids = []

    def update_queue(self, waiting_job_ids: List[str]) -> None:
        """
        Sync the current state of waiting jobs. E.g. Called by the environment.
        """
        self.waiting_job_ids = waiting_job_ids

    def map(self, action: int, current_time: float) -> List[Dict[str, Any]]:
        """
        Maps discrete index to a job execution.
        If action is 0 and there are jobs, run the first job.
        For simplicity, we assume action corresponds to index in waiting_job_ids.
        If invalid, we return an empty list or rejection.
        """
        # If action is 'wait' or do nothing
        if action == self.max_queue_size or action >= len(self.waiting_job_ids):
            # Tell BatSim to call us back in e.g. 10 time units or when an event occurs
            # Currently BatSim handles empty events by just advancing.
            return []
            
        selected_job_id = self.waiting_job_ids.pop(action)
        
        # We need a proper allocation policy, for now naive string allocation "0"
        # In a real system, the mapper would query resource availability.
        alloc = "0" 
        
        return [
            BatSimProtocol.build_execute_job(
                timestamp=current_time, 
                job_id=selected_job_id, 
                alloc=alloc
            )
        ]

    def get_space(self) -> gym.Space:
        # action space: [0, max_queue_size - 1] select job, max_queue_size means 'wait'
        return spaces.Discrete(self.max_queue_size + 1)
