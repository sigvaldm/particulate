import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

def arrow(ax, base, size=None, tip=None, color='C0', radius=0.01):

    width = radius*2/3

    if size is None:
        size = np.array(tip)-np.array(base)

    arrowstyle = {
        'width': width,
        'head_width': 4*width,
        'head_length': 4*width,
        'length_includes_head': False,
        'facecolor': color,
        'linewidth': 0,
    }
    circlestyle = {
        'color': color,
        'radius': radius,
    }

    ax.arrow(base[0], base[1], size[0], size[1], **arrowstyle)
    circ = plt.Circle(base, **circlestyle)
    ax.add_patch(circ)

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
