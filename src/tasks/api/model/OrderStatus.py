from dataclasses import dataclass


@dataclass
class OrderStatus:
    Active = "ACTIVE"
    Cancelled = "CANCELLED"
