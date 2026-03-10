from abc import ABC, abstractmethod
from typing import Any, List, Dict
import gymnasium as gym

class ActionMapper(ABC):
    """
    Abstract base class mapping RL actions to BatSim Protocol events.
    """
    
    @abstractmethod
    def reset(self) -> None:
        """Resets the state of the action mapper."""
        pass
        
    @abstractmethod
    def map(self, action: Any, current_time: float) -> List[Dict[str, Any]]:
        """
        Maps a Gym action to a list of BatSim events (e.g., EXECUTE_JOB).
        Returns a list of protocol-compatible event dictionaries.
        """
        pass
        
    @abstractmethod
    def get_space(self) -> gym.Space:
        """Returns the Action Space defined by this mapper."""
        pass
