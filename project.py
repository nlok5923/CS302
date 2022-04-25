import math
import random

with open('./project_input.txt') as file:
    projects = file.read().split()

print(projects)

thrlen = int(input('Enter no. of teachers '))
stlen = int(input('Enter no. of students '))

stds = {}
thrs = {}
T_LIM = 2

prlen = len(projects)

r_mapping = {idx : i for idx, i in enumerate(projects)}

spr = prlen//stlen
for i in range(stlen):
    if i == stlen - 1:
        stds[i] = [projects[j] for j in range(i*spr, prlen)]
        continue
    stds[i] = [projects[i*spr + j] for j in range(spr)]

for i in range(stlen):
    for temp in range(2):
        idx = random.randint(0, prlen - 1)
        while r_mapping[idx] in stds[i]:
            idx = random.randint(0, prlen - 1)
        stds[i].append(r_mapping[idx])

tpr = prlen//thrlen
for i in range(thrlen):
    if i == thrlen - 1:
        thrs[i] = [projects[j] for j in range(i*tpr, prlen)]
        continue
    thrs[i] = [projects[i*tpr + j] for j in range(tpr)]

for i in range(thrlen):
    for temp in range(2):
        idx = random.randint(0, prlen - 1)
        while r_mapping[idx] in thrs[i]:
            idx = random.randint(0, prlen - 1)
        thrs[i].append(r_mapping[idx])

print('Students - ')
print(stds)
print('Teachers - ')
print(thrs)

# def check_constraints(matrix):
#     for i in matrix:
#         count = 0
#         for j in i:
#             if j == 1:
#                 count += 1
#         if count > 1:
#             return False
    
#     rlen = len(matrix)
#     clen = len(matrix[0])
#     for column in range(clen):
#         count = 0
#         for row in range(rlen):
#             if matrix[row][column] == 1:
#                 count += 1
#         if count > 1:
#             return False
    
#     for sidx, student in enumerate(matrix):
#         for idx, choice in enumerate(student):
#             if choice == 1:
#                 if not (r_mapping[idx] in  stds[sidx]):
#                     return False

#     return True

def recurse_call(teach, assign, level, ans_seq):
    res_seq = []
    if level == stlen - 1:
        for i in assign[level]:
            if teach[i] + 1 <= T_LIM:
                ans_seq.append(i)
                return ans_seq, True
        return ans_seq, False
    for i in assign[level]:
        if teach[i] + 1 <= T_LIM:
            teach[i] += 1
            res_seq, ans = recurse_call(teach.copy(), assign.copy(), level + 1, ans_seq)
            teach[i] -= 1
            if ans == True:
                res_seq.append(i)
                return res_seq,True
    return res_seq, False

def teach_constraint(matrix):
    assign = []
    for row in matrix:
        for cidx, col in enumerate(row):
            if col == 1:
                temp = []
                for teacher, subject in thrs.items():
                    if r_mapping[cidx] in subject:
                        temp.append(teacher)
        assign.append(temp)
    teach = [0 for i in range(thrlen)]
    ans = False
    res_seq = []
    for val in assign[0]:
        teach[val] = 1
        res_seq, ans = recurse_call(teach.copy(), assign.copy(), 1, [])
        teach[val] = 0
        if ans == True:
            res_seq.append(val)
            return res_seq, True
    return res_seq,False

def random_gen():
    matrix = [[0 for j in range(prlen)] for i in range(stlen)]
    booked = []
    t_idx = []
    while True:
        for i in range(stlen):
            idx = random.randint(0,len(projects) - 1)
            while not(r_mapping[idx] in stds[i]) or idx in booked:
                idx = random.randint(0,len(projects) - 1)
            matrix[i][idx] = 1
            booked.append(idx)
        res_seq, val = teach_constraint(matrix)
        if val:
            return matrix.copy()

        # if check_constraints(matrix):
        #     return matrix.copy()
        # else:
        #     for i in matrix:
        #         for j in range(len(i)):
        #             i[j] = 0

C = 12

def energy(matrix):
    val = 0
    for ridx, row in enumerate(matrix):
        for cidx, col in enumerate(row):
            if col == 1:
                val += stds[ridx].index(r_mapping[cidx]) + 1
    return val

my_sequence = [random_gen()]
c_energy = 0
max_energy = 0
idx = -1
for i in range(10000):
    idx -= 1
    temp = random_gen()
    ctr = 0
    while temp in my_sequence and ctr < 900000:
        temp = random_gen()
        ctr += 1
    if ctr == 900000:
        break
    my_sequence.append(temp)
    c_energy = energy(my_sequence[-1])
    if c_energy > max_energy or math.exp((max_energy - c_energy)/C) > 0.5:
        max_energy = c_energy
        idx = -1

for r_idx, row in enumerate(my_sequence[idx]):
    for c_idx, col in enumerate(row):
        if col == 1:
            print("Student", r_idx + 1, "-", r_mapping[c_idx])

ans_seq, val = teach_constraint(my_sequence[idx])
for student in range(stlen):
    print("Student", student + 1, "assigned to teacher", ans_seq[stlen - 1 - student] + 1)