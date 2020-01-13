import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def arrow_old(ax, base, length=None, tip=None, color='C0', size=0.01):

    width = size*2/3

    if length is None:
        length = np.array(tip)-np.array(base)

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
        'radius': size,
    }

    circ = plt.Circle(base, **circlestyle)
    ax.add_patch(circ)
    if np.linalg.norm(length)>1e-10:
        ax.arrow(base[0], base[1], length[0], length[1], **arrowstyle)

def circle(ax, base, color='C0', size=0.01):

    width = size*2/3
    circlestyle = {
        'color': color,
        'radius': size,
        'picker': True,
    }
    circle = plt.Circle(base, **circlestyle)
    circle.arrow = None
    return ax.add_patch(circle)

def arrow(ax, circle, length=None, tip=None, color='C0', size=0.01):

    base = circle.center

    width = size*2/3

    if length is None:
        length = np.array(tip)-np.array(base)

    arrowstyle = {
        'width': width,
        'head_width': 4*width,
        'head_length': 4*width,
        'length_includes_head': False,
        'facecolor': color,
        'linewidth': 0,
        'picker': True,
    }
    arrow = ax.arrow(base[0], base[1], length[0], length[1], **arrowstyle)
    arrow.circle = circle
    arrow.length = length
    circle.arrow = arrow
    return arrow

class Particle(object):
    def __init__(self, pos, vel, color='C0'):
        self.pos = pos
        self.vel = vel
        self.color = color

class Interactive(object):

    def __init__(self, fig, ax=None):

        self.state = 2 # 0: place particle, 1: place velocity vector
        self.fig = fig
        self.ax = fig.axes[0] if ax == None else ax

        # self.current_artist = circle(self.ax, [0.5, 0.5])
        circ = circle(self.ax, [0.5, 0.5])
        arrow(self.ax, circ, [0.1,0])
        self.current_artist = None
        self.just_picked = False

        fig.canvas.mpl_connect('button_press_event', self.onClick)
        fig.canvas.mpl_connect('motion_notify_event', self.onMove)
        fig.canvas.mpl_connect('pick_event', self.onPick)

    def onClick(self, event):
        pos = [event.xdata, event.ydata]

        if self.just_picked:
            self.just_picked = False
            return

        if isinstance(self.current_artist, mpl.patches.Circle):
            if self.current_artist.arrow is None:
                self.current_artist = arrow(self.ax, self.current_artist, tip=pos)
            else:
                self.current_artist = None
        elif isinstance(self.current_artist, mpl.patches.FancyArrow):
            self.current_artist = None
        elif event.dblclick:
            self.current_artist = circle(self.ax, pos)

    def onMove(self, event):
        pos = [event.xdata, event.ydata]

        if isinstance(self.current_artist, mpl.patches.Circle):
            # Currently holding and moving a circle, perhaps with an arrow
            length = None
            if self.current_artist.arrow is not None:
                length = self.current_artist.arrow.length
                self.current_artist.arrow.remove()
            self.current_artist.remove()
            self.current_artist = circle(self.ax, pos)
            if length is not None:
                self.current_artist.arrow = arrow(self.ax, self.current_artist, length=length)

        elif isinstance(self.current_artist, mpl.patches.FancyArrow):
            # Currently holding and moving an arrow
            self.current_artist.remove()
            self.current_artist = arrow(self.ax, self.current_artist.circle, tip=pos)

        self.fig.canvas.draw()

    def onPick(self, event):

        if self.current_artist is None:
            self.current_artist = event.artist
            self.just_picked = True
