import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import matplotlib.colors as mcolors
import os



def centrality_measurements(H):
# calculate
    temp_deg = nx.degree_centrality(H)
    temp_in_deg = nx.in_degree_centrality(H)
    temp_out_deg = nx.out_degree_centrality(H)
    temp_close_centr = nx.closeness_centrality(H)
    temp_bet_centr = nx.betweenness_centrality(H)
    temp_eig_centr = nx.eigenvector_centrality_numpy(H)
    temp_katz_centr = nx.katz_centrality_numpy(H)

    return temp_deg ,  temp_in_deg,   temp_out_deg,  temp_close_centr,  temp_bet_centr, temp_eig_centr,    temp_katz_centr


def centrality_drawing(G, measures, measure_name):
    pos = nx.spring_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=250, cmap=plt.cm.plasma,
                                   node_color=measures.values(),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))

    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()


def save_as_csv(file_name, temp_data, columns):

    temp_df = pd.DataFrame(temp_data.items(), columns=columns)
    temp_df.to_csv(path_or_buf=file_name + '.csv', sep=',', index=False)


def save_to_file(G, temp_deg, temp_in_deg, temp_out_deg, temp_close_centr, temp_bet_centr, temp_eig_centr, temp_katz_centr,j):

    directory = 'Subgraphs/Centralities/' + 'T' + str(j)
    if not os.path.exists(directory):
        os.makedirs(directory)

    temp_path = temp_path = directory + '/' + str(G.graph['name'])

    save_as_csv(temp_path + '_in_degree_centrality', temp_deg, ['Node', 'Degree Centrality'])
    save_as_csv(temp_path + '_in_degree_centrality', temp_in_deg, ['Node', 'In Degree Centrality'])
    save_as_csv(temp_path + '_out_degree_centrality', temp_out_deg, ['Node', 'Out Degree Centrality'])
    save_as_csv(temp_path + '_close_centrality', temp_close_centr, ['Node', 'Closeness Centrality'])
    save_as_csv(temp_path + '_bet_centrality', temp_bet_centr, ['Node', 'Betweenness Centrality'])
    save_as_csv(temp_path + '_eig_centrality', temp_eig_centr, ['Node', 'Eigenvector Centrality'])
    save_as_csv(temp_path + '_katz_centrality', temp_katz_centr, ['Node', 'Katz Centrality'])

def draw_all(G, temp_deg, temp_in_deg, temp_out_deg, temp_close_centr, temp_bet_centr, temp_eig_centr, temp_katz_centr):
    centrality_drawing(G, temp_deg, 'DiGraph Degree Centrality')
    centrality_drawing(G, temp_in_deg, 'Digraph In-Degree Centrality')
    centrality_drawing(G, temp_out_deg, 'Digraph Out-Degree Centrality')
    centrality_drawing(G, temp_close_centr, 'Closeness Centrality')
    centrality_drawing(G, temp_bet_centr, 'Betweenness Centrality')
    centrality_drawing(G, temp_eig_centr,'DiGraph Eigenvector Centrality')
    centrality_drawing(G, temp_katz_centr,  'DiGraph Katz Centrality')
