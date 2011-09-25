import unittest

def suite():
    return unittest.TestLoader().loadTestsFromNames([
        'djra.radmin.tests.test_dashboard',
        'djra.radmin.tests.test_users',
        'djra.radmin.tests.test_groups',
    ])
