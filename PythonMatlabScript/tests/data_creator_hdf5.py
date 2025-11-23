import numpy as np
import h5py

with h5py.File("hdf5_small.mat", "w") as f:
	# Top-level datasets
	f.create_dataset("a", data=42)
	f.create_dataset("v", data=np.array([1, 2, 3]))
	f.create_dataset("M", data=np.array([[1, 2],
	                                     [3, 4]]))

	# Struct-like group "s"
	group_s = f.create_group("s")
	group_s.create_dataset("value", data=99)

	# Nested subgroup "sub"
	sub = group_s.create_group("sub")
	sub.create_dataset("x", data=123)
	sub.create_dataset("y", data=np.array([10, 20]))
