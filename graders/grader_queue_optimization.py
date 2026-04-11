
def grade(output: dict, ground_truth: dict = None) -> float:
    throughput = output.get("throughput", 0)
    avg_queue = output.get("avg_queue", 999)
    final_queue = output.get("final_queue", 999)
    score = 0
    if throughput >= 60: score += 1
    if avg_queue <= 10: score += 1
    if final_queue <= 15: score += 1
    return round(max(0.01, min(0.1 + (score / 3.0) * 0.8, 0.99)), 4)
