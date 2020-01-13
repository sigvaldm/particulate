import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

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

def arrow(ax, circle, length=None, tip=None, size=0.01):
    # TBD: fetch size from circle

    base = circle.center

    width = size*2/3

    if length is None:
        length = np.array(tip)-np.array(base)

    arrowstyle = {
        'width': width,
        'head_width': 4*width,
        'head_length': 4*width,
        'length_includes_head': False,
        'facecolor': circle.get_fc(),
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

# TODO: Straight angles when holding down ALT
# TODO: Move only starting point when holding down CTRL (or when NOT holding it down)

class Interactive(object):

    def __init__(self, fig, ax=None, colors=('C0', 'C3')):

        self.state = 2 # 0: place particle, 1: place velocity vector
        self.fig = fig
        self.ax = fig.axes[0] if ax == None else ax
        self.color_ind = 0
        self.colors = colors
        self.color = self.colors[self.color_ind]

        # self.current_artist = circle(self.ax, [0.5, 0.5])
        self.current_artist = None
        self.just_picked = False

        fig.canvas.mpl_connect('button_press_event', self.onClick)
        fig.canvas.mpl_connect('motion_notify_event', self.onMove)
        fig.canvas.mpl_connect('pick_event', self.onPick)

    def onClick(self, event):
        if event.inaxes != self.ax: return # Mouse outside axes
        pos = [event.xdata, event.ydata]

        if event.button==MouseButton.LEFT:

            if self.just_picked:
                self.just_picked = False
                return

            # Place circle
            if isinstance(self.current_artist, mpl.patches.Circle):
                if self.current_artist.arrow is None:
                    self.current_artist = arrow(self.ax, self.current_artist, tip=pos)
                else:
                    self.current_artist = None

            # Place arrow
            elif isinstance(self.current_artist, mpl.patches.FancyArrow):
                self.current_artist = None

            # New circle
            elif event.dblclick:
                circ = circle(self.ax, pos, color=self.color)
                self.current_artist = arrow(self.ax, circ, tip=pos)

        elif event.button==MouseButton.MIDDLE:

            self.next_color()

            if isinstance(self.current_artist, mpl.patches.Circle):
                # self.current_artist.set_fc(self.color) # Doesn't work
                new_circle = circle(self.ax, self.current_artist.center, color=self.color)
                if self.current_artist.arrow is not None:
                    self.current_artist.arrow.set_fc(self.color)
                    self.current_artist.arrow.circle = new_circle
                    new_circle.arrow = self.current_artist.arrow
                self.current_artist.remove()
                self.current_artist = new_circle

            elif isinstance(self.current_artist, mpl.patches.FancyArrow):
                self.current_artist.set_fc(self.color)
                # self.current_artist.circle.set_fc(self.color) # Doesn't work
                self.current_artist.circle.remove()
                self.current_artist.circle = circle(self.ax, self.current_artist.circle. center, color=self.color)
                self.current_artist.circle.arrow = self.current_artist

            if self.just_picked:
                self.just_picked = False
                self.current_artist = None

        elif event.button==MouseButton.RIGHT:

            if isinstance(self.current_artist, mpl.patches.Circle):
                if self.current_artist.arrow is not None:
                    self.current_artist.arrow.remove()
                self.current_artist.remove()
                self.current_artist = None

            elif isinstance(self.current_artist, mpl.patches.FancyArrow):
                self.current_artist.circle.arrow = None
                self.current_artist.remove()
                self.current_artist = None

            if self.just_picked:
                self.just_picked = False
                self.current_artist = None


        self.fig.canvas.draw()

    def onMove(self, event):
        if event.inaxes != self.ax: return # Mouse outside axes
        pos = [event.xdata, event.ydata]

        if isinstance(self.current_artist, mpl.patches.Circle):
            # Currently holding and moving a circle, perhaps with an arrow
            length = None
            if self.current_artist.arrow is not None:
                length = self.current_artist.arrow.length
                self.current_artist.arrow.remove()
            color = self.current_artist.get_fc()
            self.current_artist.remove()
            self.current_artist = circle(self.ax, pos, color=color)
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

    def next_color(self):
        self.color_ind = (self.color_ind+1)%len(self.colors)
        self.color = self.colors[self.color_ind]
