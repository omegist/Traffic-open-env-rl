#!/usr/bin/env python3
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tasks.task_phase_management import run_phase_management
from tasks.task_queue_optimization import run_queue_optimization
from tasks.task_emergency_response import run_emergency_response

if __name__ == "__main__":
    print("🚦 Smart Traffic Intersection - Demo")
    print("-" * 40)
    s1 = run_phase_management()
    print(f"phase_management    score: {s1}")
    s2 = run_queue_optimization()
    print(f"queue_optimization  score: {s2}")
    s3 = run_emergency_response()
    print(f"emergency_response  score: {s3}")
    print("-" * 40)
    print(f"All scores in range: {all(0 < s < 1 for s in [s1, s2, s3])}")
