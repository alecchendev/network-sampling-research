
from SamplingMethods import *
import operator as op
from functools import reduce
from math import *

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

def get_average_iterable(values):
    total = 0.0
    for value in values:
        total += value
    return total / len(values)

def get_average_degree(network):
    return 2.0 * network.n_edges / network.n_nodes

def get_average(network, node_statistic, restriction):
    total = 0.0
    for node in network.nodes:
        if not restriction(node):
            total += node_statistic(node)
    average = (0.0 + total) / network.n_nodes
    return average

#cant import from sampling methods
def get_random_node(nodes):
    random_index = random.randint(0, len(nodes) - 1)
    return list(nodes)[random_index]

def get_pdf(network, node_statistic, restriction, upper_bound, n_steps, scale = 1.0):
    step_size = (0.0 + upper_bound) / (n_steps - 1)
    distribution = [0.0 for i in range(0, n_steps + 1)]
    count = 0.0
    for node in network.nodes:
        if not restriction(node):
            statistic = (0.0 + node_statistic(node)) / scale
            index = int(round(statistic / step_size))
            distribution[index] += 1.0
            count += 1.0
    if count == 0:
        return distribution
    for i in range(0, len(distribution)):
        distribution[i] = distribution[i] / count
    return distribution

def get_cdf(pdf):
    cdf = []
    for i in range(0, len(pdf)):
        element = 0.0
        for j in range(0, i+1):
            element += pdf[j]
        cdf.append(element)
    return cdf

def ks_test(cdf1, cdf2):
    distribution_difference = set()
    for index in range(0, len(cdf1)):
        difference = abs(cdf1[index] - cdf2[index])
        distribution_difference.add(difference)
    max_difference = max(distribution_difference)
    return max_difference

def get_scaled_distribution(distribution, n_steps):
    scaled_distribution = []
    n_values = len(distribution)
    step = (0.0 + n_values - 1) / (n_steps - 1)
    for index in range(0, n_steps):
        value = find_interpolation(distribution, index * step)
        scaled_distribution.append(value)
    return scaled_distribution

def ks_test_scaled(cdf1, cdf2, n_steps):
    max_difference = 0
    cdf1_len = len(cdf1)
    cdf2_len = len(cdf2)
    cdf1_step = (0.0 + cdf1_len - 1) / (n_steps - 1)
    cdf2_step = (0.0 + cdf2_len - 1) / (n_steps - 1)
    for index in range(0, n_steps):
        value1 = find_interpolation(cdf1, index * cdf1_step)
        value2 = find_interpolation(cdf2, index * cdf2_step)
        difference = abs(value1 - value2)
        if (difference > max_difference):
            max_difference = difference
    return max_difference

def find_interpolation(distribution, index):
    upper_index = int(ceil(index))
    if (upper_index > len(distribution) - 1):
        upper_index = len(distribution) - 1
    lower_index = int(floor(index))
    if (upper_index == lower_index):
        return distribution[int(index)]
    slope = (distribution[upper_index] - distribution[lower_index]) / (upper_index - lower_index)
    interpolation = distribution[lower_index] + slope * (index - lower_index)
    return interpolation

def add_lists(adder, receiving):
    for i in range(0, len(adder)):
        receiving[i] += adder[i]