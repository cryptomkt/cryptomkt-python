from dataclasses import dataclass
from typing import Optional


@dataclass
class CommitRisk:
    score: Optional[int] = None
    rbf: Optional[str] = None
    low_fee: Optional[str] = None
