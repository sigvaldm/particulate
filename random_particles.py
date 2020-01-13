import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from particulate import *

fig, ax = plt.subplots()

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_aspect('equal')

colors = ['C0', 'C3']

for c in colors:
    pos = np.random.rand(20,2)
    vel = 0.03*np.random.randn(20,2)
    for p, v in zip(pos, vel):
        Particle(p, v, c).plot(ax)

plt.show()
