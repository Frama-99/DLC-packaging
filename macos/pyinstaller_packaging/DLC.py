# import multiprocessing
# multiprocessing.freeze_support()

print("Loading DeepLabCut... This may take about 30 seconds.")

# This line below allows for a mismatched version of HDF5 
# (still need to figure out the cause of the mismatch version)
os.environ["HDF5_DISABLE_VERSION_CHECK"] = "2"
import deeplabcut
deeplabcut.launch_dlc()