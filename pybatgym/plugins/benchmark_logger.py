"""Benchmark Logger plugin for PyBatGym.

Generates benchmark_summary.csv and per_episode_metrics.csv in the results folder.
"""

from __future__ import annotations

import csv
import os
import time
from pathlib import Path
from typing import Any, Optional


class BenchmarkLogger:
    """Helper class to log simulation results to CSV for academic reporting."""

    SUMMARY_COLUMNS = [
        "experiment_id", "policy", "workload", "platform", "seed",
        "total_reward", "completed_jobs", "avg_waiting_time",
        "avg_bounded_slowdown", "utilization", "makespan",
        "throughput", "num_steps", "invalid_actions",
        "terminated", "truncated"
    ]

    def __init__(self, output_dir: str = "pybatgym/results") -> None:
        # Resolve path relative to current working directory if not absolute
        self.output_dir = Path(output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.summary_path = self.output_dir / "benchmark_summary.csv"
        self.episode_path = self.output_dir / "per_episode_metrics.csv"
        
        self._init_files()

    def _init_files(self) -> None:
        """Initialize CSV files with headers if they don't exist."""
        if not self.summary_path.exists():
            with open(self.summary_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.SUMMARY_COLUMNS)
        
        if not self.episode_path.exists():
            with open(self.episode_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                # Episode file includes an episode index and timestamp
                writer.writerow(["timestamp", "episode_idx"] + self.SUMMARY_COLUMNS)

    def log_episode(
        self, 
        episode_idx: int, 
        metrics: dict[str, Any], 
        experiment_id: str = "exp",
        policy: str = "unknown",
        workload: str = "unknown",
        platform: str = "unknown",
        seed: int = 0
    ) -> None:
        """Log a single episode's results."""
        row_data = self._build_row(metrics, experiment_id, policy, workload, platform, seed)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.episode_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, episode_idx] + row_data)

    def log_summary(
        self, 
        metrics: dict[str, Any], 
        experiment_id: str = "exp",
        policy: str = "unknown",
        workload: str = "unknown",
        platform: str = "unknown",
        seed: int = 0
    ) -> None:
        """Log a final summary (usually averaged over episodes) to the summary file."""
        row_data = self._build_row(metrics, experiment_id, policy, workload, platform, seed)
        
        with open(self.summary_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row_data)

    def _build_row(
        self, 
        metrics: dict[str, Any], 
        experiment_id: str,
        policy: str,
        workload: str,
        platform: str,
        seed: int
    ) -> list[Any]:
        """Map metrics dictionary to the fixed column order."""
        # Calculate throughput if not provided: completed_jobs / makespan
        makespan = metrics.get("makespan", 0.0)
        completed = metrics.get("completed_jobs", 0)
        throughput = metrics.get("throughput")
        if throughput is None and makespan > 0:
            throughput = completed / makespan
        
        # Build the row based on SUMMARY_COLUMNS
        row = []
        for col in self.SUMMARY_COLUMNS:
            if col == "experiment_id": row.append(experiment_id)
            elif col == "policy": row.append(policy)
            elif col == "workload": row.append(workload)
            elif col == "platform": row.append(platform)
            elif col == "seed": row.append(seed)
            elif col == "throughput": row.append(f"{throughput:.6f}" if throughput is not None else "0.0")
            else:
                val = metrics.get(col, 0)
                # Format floats for cleaner CSV
                if isinstance(val, float):
                    row.append(f"{val:.6f}")
                else:
                    row.append(val)
        return row
