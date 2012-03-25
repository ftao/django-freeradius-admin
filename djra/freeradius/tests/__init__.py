import unittest

def suite():
    return unittest.TestLoader().loadTestsFromNames([
        'djra.freeradius.tests.test_models',
    ])  

