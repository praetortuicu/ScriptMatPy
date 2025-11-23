import numpy as np
import scipy.io as sio

# Build nested test structure
test_data = {
	"a": 42,
	"v": np.array([1, 2, 3]),
	"M": np.array([[1, 2],
		           [3, 4]]),
	"s": {
		"value": 99,
		"sub": {
			"x": 123,
			"y": np.array([10, 20])
		}
	}
}

# Save to classic MATLAB Level-5 .mat file
sio.savemat("std_small.mat", test_data)
