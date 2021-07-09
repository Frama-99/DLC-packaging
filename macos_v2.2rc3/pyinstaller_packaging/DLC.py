# import multiprocessing
# multiprocessing.freeze_support()

if __name__ == '__main__':
    print("Loading DeepLabCut... This may take about 30 seconds.")

    import deeplabcut
    deeplabcut.launch_dlc()