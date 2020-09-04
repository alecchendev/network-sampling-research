
import random
from Network import *
from Statistics import get_cdf
import time

#random network generation
#for 1000 nodes 5000 edges it takes less than 4 seconds, 10000 edges roughly 12 seconds
def random_network(n_nodes, n_edges, min_degree = 0):
    nodes = set(list(range(n_nodes)))
    edges = set()
    new_network = Network(nodes, edges)
    print("Filling random network...")
    #increases run time by a decent bit near higher nodes and edges
    if (n_edges >= max_edges(n_nodes)):
        print("complete network")
        return complete_network(n_nodes)

    raise_min(new_network, min_degree, n_edges)
    maxed_nodes = set()
    degree_max = n_nodes - 1
    for i in range(0, n_edges - new_network.n_edges):
        possible_nodes = new_network.nodes.difference(maxed_nodes)
        node1 = get_random_node(possible_nodes)
        possible_nodes.remove(node1)
        new_adj_nodes = possible_nodes.difference(new_network.adj[node1])
        node2 = get_random_node(new_adj_nodes)
        new_edge = (node1, node2)
        new_network.add_edges({new_edge})
        if new_network.degree(node1) == (degree_max):
            maxed_nodes.add(node1)
        if new_network.degree(node2) == (degree_max):
            maxed_nodes.add(node2)
    print("Done filling.")
    return new_network

def is_viable_edge(edge, edges):
    if (edge[0] != edge[1]):
        if (edge not in edges) and ((edge[1], edge[0]) not in edges):
            return True
    print("not viable")
    return False

def get_random_node(nodes):
    random_index = random.randint(0, len(nodes) - 1)
    return list(nodes)[random_index]

def get_random_edge(edges):
    random_index = random.randint(0, len(edges) - 1)
    return list(edges)[random_index]

def raise_min(network, min_degree, n_edges):
    for node in network.nodes:
        possible_nodes = network.nodes.copy().difference(network.adj[node])
        possible_nodes.remove(node)
        while (network.degree(node) < min_degree) and (network.n_edges < n_edges):
            node2 = get_random_node(possible_nodes)
            new_edge = (node, node2)
            network.add_edges({new_edge})
            possible_nodes.remove(node2)

def complete_network(n_nodes):
    nodes = set(list(range(n_nodes)))
    edges = set()
    network = Network(nodes, edges)
    for i in range(0, n_nodes):
        for j in range(i + 1, n_nodes):
            node1 = list(network.nodes)[i]
            node2 = list(network.nodes)[j]
            new_edge = (node1, node2)
            edges.add(new_edge)
    network.add_edges(edges)
    return network

def max_edges(n_nodes):
    return (n_nodes * (n_nodes - 1) / 2)

#random degree node methods
def random_degree_node_sample1(network, sample_size):
    new_nodes = set()
    for node in network.nodes:
        random_num = random.uniform(0, 1)
        node_prob = (0.0 + network.degree(node)) / network.max_degree * 0.5
        if random_num < node_prob:
            new_nodes.add(node)
    return new_nodes

def random_degree_node_sample(network, sample_size):
    new_nodes = set()
    node_probabilities = {}
    print("calculating cdf...")
    for i in range(0, network.n_nodes):
        node = list(network.nodes)[i]
        probability = (0.0 + network.degree(node)) / (2.0 * network.n_edges)
        if (i == 0):
            node_probabilities[i] = probability
        else:
            node_probabilities[i] = probability + node_probabilities[i-1]
    print("calculating nodes...")
    for i in range(0, int(round(network.n_nodes * sample_size))):
        random_num = random.uniform(0, max(node_probabilities.values()))
        new_node = min(node_probabilities, key=lambda node: abs(node_probabilities[node] - random_num))
        new_nodes.add(new_node)
        #del node_probabilities[new_node]
        node_probabilities.pop(new_node, None)
    return new_nodes

def random_degree_node_network(network, sample_size):
    nodes = random_degree_node_sample(network, sample_size)
    edges = induce_edges(nodes, network.edges)
    return Network(nodes, edges)

#random edge selection
def random_edge_network(network, sample_size, induced = False):
    new_nodes = set()
    new_edges = set()
    possible_edges = network.edges.copy()
    while len(new_nodes) < int(round(network.n_nodes * sample_size)):
        new_edge = get_random_edge(possible_edges)
        new_edges.add(new_edge)
        possible_edges.remove(new_edge)
        new_nodes.add(new_edge[0])
        new_nodes.add(new_edge[1])
    nodes = new_nodes
    edges = get_edges(induced, nodes, network.edges, new_edges)
    return Network(nodes, edges)

#snowball methods
'''This algorithm every once in a while gets lower than the target sample_size for two reasons
   Case 1: It is a disconnected network, so it literally cannot snowball to some of the nodes
   Case 2: It visits nodes with similar neighbors, causing it to cut off because it has no 
   possible new nodes to visit
   Case 2 can be solved by telling it to visit neighbors with the least similar neighbors but I'm lazy'''
def snowball_network(network, sample_size, n_neighbors, induced = False):
    visited_nodes, visited_edges, nodes_queue, temp_visited = set(), set(), set(), set()
    starting_node = get_random_node(network.nodes)
    nodes_queue.add(starting_node)
    visited_nodes.update(nodes_queue)
    while (len(nodes_queue) > 0) and (len(visited_nodes) < (sample_size * network.n_nodes)):
        for node in nodes_queue:
            new_neighbors = network.adj[node].difference(visited_nodes).difference(temp_visited)
            neighbor_limit = min(len(new_neighbors), n_neighbors)
            visit_neighbors(neighbor_limit, new_neighbors, visited_edges, node, temp_visited)
        update_visited_nodes(visited_nodes, temp_visited, sample_size, network.n_nodes, visited_edges)
        nodes_queue.clear()
        nodes_queue.update(temp_visited)
        temp_visited.clear()
    nodes = visited_nodes
    edges = get_edges(induced, nodes, network.edges, visited_edges)
    return Network(nodes, edges)

#snowball helper methods
def remove_common(set1, set2):
    new_set = set()
    for element in set1:
        if element not in set2:
            new_set.add(element)
    return new_set

def visit_neighbors(neighbor_limit, new_neighbors, visited_edges, node, temp_visited):
    neighbor_nodes = set()
    for i in range(0, neighbor_limit):
        random_node = get_random_node(new_neighbors)
        neighbor_nodes.add(random_node)
        new_edge = (node, random_node)
        if is_viable_edge(new_edge, visited_edges):
            visited_edges.add(new_edge)
        new_neighbors.remove(random_node)
    temp_visited.update(neighbor_nodes)

def update_visited_nodes(visited_nodes, temp_visited, sample_size, n_nodes, visited_edges):
    if overflows_sample_size(visited_nodes, temp_visited, sample_size, n_nodes):
        fill_nodes_to_brim(temp_visited, visited_nodes, sample_size, n_nodes)
        fill_edges_to_brim(temp_visited, visited_nodes, visited_edges)
    else:
        visited_nodes.update(temp_visited)

def overflows_sample_size(visited_nodes, temp_visited, sample_size, n_nodes):
    return len(visited_nodes) + len(temp_visited) > (sample_size * n_nodes)

def fill_nodes_to_brim(temp_visited, visited_nodes, sample_size, n_nodes):
    for node in temp_visited:
        if len(visited_nodes) < (sample_size * n_nodes):
            visited_nodes.add(node)
        else:
            break

def fill_edges_to_brim(temp_visited, visited_nodes, visited_edges):
    unwanted_nodes = temp_visited.difference(visited_nodes)
    for node in unwanted_nodes:
        for edge in visited_edges.copy():
            if (node in edge):
                visited_edges.remove(edge)

def get_edges(induced, nodes, edges, visited_edges):
    if induced:
        return induce_edges(nodes, edges)
    else:
        return visited_edges

#other
def induce_edges(nodes, edges):
    new_edges = set()
    for edge in edges:
        if edge[0] in nodes and edge[1] in nodes:
            new_edges.add(edge)
    return new_edges