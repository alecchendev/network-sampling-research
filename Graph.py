
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

import networkx as nx

def matplotlib_graph(nx_graph):
    plt.subplot(121)
    nx.draw(nx_graph)   # default spring_layout
    plt.show()

def plotly_graph(G, gNodes, gEdges):
    # getting positions of nodes
    pos = nx.spring_layout(G)
    # print(pos)
    Xn = [pos[k][0] for k in gNodes]
    Yn = [pos[k][1] for k in gNodes]

    # defining plotly trace for the nodes
    labels = []
    for node in gNodes:
        labels.append(str(node))

    trace_nodes = dict(type='scatter',
                       x=Xn,
                       y=Yn,
                       mode='markers',
                       marker=dict(size=15, color='rgb(0,240,0)'),
                       text=labels,
                       hoverinfo='text')

    # record the coordinates of the edges' nodes
    Xe = []
    Ye = []
    for e in G.edges():
        Xe.extend([pos[e[0]][0], pos[e[1]][0], None])
        Ye.extend([pos[e[0]][1], pos[e[1]][1], None])

    # define plotly trace for edges
    trace_edges = dict(type='scatter',
                       mode='lines',
                       x=Xe,
                       y=Ye,
                       line=dict(width=1, color='rgb(25,25,25)'),
                       hoverinfo='none'
                       )

    # misc definitions needed for plotly to graph
    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
                )
    layout = dict(title='My Graph',
                  font=dict(family='Balto'),
                  width=600,
                  height=600,
                  autosize=False,
                  showlegend=False,
                  xaxis=axis,
                  yaxis=axis,
                  margin=dict(
                      l=40,
                      r=40,
                      b=85,
                      t=100,
                      pad=0,

                  ),
                  hovermode='closest',
                  plot_bgcolor='#efecea',  # set background color
                  )

    fig = dict(data=[trace_edges, trace_nodes], layout=layout)

    # plot it
    py.plot(fig)