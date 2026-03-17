from enum import Enum
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from heapq import heapify, heappop, heappush

class ConstraintType(Enum):
    EQ = "="
    NE = "!"
    GT = ">"
    LT = "<"

@dataclass
class CspState:
    available_vals: Dict[str, Set[int]]
    latest_assigned_val: Tuple[str, int]
    assigned_vals: List[Tuple[str, int]]
    

class CspSolver:
    constraint_graph: Dict[str, Tuple[ConstraintType, str]]
    var_domain: Dict[str, Set[int]]
    forward_check: bool

    def __init__(self, var_domain: Dict[str, Set[int]], constraint_graph: Dict[str, Tuple[ConstraintType, str]], forward_check: bool):
        self.constraint_graph = constraint_graph
        self.var_domain = var_domain
        self.forward_check = forward_check

    def is_goal_state(self, state: CspState)->bool:
        return len(state.assigned_vals) == len(self.var_domain)

    def is_fail_state(self, state: CspState)->bool:
        return any(
                (len(available_vals) == 0 
                 for available_vals in state.available_vals.values()))

    def next_states(self, state: CspState)->List[CspState]:
        raise NotImplemented
        

    def dfs(self)->None:
        state_queue: List[Tuple[float, CspState]] = []
        init_state: CspState = CspState(available_vals=self.var_domain, latest_assigned_val=("", -1), assigned_vals=[])
        heappush(state_queue, (0, init_state))
        leaf_met: int = 0
