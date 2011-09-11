import unittest

def suite():
    return unittest.TestLoader().loadTestsFromNames([
        'djra.api.tests.test_raduser',
        'djra.api.tests.test_radgroup',
    ])
