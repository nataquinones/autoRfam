"""
Description:
Takes .tsv file with columns "query" and "target"
(made for nhmmertbl_parse.py output) to make into networkx matrix
and compute connected components (and/or cliques.) Returns pickle list file.

Use:
cluster_ali.py <in>
<in> .tsv file with columns "query" and "target"
"""

import networkx as nx
import os
import pandas as pd
import pickle
from scipy.sparse import dok_matrix
import sys


# .............................FUNCTIONS...................................


def read_tsv(tsvin):
    """
    Read tsv file into pandas df
    """
    df_tbl = pd.read_csv(tsvin, sep="\t")
    return df_tbl


def map_urstoint(df_tbl):
    """
    Takes dataframe from read_tsv and maps URS to integers to handle
    matrix axes.
    [0] map_dict: dictonary relating URS:int
    [1] q_list: list of the set of queries
    [2] rev_map_dict: dictonary relating int:URS
    """
    map_dict = {}
    q_list = list(set(df_tbl["query"]))
    for i in range(0, len(q_list)):
        map_dict[q_list[i]] = i
    # reversed dictionary
    rev_map_dict = {v: k for k, v in map_dict.items()}
    return map_dict, q_list, rev_map_dict


def make_matrix(df_tbl, q_list, map_dict):
    """
    Takes dataframe from read_tsv(), q_list and map_dict from map_urstoint(),
    makes scipy sparce dok_matrix and then networkx graph.
    Returns networkx style graph.
    """
    # drop lines where target not in query
    df_tbl = df_tbl[df_tbl["target"].isin(q_list)]
    # make matrix
    sparse = dok_matrix((len(q_list), len(q_list)))
    # fill sparse matrix
    for urs in q_list:
        i = map_dict[urs]
        for target in df_tbl[df_tbl["query"] == urs]["target"]:
            j = map_dict[target]
            sparse[i, j] = 1
    graph = nx.from_scipy_sparse_matrix(sparse)
    return graph


def find_components(graph, rev_map_dict):
    """
    Takes networkx graph [from make_matrix()] and makes list of lists of
    connected components. Replaces with names from int:URS map,
    [from rev_map_dict from map_urstoint()]
    """
    components_set = list(nx.connected_components(graph))
    components = []
    for i in range(0, len(components_set)):
        components.append(list(components_set[i]))

    components_names = []
    for i in range(0, len(components)):
        sublist = []
        for j in components[i]:
            sublist.append(rev_map_dict[j])
        components_names.append(sublist)
    return components_names


def find_cliques(graph, rev_map_dict):
    """
    Takes networkx graph [from make_matrix()] and makes list of lists of
    cliques. Replaces with names from int:URS map,
    [from rev_map_dict from map_urstoint()]
    """
    cliques = list(nx.find_cliques(graph))
    cliques_names = []
    for i in range(0, len(cliques)):
        sublist = []
        for j in cliques[i]:
            sublist.append(rev_map_dict[j])
        cliques_names.append(sublist)
    return cliques_names


def main(tsvin, listout):
        df_tbl = read_tsv(tsvin)
        mapping = map_urstoint(df_tbl)
        map_dict = mapping[0]
        q_list = mapping[1]
        rev_map_dict = mapping[2]
        graph = make_matrix(df_tbl, q_list, map_dict)
        comp_list = find_components(graph, rev_map_dict)
        with open(listout, 'wb') as f:
            pickle.dump(comp_list, f)

# .........................................................................

if __name__ == '__main__':
    IN_TSV = sys.argv[1]
    COMP_OUT = os.path.join(os.path.dirname(IN_TSV), "comp.list")
    main(IN_TSV, COMP_OUT)
    
