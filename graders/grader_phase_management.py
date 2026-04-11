
def grade(output: dict, ground_truth: dict = None) -> float:
    throughput = output.get("throughput", 0)
    unnecessary = output.get("unnecessary_phase_changes", 999)
    phase_changes = output.get("phase_changes", 0)
    score = 0
    if throughput >= 40: score += 1
    if unnecessary <= 20: score += 1
    if phase_changes >= 1: score += 1
    return round(max(0.01, min(0.1 + (score / 3.0) * 0.8, 0.99)), 4)
