import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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
