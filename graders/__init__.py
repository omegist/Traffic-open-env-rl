from .grader_phase_management import grade as grade_phase_management
from .grader_queue_optimization import grade as grade_queue_optimization
from .grader_emergency_response import grade as grade_emergency_response

GRADERS = {
    "phase_management":   grade_phase_management,
    "queue_optimization": grade_queue_optimization,
    "emergency_response": grade_emergency_response,
}

TASK_GRADER_MAP = GRADERS
TASK_COUNT = 3
