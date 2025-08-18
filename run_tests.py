#!/usr/bin/env python3
"""
Test runner script for the HMM POS Tagging project.

This script runs all available tests including unit tests and integration tests.
"""

import sys
import os
import subprocess


def run_unit_tests():
    """Run unit tests using unittest."""
    print("Running Unit Tests")
    print("=" * 50)
    
    try:
        # Run the unit tests
        result = subprocess.run([sys.executable, 'test_helpers.py'], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running unit tests: {e}")
        return False


def run_integration_tests():
    """Run integration tests."""
    print("\nRunning Integration Tests")
    print("=" * 50)
    
    try:
        # Run the integration tests
        result = subprocess.run([sys.executable, 'tests.py'], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running integration tests: {e}")
        return False


def run_pytest():
    """Run tests using pytest if available."""
    print("\nRunning Tests with pytest")
    print("=" * 50)
    
    try:
        # Check if pytest is available
        result = subprocess.run([sys.executable, '-m', 'pytest', '--version'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("pytest not available, skipping pytest tests")
            return True
        
        # Run pytest
        result = subprocess.run([sys.executable, '-m', 'pytest', 'test_helpers.py', '-v'], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pytest: {e}")
        return False


def main():
    """Main test runner function."""
    print("HMM POS Tagging Project - Test Suite")
    print("=" * 60)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run all test suites
    results = []
    
    # Unit tests
    unit_result = run_unit_tests()
    results.append(("Unit Tests", unit_result))
    
    # Integration tests
    integration_result = run_integration_tests()
    results.append(("Integration Tests", integration_result))
    
    # Pytest (if available)
    pytest_result = run_pytest()
    results.append(("Pytest", pytest_result))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name:20}: {status}")
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    # Exit with appropriate code
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()