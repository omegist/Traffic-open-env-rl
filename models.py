from enum import Enum
from pydantic import BaseModel
from typing import Optional, Dict

class LightPhase(str, Enum):
    NS_GREEN = "NS_GREEN"
    EW_GREEN = "EW_GREEN"

class Action(BaseModel):
    action_type: str

class Observation(BaseModel):
    queues: Dict[str, int]
    current_phase: str
    emergency_vehicle_present: bool
    emergency_direction: Optional[str] = None
    step_count: int

class State(BaseModel):
    queues: Dict[str, int]
    phase: str
    emergency_present: bool
    emergency_dir: Optional[str] = None
    step_count: int
    throughput: int
    emergencies_handled: int
