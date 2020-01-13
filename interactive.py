from particulate import *

fig, ax = plt.subplots()

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_aspect('equal')

try:
    population = Population()
    population.load('dummy.npz')
    population.plot(ax)
except:
    pass

inter = Interactive(fig)
plt.show()

population.fetch(ax)
population.save('dummy.npz')
