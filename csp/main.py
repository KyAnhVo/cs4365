#!/usr/bin/env python3

from csp_solver import CspSolver
from typing import Dict, Set, List
import csv
import sys
import pprint

reverse_func: Dict[str, str] = {
        ">": "<",
        "<": ">",
        "=": "=",
        "!": "!",
        }

def main():
    domain_path: str = sys.argv[1]
    con_path: str = sys.argv[2]
    fc: bool = sys.argv[3] == "fc"

    domain_dict: Dict[str, Set[int]] = {}
    with open(domain_path, mode='r') as f_domain:
        dom_csv = csv.reader(f_domain, delimiter=" ")
        for row in dom_csv:
            var_name = row[0][0]
            domain_set = set((int(x) for x in row[1:] if x != "" and x != " "))
            domain_dict[var_name] = domain_set

    constraint_matrix: Dict[str, Dict[str, str]] = {}
    for var_name in domain_dict.keys():
        constraint_matrix[var_name] = {}
        for other_var_name in domain_dict.keys():
            constraint_matrix[var_name][other_var_name] = ""

    with open(con_path, mode='r') as f_con:
        con_csv = csv.reader(f_con, delimiter=" ")
        for row in con_csv:
            constraint_matrix[row[0]][row[2]] = row[1]
            constraint_matrix[row[2]][row[0]] = reverse_func[row[1]]

    solver = CspSolver(domain_dict, constraint_matrix, fc)
    solver.dfs()

if __name__ == "__main__":
    main()
