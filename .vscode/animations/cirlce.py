import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

def gen(n):
    phi = 0
    fullCircle = np.radians(360)
    startHeight = 10
    downPerRevolution = 2
    z = startHeight
    rotations = 0
    what = 0
    endCircleCount = 10 * fullCircle
    previousZ = 0
    while phi < endCircleCount:
        if 7*fullCircle >= phi >= 2*fullCircle:
            z +=    downPerRevolution*-endCircleCount/(n*fullCircle)
        else:
            z = z
        yield np.array([np.cos(phi), np.sin(phi), z])

        if phi >= rotations * fullCircle:
            rotations += 1
            print(f'Rotation {rotations}: z = {z:.2f}')

        
        what += (np.cos((10*fullCircle/n)-1))
        phi += endCircleCount/n
        #print(rotations, z)
        

def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])

N = 500

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