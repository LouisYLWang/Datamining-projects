def manhattan_dist(v1, v2):
   return float(sum(abs(v1-v2)))
def hamming_dist(v1, v2):
   v1[v1>0]=1
   v2[v2>0]=1
   return float(sum(abs(v1-v2)))

def euclidean_dist(v1, v2):
   return float(np.sqrt(sum(pow(v1-v2)))**0.5)

def chebyshev_dist(v1, v2):
   return float(max(abs(v1-v2)))

def minkowski_dist(v1, v2, p):
   return float((sum(abs(v1-v2)**p))**(1/p))
