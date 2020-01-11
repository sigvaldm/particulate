import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from particulate import *

fig, ax = plt.subplots()

colors = ['C0', 'C3']

for c in colors:
    pos = np.random.rand(20,2)
    vel = 0.03*np.random.randn(20,2)
    for p, v in zip(pos, vel):
        arrow(ax, p, v, color=c)

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_aspect('equal')

plt.show()
