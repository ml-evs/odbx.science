import numpy as np


def check_shape(v, shape, field):
    """Check that the array `v` has the correct `shape` for the given `field`."""
    vshape = np.shape(np.asarray(v))
    if vshape != shape:
        raise ValueError(
            "Wrong array shape for {}! Should be {}, not {}".format(
                field, shape, vshape
            )
        )
