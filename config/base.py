import json
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os

@dataclass
class ClusterConfig:
    platform_file: str
    num_resources: int
    speeds: list[float] = field(default_factory=list)

@dataclass
class WorkloadConfig:
    workload_file: str
    num_jobs: Optional[int] = None
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EnvironmentConfig:
    batsim_endpoint: str = "tcp://*:28000"
    export_dir: str = "/tmp/batsim_export"
    batsim_log_level: str = "quiet"
    cluster: Optional[ClusterConfig] = None
    workload: Optional[WorkloadConfig] = None

    def get_batsim_command(self) -> list[str]:
        """Constructs the BatSim CLI command from the config."""
        cmd = ["batsim"]
        if self.cluster:
            cmd.extend(["-p", self.cluster.platform_file])
        if self.workload:
            cmd.extend(["-w", self.workload.workload_file])
            
        cmd.extend(["-e", self.export_dir])
        cmd.extend(["-s", self.batsim_endpoint])
        cmd.extend(["-m", "10000"]) # Disable strict time constraints for slow RL
        cmd.extend(["-v", self.batsim_log_level])
        return cmd

def load_config_from_json(filepath: str) -> EnvironmentConfig:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")
        
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    cluster_data = data.get("cluster", {})
    workload_data = data.get("workload", {})
    
    cluster = ClusterConfig(**cluster_data) if cluster_data else None
    workload = WorkloadConfig(**workload_data) if workload_data else None
    
    env_data = {k: v for k, v in data.items() if k not in ["cluster", "workload"]}
    
    return EnvironmentConfig(cluster=cluster, workload=workload, **env_data)
