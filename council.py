from concurrent.futures import ThreadPoolExecutor, as_completed
from answer_agent import generate_answer
from judge_agent import judge
from safety_gate import safety_check
from decision import Decision
from audit_log import log_event

def run_council(question: str):

    if not safety_check(question):
        raise ValueError("❌ Safety gate blocked the question")

    # Generate answers in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        answer_futures = {
            executor.submit(generate_answer, question, temp): temp 
            for temp in [0.6, 0.8, 1.0]
        }
        answers = [future.result() for future in answer_futures.keys()]

    # Judge all answers in parallel (2 judges per answer = 6 parallel calls)
    judge_scores = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        judge_futures = []
        for i, ans in enumerate(answers):
            # Submit 2 judge calls per answer
            judge_futures.append((i, executor.submit(judge, question, ans)))
            judge_futures.append((i, executor.submit(judge, question, ans)))
        
        # Collect results
        judge_results = {}
        for answer_idx, future in judge_futures:
            if answer_idx not in judge_results:
                judge_results[answer_idx] = []
            judge_results[answer_idx].append(future.result())
        
        # Calculate average scores
        for i in range(len(answers)):
            judge_scores[f"answer_{i}"] = sum(judge_results[i]) / len(judge_results[i])

    winner_idx = max(judge_scores, key=judge_scores.get)
    winning_answer = answers[int(winner_idx.split("_")[1])]

    decision = Decision(
        question=question,
        winning_answer=winning_answer,
        confidence=judge_scores[winner_idx] / 10,
        risks=["Possible hallucination", "Context missing"],
        citations=["LLM-generated; verify independently"],
        judge_scores=judge_scores
    )

    log_event(decision.__dict__)
    print(decision)
    return decision
