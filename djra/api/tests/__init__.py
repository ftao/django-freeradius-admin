import unittest

def suite():
    return unittest.TestLoader().loadTestsFromNames([
        'djra.api.tests.test_raduser',
        'djra.api.tests.test_radgroup',
        'djra.api.tests.test_radacct',
        'djra.api.tests.test_models',
    ])
