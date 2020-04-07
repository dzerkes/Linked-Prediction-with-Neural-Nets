import matplotlib.pyplot as plt

import networkx as nx
import pandas as pd


user_input = raw_input('Please insert the number of graph you want for plotting. \n (example 2 ) ->\t')

name = 'Subgraphs/Stackoverflow_sub_graph_' + str(user_input) + '.csv'

df = pd.read_csv(name, sep=",", header=None, names=['SourceID', 'TargetID', 'Timestamp'])
G = nx.from_pandas_edgelist(df, source='SourceID', target='TargetID', edge_attr=True, create_using=nx.DiGraph())
plt.subplot(2, 2,1)
plt.title(name)
nx.draw(G, node_size=25, arrow_size=10)

plt.gcf().canvas.set_window_title('Stackoverflow Sub Graphs')
plt.gcf().set_size_inches(15, 10)
plt.show()
