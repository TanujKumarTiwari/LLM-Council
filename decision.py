from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Decision:
    question: str
    winning_answer: str
    confidence: float
    risks: List[str]
    citations: List[str]
    judge_scores: Dict[str, float]