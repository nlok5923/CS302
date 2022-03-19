import time

goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]

class node:
    def __init__ (self, input, parent):
        self.sequence = input
        self.parent = parent

def generate_obj(input_sequence, parent):
    obj = node(input_sequence, parent)
    return obj

def print_sequence(input):
    for i in range(3):
        for j in range(3):
            print(input[3*i + j], end = " ")
        print()
    print()
        
def back_track(input_node):
    temp = input_node
    len = 0
    container = []
    container.append(input_node.sequence)
    while(temp.parent != None):
        temp = temp.parent
        container.append(temp.sequence)
        len += 1
    return len, container

def swap(r1, c1, r2, c2, seq):
    sequence = seq.copy()
    val = sequence[3*r1 + c1]
    sequence[3*r1 + c1] = sequence[3*r2 + c2]
    sequence[3*r2 + c2] = val
    return sequence

def index(val, seq):
    for i in range(9):
        if seq[i] == val:
            break
    val = i
    r = val//3
    c = val % 3
    return r,c

def generate_sequence(start, depth):
    input_s = start
    prev_index = [0, 0]
    for i in range(0, depth):
        r0, c0 = index(0, input_s)
        for m in [1, -1]:
            if r0 + m < 3 and r0 + m > 0 and r0 + m != prev_index[0]:
                input_s = swap(r0, c0, r0 + m, c0, input_s)
                prev_index = r0, c0
                break
            if c0 + m < 3 and c0 + m > 0 and c0 + m != prev_index[1]:
                input_s = swap(r0, c0, r0, c0 + m, input_s)
                prev_index = r0, c0
                break
    return input_s

def Agent(current_depth, depth, node, visited):
    if node.sequence == goal:
        return node
    if current_depth == depth:
        return None
    possible_seq = []
    current_seq = node.sequence
    r0, c0 = index(0, current_seq)
    for m in [1, -1]:
        if r0 + m < 3 and r0 + m >= 0:
            temp_sequence = swap(r0, c0, r0 + m, c0, current_seq)
            i = 0
            while i < len(visited):
                if visited[i].sequence == temp_sequence:
                    break
                i += 1
            if i == len(visited):
                possible_seq.append(temp_sequence)
        if c0 + m < 3 and c0 + m >= 0:
            temp_sequence = swap(r0, c0, r0, c0+m, current_seq)
            i = 0
            while i < len(visited):
                if visited[i].sequence == temp_sequence:
                    break
                i += 1
            if i == len(visited):
                possible_seq.append(temp_sequence)
    for seq in possible_seq:
        new_node = generate_obj(seq, node)
        visited.append(new_node)
        output = Agent(current_depth + 1, depth, new_node, visited)
        # print(output)
        if output != None and output.sequence == goal:
            return output
        visited.pop()
    return None
            
# Main code
print("Enter goal_sequence - ", end = "")
goal = input().split()
print(goal)
if len(goal) != 9:
        print("The length of sequence should be equal to 9")
        exit
goal = [int(i) for i in goal]
print("Enter depth - ", end = "")
depth = int(input())
input_s = generate_sequence(goal, depth)
current_node = generate_obj(input_s, None)
start = time.time()
output = Agent(0, depth, current_node, [current_node])
end = time.time()
if output != None and output.sequence == goal:
    print("Goal Found")
    print_sequence(output.sequence)
    length, container = back_track(output)
    for i in reversed(container):
        print_sequence(i)
    print("Height is ", length)
else:
    print("Goal not found")
print("Time taken is - ", end - start, "sec")
