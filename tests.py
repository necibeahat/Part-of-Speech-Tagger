"""
Simple test module for Jupyter notebook compatibility.

This module provides basic testing functions that can be imported
and used within the Jupyter notebooks for the HMM POS tagging project.
"""

import os
from helpers import read_data, read_tags


def test_data_loading():
    """Test that data files can be loaded successfully."""
    try:
        # Test loading Brown corpus data
        brown_file = os.path.join('data', 'brown-universal.txt')
        if os.path.exists(brown_file):
            data = read_data(brown_file)
            print(f"✓ Successfully loaded {len(data)} sentences from Brown corpus")
        else:
            print("⚠ Brown corpus file not found")
        
        # Test loading tags
        tags_file = os.path.join('data', 'tags-universal.txt')
        if os.path.exists(tags_file):
            tags = read_tags(tags_file)
            print(f"✓ Successfully loaded {len(tags)} POS tags")
            print(f"  Tags: {sorted(list(tags))}")
        else:
            print("⚠ Tags file not found")
            
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False


def test_data_integrity():
    """Test data integrity and format."""
    try:
        brown_file = os.path.join('data', 'brown-universal.txt')
        tags_file = os.path.join('data', 'tags-universal.txt')
        
        if not os.path.exists(brown_file) or not os.path.exists(tags_file):
            print("⚠ Data files not found, skipping integrity test")
            return False
        
        # Load data
        data = read_data(brown_file)
        tags = read_tags(tags_file)
        
        # Check that we have reasonable amount of data
        if len(data) < 1000:
            print(f"⚠ Warning: Only {len(data)} sentences found, expected more")
        
        # Check that universal tagset has expected tags
        expected_universal_tags = {'.', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'X'}
        if not expected_universal_tags.issubset(tags):
            missing_tags = expected_universal_tags - tags
            print(f"⚠ Warning: Missing expected tags: {missing_tags}")
        
        # Sample a few sentences to check format
        sample_sentences = list(data.items())[:3]
        for sent_id, sentence in sample_sentences:
            if len(sentence.words) != len(sentence.tags):
                print(f"✗ Error: Sentence {sent_id} has mismatched words and tags")
                return False
        
        print("✓ Data integrity check passed")
        return True
        
    except Exception as e:
        print(f"✗ Error in data integrity test: {e}")
        return False


def run_all_tests():
    """Run all available tests."""
    print("Running POS Tagger Tests")
    print("=" * 40)
    
    tests = [
        ("Data Loading", test_data_loading),
        ("Data Integrity", test_data_integrity),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("Test Summary:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name}: {status}")
    
    return passed == total


if __name__ == "__main__":
    run_all_tests()