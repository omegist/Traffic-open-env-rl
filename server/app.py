import sys, os
sys.path.insert(0, "/app")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

try:
    from .models import Action, LightPhase
    from .traffic_environment import TrafficEnv
except ImportError:
    from models import Action, LightPhase
    from server.traffic_environment import TrafficEnv

# ── Load graders at startup — crash immediately if missing ──
try:
    from graders import GRADERS
    assert len(GRADERS) == 3, f"Expected 3 graders, got {len(GRADERS)}"
except ImportError:
    import importlib.util as _ilu
    _gpath = "/app/graders/__init__.py"
    if not os.path.exists(_gpath):
        _gpath = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "graders", "__init__.py"
        )
    _spec = _ilu.spec_from_file_location("graders", _gpath)
    _mod  = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    GRADERS = _mod.GRADERS

app = FastAPI(title="Smart Traffic Intersection")
env = TrafficEnv()

TASKS = [
    {
        "id": "phase_management",
        "name": "Phase Management",
        "description": "Manage traffic light phases efficiently.",
        "grader": "graders.grader_phase_management:grade",
        "grader_endpoint": "/grade",
        "grader_params": {"task": "phase_management"},
        "score_range": {"min": 0.01, "max": 0.99},
    },
    {
        "id": "queue_optimization",
        "name": "Queue Optimization",
        "description": "Minimize vehicle queue lengths under heavy traffic.",
        "grader": "graders.grader_queue_optimization:grade",
        "grader_endpoint": "/grade",
        "grader_params": {"task": "queue_optimization"},
        "score_range": {"min": 0.01, "max": 0.99},
    },
    {
        "id": "emergency_response",
        "name": "Emergency Response",
        "description": "Handle emergency vehicles correctly.",
        "grader": "graders.grader_emergency_response:grade",
        "grader_endpoint": "/grade",
        "grader_params": {"task": "emergency_response"},
        "score_range": {"min": 0.01, "max": 0.99},
    },
]


class ResetRequest(BaseModel):
    difficulty: Optional[str] = "easy"
    class Config:
        extra = "allow"

class ActionRequest(BaseModel):
    action_type: str

class GradeRequest(BaseModel):
    throughput: Optional[int] = 0
    unnecessary_phase_changes: Optional[int] = 5
    phase_changes: Optional[int] = 1
    avg_queue: Optional[float] = 10.0
    final_queue: Optional[int] = 10
    emergencies: Optional[int] = 0
    false_activations: Optional[int] = 0
    emergency_events_seen: Optional[int] = 1
    class Config:
        extra = "allow"


@app.get("/health")
def health():
    return {"status": "ok", "graders_loaded": len(GRADERS), "tasks": len(TASKS)}


@app.get("/state")
def state():
    return env.state()


@app.get("/observation_space")
def observation_space():
    return {
        "queues": {"type": "dict", "keys": ["North", "South", "East", "West"]},
        "current_phase": {"type": "string", "values": ["NS_GREEN", "EW_GREEN"]},
        "emergency_vehicle_present": {"type": "bool"},
        "emergency_direction": {"type": "string", "nullable": True},
        "step_count": {"type": "int"},
    }


@app.get("/action_space")
def action_space():
    return {
        "action_type": {
            "type": "string",
            "values": ["change_phase", "extend_green", "activate_emergency_mode"]
        }
    }


@app.post("/reset")
def reset(body: ResetRequest = None, difficulty: str = "easy"):
    diff = (body.difficulty if body and body.difficulty else None) or difficulty or "easy"
    obs = env.reset(diff)
    return obs


@app.post("/step")
def step(action: ActionRequest):
    obs, reward, done, info = env.step(action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}


@app.get("/metrics")
def metrics():
    return {"throughput": env.throughput, "emergencies": env.emergencies_handled}


@app.get("/tasks")
def list_tasks():
    return {"tasks": TASKS, "task_count": len(TASKS)}


@app.get("/tasks/count")
def tasks_count():
    return {"count": len(TASKS), "task_count": len(TASKS)}


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    for t in TASKS:
        if t["id"] == task_id:
            return t
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.get("/graders")
def list_graders():
    return {
        "grader_count": len(GRADERS),
        "graders": {t["id"]: t["grader"] for t in TASKS}
    }


@app.post("/grade")
def grade_endpoint(task: str = Query(...), request: GradeRequest = None):
    grader_fn = GRADERS.get(task)
    if grader_fn is None:
        return JSONResponse(status_code=400, content={"error": f"Unknown task: {task}", "score": 0.1})
    if request is not None:
        output = request.dict()
    else:
        output = {
            "throughput": env.throughput,
            "unnecessary_phase_changes": 5,
            "phase_changes": max(env.step_count // 10, 1),
            "avg_queue": sum(env.queues.values()) / max(env.step_count, 1),
            "final_queue": sum(env.queues.values()),
            "emergencies": env.emergencies_handled,
            "false_activations": 0,
            "emergency_events_seen": max(env.emergencies_handled, 1),
        }
    score = grader_fn(output)
    score = float(max(0.01, min(score, 0.99)))
    return {"task": task, "score": score, "grader": f"graders.grader_{task}:grade"}


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
