import networkx as nx
import os
import pandas as pd
import pickle
from scipy.sparse import dok_matrix
import sys


# .............................FUNCTIONS...................................


def read_tbl(tbl_file):
    # read table into pandas df
    df_tbl = pd.read_table(tbl_file, delim_whitespace=True)
    return df_tbl


def map_urstoint(df_tbl):
    map_dict = {}
    q_list = list(set(df_tbl["query"]))
    for i in range(0, len(q_list)):
        map_dict[q_list[i]] = i
    # reversed dictionary
    rev_map_dict = {v: k for k, v in map_dict.items()}
    return map_dict, q_list, rev_map_dict


def make_matrix(df_tbl, q_list, map_dict):
    """
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
    """
    cliques = list(nx.find_cliques(graph))
    cliques_names = []
    for i in range(0, len(cliques)):
        sublist = []
        for j in cliques[i]:
            sublist.append(rev_map_dict[j])
        cliques_names.append(sublist)
    with open(cliq_out, 'wb') as f:
        pickle.dump(cliques_names, f)
    return cliques_names


def main(tbl_file):
        df_tbl = read_tbl(tbl_file)
        mapping = map_urstoint(df_tbl)
        map_dict = mapping[0]
        q_list = mapping[1]
        rev_map_dict = mapping[2]
        graph = make_matrix(df_tbl, q_list, map_dict)
        comp_list = find_components(graph, rev_map_dict)
        return comp_list

# .........................................................................

if __name__ == '__main__':
    TBL_FILE = sys.argv[1]
    COMP_OUT = os.path.join(os.path.dirname(TBL_FILE), "comp.list.tsv")
    COMP_LIST = main(TBL_FILE)
    with open(COMP_OUT, 'wb') as f:
            pickle.dump(COMP_LIST, f)
