# AutoMeta
A small package of useful tools for setting up and interfacing with NASA/NAIF's SPICE toolkit (via SpiceyPy)

Currently, the most useful tool included is `make_Metakernel()`, which accesses `wget` via a Python interface to automatically downloads the kernels required for a given spacecraft's trajectory, stores them in an appropriate directory structure, and then writes a metakernel containing symbolic links to all the downloaded kernels.

Please note that this package is a *work in progress*, and is available as-is. The current release is *not* guaranteed to be stable. Please feel free to raise issues or submit changes!

## Usage
Basic usage to create a spacecraft Metakernel: <br>
(1) From the installation directory, run: <br>
`>>> make_Metakernel.py` <br>
You will then be prompted for the target spacecraft name and the SPICE base directory: <br>
    - Enter names in plaintext, not with quote characters (e.g. ', ", >, ), }, ]) <br>
    - If you wish to create a SPICE directory in the current directory, simply press enter during the second prompt <br>

(2) From the installation directory, run: <br>
`>>> from make_Metakernel import *` <br>
`>>> metakernel_filepath = make_Metakernel('spacecraft', basedir='/Your/Directory/Here')` <br>
Where `'spacecraft'` is the target spacecraft as a string, and `'/Your/Directory/Here'` is the chosen base directory for SPICE (again, an empty string (`''`) will create the SPICE directory in your current location) <br>
You can then check the metakernel location with: <br>
`>>> print(metakernel_filepath)` <br>

If a spacecraft you need is not currently supported by `make_Metakernel()`, you find some other bug with the code as is, or you have suggestions for useful features and/or interfaces for this code to provide, please feel free to raise an issue.


