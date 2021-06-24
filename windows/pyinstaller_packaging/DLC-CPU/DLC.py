import multiprocessing
multiprocessing.freeze_support()

print("Loading DeepLabCut... This may take about 30 seconds.")
import deeplabcut
deeplabcut.launch_dlc()