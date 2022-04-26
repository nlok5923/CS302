import math
import random

# project input files contains the list of projects
with open('./project_input.txt') as file:
    projects = file.read().split()

print(projects)

# prompt for to take no of teachers and no of students as input
no_of_teachers = int(input('Enter no. of teachers '))
no_of_students = int(input('Enter no. of students '))

# maintaining the students and teachers dictionary
students = {}
teachers = {}

# denotes that a teacher can't supervise more than two project
TEACHER_LIMIT = 2

no_of_projects = len(projects)

project_index_mapping = {idx : i for idx, i in enumerate(projects)}

project_student_ratio = no_of_projects//no_of_students

"""
Below snippet of code generates a students dictionary which contains the list of projects for each student and projects are arranged in 
increasing order of their preferences
"""
for i in range(no_of_students):
    if i == no_of_students - 1:
        students[i] = [projects[j] for j in range(i*project_student_ratio, no_of_projects)]
        continue
    students[i] = [projects[i*project_student_ratio + j] for j in range(project_student_ratio)]

for i in range(no_of_students):
    for temp in range(2):
        idx = random.randint(0, no_of_projects - 1)
        while project_index_mapping[idx] in students[i]:
            idx = random.randint(0, no_of_projects - 1)
        students[i].append(project_index_mapping[idx])

project_teacher_ratio = no_of_projects//no_of_teachers

"""
Below snippet of code generates a teachers dictionary which contains the list of projects for each teacher and projects are arranged in 
increasing order of their preferences 
"""
for i in range(no_of_teachers):
    if i == no_of_teachers - 1:
        teachers[i] = [projects[j] for j in range(i*project_teacher_ratio, no_of_projects)]
        continue
    teachers[i] = [projects[i*project_teacher_ratio + j] for j in range(project_teacher_ratio)]

for i in range(no_of_teachers):
    for temp in range(2):
        idx = random.randint(0, no_of_projects - 1)
        while project_index_mapping[idx] in teachers[i]:
            idx = random.randint(0, no_of_projects - 1)
        teachers[i].append(project_index_mapping[idx])

print('Students - ')
print(students)
print('Teachers - ')
print(teachers)

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
#                 if not (project_index_mapping[idx] in  students[sidx]):
#                     return False

#     return True

def recurse_call(teach, assign, level, ans_seq):
    res_seq = []
    if level == no_of_students - 1:
        for i in assign[level]:
            if teach[i] + 1 <= TEACHER_LIMIT:
                ans_seq.append(i)
                return ans_seq, True
        return ans_seq, False
    for i in assign[level]:
        if teach[i] + 1 <= TEACHER_LIMIT:
            teach[i] += 1
            res_seq, ans = recurse_call(teach.copy(), assign.copy(), level + 1, ans_seq)
            teach[i] -= 1
            if ans == True:
                res_seq.append(i)
                return res_seq,True
    return res_seq, False

"""
As we are maintaining a state matrix for teacher as well so the below piece of code checks that each teacher in the state matrix should be assigned to only one student
"""
def teach_constraint(matrix):
    assign = []
    for row in matrix:
        for cidx, col in enumerate(row):
            if col == 1:
                temp = []
                for teacher, subject in teachers.items():
                    if project_index_mapping[cidx] in subject:
                        temp.append(teacher)
        assign.append(temp)
    teach = [0 for i in range(no_of_teachers)]
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

"""
Below piece of code generates random matrix and checks if it satisfies the constraints
"""
def random_gen():
    matrix = [[0 for j in range(no_of_projects)] for i in range(no_of_students)]
    booked = []
    t_idx = []
    while True:
        for i in range(no_of_students):
            idx = random.randint(0,len(projects) - 1)
            while not(project_index_mapping[idx] in students[i]) or idx in booked:
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
                val += students[ridx].index(project_index_mapping[cidx]) + 1
    return val

my_sequence = [random_gen()]
c_energy = energy(my_sequence[0])
max_energy = c_energy
idx = 0
for i in range(1000):
    temp = random_gen()
    ctr = 0
    while temp in my_sequence and ctr < 90000:
        temp = random_gen()
        ctr += 1
    if ctr == 90000:
        break
    my_sequence.append(temp)
    idx -= 1
    c_energy = energy(my_sequence[-1])
    C = 1 / c_energy
    if c_energy > max_energy or math.exp((max_energy - c_energy)/C) > 0.5:
        max_energy = c_energy
        idx = -1

# print("i",i)

for r_idx, row in enumerate(my_sequence[idx]):
    for c_idx, col in enumerate(row):
        if col == 1:
            print("Student", r_idx + 1, "-", project_index_mapping[c_idx])

ans_seq, val = teach_constraint(my_sequence[idx])
for student in range(no_of_students):
    print("Student", student + 1, "assigned to teacher", ans_seq[no_of_students - 1 - student] + 1)