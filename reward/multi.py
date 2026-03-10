from typing import List, Tuple
from pybatgym.reward.base import RewardCalculator
from pybatgym.batsim.events import BatSimEvent

class MultiObjectiveRewardCalculator(RewardCalculator):
    """
    Combines multiple reward calculators using a weighted sum.
    """
    
    def __init__(self, calculators_with_weights: List[Tuple[RewardCalculator, float]]):
        self.calculators = [cw[0] for cw in calculators_with_weights]
        self.weights = [cw[1] for cw in calculators_with_weights]
        
    def reset(self) -> None:
        for calc in self.calculators:
            calc.reset()
            
    def update(self, event: BatSimEvent) -> None:
        for calc in self.calculators:
            calc.update(event)
            
    def calculate(self, current_time: float) -> float:
        total_reward = 0.0
        for calc, weight in zip(self.calculators, self.weights):
            total_reward += weight * calc.calculate(current_time)
        return total_reward
