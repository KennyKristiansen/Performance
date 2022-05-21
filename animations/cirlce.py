import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

class rotationBasedPattern():
    def __init__(self) -> None:
        self.fullCircle = np.radians(360)
        self.start :int = 1
        self.stop :int = 1
        self.position :int = 1
        self.overlap :float = 1
        self.n :int = 1
        self.z :int = 1

    def rotationBasedPatter(self, start, stop, overlap):
        if overlap not in range(-101,101):
            print('wrong overlap')
        overlap = (self.scale(overlap, (-100, 100), (2.0, 0.0)))
        fullCircle = np.radians(360)
        if stop * fullCircle >= self.position >= start * fullCircle:
            self.z += -overlap * (fullCircle * 10) / (self.n * fullCircle)
            self.overlap = overlap
        return(self.z)
    
    def scale(self, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def gen(n):
    fullCircle = np.radians(360)
    startHeight = 10
    z = startHeight
    rotations = 0
    endCircleCount = 10 * fullCircle
    filmHeight = 1

    pattern = rotationBasedPattern()
    pattern.n = n
    pattern.z = startHeight

    while pattern.position/2 < endCircleCount:
        
        z = pattern.rotationBasedPatter(start=0,stop=3,overlap=100)
        z = pattern.rotationBasedPatter(3,7,25)
        z = pattern.rotationBasedPatter(7,8,-100)
        z = pattern.rotationBasedPatter(8,10,-50)
        if not z > 0:
            z = 0
        yield np.array([np.cos(pattern.position), np.sin(pattern.position), z])
        yield np.array([np.cos(pattern.position), np.sin(pattern.position), z-filmHeight])
        if pattern.position >= rotations * fullCircle:
            rotations += 1
            print(f"Rotation {rotations}: z = {z:.2f}")
            print(pattern.overlap)

        pattern.position += endCircleCount / pattern.n
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
    fig, update, frames=N*2, fargs=(data, line), interval=0.2, blit=False
)
# ani.save('matplot003.gif', writer='imagemagick', fps=60)
plt.show()
