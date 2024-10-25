import unittest

def run_all_tests():
    # Load all tests from the `unit_tests`, `functional_tests`, and `integration_tests` directories
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Specify the directories to search for test files
    for test_dir in ['unit_tests', 'functional_tests', 'integration_tests']:
        suite.addTests(loader.discover(test_dir))

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_all_tests()