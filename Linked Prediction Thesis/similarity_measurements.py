import networkx as nx
from centrality_measurements import save_as_csv
import os
from collections import OrderedDict
import numpy

def save_to_file_similarities(E1,j):
    node_list = list(E1.nodes)
    temp_short_path, temp_cn, temp_jc, temp_a, temp_pa = {} , {}, {}, {}, {}
    #calculation start
    for node1 in node_list:
        for node2 in node_list:
            temp = nx.jaccard_coefficient(E1, [(node1,node2)] )
            for u, v, p in temp:
                temp_jc[u,v]=p


            temp = nx.adamic_adar_index(E1, [(node1,node2)])
            try:
                for u, v, p in temp:
                    temp_a[u,v]= p

            except:
                    temp_a[u,v]= 0.0


            temp = nx.preferential_attachment(E1, [(node1,node2)] )
            for u, v, p in temp:
                temp_pa[u,v] = p

            temp = sorted(nx.common_neighbors(E1, node1, node2))
            temp_common_neighbors = []
            temp = sorted(nx.common_neighbors(E1, node1, node2))
            for common_neighbor in temp:
                temp_common_neighbors.append(common_neighbor)
            temp_cn[node1, node2] = (len(temp_common_neighbors))

            #Ill use Exception Checking cause we have DiGraph and maybe there is no path between to nodes
            #so an error would compile
            try:
                length = nx.shortest_path_length(E1, node1, node2)
                temp_short_path[node1, node2] =length

            except:
                temp_short_path[node1,node2]=0.0


    #calculation ends
    temp_cn         = OrderedDict(sorted(temp_cn.items(), key=lambda kx: kx[1]))
    temp_short_path = OrderedDict(sorted(temp_short_path.items(), key=lambda kx: kx[1]))
    temp_jc         = OrderedDict(sorted(temp_jc.items(), key=lambda kx: kx[1]))
    temp_a          = OrderedDict(sorted(temp_a.items(), key=lambda kx: kx[1]))
    temp_pa         = OrderedDict(sorted(temp_pa.items(), key=lambda kx: kx[1]))
    directory = 'Subgraphs/Similarities/' + 'T' + str(j-1) + '-' + 'T' +str(j+1) + '_E_' + 'T' + str(j-1) + '-' + 'T' +str(j)
    if not os.path.exists(directory):
        os.makedirs(directory)

    temp_path = temp_path = directory + '/' + str(E1.graph['name'])

    save_as_csv(temp_path + '_shortest_path', temp_short_path, ['Node', 'Length of Shortest Path'])
    save_as_csv(temp_path + '_jaccard_coef', temp_jc, ['(Node1, Node2)', 'Jaccard Coefficient'])
    save_as_csv(temp_path + '_pref_attach.txt', temp_pa, ['(Node1, Node2)', 'Preferential Attachment'])
    save_as_csv(temp_path + '_adamic_index.txt', temp_a, ['(Node1, Node2)', 'Adamic Index'])
    save_as_csv(temp_path + '_common_neigh.txt', temp_cn, ['(Node1, Node2)', '# of Common Neighbors'])

def nodes_connected(E1, u, v):
    return u in E1.neighbors(v)

#https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.operators.binary.intersection.html
def intersection_of_two_graphs_edges(H1,H2):
    #we dont use the nx.intersection because sets of graph is not equal and it compiles an error
    #Also we are not losing attributes
    intersected_graph= nx.Graph(H1.edges) # in documentation it was with Copy but with that we had error on similarities calculation
    intersected_graph.remove_nodes_from(n for n in H1 if n not in H2)
    return intersected_graph

def intersection_of_two_graphs(G,H):
    R=G.copy()
    R.remove_nodes_from(n for n in G if n not in H)
    return R

def get_N(cartesian1,cartesian2,remove1,remove2):
    product_graph = nx.cartesian_product(cartesian1,cartesian2)
    product_graph.remove_nodes_from(remove1.edges())
    product_graph.remove_nodes_from(remove2.edges())

    return product_graph


def calculate_similarities(E1,tmp_string = None):
    features = []
    ytarget  = []
    tmp_feat = {}
    tmp_y    = {}
    temp_common_neighbors = []
    node_list = list(E1.nodes)
    for node1 in node_list:
        for node2 in node_list:
	    connected = 0
            if tmp_string == "n":
                if nodes_connected(E1,node1,node2):
                    continue
                else:
                    temp = nx.jaccard_coefficient(E1, [(node1,node2)] )
                    for u, v, p in temp:
                        tmp_feat[u,v]=[p]
                        tmp_y[u,v] = connected

                    temp = nx.adamic_adar_index(E1, [(node1,node2)])
                    try:
                        for u, v, p in temp:
                            tmp_feat[u,v].append(p)
                            tmp_y[u,v] = connected
                    except:
                            tmp_feat[u,v].append(0.0)
                            tmp_y[u,v] = connected

                    temp = nx.preferential_attachment(E1, [(node1,node2)] )
                    for u, v, p in temp:
                        tmp_feat[u,v].append(p)
                        tmp_y[u,v] = connected
                    temp = sorted(nx.common_neighbors(E1, node1, node2))
                    temp_common_neighbors = []
                    temp = sorted(nx.common_neighbors(E1, node1, node2))
                    for common_neighbor in temp:
                        temp_common_neighbors.append(common_neighbor)
                    tmp_feat[node1, node2].append(len(temp_common_neighbors))

                    #Ill use Exception Checking cause we have DiGraph and maybe there is no path between to nodes
                    #so an error would compile
                    try:
                        length = nx.shortest_path_length(E1, node1, node2)
                        tmp_feat[node1, node2].append(length)
                        tmp_y[node1,node2] = connected
                    except:
                        tmp_feat[node1,node2].append(0.0)
                        tmp_y[node1,node2] = connected

            else:
                if nodes_connected(E1,node1,node2):
                    connected = 1
                temp = nx.jaccard_coefficient(E1, [(node1,node2)] )
                for u, v, p in temp:
                    tmp_feat[u,v]=[p]
                    tmp_y[u,v] = connected

                temp = nx.adamic_adar_index(E1, [(node1,node2)])
                try:
                    for u, v, p in temp:
                        tmp_feat[u,v].append(p)
                        tmp_y[u,v] = connected
                except:
                        tmp_feat[u,v].append(0.0)
                        tmp_y[u,v] = connected

                temp = nx.preferential_attachment(E1, [(node1,node2)] )
                for u, v, p in temp:
                    tmp_feat[u,v].append(p)
                    tmp_y[u,v] = connected
                temp = sorted(nx.common_neighbors(E1, node1, node2))
                temp_common_neighbors = []
                temp = sorted(nx.common_neighbors(E1, node1, node2))
                for common_neighbor in temp:
                    temp_common_neighbors.append(common_neighbor)
                tmp_feat[node1, node2].append(len(temp_common_neighbors))

                #Ill use Exception Checking cause we have DiGraph and maybe there is no path between to nodes
                #so an error would compile
                try:
                    length = nx.shortest_path_length(E1, node1, node2)
                    tmp_feat[node1, node2].append(length)
                    tmp_y[node1,node2] = connected
                except:
                    tmp_feat[node1,node2].append(0.0)
                    tmp_y[node1,node2] = connected



    for key, value in tmp_feat.items():
        features.append(value)
    for key,value in tmp_y.items():
        ytarget.append(value)


    features_numpy = numpy.array(features)
    y_target_numpy = numpy.array(ytarget)

    return features_numpy , y_target_numpy
