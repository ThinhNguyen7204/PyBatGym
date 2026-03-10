from abc import ABC, abstractmethod
from typing import Any
import gymnasium as gym

from pybatgym.batsim.events import BatSimEvent

class ObservationBuilder(ABC):
    """
    Abstract base class for all observation builders.
    Observation builders listen to BatSim events and construct 
    Gymnasium-compatible numerical spaces.
    """
    
    @abstractmethod
    def reset(self) -> None:
        """Resets the internal state of the observer."""
        pass
        
    @abstractmethod
    def update(self, event: BatSimEvent) -> None:
        """Updates internal state based on incoming BatSim events."""
        pass
        
    @abstractmethod
    def get_observation(self) -> Any:
        """Returns the current observation matching the observation_space."""
        pass
        
    @abstractmethod
    def get_space(self) -> gym.Space:
        """Returns the Gymnasium Space object defining this observation."""
        pass
