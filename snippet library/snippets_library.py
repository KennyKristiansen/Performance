def scale(val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]
src = [0,100]
dst = [10,20]
val = 50
scale(val, src, dst) # returns 15
