"""
Config Layer for PyBatGym

1. Design Review:
Allows researchers to define Cluster, Workload, and Environment configs inside JSON files, standardizing experiments.
Constructs BatSim arguments deterministically.

2. Code:
Implemented in:
- `base.py`: Defines dataclasses for Cluster, Workload, and Env config, and JSON loader.

3. Usage Example:
```python
from pybatgym.config import load_config_from_json

config = load_config_from_json("experiment_1.json")
batsim_command = config.get_batsim_command()
# e.g. ["batsim", "-p", "platform.xml", "-w", "workload.json", "-e", "/tmp/batsim_export", ...]
```
"""

from .base import ClusterConfig, WorkloadConfig, EnvironmentConfig, load_config_from_json

__all__ = ["ClusterConfig", "WorkloadConfig", "EnvironmentConfig", "load_config_from_json"]
