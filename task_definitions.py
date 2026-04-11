
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graders.grader_phase_management import grade as grade_phase_management
from graders.grader_queue_optimization import grade as grade_queue_optimization
from graders.grader_emergency_response import grade as grade_emergency_response

TASKS = [
    {
        "id": "phase_management",
        "name": "Phase Management",
        "description": "Manage traffic light phases efficiently.",
        "grader": grade_phase_management,
        "difficulty": "easy",
        "score_range": (0.01, 0.99),
    },
    {
        "id": "queue_optimization",
        "name": "Queue Optimization",
        "description": "Keep vehicle queues short under heavy traffic.",
        "grader": grade_queue_optimization,
        "difficulty": "hard",
        "score_range": (0.01, 0.99),
    },
    {
        "id": "emergency_response",
        "name": "Emergency Response",
        "description": "Handle emergency vehicles correctly.",
        "grader": grade_emergency_response,
        "difficulty": "medium",
        "score_range": (0.01, 0.99),
    },
]

TASK_COUNT = 3

def get_task(task_id: str) -> dict:
    for t in TASKS:
        if t["id"] == task_id:
            return t
    raise ValueError(f"Unknown task: {task_id}")

def grade_task(task_id: str, output: dict) -> float:
    task = get_task(task_id)
    score = task["grader"](output)
    return float(max(0.01, min(score, 0.99)))
