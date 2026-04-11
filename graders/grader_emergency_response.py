
def grade(output: dict, ground_truth: dict = None) -> float:
    emergencies = output.get("emergencies", 0)
    false_activations = output.get("false_activations", 999)
    events_seen = max(output.get("emergency_events_seen", 1), 1)
    score = 0
    if emergencies >= 2: score += 1
    if false_activations <= 3: score += 1
    if emergencies / events_seen >= 0.5: score += 1
    return round(max(0.01, min(0.1 + (score / 3.0) * 0.8, 0.99)), 4)
