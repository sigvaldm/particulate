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
    circ = plt.Circle(base, **circlestyle)
    return ax.add_patch(circ)

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
    return arrow

class Particle(object):
    def __init__(self, pos, vel, color='C0'):
        self.pos = pos
        self.vel = vel
        self.color = color

class Interactive(object):

    def __init__(self, fig, ax=None):

        self.state = 0 # 0: place particle, 1: place velocity vector
        self.fig = fig
        self.ax = fig.axes[0] if ax == None else ax

        self.current_circle = circle(self.ax, [0.5,0.5])
        self.current_arrow = None

        fig.canvas.mpl_connect('button_press_event', self.onClick)
        fig.canvas.mpl_connect('motion_notify_event', self.onMove)
        fig.canvas.mpl_connect('pick_event', self.onPick)

    def onClick(self, event):
        self.state = (self.state+1)%3

        # if self.state==0:
        #     self.current_circle = None
        #     self.current_arrow = None

        # if self.state==0:
        #     self.current_circle = circle(self.ax, [event.xdata, event.ydata])
        # elif self.state==1:
        #     self.current_arrow = arrow(self.ax, self.current_circle, tip=[event.xdata, event.ydata])
        #     self.current_circle = None
        # elif self.state==2:
        #     self.current_arrow = None

        if self.state==0:
            self.current_circle = circle(self.ax, [0.5, 0.5])
        elif self.state==1:
            self.current_arrow = arrow(self.ax, self.current_circle, tip=[event.xdata, event.ydata])
            self.current_circle = None
        elif self.state==2:
            self.current_arrow = None

    def onMove(self, event):
        # if self.state==0:
        #     new_circle = circle(self.ax, [event.xdata, event.ydata])
        #     if self.current_circle is not None: self.current_circle.remove()
        #     self.current_circle = new_circle
        # elif self.state==1:
        #     new_arrow = arrow(self.ax, self.current_circle, tip=[event.xdata, event.ydata])
        #     if self.current_arrow is not None: self.current_arrow.remove()
        #     self.current_arrow = new_arrow

        if self.current_circle is not None:
            self.current_circle.remove()
            self.current_circle = circle(self.ax, [event.xdata, event.ydata])
        elif self.current_arrow is not None:
            self.current_arrow.remove()
            self.current_arrow = arrow(self.ax, self.current_arrow.circle, tip=[event.xdata, event.ydata])

        self.fig.canvas.draw()

    def onPick(self, event):
        if self.state==2:
            if isinstance(event.artist, plt.Circle):
                self.current_circle = event.artist
                self.state = 0
            else:
                self.current_arrow = event.artist
                self.state = 0
