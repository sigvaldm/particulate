from particulate import *

fig, ax = plt.subplots()

interact = Interactive(fig)

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_aspect('equal')

plt.show()

particles = []
for circ in ax.patches:
    pos = np.array(circ.center)
    if circ.arrow is not None:
        length = np.array(circ.arrow.length)
    else:
        length = 0
    color = circ.get_fc()
    particles.append(Particle(pos, length, color))

print(len(particles))
