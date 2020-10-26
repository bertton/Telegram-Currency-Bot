from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Currency:
    from_currency: str
    to_currency: str
    amount: Decimal