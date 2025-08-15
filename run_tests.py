#!/usr/bin/env python3
"""
Simple test runner to verify the architecture diagram integration.
"""

import sys
import os
sys.path.insert(0, '/workspace')

# Import and run the tests
from test_architecture import TestArchitectureDiagram
import unittest

if __name__ == '__main__':
    print("Running Architecture Diagram Integration Tests")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestArchitectureDiagram)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed! Architecture diagram successfully integrated.")
    else:
        print("❌ Some tests failed. Please check the output above.")
        
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")