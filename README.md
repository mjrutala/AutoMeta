# DIASPICETools
A small package of useful tools for setting up and interfacing with NASA/NAIF's SPICE toolkit (via SpiceyPy)

Currently, the most useful tool included is `make_Metakernel()`, which accesses `wget` via a Python interface to automatically downloads the kernels required for a given spacecraft's trajectory, stores them in an appropriate directory structure, and then writes a metakernel containing symbolic links to all the downloaded kernels.

Basic usage to create a spacecraft Metakernel:
(1) From the installation directory, run:
`>>> make_Metakernel.py`
You will then be prompted for the target spacecraft name and the SPICE base directory:
    - Enter names in plaintext, not with quote characters (e.g. ', ", >, ), }, ])
    - If you wish to create a SPICE directory in the current directory, simply press enter during the second prompt

(2) From the installation directory, run:
`>>> from make_Metakernel import *`
`>>> metakernel_filepath = make_Metakernel('spacecraft', basedir='/Your/Directory/Here')`
Where `'spacecraft'` is the target spacecraft as a string, and `'/Your/Directory/Here'` is the chosen base directory for SPICE (again, an empty string (`''`) will create the SPICE directory in your current location)
You can then check the metakernel location with:
`>>> print(metakernel_filepath)`

If a spacecraft you need is not currently supported by `make_Metakernel()`, you find some other bug with the code as is, or you have suggestions for useful features and/or interfaces for this code to provide, please feel free to raise an issue.


