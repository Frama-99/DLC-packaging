# Packaging Instructions
## Information
- Packaging OS: macOS Catalina
- DLC Version: v2.1.9
- Executable Works on: macOS Catalina
- Executable Errors on: macOS Big Sur
   - Reason: frame labelling toolbox and graph displays (both leveraging
     matplotlib) crashes (more information below)
- Status: Deprecated, since deeplabcut v2.2rc3 is released

## Step by Step Instructions
0. Secure a Mac with macOS Catalina
1. Follow steps from DLC to install the DLC-CPU conda environment, and
   activate it.
2. Install `pyinstaller` using `pip install pyinstaller` (not conda)
3. Run `pyi-makespec --windowed DLC.py` to generate a template `.spec` file
   for the script
4. In the `.spec` file, add the hidden imports specified below
5. Run `pyinstaller DLC.spec`
6. Copy the `deeplabcut` folder into `dist/DLC.app/Contents/MacOS/` to fill
   in the missing media
7. Copy `libpng16.16.dylib` (follow instructions
   [here](https://stackoverflow.com/questions/61824188/issue-converting-python-script-with-pyinstaller-import-error-incompatible-libr)
   to download the library) into `dist/DLC.app/Contents/MacOS/` to resolve
   the library version conflict error

# Detailed Troubleshooting Steps
## Packaging with pyinstaller on macOS Big Sur
The first attempt was to compile DLC using pyinstaller on macOS Big Sur.
This is the error message: 
```
4103 ERROR: Can not find path /usr/lib/libSystem.B.dylib (needed by /Users/frankma/opt/anaconda3/envs/DLC-CPU/bin/python3.7)
```
The final error is ```RecursionError: maximum recursion depth exceeded```,
but this is probably caused indirectly by the missing library.

It turns out that Apple moved around some libraries and pyinstaller can no
longer find them. According to [this
thread](https://github.com/pyinstaller/pyinstaller/issues/5107) on the
pyinstaller GitHub, they fixed this issue for Python 3.8+, but not for
Python 3.7.

I tried upgrading DLC to Python 3.8 but this didn't work out, since DLC
relies on TensorFlow 1.x, which does not have supoort for Python versions
beyond 3.7. The DLC team is working on support for TF 2.x at their repo
[DeepLabCut-core](https://github.com/DeepLabCut/DeepLabCut-core) (which
should work with Python 3.8), but they haven't worked out the GUI component
of it yet. Our user base is likely to need the GUI component, so trying to
leverage DLC-core wouldn't work.

## Packaging with pyinstaller on macOS Catalina
I managed to hunt down a Mac that hasn't been upgraded to Big Sur yet, and
tried using pyinstaller there. This worked a lot smoother. To generate a
`.app` macOS application bundle, use `pyinstaller --windowed DLC.py`. 

### Resolving `ModuleNotFound` errors
Similar to the packaging process for Windows, many hidden imports need to
be added to prevent `ModuleNotFound` errors when running the executable:
```
'sklearn.neighbors._typedefs',
'sklearn.utils._cython_blas', 
'sklearn.utils._weight_vector',
'sklearn.neighbors._quad_tree',
'sklearn.tree', 
'sklearn.tree._utils',
'skimage.filters.rank.core_cy_3d',
'statsmodels.tsa.statespace._filters',
'statsmodels.tsa.statespace._filters._conventional',
'statsmodels.tsa.statespace._filters._univariate',
'statsmodels.tsa.statespace._filters._univariate_diffuse',
'statsmodels.tsa.statespace._filters._inversions',
'statsmodels.tsa.statespace._smoothers',
'statsmodels.tsa.statespace._smoothers._alternative',
'statsmodels.tsa.statespace._smoothers._classical',
'statsmodels.tsa.statespace._smoothers._conventional',
'statsmodels.tsa.statespace._smoothers._univariate',
'statsmodels.tsa.statespace._smoothers._univariate_diffuse'
```

### Resolving missing graphics errors
Similar to Windows, we need to paste the `deeplabcut` folder into the
distribution folder to fill in some missing media. Just clone the latest
DLC repo from GitHub and copy the `deeplabcut` folder into
`DLC.app/Contents/MacOS`. 

### Resolving `libpng16.16.dylib` incompatibility error
The next error I got when starting the packaged app was this:
```
ImportError: dlopen(<working directory>/dist/DLC.app/Contents/MacOS/cv2/cv2.cpython-37m-darwin.so, 2): Library not loaded: @loader_path/libpng16.16.dylib
  Referenced from: <working directory>/dist/DLC.app/Contents/MacOS/libfreetype.6.dylib
  Reason: Incompatible library version: libfreetype.6.dylib requires version 54.0.0 or later, but libpng16.16.dylib provides version 38.0.0
```
The [first
solution](https://stackoverflow.com/questions/46246649/manually-specify-library-when-pyinstaller-sees-conflicting-versions)
I tried suggested to add this line to `DLC.spec`:
```
a.binaries = a.binaries - TOC([('libpng16.16.dylib',None,None)])
```
... but this resulted in this new error that I didn't know how to solve
when running the executable:
```
[51547] mod is NULL - structTraceback (most recent call last):
  File "struct.py", line 14, in <module>
ImportError: cannot import name '_clearcache' from '_struct' (unknown location)
[51547] mod is NULL - pyimod02_archiveTraceback (most recent call last):
  File "PyInstaller/loader/pyimod02_archive.py", line 30, in <module>
ModuleNotFoundError: No module named 'struct'
[51547] mod is NULL - pyimod03_importersTraceback (most recent call last):
  File "PyInstaller/loader/pyimod03_importers.py", line 26, in <module>
ModuleNotFoundError: No module named 'pyimod02_archive'
Traceback (most recent call last):
  File "PyInstaller/loader/pyiboot01_bootstrap.py", line 17, in <module>
ModuleNotFoundError: No module named 'pyimod03_importers'
[51547] Failed to execute script pyiboot01_bootstrap
```

Then I found [another
solution](https://stackoverflow.com/questions/61824188/issue-converting-python-script-with-pyinstaller-import-error-incompatible-libr)
that suggested to download the `libpng` library separately and copy it into
the app bundle, which worked like a charm!

### Resolving `HDF5` library version mismatch error
I didn't know how to solve this, but I wanted to see if I could just
suppress the error and risk the version mismatch. To suppress the error,
set the environment variable in `DLC.py`:
```
os.environ["HDF5_DISABLE_VERSION_CHECK"] = "2"
```
The version mismatch didn't seem to result in any errors per testing below.

## Testing on macOS Catalina
I made two test projects, one using the native Python distribution of DLC,
and another using the pyinstaller packaged version. I tested the following
functions:
- Project creation
- Frame extraction
- Frame labelling
- Training dataset creation
- Network training
- Network evaluation
- Video analysis
- Labelled video creation

All of these functions work on the packaged version, at comparable speeds
compared to the native Python distribution.

## Testing the Catalina packaged DLC on Big Sur
Next is testing if the app packaged on Catalina will work on Big Sur. I
made another test project and tested the functions above. Two things
resulted in crashes:
- In frame labelling, loading a folder of images result in a segmentation
  fault
- In video analysis, if the "want to plot the trajectories" option is
  checked (along with "want plots to pop up?"), a segmentation fault
  occurs. The data generated from the video as well as the plot generated
  are both valid and intact; it seems that only showing the plot (a result
  of a call to `plt.show()`) results in the seg fault

It seemed pretty likely that the `show()` function from `matplotlib` is
causing the seg fault. It looks like other people have been experiencing
this too and someone suggested to [simply uninstall and
reinstall](https://stackoverflow.com/questions/64841082/segmentation-fault-11-python-after-upgrading-to-os-big-sur)
`matplotlib`. This resulted in the error below:
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
deeplabcut 2.1.10.4 requires matplotlib==3.1.3, but you have matplotlib 3.4.2 which is incompatible.
```
It does appear that the new version of matplotlib was successfully
installed though.

I first tested this on macOS Catalina, which worked without problems either
through the native Python package or through the pyinstaller packaged
bundle. 

... but the packaged version still results in a segmentation fault on Big
Sur. It seems that there is something else other than matplotlib's version
that is causing the seg fault in the packaged version. A lot of people in
forums talk about having the wrong backend causing the seg fault. So to
further troubleshoot, I wrote a simple script that prints out the version,
backend, and shows a plot using matplotlib (this is the updated mpl on
Catalina). I packaged the script with pyinstaller on Catalina, and
transferred the binary to Big Sur.

```
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
```

On both Catalina and Big Sur, the packaged app prints out `3.4.2` as the
version as expected. The backend is `MacOSX`. Using the `--windowed` flag
(which generates a `.app` bundle) didn't make a difference; the version is
still `3.4.2` and the backend is still `MacOSX` on both system versions.

I then wanted to see if importing DLC interact with the backend that
matplotlib uses. As a baseline, I first added the script above
is added before `import deeplabcut`. The result is consistent- the version
is `3.4.2` and the backend is `MacOSX`. Very interestingly, doing this
causes DLC to fail to launch, with the error below:
```
Traceback (most recent call last):
  File "DLC.py", line 33, in <module>
  File "PyInstaller/loader/pyimod03_importers.py", line 540, in exec_module
  File "deeplabcut/__init__.py", line 32, in <module>
  File "matplotlib/__init__.py", line 1080, in use
  File "matplotlib/pyplot.py", line 288, in switch_backend
ImportError: Cannot load backend 'WXAgg' which requires the 'wx' interactive framework, as 'macosx' is currently running
```

It looks like DLC is trying to use the `WXAgg` backend, whereas matplotlib
defaulted to using `MacOSX` in the script added.

Next I added the script above in between `import deeplabcut` and
`deeplabcut.launch_dlc()`. On both Catalina and Big Sur, the version
remains to be `3.4.2` but the backend became `WXAgg`. On Catalina, the
sample graph is displayed successfully, and after closing it the DLC GUI
launches with no problem. On Big Sur, a seg fault occurs when the graph is
attempted to be shown. It's clear that `WXAgg` is causing the problem on
Big Sur.

I thought that setting the mpl backend back to `MacOSX` after importing DLC
might be worth a try, but this did not work on either Catalina or Big Sur.
It looks like [DLC requires matplotlib to use
`WXAgg`](https://github.com/DeepLabCut/DeepLabCut/search?q=wxagg) and
modifying what matplotlib backend to use would probably require modifying
the DLC code.