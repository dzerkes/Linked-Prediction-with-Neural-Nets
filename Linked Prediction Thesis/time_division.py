import pandas as pd
import networkx as nx

def timediv(parts,N):
     ##isws ksanavalw to tmpstring2 gia na min anoigw olo auto to arxeio

    #1) find Tmin and Tmax
    tmp_string_1 = 'Dataset/sliced_dataset_0.txt'
    tmp_string_2 = 'Dataset/sliced_dataset_8192.txt'
    dataframe1 = pd.read_csv(tmp_string_1, sep=" ", header=None, names=['SourceID', 'TargetID', 'Timestamp'])
    dataframe2 = pd.read_csv(tmp_string_2, sep=" ", header=None, names=['SourceID', 'TargetID', 'Timestamp'])
    Tmin = dataframe1.Timestamp.iloc[0]
    Tmax = dataframe2.Timestamp.iloc[-1]
    #print ('Tmin= %d, Tmax= %d' % (Tmin, Tmax))

    DT = Tmax - Tmin

    dt = DT/N
    #create the {t0,t1,...tj,...tn }
    #2) Breaak [Tmin,Tmax]
    T=[]
    for j in range (0,N+1):
        tj = Tmin + j * dt
        T.append(tj)
    return T

def get_graph_by_time_sector(k,t1,t2,df):
    data = df[(df.Timestamp >= t1) & (df.Timestamp <= t2)]
    G = nx.from_pandas_edgelist(data, source='SourceID', target='TargetID', edge_attr=True, create_using=nx.DiGraph())
    G.graph['name'] = 'Stackoverflow_sub_graph_' + str(k)
    #print nx.info(G1)

    #3) we save the graph and we can plot it later with another script
    data.to_csv(path_or_buf='Subgraphs/' + str(G.graph['name']) + '.csv', sep=',', index=False)
    return G
