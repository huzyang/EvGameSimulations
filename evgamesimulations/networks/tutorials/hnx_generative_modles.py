import hypernetx as hnx
import hypernetx.algorithms.generative_models as gm
import random
import matplotlib.pyplot as plt
import time
import warnings
warnings.simplefilter('ignore')

from collections import Counter

n = 100 # 点数
m = n   # 边数
p = 0.01    # 节点与超边链接的概率

# generate ER hypergraph
H = gm.erdos_renyi_hypergraph(n, m, p)

print('Expected # pairs: ', int(n*m*p))     # 期望的顶点超边对
print('Output # pairs: ', H.incidence_matrix().count_nonzero())     # 实际的顶点超边对

plt.subplots(figsize=(5,5))
hnx.draw(H)