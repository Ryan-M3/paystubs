from enum import Enum


class AcctType(Enum):
    asset     = 0
    liability = 1
    capital   = 2
    revenue   = 3
    expense   = 4
    gain      = 5
    loss      = 6
    contra    = 7
    adjunct   = 8
