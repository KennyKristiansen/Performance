import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from regex import P

fig = plt.figure()
ax = fig.add_subplot(projection="3d")


class ExceptionOutOfRange(BaseException):
    def __init__(self, message, base_message=None, *args):
        self.message = message
        self.base_message = base_message


class rotationBasedPattern:
    def __init__(self) -> None:
        self.fullCircle = np.radians(360)
        self.start: int = 1
        self.stop: int = 1
        self.position: int = 1
        self.overlap: float = 1
        self.n: int = 1
        self.PosZ: int = 1

    def rotationBasedPattern(self, start, stop, overlap):
        if overlap not in range(-101, 101):
            raise ExceptionOutOfRange("Overlap out of range.")
        overlap = self.scale(overlap, (-100, 100), (0.4, 0.0))
        fullCircle = np.radians(360)
        if stop * fullCircle >= self.position >= start * fullCircle:
            self.PosZ += -overlap * (fullCircle * 10) / (self.n * fullCircle)
            self.overlap = overlap
        return self.PosZ

    def percentageBasedPattern(self, productHeight, start, stop, overlap):
        if overlap not in range(-101, 101):
            raise ExceptionOutOfRange("Overlap out of range.")
        overlap = self.scale(overlap, (-100, 100), (0.4, 0.0))
        fullCircle = np.radians(360)
        start = (-productHeight / 100) * start + productHeight
        stop = (-productHeight / 100) * stop + productHeight
        if start >= self.PosZ >= stop:
            self.PosZ += -overlap * (fullCircle * 10) / (self.n * fullCircle)
            self.overlap = overlap
        return self.PosZ

    def scale(self, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def gen(n):
    fullCircle = np.radians(360)
    startHeight = 2
    PosZ = startHeight
    rotations = 0
    endCircleCount = 10 * fullCircle
    filmHeight = 0.2

    pattern = rotationBasedPattern()
    pattern.n = n
    pattern.PosZ = startHeight

    while pattern.position < endCircleCount:

        PosZ = pattern.rotationBasedPattern(start=0, stop=1, overlap=100)
        PosZ = pattern.rotationBasedPattern(2, 4, -100)
        PosZ = pattern.percentageBasedPattern(startHeight, 35, 100, -100)

        if not PosZ > 0:
            PosZ = 0
        PosX = np.cos(pattern.position)
        PosY = np.sin(pattern.position)
        yield np.array([PosX, PosY, PosZ])
        yield np.array([PosX, PosY, PosZ - filmHeight])

        if pattern.position >= rotations * fullCircle:
            rotations += 1
            print(f"Rotation {rotations}: PosZ = {PosZ:.2f}")

        pattern.position += endCircleCount / pattern.n
        # print(rotations, PosZ)


def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])


N = 500

data = np.array(list(gen(N))).T

(line,) = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], lw=1, color="b")

# Setting the axes properties
ax.set_xlim3d([-2.0, 2.0])
ax.set_xlabel("X")

ax.set_ylim3d([-2.0, 2.0])
ax.set_ylabel("Y")

ax.set_zlim3d([0.0, 2.0])
ax.set_zlabel("Z")

ani = animation.FuncAnimation(
    fig, update, frames=N * 2, fargs=(data, line), interval=0.2, blit=False
)
# ani.save('matplot003.gif', writer='imagemagick', fps=60)
plt.show()
