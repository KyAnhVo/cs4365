from types import LambdaType
from typing import Dict, List, Tuple, Set
from pprint import pprint

import copy

constraint_functions: Dict[str, LambdaType] = {
    "=":    lambda x, y:    x == y,
    "!":    lambda x, y:    x != y,    
    ">":    lambda x, y:    x > y,
    "<":    lambda x, y:    x < y,
    "":     lambda x, y:    True,
}

class CspState:
    available_vals: Dict[str, Set[int]]
    latest_assigned_val: Tuple[str, int]
    assigned_vals: List[Tuple[str, int]]
    remaining_vars: List[str]

    def __init__(self, 
            available_vals: Dict[str, Set[int]], 
            latest_assigned_val: Tuple[str, int], 
            assigned_vals: List[Tuple[str, int]], 
            remaining_vars: List[str]):
        self.available_vals = available_vals
        self.latest_assigned_val = latest_assigned_val
        self.assigned_vals = assigned_vals
        self.remaining_vars = remaining_vars

    def fc(self, constraint_graph: Dict[str, Dict[str, str]]):
        var, val = self.latest_assigned_val
        for other_var in self.remaining_vars:
            func = constraint_functions[constraint_graph[var][other_var]]
            throwout_lst = [other_val for other_val in self.available_vals[other_var] if not func(val, other_val)]

            for other_val in throwout_lst:
                self.available_vals[other_var].remove(other_val)

    def choose(self, var_val_pair: Tuple[str, int]):
        chosen_var, chosen_val = var_val_pair
        if chosen_val not in self.available_vals[chosen_var]:
            return CspState({}, ("", -1), [], list())
        
        available_vals: Dict[str, Set[int]] = copy.deepcopy(self.available_vals)
        available_vals[chosen_var] = {chosen_val}
        
        latest_assigned_val: Tuple[str, int] = (chosen_var, chosen_val)
        
        assigned_vals: List[Tuple[str, int]] = copy.deepcopy(self.assigned_vals)
        assigned_vals.append(latest_assigned_val)

        remaining_vars = copy.deepcopy(self.remaining_vars)
        remaining_vars.remove(chosen_var)

        return CspState(available_vals=available_vals,
                        latest_assigned_val=latest_assigned_val,
                        assigned_vals=assigned_vals,
                        remaining_vars=remaining_vars)

class CspSolver:
    constraint_graph: Dict[str, Dict[str, str]]
    var_domain: Dict[str, Set[int]]
    forward_check: bool

    def __init__(self, var_domain: Dict[str, Set[int]], constraint_graph: Dict[str, Dict[str, str]], forward_check: bool):
        self.constraint_graph = constraint_graph
        self.var_domain = var_domain
        self.forward_check = forward_check

    def is_goal_state(self, state: CspState):
        return len(state.assigned_vals) == len(self.var_domain) and not self.is_fail_state(state)

    def is_fail_state(self, state: CspState):
        for var, val in state.assigned_vals:
            for other_var, other_val in state.assigned_vals:
                if not constraint_functions[self.constraint_graph[var][other_var]](val, other_val):
                    return True
        return any(
                (len(x) == 0) for x in state.available_vals.values() )

    def next_states(self, state: CspState):
        # sort all remaining variables in most constrained, then most constraining
        
        # min remaining values (most constrained)


        min_val_count = min(len(state.available_vals[v]) for v in state.remaining_vars)
        mrv_candidates = [v for v in state.remaining_vars if len(state.available_vals[v]) == min_val_count]


        # then most constraining

        max_deg: int = -1
        max_var: str = ""
        for var in mrv_candidates:
            deg: int = 0
            for other_var in state.remaining_vars:
                if self.constraint_graph[var][other_var] != "":
                    deg += 1
            if max_deg < deg:
                max_deg = deg
                max_var = var


        # then least constraining values

        constraint_val_count: Dict[int, int] = {val: 0 for val in state.available_vals[max_var]}
        for val in state.available_vals[max_var]:
            for other in state.remaining_vars:
                if other == max_var:
                    continue
                func = constraint_functions[self.constraint_graph[max_var][other]]
                for other_val in state.available_vals[other]:
                    if not func(val, other_val):
                        constraint_val_count[val] += 1

        vals_sorted = sorted((x for x in constraint_val_count), key=lambda x: constraint_val_count[x])
        states = [state.choose((max_var, val)) for val in vals_sorted]
        
        if not self.forward_check:
            return states

        for i in range(len(states)):
            states[i].fc(self.constraint_graph)
        return states
            

        
    def dfs(self):
        self.dfs_recurse(
                state=CspState(available_vals=self.var_domain,
                     latest_assigned_val= ("", -1),
                     assigned_vals=[],
                     remaining_vars=list(self.var_domain.keys())
            ),
            leafs_met=0
        )

    def dfs_recurse(self, state: CspState, leafs_met: int):

        is_goal: bool = self.is_goal_state(state)
        is_fail: bool = self.is_fail_state(state)
        if is_goal or is_fail:
            print_str: str = ""
            print_str += f"{leafs_met + 1}. "
            for var, val in state.assigned_vals:
                print_str += f"{var}={val}, "
            print_str = print_str[:-2] + " "
            print_str += " failure" if is_fail else " solution"
            print(print_str)
            return leafs_met + 1, is_goal
            
        children: List[CspState] = self.next_states(state)
        for s in children:
            leafs_met_modified, completed = self.dfs_recurse(s, leafs_met)
            leafs_met = leafs_met_modified
            if completed: 
                return (leafs_met, True)

        return leafs_met, False
