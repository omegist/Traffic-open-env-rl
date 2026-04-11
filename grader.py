
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from graders.grader_phase_management import grade as grade_phase_management
from graders.grader_queue_optimization import grade as grade_queue_optimization
from graders.grader_emergency_response import grade as grade_emergency_response

GRADERS = {
    "phase_management":   grade_phase_management,
    "queue_optimization": grade_queue_optimization,
    "emergency_response": grade_emergency_response,
}

TASK_COUNT = 3

def grade(episode_data: dict, task: str) -> float:
    grader_fn = GRADERS.get(task)
    if grader_fn is None:
        raise ValueError(f"Unknown task: {task}")
    score = grader_fn(episode_data)
    return float(max(0.01, min(score, 0.99)))

grade_episode = grade
