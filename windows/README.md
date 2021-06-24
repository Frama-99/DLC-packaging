# Packaging DLC with Whisking into an Installable Package

## `pyinstaller`: Packaging `.py` file into executable
We will be using `pyinstaller` to convert the `.py` file into a `.exe`.
This is great because we also avoid the need for the enduser to install
anaconda since `pyinstaller` packages everything.

- First, switch into the conda environment that has the required
  dependencies to run the script (e.g. `conda activate DLC_GPU`)
- Run `pip install 'setuptools<45.0.0'`. This is because there has been
  [known issues](https://github.com/pypa/setuptools/issues/1963) that
  `pyinstaller` has with newer versions of setuptools. 
- Install `pyinstaller` with `pip install pyinstaller`.
- Run `pyinstaller <filename of .py or .spec>` (consult online sources for
  available flags)
    - Use the `--debug all` flag to show additional output when running
      your executable. For me, the debug option doesn't work when compiling
      with TensorFlow. This seems to be a [known
      issue](https://github.com/pyinstaller/pyinstaller/issues/4034).
    - The `-F` flag compiles everything into one single `.exe` file rather
      than many `.dll`s.
    - To actually see any outputs of the executable without having the
      terminal window close immediately, run the executable in a terminal
      (rather than double clicking on it).
  - For DLC, it is likely better to perform a normal compilation rather
    than compiling into a single executable (do not use the `-F` flag).
    - The former results in much faster launch time
    - Also, in the case of a normal compilation, the `deeplabcut` source
      folder needs to be pasted into the distribution folder (`dist/DLC`)
      in order for DLC to function correctly. Not yet certain if these
      errors would also be present in the case of a single executable (if
      they are, then it would mean that a normal compilation is the only
      option). 
- Paste the `deeplabcut` package into the `dist` directory that holds the
  generated binary. This helps to fill in some required media.

## Troubleshooting `pyinstaller`
Many errors could come up, either in running `pyinstaller` or in running
DLC after. Here are some problems that I encountered:
- Problem: `ModuleNotFound` errors while running the executable. 
  - Solution: this means that `pyinstaller` missed some dependencies. Fix
    this by adding a `--hidden-imports` flag (e.g. `--hidden-imports
    sklearn.neighbors._typedefs`)
- Problem: `AttributeError` when running the executable, even when the
  attribute is there in the source. I ran into this problem when trying to
  train a model with a dataset generated with the `tensorpack` option.
  - Solution: In the `dist` directory, paste in the library that is causing
    the error from your local machine's `site-packages`. Usually only a few
    files from the library will be needed, but this somehow solves the
    issue.
- Problem: The `-i` option to add an icon to modify the icon of the
  executable just doesn't work...
    - Solution: I haven't yet found out how to solve this, but the free
      application "Resource Hacker" is a good workaround for changing the
      logo of the executable.
- Problem: something else...
  - Solution: Reference [these
    "recipes"](https://github.com/pyinstaller/pyinstaller/wiki/Recipes)
    from `pyinstaller` for things that might require special steps. For
    example, I solved the issue with using datasets augmented by
    `tensorpack` by referencing [this
    recipe](https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing).
    
## Creating an installer with Advanced Installer
Advanced Installer helps us create an all-in-one installer that installs
the binaries created using `pyinstaller` to the user's computer. It
requires minimal technical knowledge and creates an installer with a UI
that resembles that of other established applications. 

Advanced installer's interface is intuitive and there is very good
documentation available. A few tips:
- If the project is open source, you can request a free license.
- You can create desktop and start menu shortcuts in the "Files and
  Folders" tab.
- You can add pre-requisites that the user need to install. For example,
  for DLC-GPU, this would be CUDA. You can also choose whether or not the
  pre-requisite is shown to the user based on certain conditions such as
  their OS. 
- Under "Install Parameters", there is an option for Installation type that
  is "Per-machine if user is administrator, per-user otherwise". This is
  very convenient to make sure that non-admins are able to install the
  software without having to change the installation directory themselves.