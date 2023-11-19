# %%
import numpy as np
import pandas as pd
import pulp

# %%
problem = pd.read_csv('input.csv', header=None).to_numpy()
is_fixed = np.zeros((9, 9), dtype=bool)

is_fixed[problem != '.'] = True
problem[problem == '.'] = '0'
problem = problem.astype(np.int8)


# %%
m = pulp.LpProblem(name='Sudoku')
N = range(9)

x = [[[pulp.LpVariable('x' + str(i + 1) + str(j + 1) + str(k + 1), cat = 'Binary') for k in N] for j in N] for i in N]

for i in N:
	for j in N:
		m += pulp.lpSum(x[i][j][k] for k in N) == 1

for i in N:
	for k in N:
		m += pulp.lpSum(x[i][j][k] for j in N) == 1

for j in N:
	for k in N:
		m += pulp.lpSum(x[i][j][k] for i in N) == 1

for k in N:
	for area_num in N:
		r = int(area_num / 3)
		c = area_num % 3
		m += pulp.lpSum(x[i][j][k] for i in range(3 * r, 3 * (r + 1)) for j in range(3 * c, 3 * (c + 1))) == 1

for i in N:
	for j in N:
		if problem[i][j]:
			m += x[i][j][problem[i][j] - 1] == 1

solver = pulp.CPLEX_CMD(msg = 0)
m.solve(solver)

# %%
result = np.empty((9, 9), dtype=np.int8)
for i in N:
	for j in N:
		for k in N:
			if pulp.value(x[i][j][k]) > 0.5:
				result[i][j] = k + 1

# %%
def print_3chars(chars, is_fixed):
	for i, c in enumerate(chars):
		if is_fixed[i]:
			print(' \033[1m' + (str(c) if c else ' ') + '\033[0m ', end='')
		else:
			print(' \033[91m' + (str(c) if c else ' ') + '\033[0m ', end='')

def print_line(row, is_fixed):
	print('\033[90m│\033[0m', end='')
	print_3chars(row[0:3], is_fixed[0:3])
	print('\033[90m│\033[0m', end='')
	print_3chars(row[3:6], is_fixed[3:6])
	print('\033[90m│\033[0m', end='')
	print_3chars(row[6:9], is_fixed[6:9])
	print('\033[90m│\033[0m')

def print_3lines(rows, is_fixed):
	for i, r in enumerate(rows):
		print_line(r, is_fixed[i])

def print_map(map, is_fixed):
	print('\033[90m┌─────────┬─────────┬─────────┐\033[0m')
	print_3lines(map[0:3], is_fixed[0:3])
	print('\033[90m├─────────┼─────────┼─────────┤\033[0m')
	print_3lines(map[3:6], is_fixed[3:6])
	print('\033[90m├─────────┼─────────┼─────────┤\033[0m')
	print_3lines(map[6:9], is_fixed[6:9])
	print('\033[90m└─────────┴─────────┴─────────┘\033[0m')
	return

# %%
print('******* Sudoku Problem ********')
print_map(problem, is_fixed)

print('\n******** Sudoku Result ********')
print_map(result, is_fixed)


