# DIASPICETools
A small package of useful tools for setting up and interfacing with NASA/NAIF's SPICE toolkit (via SpiceyPy)

Currently, the most useful tool included is `make_Metakernel()`, which accesses `wget` via a Python interface to automatically downloads the kernels required for a given spacecraft's trajectory, stores them in an appropriate directory structure, and then writes a metakernel containing symbolic links to all the downloaded kernels.

If a spacecraft you need is not currently supported by `make_Metakernel()`, you find some other bug with the code as is, or you have suggestions for useful features and/or interfaces for this code to provide, please feel free to raise an issue.


