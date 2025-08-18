"""
Unit tests for the helpers.py module.

This module contains tests for the utility functions used in the 
Hidden Markov Model POS tagging project.
"""

import unittest
import tempfile
import os
from collections import OrderedDict
from helpers import read_data, read_tags, Sentence


class TestHelpers(unittest.TestCase):
    """Test cases for helper functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary test data files
        self.test_data_content = """sentence1
word1	TAG1
word2	TAG2
word3	TAG1

sentence2
hello	NOUN
world	NOUN
!	.

sentence3
the	DET
quick	ADJ
brown	ADJ
fox	NOUN"""
        
        self.test_tags_content = """NOUN
VERB
ADJ
DET
.
TAG1
TAG2"""
        
        # Create temporary files
        self.temp_data_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.temp_tags_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        
        self.temp_data_file.write(self.test_data_content)
        self.temp_data_file.close()
        
        self.temp_tags_file.write(self.test_tags_content)
        self.temp_tags_file.close()
    
    def tearDown(self):
        """Clean up after each test method."""
        # Remove temporary files
        os.unlink(self.temp_data_file.name)
        os.unlink(self.temp_tags_file.name)
    
    def test_read_data_structure(self):
        """Test that read_data returns the correct data structure."""
        result = read_data(self.temp_data_file.name)
        
        # Check that result is an OrderedDict
        self.assertIsInstance(result, OrderedDict)
        
        # Check that we have the expected number of sentences
        self.assertEqual(len(result), 3)
        
        # Check that keys are sentence identifiers
        expected_keys = ['sentence1', 'sentence2', 'sentence3']
        self.assertEqual(list(result.keys()), expected_keys)
    
    def test_read_data_sentence_content(self):
        """Test that read_data correctly parses sentence content."""
        result = read_data(self.temp_data_file.name)
        
        # Test first sentence
        sentence1 = result['sentence1']
        self.assertIsInstance(sentence1, Sentence)
        self.assertEqual(sentence1.words, ('word1', 'word2', 'word3'))
        self.assertEqual(sentence1.tags, ('TAG1', 'TAG2', 'TAG1'))
        
        # Test second sentence
        sentence2 = result['sentence2']
        self.assertEqual(sentence2.words, ('hello', 'world', '!'))
        self.assertEqual(sentence2.tags, ('NOUN', 'NOUN', '.'))
        
        # Test third sentence
        sentence3 = result['sentence3']
        self.assertEqual(sentence3.words, ('the', 'quick', 'brown', 'fox'))
        self.assertEqual(sentence3.tags, ('DET', 'ADJ', 'ADJ', 'NOUN'))
    
    def test_read_tags_structure(self):
        """Test that read_tags returns the correct data structure."""
        result = read_tags(self.temp_tags_file.name)
        
        # Check that result is a frozenset
        self.assertIsInstance(result, frozenset)
        
        # Check that we have the expected number of tags
        self.assertEqual(len(result), 7)
    
    def test_read_tags_content(self):
        """Test that read_tags correctly parses tag content."""
        result = read_tags(self.temp_tags_file.name)
        
        expected_tags = {'NOUN', 'VERB', 'ADJ', 'DET', '.', 'TAG1', 'TAG2'}
        self.assertEqual(result, expected_tags)
    
    def test_sentence_namedtuple(self):
        """Test that Sentence namedtuple works correctly."""
        # Test creating a Sentence
        words = ('the', 'cat', 'sat')
        tags = ('DET', 'NOUN', 'VERB')
        sentence = Sentence(words, tags)
        
        # Test accessing fields
        self.assertEqual(sentence.words, words)
        self.assertEqual(sentence.tags, tags)
        
        # Test that it's immutable (characteristic of namedtuples)
        with self.assertRaises(AttributeError):
            sentence.words = ('new', 'words')
    
    def test_read_data_empty_file(self):
        """Test read_data behavior with empty file."""
        # Create empty temporary file
        empty_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        empty_file.write("")
        empty_file.close()
        
        try:
            result = read_data(empty_file.name)
            self.assertIsInstance(result, OrderedDict)
            self.assertEqual(len(result), 0)
        finally:
            os.unlink(empty_file.name)
    
    def test_read_tags_empty_file(self):
        """Test read_tags behavior with empty file."""
        # Create empty temporary file
        empty_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        empty_file.write("")
        empty_file.close()
        
        try:
            result = read_tags(empty_file.name)
            self.assertIsInstance(result, frozenset)
            # Empty file should result in frozenset with one empty string
            self.assertEqual(len(result), 1)
            self.assertIn('', result)
        finally:
            os.unlink(empty_file.name)
    
    def test_read_data_malformed_input(self):
        """Test read_data behavior with malformed input."""
        malformed_content = """sentence1
word1	TAG1
malformed_line_without_tab
word3	TAG1"""
        
        malformed_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        malformed_file.write(malformed_content)
        malformed_file.close()
        
        try:
            # This should raise an exception or handle gracefully
            # The exact behavior depends on the implementation
            with self.assertRaises((ValueError, IndexError)):
                read_data(malformed_file.name)
        finally:
            os.unlink(malformed_file.name)


class TestDataIntegrity(unittest.TestCase):
    """Test cases for data integrity and file existence."""
    
    def test_data_files_exist(self):
        """Test that required data files exist."""
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        
        # Check if data directory exists
        self.assertTrue(os.path.exists(data_dir), "Data directory should exist")
        
        # Check if required files exist
        brown_file = os.path.join(data_dir, 'brown-universal.txt')
        tags_file = os.path.join(data_dir, 'tags-universal.txt')
        
        self.assertTrue(os.path.exists(brown_file), "Brown corpus file should exist")
        self.assertTrue(os.path.exists(tags_file), "Tags file should exist")
    
    def test_tags_file_content(self):
        """Test that tags file contains expected universal tags."""
        tags_file = os.path.join(os.path.dirname(__file__), 'data', 'tags-universal.txt')
        
        if os.path.exists(tags_file):
            tags = read_tags(tags_file)
            
            # Universal tagset should have 12 tags
            expected_tags = {'.', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'X'}
            
            # Check that all expected tags are present
            for tag in expected_tags:
                self.assertIn(tag, tags, f"Tag '{tag}' should be in universal tagset")
    
    def test_brown_file_format(self):
        """Test that Brown corpus file has correct format."""
        brown_file = os.path.join(os.path.dirname(__file__), 'data', 'brown-universal.txt')
        
        if os.path.exists(brown_file):
            # Read first few lines to check format
            with open(brown_file, 'r') as f:
                lines = f.readlines()[:10]  # Read first 10 lines
            
            # Should have sentence identifiers and word-tag pairs
            sentence_found = False
            word_tag_found = False
            
            for line in lines:
                line = line.strip()
                if line and '\t' not in line:
                    sentence_found = True
                elif '\t' in line:
                    word_tag_found = True
                    # Check that line has exactly one tab (word\ttag format)
                    parts = line.split('\t')
                    self.assertEqual(len(parts), 2, f"Line should have word\\ttag format: {line}")
            
            self.assertTrue(sentence_found, "Should find sentence identifiers")
            self.assertTrue(word_tag_found, "Should find word-tag pairs")


if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestHelpers))
    suite.addTest(unittest.makeSuite(TestDataIntegrity))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")