from abc import ABC, abstractmethod
from pybatgym.batsim.events import BatSimEvent

class RewardCalculator(ABC):
    """
    Abstract base class for calculating RL rewards.
    It tracks BatSim events to understand the simulation state
    and produces a float reward at each step.
    """
    
    @abstractmethod
    def reset(self) -> None:
        """Resets the state of the reward calculator."""
        pass
        
    @abstractmethod
    def update(self, event: BatSimEvent) -> None:
        """Updates internal state based on incoming BatSim events."""
        pass
        
    @abstractmethod
    def calculate(self, current_time: float) -> float:
        """Returns the reward for the current environment step."""
        pass
