from particulate import *

fig, ax = plt.subplots()

interact = Interactive(fig)

ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_aspect('equal')

population = Population()
try:
    population.load('dummy.npz')
except:
    pass

population.plot(ax)

plt.show()

population = interact.get_population()
population.save('dummy.npz')
