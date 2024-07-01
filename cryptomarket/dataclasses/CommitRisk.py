from dataclasses import dataclass
from typing import Optional


@dataclass
class CommitRisk:
    score: Optional[int] = None
    rbf: Optional[bool] = None
    low_fee: Optional[bool] = None
