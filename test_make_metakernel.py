import unittest

from make_Metakernel import *

class TestMakeKernel(unittest.TestCase):
    
    def test_requests(self):
        # no force update
        run_requestsForSPICE('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/',
                         './SPICE/generic/kernels/lsk',
                         'naif????.tls',
                         show_progress=True,
                         force_update=False,
                         )
        
        # force update
        run_requestsForSPICE('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/',
                         './SPICE/generic/kernels/lsk',
                         'naif????.tls',
                         show_progress=True,
                         force_update=True,
                         )
        
        # no progress bar
        run_requestsForSPICE('https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/',
                         './SPICE/generic/kernels/lsk',
                         'naif????.tls',
                         show_progress=False,
                         force_update=True,
                         )

    def test_Metakernels(self):
        make_Metakernel('juno')

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()