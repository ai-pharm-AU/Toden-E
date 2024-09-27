#! /usr/bin/python


__author__ = 'Michael Neylon'

# CoCo Calculation


from scipy.stats import hypergeom
from math import log10
import math

#hypergeom.pmf(k, M, n, N) =
#choose(n,k)*choose(M-n,N-k)/choose(M,N)
#for N - (M-n) <= k <= min(m,N)

class CoCo:
    """Class to calculate the CoCo Score for a given gene-set in a network."""
    def __init__(self,total_nodes,total_interactions,total_triangles,local_nodes,local_interactions,local_triangles):
        self.Nint = (((float(total_nodes)) * (float(total_nodes)-1))/2)
        self.Kint = total_interactions
        self.nint = (((float(local_nodes))*(float(local_nodes)-1))/2)
        self.kint = local_interactions
        self.Ntri = (((float(total_nodes))*(float(total_nodes)-1)*(float(total_interactions)-2))/6)
        self.Ktri = total_triangles
        self.ntri = (((float(local_nodes))*(float(local_nodes)-1)*(float(local_nodes)-2)) / 6)
        self.ktri = local_triangles
        self.coco = self.CoI() + self.CoT()

    def CoI(self):
        if self.kint == 0:
            self.co_i = 0
            return self.co_i
        else:
            sign = ((float(self.kint)/float(self.nint)) - (float(self.Kint)/float(self.Nint)))
            p = hypergeom.pmf(self.kint,self.Nint,self.Kint,self.nint)
            if p != 0:
                if sign < 0:
                    result = abs(log10(p))*(-1)
                else:
                    result = abs(log10(p))
            else:
                result = p
           # print "CoI: ", result
            if math.isnan(result):
                self.co_i = 0.0
                return self.co_i
            else:
                self.co_i = result
                return self.co_i

    def CoT(self):
        if self.ktri == 0:
            self.co_t = 0
            return self.co_t
        else:
            if self.ntri != 0:
                sign = ((float(self.ktri)/float(self.ntri)) - (float(self.Ktri)/float(self.Ntri)))
            else:
                sign = ((float(self.ktri)/(0.000000000000001)) - (float(self.Ktri)/float(self.Ntri)))
            p = hypergeom.pmf(self.ktri,self.Ntri,self.Ktri,self.ntri)
            if p != 0:
                if sign < 0:
                    result = abs(log10(p))*(-1)
                else:
                   result = abs(log10(p))
            else:
                result = p
            #print "CoT: ", result
            #print result
            if math.isnan(result):
                self.co_t = 0.0
                return self.co_t
            else:
                self.co_t = result
                return self.co_t