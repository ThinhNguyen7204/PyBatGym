from pybatgym.reward.base import RewardCalculator
from pybatgym.batsim.events import BatSimEvent, EventType, JobCompletedEvent

class SlowdownRewardCalculator(RewardCalculator):
    """
    Calculates a reward based on job slowdowns.
    Slowdown = (WaitTime + RunTime) / RunTime
    Reward is negative normalized slowdown, or negative sum of slowddowns.
    """
    
    def __init__(self):
        self.completed_slowdowns = []
        
    def reset(self) -> None:
        self.completed_slowdowns = []
        
    def update(self, event: BatSimEvent) -> None:
        if event.type == EventType.JOB_COMPLETED and isinstance(event, JobCompletedEvent):
            # BatSim usually returns accurate times, assuming we track job_profiles
            # Here we mock retrieving job runtime and calculating wait time.
            wait_time = event.data.get("waiting_time", 0.0)
            run_time = event.data.get("execution_time", 1.0)
            # Avoid division by zero
            run_time = max(run_time, 1e-5) 
            slowdown = (wait_time + run_time) / run_time
            self.completed_slowdowns.append(slowdown)

    def calculate(self, current_time: float) -> float:
        if not self.completed_slowdowns:
            return 0.0
            
        # Example: Sparse negative average slowdown of recently completed jobs
        avg_sd = sum(self.completed_slowdowns) / len(self.completed_slowdowns)
        self.completed_slowdowns.clear() # clear after applying reward
        
        return -float(avg_sd)

class UtilizationRewardCalculator(RewardCalculator):
    """
    Calculates a dense reward based on current system utilization.
    E.g., Number of running jobs / Total jobs capacity (or resource usage).
    """
    
    def __init__(self, max_resources: int = 100):
        self.max_resources = max_resources
        self.running_jobs = 0
        
    def reset(self) -> None:
        self.running_jobs = 0
        
    def update(self, event: BatSimEvent) -> None:
        # Simplistic tracking for demonstration
        if event.type == EventType.JOB_SUBMITTED:
            pass # Job is just waiting
        elif event.type == EventType.JOB_COMPLETED:
            self.running_jobs = max(0, self.running_jobs - 1)
            
    def notify_job_started(self) -> None:
        """Called by ActionMapper when a job is scheduled."""
        self.running_jobs += 1

    def calculate(self, current_time: float) -> float:
        return self.running_jobs / float(self.max_resources)
