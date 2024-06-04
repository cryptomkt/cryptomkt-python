from dataclasses import dataclass


@dataclass
class CommitRisk:
    score: int
    rbf: str
    low_fee: str
