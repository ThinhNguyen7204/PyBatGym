from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

class EventType(Enum):
    SIMULATION_BEGIN = "SIMULATION_BEGIN"
    SIMULATION_ENDS = "SIMULATION_ENDS"
    JOB_SUBMITTED = "JOB_SUBMITTED"
    JOB_COMPLETED = "JOB_COMPLETED"
    JOB_KILLED = "JOB_KILLED"
    RESOURCE_STATE_CHANGED = "RESOURCE_STATE_CHANGED"
    REQUESTED_CALL = "REQUESTED_CALL"
    NOTIFY = "NOTIFY"

@dataclass
class BatSimEvent:
    timestamp: float
    type: EventType
    data: Dict[str, Any]

@dataclass
class JobSubmittedEvent(BatSimEvent):
    job_id: str
    job_profile: Dict[str, Any]

@dataclass
class JobCompletedEvent(BatSimEvent):
    job_id: str
    job_state: str
    return_code: int
    alloc: str

def parse_event(event_dict: Dict[str, Any]) -> BatSimEvent:
    timestamp = event_dict.get("timestamp", 0.0)
    event_type = EventType(event_dict.get("type"))
    data = event_dict.get("data", {})
    
    if event_type == EventType.JOB_SUBMITTED:
        return JobSubmittedEvent(
            timestamp=timestamp,
            type=event_type,
            data=data,
            job_id=data.get("job_id", ""),
            job_profile=data.get("job", {})
        )
    elif event_type == EventType.JOB_COMPLETED:
        return JobCompletedEvent(
            timestamp=timestamp,
            type=event_type,
            data=data,
            job_id=data.get("job_id", ""),
            job_state=data.get("job_state", ""),
            return_code=data.get("return_code", 0),
            alloc=data.get("alloc", "")
        )
    else:
        return BatSimEvent(timestamp=timestamp, type=event_type, data=data)
