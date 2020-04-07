import pandas as pd
import copy
import networkx as nx
from time_division import *
from centrality_measurements import *
from similarity_measurements import *
from sklearn.model_selection import KFold
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

##################################################################################################
     # variables that user can adjust
target_names = ['class 0', 'class 1'] # for classification_report
parts = 20 # we cam see it from subdatasets.py
N=500 # Number N that [Tmin,Tmax] is going to break
kf = KFold(n_splits=10) # cross-validation number of splits
clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(45,90), random_state=1)
#np.set_printoptions(threshold=numpy.nan) print full np array
#################################################################################################

T=[]
T = timediv(parts,N)

draw = False
save = False
k = 0 # choose sub dataset

tmp_string = 'Dataset/sliced_dataset_' + str(k) + '.txt'
#tmp_string = 'Dataset/sx-stackoverflow.txt'
df = pd.read_csv(tmp_string, sep=" ", header=None, names=['SourceID', 'TargetID', 'Timestamp'])
    # normally it is 0 to N so 0,n+1 but we just want to test if it is working now
for i in range(0,2):

    G_after = get_graph_by_time_sector(i,T[i], T[i+1],df)
    #centrality calculation
    deg,in_deg,out_deg,close_centr,bet_centr, eig_centr,katz_centr= centrality_measurements(G_after)

    if draw:
        draw_all(G_after,deg,in_deg,out_deg,close_centr,bet_centr, eig_centr,katz_centr)

    if save:
        save_to_file(G_after,deg,in_deg,out_deg,close_centr,bet_centr, eig_centr,katz_centr,i)



    if i > 0: # so we have previous time sector -> Ti-1 , Ti
        #code
        print("calculating V*")
        V = intersection_of_two_graphs(G_before,G_after).to_undirected()
        V.graph['name'] = 'V*(%d, %d)' % (T[i-1], T[i+1])
        print nx.info(V)


        print("calculating E*[Ti-1,Ti]")
        E_before = intersection_of_two_graphs_edges(V , G_before) # intersection of previous graph with V
        E_before.graph['name'] = 'E_(%d, %d)' % (T[i-1], T[i])
        print nx.info(E_before)

        if save:
            save_to_file_similarities(E_before,i) # saves E_before similarities if we want

        print("calculating E*[Ti,Ti+1]")
        E_after = intersection_of_two_graphs_edges(G_after, V)
        E_after.graph['name'] = 'E_(%d, %d)' % (T[i], T[i+1])
        print nx.info(E_after)

        N = get_N(V,V,E_after,E_before).to_undirected()
        N.graph['name'] = 'N_(%d, %d)' % (T[i], T[i+1])
        print nx.info(N)

        feat , Y  =   calculate_similarities(E_before)
	print "calculated Ebefore similarities"
        feat_test , Y_test  =   calculate_similarities(E_after)
	print "calculated Eafter similarities"
        feat_N , Y_N =   calculate_similarities(V,"n")
	print "calculated N graph similarities"

        accuracy = []


        for train_index, test_index in kf.split(feat_N):
            print "fit starts"
            clf.fit(np.concatenate((feat_N[train_index],feat)),np.concatenate((Y_N[train_index],Y)))
            print "predict starts"
            training_results = clf.predict(np.concatenate((feat_test,feat_N[test_index])))
            print  "Accuracy Score Of Fold: ",accuracy_score(training_results, np.concatenate((Y_test,Y_N[test_index])))
            print  "Classification Report: ",classification_report(np.concatenate((Y_test,Y_N[test_index])), training_results, target_names=target_names)
            print "Confusion Matrix Follows: " , confusion_matrix(np.concatenate((Y_test,Y_N[test_index])), training_results)
            accuracy.append(accuracy_score(training_results, np.concatenate((Y_test,Y_N[test_index]))))
        print "Accuracy for T" , i ,sum(accuracy)/len(accuracy)



    #https://networkx.github.io/documentation/latest/reference/classes/generated/networkx.Graph.copy.html
     # G_after - > [Tj,Tj+1]
     # G_before  - > [Tj-1,Tj]
    G_before = copy.deepcopy(G_after)
