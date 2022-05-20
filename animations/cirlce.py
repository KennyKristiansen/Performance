import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

def rotationBasedPatter(start, stop, position ,overlap, n, z):

    fullCircle = np.radians(360)
    if stop * fullCircle >= position >= start * fullCircle:
        z += overlap * -fullCircle * 10 / (n * fullCircle)
    return( z)

def gen(n):
    phi = 0
    fullCircle = np.radians(360)
    startHeight = 10
    downPerRevolution = 2
    z = startHeight
    rotations = 0
    endCircleCount = 10 * fullCircle
    filmHeight = 2

    while phi < endCircleCount:


        
        z = rotationBasedPatter(2,3,phi,1,n,z)
        z = rotationBasedPatter(3,7,phi,0.4,n,z)
        z = rotationBasedPatter(7,8,phi,2,n,z)
        z = rotationBasedPatter(8,10,phi,0.25,n,z)

        yield np.array([np.cos(phi), np.sin(phi), z])

        if phi >= rotations * fullCircle:
            rotations += 1
            print(f"Rotation {rotations}: z = {z:.2f}")

        phi += endCircleCount / n
        # print(rotations, z)


def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])


N = 500

data = np.array(list(gen(N))).T

(line,) = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], lw=1, color="b")

# Setting the axes properties
ax.set_xlim3d([-1.0, 1.0])
ax.set_xlabel("X")

ax.set_ylim3d([-1.0, 1.0])
ax.set_ylabel("Y")

ax.set_zlim3d([0.0, 10.0])
ax.set_zlabel("Z")

ani = animation.FuncAnimation(
    fig, update, frames=N, fargs=(data, line), interval=0.2, blit=False
)
# ani.save('matplot003.gif', writer='imagemagick', fps=60)
plt.show()
