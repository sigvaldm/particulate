from particulate import *

fig, ax = plt.subplots()

state=0 # 0: place particle, 1: place velocity vector

interact = Interactive(fig)

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_aspect('equal')

# circ = plt.Circle([0.5, 0.5], 0.01)
# ax.add_patch(circ)

plt.show()
