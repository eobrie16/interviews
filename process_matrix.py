import sys

affinity_matrix = {}

def process_matrix(a, b, maxset):
    """
    Create key for each item, and a set to keep track of affinities
    Keep track of largest possible set of affinities
    """
    if affinity_matrix.has_key(a):
        if aff > t:
            affinity_matrix[a].add(b)
    else:
        if aff > t:
            affinity_matrix[a] = set([a,b])
        else:
            affinity_matrix[a] = set([a])
    # return tuple with largest set name and size
    if len(affinity_matrix[a]) > maxset[1]:
        return (min(affinity_matrix[a]),len(affinity_matrix[a]))
    elif len(affinity_matrix[a]) == maxset[1]:
        return (min(min(affinity_matrix[a]), maxset[0]), maxset[1])
    else:
        return maxset

t = float(input())
n = int(input())
maxset = ("",0)
for i in xrange(n):
    a,b,c = raw_input().strip().split()
    aff = float(c)
    maxset = process_matrix(a,b,maxset)
    maxset = process_matrix(b,a,maxset)

print maxset[0]
