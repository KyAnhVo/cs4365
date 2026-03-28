from typing import Dict, List, Set, Tuple

class TheoremProver:
    
    def __init__(self, clause_list: List[Tuple[int]], clause_set: Set[Tuple[int]], char_map: Dict[int, str]):
        self.clause_list = clause_list
        self.clause_set = clause_set
        self.char_map = char_map

    def join_clause(self, i1: int, i2: int, var: int):
        clause1 = self.clause_list[i1]
        clause2 = self.clause_list[i2]

        # the a, not a part
        if (clause1[var], clause2[var]) not in [(0, 1), (1, 0)]:
            return None

        new_clause = []
        only_var = True
        for v in range(len(clause1)):
            # we already solved this above
            if v == var: 
                new_clause.append(-1)
                continue

            
            if clause1[v] != -1 or clause2[v] != -1:
                only_var = False
            if clause1[v] == -1:
                new_clause.append(clause2[v])

            # if both are 
            elif (clause1[v], clause2[v]) in [(0, 1), (1, 0)]:
                new_clause.append(-1)
            elif 



    def print_clause(self, clause: Tuple[int], i1: int, i2: int, counter: int):
        print_str = f"{counter}. "
        for i in range(len(clause)):
            if clause[i] == -1:
                continue
            if clause[i] == 0:
                print_str += f"~{self.char_map[i] }"
            else:
                print_str += f"{self.char_map[i] } "
        if print_str == f"{counter}. ":
            print_str += "Contradiction "
        if i1 == -1 and i2 == -1:
            print_str += "{}"
        else:
            print_str += "{" + f"{i1 + 1}, {i2 + 1}" + "}"
        print(print_str)

    def solve(self):
        raise NotImplemented
