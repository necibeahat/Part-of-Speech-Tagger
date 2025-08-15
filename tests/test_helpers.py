"""
Unit tests for the helpers module.

This module contains tests for the utility functions and classes
used in the Part-of-Speech Tagger project.
"""

import pytest
import sys
import os
from collections import OrderedDict

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from helpers import read_data, read_tags, Sentence, Subset, Dataset
except ImportError as e:
    pytest.skip(f"Could not import helpers module: {e}", allow_module_level=True)


class TestSentence:
    """Test cases for the Sentence namedtuple."""
    
    def test_sentence_creation(self):
        """Test that Sentence namedtuple works correctly."""
        words = ["The", "cat", "sat"]
        tags = ["DT", "NN", "VBD"]
        sentence = Sentence(words, tags)
        assert sentence.words == words
        assert sentence.tags == tags
    
    def test_sentence_immutability(self):
        """Test that Sentence is immutable."""
        words = ["The", "cat"]
        tags = ["DT", "NN"]
        sentence = Sentence(words, tags)
        
        # Should not be able to modify
        with pytest.raises(AttributeError):
            sentence.words = ["New", "words"]


class TestHelperFunctions:
    """Test cases for helper functions."""
    
    def test_read_tags_function_exists(self):
        """Test that read_tags function exists and is callable."""
        assert callable(read_tags)
    
    def test_read_data_function_exists(self):
        """Test that read_data function exists and is callable."""
        assert callable(read_data)
    
    def test_read_tags_with_sample_data(self, tmp_path):
        """Test read_tags with sample tag data."""
        # Create a temporary tags file
        tags_file = tmp_path / "test_tags.txt"
        tags_content = "NOUN\nVERB\nADJ\nADV"
        tags_file.write_text(tags_content)
        
        # Test the function
        tags = read_tags(str(tags_file))
        expected_tags = frozenset(["NOUN", "VERB", "ADJ", "ADV"])
        assert tags == expected_tags
    
    def test_read_data_with_sample_data(self, tmp_path):
        """Test read_data with sample sentence data."""
        # Create a temporary data file
        data_file = tmp_path / "test_data.txt"
        data_content = """b100
The	DT
cat	NN
sat	VBD

b101
A	DT
dog	NN
ran	VBD"""
        data_file.write_text(data_content)
        
        # Test the function
        data = read_data(str(data_file))
        
        # Verify structure
        assert isinstance(data, OrderedDict)
        assert "b100" in data
        assert "b101" in data
        
        # Verify sentence content
        sentence_b100 = data["b100"]
        assert sentence_b100.words == ("The", "cat", "sat")
        assert sentence_b100.tags == ("DT", "NN", "VBD")


class TestSubset:
    """Test cases for the Subset class."""
    
    def test_subset_creation(self):
        """Test Subset creation with sample data."""
        # Create sample sentences
        sentences = {
            "s1": Sentence(("The", "cat"), ("DT", "NN")),
            "s2": Sentence(("A", "dog"), ("DT", "NN")),
            "s3": Sentence(("The", "bird"), ("DT", "NN"))
        }
        
        keys = ["s1", "s2"]
        subset = Subset(sentences, keys)
        
        # Test basic properties
        assert len(subset) == 2
        assert subset.keys == keys
        assert "s1" in subset.sentences
        assert "s2" in subset.sentences
        assert "s3" not in subset.sentences
    
    def test_subset_vocab_and_tagset(self):
        """Test that Subset correctly computes vocabulary and tagset."""
        sentences = {
            "s1": Sentence(("The", "cat", "runs"), ("DT", "NN", "VBZ")),
            "s2": Sentence(("A", "dog", "walks"), ("DT", "NN", "VBZ"))
        }
        
        subset = Subset(sentences, ["s1", "s2"])
        
        expected_vocab = frozenset(["The", "cat", "runs", "A", "dog", "walks"])
        expected_tagset = frozenset(["DT", "NN", "VBZ"])
        
        assert subset.vocab == expected_vocab
        assert subset.tagset == expected_tagset


class TestDataset:
    """Test cases for the Dataset class."""
    
    def test_dataset_creation_with_files(self, tmp_path):
        """Test Dataset creation with actual files."""
        # Create test files
        tags_file = tmp_path / "tags.txt"
        tags_file.write_text("DT\nNN\nVBZ")
        
        data_file = tmp_path / "data.txt"
        data_content = """s1
The	DT
cat	NN
runs	VBZ

s2
A	DT
dog	NN
walks	VBZ

s3
The	DT
bird	NN
flies	VBZ"""
        data_file.write_text(data_content)
        
        # Create dataset
        dataset = Dataset(str(tags_file), str(data_file), train_test_split=0.6, seed=42)
        
        # Test basic properties
        assert len(dataset) == 3
        assert isinstance(dataset.training_set, Subset)
        assert isinstance(dataset.testing_set, Subset)
        
        # Test split (with seed=42, should be deterministic)
        total_sentences = len(dataset.training_set) + len(dataset.testing_set)
        assert total_sentences == 3


class TestIntegration:
    """Integration tests for the helpers module."""
    
    def test_full_workflow_simulation(self, tmp_path):
        """Test a complete workflow with the helper functions."""
        # Create test files
        tags_file = tmp_path / "universal_tags.txt"
        tags_file.write_text("DT\nNN\nVBZ\nJJ")
        
        data_file = tmp_path / "brown_data.txt"
        data_content = """sent1
The	DT
quick	JJ
cat	NN
runs	VBZ

sent2
A	DT
slow	JJ
dog	NN
walks	VBZ"""
        data_file.write_text(data_content)
        
        # Test the complete workflow
        tagset = read_tags(str(tags_file))
        sentences = read_data(str(data_file))
        dataset = Dataset(str(tags_file), str(data_file), train_test_split=0.5, seed=123)
        
        # Verify everything works together
        assert len(tagset) == 4
        assert len(sentences) == 2
        assert len(dataset.training_set) + len(dataset.testing_set) == 2
        assert dataset.tagset == tagset


if __name__ == "__main__":
    pytest.main([__file__])