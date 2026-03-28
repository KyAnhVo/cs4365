from prover import TheoremProver

char_map = {0: 'p', 1: 'q', 2: 'y', 3: 'z'}
clause_list = [
        (0, 1, -1, -1),
        (-1, -1, 1, 0),
        (1, 0, -1, -1),
        (0, 1, -1, 1),
        (0, 1, -1, 0),
        (-1, -1, -1, 1),
        (-1, -1, 0, -1),
        (1, -1, -1, -1),
        ]
clause_set = set(clause_list)

prove = TheoremProver(clause_list, clause_set, char_map)
prove.solve()

