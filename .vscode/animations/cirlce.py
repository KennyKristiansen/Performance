import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

def gen(n):
    phi = 0
    fullCircle = 2*np.pi
    startHeight = 10
    angle = 0.251
    z = 0 + startHeight
    rotations = 0
    rotation = False
    i = 0
    while phi < 10*fullCircle:
        i += 1
        print(np.cos(fullCircle/n)*i )
        #X Y Z
        if 4 >= rotations >= 2:
            z += -angle*10*fullCircle/n
        else:
            z = z
        yield np.array([np.cos(phi), np.sin(phi), z])
        if (np.cos(fullCircle)*i >= 0.0) == rotation:
            rotations += 1
            rotation = True
        elif (np.cos(phi) <= 0.0) == rotation:
            rotation = False

        phi += 10*fullCircle/n
        #print(rotations, z)
        

def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

N = 250

data = np.array(list(gen(N))).T
line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1],color='r')

# Setting the axes properties
ax.set_xlim3d([-1.0, 1.0])
ax.set_xlabel('X')

ax.set_ylim3d([-1.0, 1.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 10.0])
ax.set_zlabel('Z')

ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=100/N, blit=False)
#ani.save('matplot003.gif', writer='imagemagick')
plt.show()