# import multiprocessing
# multiprocessing.freeze_support()

print("Loading DeepLabCut... This may take about 30 seconds.")

# This line below allows for a mismatched version of HDF5 
# (still need to figure out the cause of the mismatch version)
os.environ["HDF5_DISABLE_VERSION_CHECK"] = "2"

import deeplabcut

# START: from mlp_test
import matplotlib

print(matplotlib.__version__)
print(matplotlib.get_backend())

import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

fig, ax = plt.subplots()
ax.plot(t, s)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()
plt.show()
# END: from mlp_test

deeplabcut.launch_dlc()