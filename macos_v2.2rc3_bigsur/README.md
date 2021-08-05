# pyinstaller Packaging instructions on MacOS Big Sur
1. Install and activate the DLC conda environment from the latest pull
2. Install `pyinstaller`: `pip install pyinstaller`
3. Package 
4. Download a working copy of `libiomp5.dylib` by running `conda install -c
   conda-forge llvm-openmp`, and finding the `dylib` in the conda package.
   Move this `dylib` into `DLC.app/Contents/MacOS`, replacing what's
   already there.
5. 

## Detailed Documentation
### Starting from Scratch
DeepLabCut updated the library to support TF 2.x! This means that we can
finally use pyinstaller on macOS Big Sur, since we can finally upgrade to
Python 3.8, which supports an updated pyinstaller version that fixes the
missing system library error (see `macos/README.md` for more details). 

Because of the changes that occurred in Big Sur, I wanted to start from
scratch. So I started with having just the following in the `DLC.py` file. 
```
print("Loading DeepLabCut... This may take about 30 seconds.")
import deeplabcut
deeplabcut.launch_dlc()
```

### Fixing `libiomp5.dylib` Error
The packaging went smoothly, but when launching the binary, this error
occurs:
```
INTEL MKL ERROR: dlopen(/Users/frankma/code/DLC-packaging/macos_v2.2rc3/pyinstaller_packaging/dist/DLC.app/Contents/MacOS/libmkl_intel_thread.1.dylib, 9): Library not loaded: @rpath/libiomp5.dylib
  Referenced from: /Users/frankma/code/DLC-packaging/macos_v2.2rc3/pyinstaller_packaging/dist/DLC.app/Contents/Resources/libmkl_intel_thread.1.dylib
  Reason: image not found.
Intel MKL FATAL ERROR: Cannot load libmkl_intel_thread.1.dylib.
```

It looks like the `dylib` in question is actually present in `DLC.app`.
Someone encountered a similar issue
[here](https://stackoverflow.com/questions/62903775/intel-mkl-error-using-conda-and-matplotlib-library-not-loaded-rpath-libiomp5),
which was solved by borrowing the `libiomp5.dylib` from the `llvm-openmp`
package. 

### Fixing `libpng16.16.dylib` Version Mismatch Error
After the `libiomp5.dylib` error is fixed, I encountered the same error
with `libpng` as encountered in Catalina:
```
ImportError: dlopen(/Users/frankma/code/DLC-packaging/macos_v2.2rc3/pyinstaller_packaging/dist/DLC.app/Contents/MacOS/cv2/cv2.cpython-38-darwin.so, 2): Library not loaded: @loader_path/libpng16.16.dylib
  Referenced from: /Users/frankma/code/DLC-packaging/macos_v2.2rc3/pyinstaller_packaging/dist/DLC.app/Contents/MacOS/libfreetype.6.dylib
  Reason: Incompatible library version: libfreetype.6.dylib requires version 54.0.0 or later, but libpng16.16.dylib provides version 38.0.0
```

This is fixed by [downloading the `libpng` library separately and copying it
into the app
bundle](https://stackoverflow.com/questions/61824188/issue-converting-python-script-with-pyinstaller-import-error-incompatible-libr).
For more details, refer to `macos/README.md`.

### Fixing `tensorpack` Error
The next problem is related to `tensorpack`:
```
AttributeError: module 'tensorpack.tfutils' has no attribute 'optimizer'
```

This is an error that I had previously encountered in Windows, but
interesting not on Catalina. This was fixed by copying the entire
`tensorpack` folder from the pip installation into the distribution folder,
which for some reason fixes the error.

### Filling in Missing DLC Graphics and Auxillary Files
Similar to Windows and Catalina, some files from DLC needs to be
supplemented to the dist folder. These are:
- `deeplabcut/gui/media/dlc_1-01.png`
- `deeplabcut/gui/media/logo.png`
- `deeplabcut/pose_cfg.yaml`

These steps were needed to launch DLC successfully
Curiously, no hidden imports needed to be added at this point to launch
DLC. The `HDF5` library version did not result in an error either (which
was an issue in the Catalina-made package). 

## Troubleshooting while Using DLC
### Fixing error where commands appear to execute multiple times
This was an error that also occurred on Windows, and is fixed by adding the
following two lines at the start of the `DLC.py`:
```
import multiprocessing
multiprocessing.freeze_support()
```

### Fixing segfault while K-means clustering
```
*** Received signal 11 ***
*** BEGIN MANGLED STACK TRACE ***
0   libtensorflow_framework.2.dylib     0x00000001153210e7 _ZN10tensorflow7testingL17StacktraceHandlerEiP9__siginfoPv + 183
1   libsystem_platform.dylib            0x00007fff205fed7d _sigtramp + 29
2   ???                                 0x0000000000000000 0x0 + 0
3   libomp.dylib                        0x00000001585d8e77 _ZL27__kmp_hyper_barrier_release12barrier_typeP8kmp_infoiiiPv + 151
4   libomp.dylib                        0x00000001585db5fe _Z18__kmp_fork_barrierii + 445
5   libomp.dylib                        0x00000001585c45e2 __kmp_launch_thread + 186
6   libomp.dylib                        0x00000001585ee9e4 _ZL19__kmp_launch_workerPv + 278
7   libsystem_pthread.dylib             0x00007fff205b98fc _pthread_start + 224
8   libsystem_pthread.dylib             0x00007fff205b5443 thread_start + 15
*** END MANGLED STACK TRACE ***

*** Begin stack trace ***
	tensorflow::CurrentStackTrace()
	tensorflow::testing::StacktraceHandler(int, __siginfo*, void*)
	_sigtramp

	__kmp_hyper_barrier_release(barrier_type, kmp_info*, int, int, int, void*)
	__kmp_fork_barrier(int, int)
	__kmp_launch_thread
	__kmp_launch_worker(void*)
	_pthread_start
	thread_start
*** End stack trace ***
multiprocessing/resource_tracker.py:216: UserWarning: resource_tracker: There appear to be 1 leaked semaphore objects to clean up at shutdown
[1]    4020 abort      ./dist/DLC.app/Contents/MacOS/DLC
```
...work in progress. 