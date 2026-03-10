"""
Reward Layer for PyBatGym

1. Design Review:
Maintains state asynchronously via the `RewardCalculator` interface. 
These calculators listen to job events and produce continuous rewards for RL training.
It includes base `RewardCalculator`, `SlowdownRewardCalculator`, `UtilizationRewardCalculator`, and `MultiObjectiveRewardCalculator` for weighted combination.

2. Code:
Implemented in:
- `base.py`: The `RewardCalculator` ABC.
- `metrics.py`: `SlowdownRewardCalculator` and `UtilizationRewardCalculator`.
- `multi.py`: `MultiObjectiveRewardCalculator`.

3. Usage Example:
```python
from pybatgym.reward.metrics import SlowdownRewardCalculator, UtilizationRewardCalculator
from pybatgym.reward.multi import MultiObjectiveRewardCalculator

slowdown_calc = SlowdownRewardCalculator()
util_calc = UtilizationRewardCalculator(max_resources=100)

multi_reward = MultiObjectiveRewardCalculator([
    (slowdown_calc, 0.7),
    (util_calc, 0.3)
])
```
"""

from .base import RewardCalculator
from .metrics import SlowdownRewardCalculator, UtilizationRewardCalculator
from .multi import MultiObjectiveRewardCalculator

__all__ = [
    "RewardCalculator", 
    "SlowdownRewardCalculator", 
    "UtilizationRewardCalculator", 
    "MultiObjectiveRewardCalculator"
]
