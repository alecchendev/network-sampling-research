
import operator as op
from functools import reduce

class Network():
    def __init__(self, nodes, edges):
        print("Initializing network...")
        self.nodes = set()
        self.edges = set()
        self.n_nodes = 0
        self.n_edges = 0
        self.adj = {}
        self.add_nodes(nodes)
        self.add_edges(edges)
        print("Done initializing.")

    def add_nodes(self, nodes):
        self.nodes.update(nodes)
        for node in nodes:
            self.adj[node] = set()
        self.n_nodes = self.calc_n_nodes()

    def add_edges(self, edges):
        self.edges.update(edges)
        for edge in edges:
            self.adj[edge[0]].add(edge[1])
            self.adj[edge[1]].add(edge[0])
        self.n_edges = self.calc_n_edges()

    def clear_nodes(self):
        self.nodes.clear()
        self.edges.clear()
        self.adj = {}

    def clear_edges(self):
        self.edges.clear()
        for node in self.adj:
            self.adj[node] = set()

    def calc_n_nodes(self):
        return len(self.nodes)

    def calc_n_edges(self):
        return len(self.edges)

    def degree(self, node):
        return len(self.adj[node])

    def max_degree(self):
        degrees = set()
        for node in self.nodes:
            degrees.add(self.degree(node))
        return max(degrees)

    def clustering_coefficient(self, node):
        degree = self.degree(node)
        if (degree <= 1):
            raise Exception("node has no edges, therefore no clustering coefficient")
            #return 0.0
        n_neighbor_edges = 0.0
        neighbors = list(self.adj[node])
        for i in range(0, len(neighbors)):
            for j in range(i+1, len(neighbors)):
                if (neighbors[i], neighbors[j]) in self.edges or (neighbors[j], neighbors[i]) in self.edges:
                    n_neighbor_edges += 1.0
        cc = 2.0 * n_neighbor_edges / (degree * (degree - 1.0))
        return cc

    def no_cc(self, node):
        return self.degree(node) <= 1

    def max_cc(self):
        ccs = set()
        for node in self.nodes:
            if not self.no_cc(node):
                ccs.add(self.clustering_coefficient(node))
        return max(ccs)

    def restriction(self, node):
        return False

    def remove_self_edges(self):
        new_edges = set()
        for edge in self.edges:
            if (edge[0] != edge[1]):
                new_edges.add(edge)
        self.clear_edges()
        self.add_edges(new_edges)

    def random_node(self):
        random_index = random.randint(0, len(self.nodes) - 1)
        return list(self.nodes)[random_index]

    def maxed_nodes(self):
        nodes = set()
        for node in self.nodes:
            if (self.degree(node) == (self.n_nodes - 1)):
                nodes.add(node)
        return nodes

    def n_triangles(self):
        n_triangles = 0.0
        finished_nodes = set()
        for node in self.adj:
            neighbors = list(self.adj[node].difference(finished_nodes))
            for i in range(0, len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    if (neighbors[i], neighbors[j]) in self.edges or (neighbors[j], neighbors[i]) in self.edges:
                        n_triangles += 1.0
            finished_nodes.add(node)
        return n_triangles

    def transitivity(self):
        n_triangles = 0.0
        n_triples = 0.0
        for node in self.adj:
            neighbors = list(self.adj[node])
            for i in range(0, len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    n_triples += 1.0
                    if (neighbors[i], neighbors[j]) in self.edges or (neighbors[j], neighbors[i]) in self.edges:
                        n_triangles += 1.0
        if (n_triples == 0):
            return 0.0
        return (n_triangles / 3.0) / (n_triples / 3.0)

    #this is slower than n_triangles because it creates a list then finds whether it's complete
    def k_core(self, k):
         n_k_core = 0.0
         finished_nodes = set()
         for node in self.adj:
             neighbors = list(self.adj[node].difference(finished_nodes))
             n_neighbors = len(neighbors)
             if n_neighbors >= k - 1:
                 k_node_groups = set()
                 self.nodes_choose_r_nodes(neighbors, k - 1, k_node_groups, set(), 0, 0)
                 for k_node_group in k_node_groups:
                     if self.is_complete(k_node_group):
                         n_k_core += 1.0
             finished_nodes.add(node)
         return n_k_core

    def nodes_choose_r_nodes(self, nodes, r, r_node_groups, r_node_group, runs, start_index):
        if (runs < r):
            runs += 1
            for i in range(start_index, len(nodes)):
                r_node_group_temp = r_node_group.copy()
                r_node_group_temp.add(list(nodes)[i])
                self.nodes_choose_r_nodes(nodes, r, r_node_groups, r_node_group_temp, runs, i+1)
        else:
            r_node_groups.add(tuple(r_node_group))

    #cant import from statistics
    def ncr(self, n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom

    def is_complete(self, nodes):
        for node1_index in range(0, len(nodes)):
            for node2_index in range(node1_index + 1, len(nodes)):
                if nodes[node2_index] not in self.adj[nodes[node1_index]]:
                    return False
        return True

