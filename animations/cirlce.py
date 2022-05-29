import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")


class ExceptionOutOfRange(BaseException):
    def __init__(self, message, base_message=None, *args):
        self.message = message
        self.base_message = base_message


class wrappingPattern:
    def __init__(self) -> None:
        self.position: int = 0
        self.overlap: float = 0
        self.n: int = 0
        self.PosZAdjustment: int = 0
        self.PosZ = 0
        self.filmHeight = 0

    # TODO create more pattern choices, example cm based
    def rotationBased(self, startRotation, stopRotation, overlap):
        if overlap not in range(-101, 101):
            raise ExceptionOutOfRange("Overlap out of range.")
        self.overlap = self.scale(overlap, (-100, 100), (self.filmHeight * 2, 0))
        fullCircle = np.radians(360)
        if stopRotation * fullCircle >= self.position >= startRotation * fullCircle:
            self.PosZAdjustment = (
                -self.overlap * (fullCircle * 10) / (self.n * fullCircle)
            )
            return True

    # TODO
    def percentageBased(self, productHeight, start, stop, overlap):
        if overlap not in range(-101, 101):
            raise ExceptionOutOfRange("Overlap out of range.")
        self.overlap = self.scale(overlap, (-100, 100), (self.filmHeight * 2, 0.0))
        fullCircle = np.radians(360)
        start = self.scale(start, (0, 100), (productHeight, 0.0))
        stop = self.scale(stop, (0, 100), (productHeight, 0.0))
        # start = (-productHeight / 100) * start + productHeight
        # stop = (-productHeight / 100) * stop + productHeight
        FloatCompensation = 0.0001
        if start + FloatCompensation >= self.PosZ >= stop:
            self.PosZAdjustment = (
                -self.overlap * (fullCircle * 10) / (self.n * fullCircle)
            )
            return True

    # TODO wrongly implemented, does not account for product height
    def measurementBased(self, productHeight, start, stop, overlap):
        if overlap not in range(-101, 101):
            raise ExceptionOutOfRange("Overlap out of range.")
        self.overlap = self.scale(overlap, (-100, 100), (self.filmHeight * 2, 0.0))
        fullCircle = np.radians(360)

        if productHeight >= start >= self.PosZ >= stop:
            self.PosZAdjustment = (
                -self.overlap * (fullCircle * 10) / (self.n * fullCircle)
            )
            return True

    def scale(self, val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


def gen(n):
    Circle = np.radians(360)
    productHeight = 500
    PosZ = productHeight
    rotations = 0
    endCircleCount = 10 * Circle
    filmHeight = 50

    pattern = wrappingPattern()
    pattern.n = n
    pattern.PosZAdjustment = productHeight
    pattern.filmHeight = filmHeight
    yieldControl = False

    # TODO choose between rotation based or height based.
    while pattern.position < endCircleCount:
        # TODO make sure only one pattern is active at a time.
        a = pattern.rotationBased(startRotation=0, stopRotation=1, overlap=100)
        b = pattern.rotationBased(1, 4, 0)
        c = pattern.measurementBased(productHeight, 350, 200, -50)
        d = pattern.percentageBased(productHeight, 60, 100, -100)

        if not PosZ > 0 + filmHeight:
            PosZ = 0 + filmHeight
        PosX = np.cos(pattern.position) * 200
        PosY = np.sin(pattern.position) * 200
        if yieldControl:
            yield np.array([PosX, PosY, PosZ])
            yield np.array([PosX, PosY, PosZ - filmHeight])
            yieldControl = False
        else:
            yield np.array([PosX, PosY, PosZ - filmHeight])
            yield np.array([PosX, PosY, PosZ])
            yieldControl = True

        if pattern.position >= rotations * Circle:
            rotations += 1
            print(f"Rotation {rotations}: PosZ = {PosZ:.2f}")
            print(f"Control: a{a}, b{b}, c{c}, d{d},")

        PosZ += pattern.PosZAdjustment
        pattern.PosZ = PosZ
        pattern.PosZAdjustment = 0
        pattern.position += endCircleCount / pattern.n
        # print(rotations, PosZ)


def update(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])


N = 1500

data = np.array(list(gen(N))).T

(line,) = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], lw=1, color="b")

# Setting the axes properties
ax.set_xlim3d([-200, 200])
ax.set_xlabel("X")

ax.set_ylim3d([-200, 200])
ax.set_ylabel("Y")

ax.set_zlim3d([0, 500])
ax.set_zlabel("Z")

ani = animation.FuncAnimation(
    fig, update, frames=N * 2, fargs=(data, line), interval=0.2, blit=False
)
# ani.save('matplot003.gif', writer='imagemagick', fps=60)
plt.show()
