
import plotly.plotly as py
import plotly.graph_objs as go

import networkx as nx

import random
import time

from Network import *
from SamplingMethods import *
from Statistics import *
from Graph import *

def make_nodes_list(nNodes):
    nodesList = set()
    for i in range(0, nNodes):
        nodesList.add(i)
    return (nodesList)

def get_nodes_list(filename, seperator):
    data = open(filename, "r")
    nodes = set()
    for line in data:
        values = line.split(seperator)
        for value in values:
            if (value not in nodes):
                nodes.add(int(value))
    return nodes

# returns set of edges as tuples from the given file
def read_edges_file(filename, seperator):
    data = open(filename, "r")
    edgesList = set()
    for line in data:
        values = line.split(seperator)
        for i in range(0, len(values)):
            values[i] = int(values[i])
        new_edge = tuple(values)
        edgesList.add(new_edge)
    return edgesList

def output_distributions_txt(filename, cdf1, cdf2):
    output_file = open(filename, "w")
    output_file.write("\n")
    for i in range(0, len(cdf1)):
        output_file.write(str(cdf1[i]) + "\t" + str(cdf2[i]) + "\n")

def output_statistics(N, NS):
    print("Calculating statistics...")

    '''print("original nodes: " + str(N.nodes))
    print("original edges: " + str(N.edges))
    print("sample nodes: " + str(NS.nodes))
    print("sample edges: " + str(NS.edges))'''

    print("original n_nodes: " + str(N.n_nodes))
    print("sample n_nodes: " + str(NS.n_nodes))
    print("original n_edges: " + str(N.n_edges))
    print("sample n_edges: " + str(NS.n_edges))

    print("original n_triangles: " + str(N.n_triangles()))
    print("sample n_triangles: " + str(NS.n_triangles()))
    print("original transitivity: " + str(N.transitivity()))
    print("sample transitivity: " + str(NS.transitivity()))

    average_degree_o = get_average(N, N.degree, N.restriction)
    average_degree_s = get_average(NS, NS.degree, NS.restriction)
    print("original average_degree: " + str(average_degree_o))
    print("sample average_degree: " + str(average_degree_s))
    print("sample average_degree2: " + str(get_average_degree(NS)))

    average_cc_o = get_average(N, N.clustering_coefficient, N.no_cc)
    average_cc_s = get_average(NS, NS.clustering_coefficient, NS.no_cc)
    print("original average_cc: " + str(average_cc_o))
    print("sample average_cc: " + str(average_cc_s))

    degree_step_size = 1
    max_degree = max(N.max_degree(), NS.max_degree())
    degree_pdf_o = get_pdf(N, N.degree, N.restriction, max_degree, int(max_degree + 1))
    degree_cdf_o = get_cdf(degree_pdf_o)
    degree_pdf_s = get_pdf(NS, NS.degree, NS.restriction, max_degree, int(max_degree + 1))
    degree_cdf_s = get_cdf(degree_pdf_s)
    degree_ks = ks_test(degree_cdf_o, degree_cdf_s)
    print("original degree_pdf: " + str(degree_pdf_o))
    print("original degree_cdf: " + str(degree_cdf_o))
    print("sample degree_pdf: " + str(degree_pdf_s))
    print("sample degree_cdf: " + str(degree_cdf_s))
    print("degree ks: " + str(degree_ks))
    print("degree ks: " + str(degree_ks))
    output_distributions_txt("degreeDist.txt", degree_cdf_o, degree_cdf_s)

    cc_step_size = 0.05
    max_cc = 1#max(N.max_cc(), NS.max_cc())
    cc_pdf_o = get_pdf(N, N.clustering_coefficient, N.no_cc, max_cc, int(max_cc + 1))
    cc_cdf_o = get_cdf(cc_pdf_o)
    cc_pdf_s = get_pdf(NS, NS.clustering_coefficient, NS.no_cc, max_cc, int(max_cc + 1))
    cc_cdf_s = get_cdf(cc_pdf_s)
    cc_ks = ks_test(cc_cdf_o, cc_cdf_s)
    print("original cc_pdf: " + str(cc_pdf_o))
    print("original cc_cdf: " + str(cc_cdf_o))
    print("sample cc_pdf: " + str(cc_pdf_s))
    print("sample cc_cdf: " + str(cc_cdf_s))
    print("cc ks: " + str(cc_ks))
    output_distributions_txt("ccDist.txt", cc_cdf_o, cc_cdf_s)

    print("Done with stats.")

def get_average_runtime(num_nodes, num_edges, minimum_degree = 0):
    times = []
    for i in range(0, 100):
        starting_time = time.time()
        network = random_network(num_nodes, num_edges, minimum_degree)
        time_taken = (time.time() - starting_time)
        # print("--- %s seconds ---" % time_taken)
        times.append(time_taken)
    print("average run time: " + str(get_average_iterable(times)))

tvNodes = 3892
numNodes = tvNodes

edgesFile = "tvshow_edges.csv"
seperator = ","

###Create original network from file
#allNodes = make_nodes_list(numNodes)
#allNodes = get_nodes_list(edgesFile, seperator)
#allEdges = read_edges_file(edgesFile, seperator)
#N = Network(allNodes, allEdges)
#N.remove_self_edges()

n_nodes = 50
n_edges = int(round(ncr(n_nodes, 2) * 0.5))
min_degree = 1

###Create random network from parameters
N = random_network(n_nodes, n_edges, min_degree)

###Create sample network
print ("Starting sampling...")

NS = Network(N.nodes, N.edges)

sample_size = 0.1
starting_time = time.time()
#NS = random_degree_node_network(N, sample_size)
#NS = random_edge_network(N, sample_size, induced = True)

n_neighbors = 2
#NS = snowball_network(N, sample_size, n_neighbors, induced = True)

print (str(time.time() - starting_time))
print("Done sampling.")

###STATISTICS
output_statistics(N, NS)

###Draw network
print("Drawing graph...")

#make nx graph so you can visualize it
G = nx.Graph()
G.add_nodes_from(NS.nodes)
G.add_edges_from(NS.edges)

#print("nx average degree: " + str(G.degree))
#print("nx sample cc: " + str(nx.average_clustering(G)))

matplotlib_graph(G)
#plotly_graph(G, list(NS.nodes), list(NS.edges))