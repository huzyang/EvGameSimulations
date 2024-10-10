# -*- coding: utf-8 -*-
#!pip install hypernetx  ## uncomment to run in Colab

import hypernetx as hnx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import warnings 
warnings.simplefilter('ignore')

list_of_lists = [['book','candle','cat'],['book','coffee cup'],['coffee cup','radio']]

H = hnx.Hypergraph(list_of_lists)
list(H.nodes)
list(H.edges)
plt.subplots(figsize=(4,4))
hnx.draw(H)