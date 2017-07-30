from utils import *
import random
import copy

points = []
dis = []
roulette = []
fitnessValues = []
values = []
population = []
current_best = {}
best_value = None
best = []
UNCHANGED_GENS = 0
mutation_times = 0
POPULATION_SIZE = 30
CROSSOVER_PROBABILITY = 0.9
MUTATION_PROBABILITY = 0.01
current_generation = 0
GET_TIME = 2048


def count_distance():
    global dis
    length = len(points)
    # dis = [[0] * length] * length
    for i in range(length):
        dis_row = []
        for j in range(length):
            # dis[i][j] = distance(points[i], points[j])
            dis_row.append(int(distance(points[i], points[j])))
        dis.append(dis_row)


def evaluate(individual):
    ind_len = len(individual)
    dis_sum = dis[individual[0]][individual[ind_len - 1]]
    for i in range(1, ind_len):
        dis_sum += dis[individual[i]][individual[i - 1]]
    return dis_sum


def random_individual(n):
    a = []
    for i in range(n):
        a.append(i)
    random.shuffle(a)
    return a


def wheel_out(rand):
    for i in range(len(roulette)):
        if rand <= roulette[i]:
            return i


def set_roulette():
    global fitnessValues, roulette

    for i in range(len(fitnessValues)):
        fitnessValues[i] = 1.0 / values[i]
    fv_sum = 0
    for i2 in range(len(fitnessValues)):
        fv_sum += fitnessValues[i2]
    for i3 in range(len(roulette)):
        roulette[i3] = fitnessValues[i3] / fv_sum
    for i4 in range(len(roulette)):
        roulette[i4] += roulette[i4 - 1]


def get_current_best():
    best_p = 0
    current_best_value = values[0]

    for i in range(1, len(population)):
        if values[i] < current_best_value:
            current_best_value = values[i]
            best_p = i
    return {'best_position': best_p, 'best_value': current_best_value}


def set_best_value():
    global current_best, best_value, best, UNCHANGED_GENS, values

    for i in range(len(population)):
        values[i] = evaluate(population[i])

    current_best = get_current_best()
    if (best_value is None) or (best_value > current_best['best_value']):
        best = copy.deepcopy(population[current_best['best_position']])
        best_value = current_best['best_value']
        UNCHANGED_GENS = 0
    else:
        UNCHANGED_GENS = 1


def push_mutate(seq):
    global mutation_times
    mutation_times += 1
    m = 0
    n = 0
    while m >= n:
        m = random.randint(0, (len(seq) >> 1) - 1)
        n = random.randint(0, len(seq) - 1)

    s1 = seq[: m]
    s2 = seq[m: n]
    s3 = seq[n: len(seq)]
    s2[len(s2): len(s2)] = s1
    s2[len(s2): len(s2)] = s3
    return copy.deepcopy(s2)


def do_mutate(seq):
    global mutation_times
    mutation_times += 1
    m = 0
    n = 0
    while m >= n:
        m = random.randint(0, (len(seq) - 2) - 1)
        n = random.randint(0, len(seq) - 1)

    j = (n - m + 1) >> 1
    for i in range(j):
        swap(seq, m + i, n - i)
    return seq


def mutation():
    for i in range(POPULATION_SIZE):
        if random.random() < MUTATION_PROBABILITY:
            if random.random() > 0.5:
                population[i] = push_mutate(population[i])
            else:
                population[i] = do_mutate(population[i])
            i -= 1


def get_child(pre_or_next, x, y):
    solution = []
    px = copy.deepcopy(population[x])
    py = copy.deepcopy(population[y])
    c = px[random.randint(0, len(px) - 1)]
    solution.append(c)
    while len(px) > 1:
        if pre_or_next is True:
            dx = pre_of_list(px, px.index(c))
            dy = pre_of_list(py, py.index(c))
        else:
            dx = next_of_list(px, px.index(c))
            dy = next_of_list(py, py.index(c))
        px.pop(px.index(c))
        py.pop(py.index(c))
        c = dx if dis[c][dx] < dis[c][dy] else dy
        solution.append(c)
    return solution


def do_crossover(x, y):
    child_1 = get_child(False, x, y)
    child_2 = get_child(True, x, y)
    population[x] = child_1
    population[y] = child_2


def crossover():
    queue = []
    for k in range(POPULATION_SIZE):
        if random.random() < CROSSOVER_PROBABILITY:
            queue.append(k)
    random.shuffle(queue)
    for i in range(0, len(queue) - 1, 2):
        do_crossover(queue[i], queue[i + 1])


def selection():
    global population
    parents = []
    init_num = 4
    parents.append(population[current_best['best_position']])
    parents.append(do_mutate(copy.deepcopy(best)))
    parents.append(push_mutate(copy.deepcopy(best)))
    parents.append(copy.deepcopy(best))

    set_roulette()
    for i in range(init_num, POPULATION_SIZE):
        parents.append(population[wheel_out(random.random())])
    population = parents


def next_generation():
    global current_generation
    current_generation += 1
    selection()
    crossover()
    mutation()
    set_best_value()


def initialize():
    global values, fitnessValues, roulette
    count_distance()
    for i in range(POPULATION_SIZE):
        population.append(random_individual(len(points)))
    values = [0] * len(population)
    fitnessValues = [0] * len(values)
    roulette = [0] * len(fitnessValues)
    set_best_value()


def init_data():
    global points
    points = [
        {"x": 565, "y": 575},
        {"x": 25, "y": 185},
        {"x": 345, "y": 750},
        {"x": 945, "y": 685},
        {"x": 845, "y": 655},
        {"x": 880, "y": 660},
        {"x": 25, "y": 230},
        {"x": 525, "y": 1000},
        {"x": 580, "y": 1175},
        {"x": 650, "y": 1130},
        {"x": 1605, "y": 620},
        {"x": 1220, "y": 580},
        {"x": 1465, "y": 200},
        {"x": 1530, "y": 5},
        {"x": 845, "y": 680},
        {"x": 725, "y": 370},
        {"x": 145, "y": 665},
        {"x": 415, "y": 635},
        {"x": 510, "y": 875},
        {"x": 560, "y": 365},
        {"x": 300, "y": 465},
        {"x": 520, "y": 585},
        {"x": 480, "y": 415},
        {"x": 835, "y": 625},
        {"x": 975, "y": 580},
        {"x": 1215, "y": 245},
        {"x": 1320, "y": 315},
        {"x": 1250, "y": 400},
        {"x": 660, "y": 180},
        {"x": 410, "y": 250},
        {"x": 420, "y": 555},
        {"x": 575, "y": 665},
        {"x": 1150, "y": 1160},
        {"x": 700, "y": 580},
        {"x": 685, "y": 595},
        {"x": 685, "y": 610},
        {"x": 770, "y": 610},
        {"x": 795, "y": 645},
        {"x": 720, "y": 635},
        {"x": 760, "y": 650},
        {"x": 475, "y": 960},
        {"x": 95, "y": 260},
        {"x": 875, "y": 920},
        {"x": 700, "y": 500},
        {"x": 555, "y": 815},
        {"x": 830, "y": 485},
        {"x": 1170, "y": 65},
        {"x": 830, "y": 610},
        {"x": 605, "y": 625},
        {"x": 595, "y": 360},
        {"x": 1340, "y": 725},
        {"x": 1740, "y": 245}
    ]


if __name__ == '__main__':
    print('Init...')
    init_data()
    initialize()
    print('Start GA TSP...')
    while GET_TIME > 0:
        next_generation()
        GET_TIME -= 1
        print(best_value)
    print('End...')
