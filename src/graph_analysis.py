import networkx as nx
import pandas as pd



def create_transaction_graph(edges):

    G = nx.DiGraph()


    for _, row in edges.iterrows():

        source = row["txId1"]
        target = row["txId2"]

        G.add_edge(
            source,
            target
        )


    return G




def calculate_graph_features(G):

    features = pd.DataFrame()


    degree = dict(
        G.degree()
    )


    centrality = nx.degree_centrality(
        G
    )


    features["degree"] = pd.Series(
        degree
    )


    features["centrality"] = pd.Series(
        centrality
    )


    return features