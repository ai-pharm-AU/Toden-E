#! /bin/python 2.7

__author__ = 'Michael Neylon'

# imports

import sqlite3
from scipy.stats import hypergeom
from math import log10
import math
import sys
import coco
import itertools
import random
from tqdm import tqdm
import argparse
import csv
from multiprocessing import Process, Pool
from multiprocessing import Manager

db_file = 'algo.db'
coco_cutoff = 3.0

############################
# Command Line Interface ###
###########################

parser = argparse.ArgumentParser(description="Run topdown method to identify new PAGs.")
parser.add_argument('-i', action="store", dest="input",type=str, required=True,help='Filename for input. Must be a file with two columns in the following order: PAG_ID GENE_SYMBOL')
parser.add_argument('-o', action="store", dest="output",type=str,required=True, help="Name for base of output files. Do not add extension, ex: 'output' not 'output.txt'")
parser.add_argument('-headers', action="store_true",default=False,dest="headers",help='If you use headers in your input file, specify that with this argument so it can be skipped')

###########################################
# Calculation Constants and Data Loading ##
###########################################

def universe_constants():
    """Get constants for CoCo caluclation."""
    conn = sqlite3.connect(db_file)
    conn.text_factory = str # read text data as str and not decode as UTF8
    c = conn.cursor()
    # species = ("Homo sapiens",)
    # query = 'SELECT COUNT(DISTINCT DS_GS_ALL_GENE.GENE_SYM) FROM DS_GS_ALL_GENE JOIN DS_GS_ALL ON DS_GS_ALL_GENE.GS_ID = DS_GS_ALL.GS_ID WHERE DS_GS_ALL.ORGANISM = ?'
    query = "SELECT COUNT(DISTINCT GENE_SYM) FROM MOL_PROT_MAP_HAPPI" # new table for actual probability, only genes involved in our interactions
    c.execute(query)
    TotNodes = c.fetchone()[0]
    Nint = ((float(TotNodes) * (float(TotNodes)-1))/2)
    Ntri = ((float(TotNodes)*(float(TotNodes)-1)*(float(TotNodes)-2))/6)
    print "Total human HAPPI genes:",TotNodes
    print "Nint:",Nint
    print "Ntri:",Ntri

    g = conn.cursor()
    query3 = "SELECT COUNT(*) FROM (SELECT DISTINCT MOL_A_ID,MOL_B_ID FROM MOL_MOL_MAP WHERE MOL_A_ID <> MOL_B_ID)"
    g.execute(query3)
    Kint = g.fetchone()[0]
    print "Kint:",Kint

    f = conn.cursor()
    query4 = "SELECT COUNT(*) FROM (SELECT DISTINCT INTERACTOR_A,INTERACTOR_B,INTERACTOR_C FROM ACTUAL_TRIANGLES)"
    f.execute(query4)
    Ktri = f.fetchone()[0]
    print "Ktri:",Ktri


    return Nint,Ntri,Kint,Ktri,TotNodes
    # return genes,ints,tris

def possible_genes_list():
    """Built list of all happi genes."""
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    c = conn.cursor()
    query = 'SELECT DISTINCT GENE_SYM FROM MOL_PROT_MAP_HAPPI'
    c.execute(query)
    genes_list = [x[0] for x in c.fetchall()]
    return genes_list

def int_dict():
    """Build a list of lists of regulatory edges between genes."""
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    c = conn.cursor()
    query = 'SELECT MOL_A_ID,MOL_B_ID FROM MOL_MOL_MAP'
    c.execute(query)
    int_dict = {}
    for each in c.fetchall():
        if each[0] in int_dict:
            int_dict[each[0]].append(each[1])
        else:
            int_dict[each[0]] = [each[1]]
    for each in c.fetchall():
        if each[1] in int_dict:
            int_dict[each[1]].append(each[0])
        else:
            int_dict[each[1]] = [each[0]]
    return int_dict

def tri_list():
    """Build list of lists of triplets."""
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    c = conn.cursor()
    query = "SELECT * FROM ACTUAL_TRIANGLES"
    c.execute(query)
    tri_list = []
    for each in c.fetchall():
        triangle = [each[0],each[1],each[2]]
        tri_list.append(triangle)
    return tri_list

##################
# Top Down Class #
##################

class MaxCoCoCluster:
    """class to find cluster based on max coco score."""

    def __init__(self,nodes,total_nodes,total_ints,total_tris,interaction_dictionary,triangle_list):
        self.nodes = nodes
        # self.threshold = threshold
        self.total_nodes = total_nodes
        self.total_interactions = total_ints
        self.total_triangles = total_tris
        self.interaction_dict = interaction_dictionary
        self.triangle_list = triangle_list
        self.results = self.topdown(self.nodes)
        # self.combined_results = self.coco_maximization(nodes)

    def parameters(self,select_nodes):
        """Queries to find the universe constants for nodes, interactions, and triplets."""
        edge_count = self.edges(select_nodes)
        if len(select_nodes) > 2:
            triplet_count = self.triplets(select_nodes)
        else:
            triplet_count = 0
        return edge_count,triplet_count

    def edges(self,select_nodes):
        """Find number of edges within a given set of nodes."""
        edges = []
        for node in select_nodes:
            if node in self.interaction_dict.keys():
                possible_links = self.interaction_dict[node]
                for each in possible_links:
                    if each in select_nodes:
                        edges.append([node,each])
        if edges:
            edges = [sorted(x) for x in edges]
            edges = [list(x) for x in set(tuple(x) for x in edges)]
            edge_count = len(edges)
            return edge_count
        else:
            return 0

    def triplets(self,select_nodes):
        triplet_count = 0
        for triangle in self.triangle_list:
            if triangle[0] in select_nodes and triangle[1] in select_nodes and triangle[2] in select_nodes:
                triplet_count += 1
        return triplet_count

    def coco_maximization(self,select_nodes):
        """Find a cluster of nodes forming a subpag that meets the CoCo threshold and provides best score."""
        topdownresults = self.topdown(select_nodes)
        return topdownresults, bottomupresults

    def score_coco(self,select_nodes):
        """Query for the interactions based on nodes and edges given and return coco score."""
        local_node_count = len(select_nodes)
        edge_count,triplet_count = self.parameters(select_nodes)
        x = coco.CoCo(total_nodes=self.total_nodes,total_interactions=self.total_interactions,total_triangles=self.total_triangles,local_nodes=local_node_count,local_interactions=edge_count,local_triangles=triplet_count)
        coco_score = x.coco
        return coco_score

    def topdown(self,nodes):
        """Greedily find solution for maximal CoCo Score cluster combination from top down."""
        # be able to start with union of all the sets
        S = nodes
        yolo = []
        n = len(S)
        top = [n,S,self.score_coco(S)]
        yolo.append(top)
        x = n - 1
        Q = S
        if n > 2:
            for i in range(1,x):
                fleek = []
                random.shuffle(Q)
                # shuffle the list so that any tie in max values will pick the first instance, but randomly due to shuffle
                for combo in itertools.combinations(Q,(n-i)):
                    score = self.score_coco(combo)
                    if fleek:
                        if score > fleek[-1]:
                            fleek = [(n-i),combo,score]
                    else:
                        fleek = [(n-i),combo,score]
                Q = list(fleek[1])
                yolo.append(fleek)
        return yolo


#############################
# I/O and Calls to Classes #
############################

def main(input,output,header_bool):
    """Take input, build dict, run through top down, write results."""
    print "Building PAG dictionary from your input..."
    pag_dict = {}
    with open(input, 'rb') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        reader = csv.reader(f, dialect)
        if header_bool:
            reader.next()
        for row in tqdm(reader):
            pag_id = row[0]
            gene = row[1]
            if pag_id in pag_dict.keys():
                pag_dict[pag_id].append(gene)
            else:
                pag_dict[pag_id] = [gene]
    results = topdown(pag_dict)

    scores_table = output+"_scores.tsv"
    genes_table = output+"_genes.tsv"
    print "Writing results to files..."
    print scores_table,"contains PAG_ID,SIZE_CHOICE, and CoCo Score"
    print genes_table,"maps the candidate size choice clusters for each pag to the genes they contain. This has PAG_ID,SIZE_CHOICE, and GENE."
    with open(scores_table, 'wb') as g:
        g.write("PAG_ID" + "\t" + "SIZE_CHOICE" + "\t" + "COCO_SCORE\n")
    with open(genes_table,'wb') as h:
        h.write("PAG_ID" + "\t" + "SIZE_CHOICE" + "\t" + "GENE\n")
        with open(scores_table,'ab') as g:
            for row in tqdm(results):
                id = row[0]
                size = row[1]
                combo = row[2]
                score = row[3]
                g.write(id + "\t" + str(size) + "\t" + str(score) + "\n")
                for gene in combo:
                    h.write(id + "\t" + str(size) + "\t" + str(gene) + "\n")
    print "Finished."


def select_final(input):
    sizes = []
    scores = []
    genes = []
    for each in input:
        if int(each[0]) < 2:
            pass
        else:
            sizes.append(int(each[0]))
            genes.append(each[1])
            scores.append(float(each[2]))
    if scores:
        max_score = max(scores)
        if float(max_score) < coco_cutoff:
            return None
        else:
            index_of_max = scores.index(max_score)
            max_new_size = int(sizes[index_of_max])
            max_genes = genes[index_of_max]
            result = [max_new_size,max_genes,max_score]
            return result

def topdown(input_dictionary):
    """Take input dictionary and outputs the candidate PAGs list."""
    data = []
    print "Running topdown analysis on the PAGs..."
    for pag_id in tqdm(input_dictionary.keys()):
        sub_pag = input_dictionary[pag_id]
        sub_pag = [x for x in sub_pag if x in happi_genes_list] # remove any non happi genes from calculations
        mprimePAG = MaxCoCoCluster(sub_pag,TotNodes,Kint,Ktri,int_dict,tri_list)
        result = mprimePAG.results
        if select_final(result):
            final_result = select_final(result)
        # sub_pag is a list of nodes
        # TotNodes is total number of genes in pags, is an integer
        # Kint is number of interactions in all pags, distinct, is an integer
        # Ktri is number of distinct triplets in all pags.
        # obj.result is in form [[choice_size,[gene list],coco_score],...]
            final_result.insert(0,pag_id)
            # remove lists from outer list to append individually to total
            data.append(final_result)
    return data




def cli(arguments):
    """Command line interface."""
    input_file = arguments.input
    output_file = arguments.output
    headers = arguments.headers
    main(input_file,output_file,headers)

int_dict = int_dict()
tri_list = tri_list()
happi_genes_list = possible_genes_list()
Nint,Ntri,Kint,Ktri,TotNodes = universe_constants()

if __name__=="__main__":
    parser.print_help()
    results = parser.parse_args()
    cli(results)