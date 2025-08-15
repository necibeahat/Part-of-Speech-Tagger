"""
Test suite for helpers.py module

This module contains comprehensive tests for all functions and classes
in the helpers.py module, including data loading, model visualization,
and dataset handling functionality.
"""

import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from collections import namedtuple, OrderedDict
import numpy as np

from helpers import (
    Sentence, read_data, read_tags, model2png, show_model,
    Subset, Dataset
)


class TestSentence:
    """Test the Sentence namedtuple"""
    
    def test_sentence_creation(self):
        """Test creating a Sentence namedtuple"""
        words = ("The", "cat", "sat")
        tags = ("DET", "NOUN", "VERB")
        sentence = Sentence(words, tags)
        
        assert sentence.words == words
        assert sentence.tags == tags


class TestReadData:
    """Test the read_data function"""
    
    def test_read_data_valid_file(self):
        """Test reading valid data file"""
        # Create a temporary file with test data
        test_data = """sentence1

The	DET
cat	NOUN
sat	VERB

sentence2

A	DET
dog	NOUN
ran	VERB
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(test_data)
            temp_filename = f.name
        
        try:
            result = read_data(temp_filename)
            
            # Check that result is an OrderedDict
            assert isinstance(result, OrderedDict)
            
            # Check that we have two sentences
            assert len(result) == 2
            assert "sentence1" in result
            assert "sentence2" in result
            
            # Check sentence1 content
            sentence1 = result["sentence1"]
            assert sentence1.words == ("The", "cat", "sat")
            assert sentence1.tags == ("DET", "NOUN", "VERB")
            
            # Check sentence2 content
            sentence2 = result["sentence2"]
            assert sentence2.words == ("A", "dog", "ran")
            assert sentence2.tags == ("DET", "NOUN", "VERB")
            
        finally:
            os.unlink(temp_filename)
    
    def test_read_data_empty_file(self):
        """Test reading empty file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("")
            temp_filename = f.name
        
        try:
            result = read_data(temp_filename)
            assert isinstance(result, OrderedDict)
            assert len(result) == 0
        finally:
            os.unlink(temp_filename)
    
    def test_read_data_file_not_found(self):
        """Test reading non-existent file"""
        with pytest.raises(FileNotFoundError):
            read_data("non_existent_file.txt")


class TestReadTags:
    """Test the read_tags function"""
    
    def test_read_tags_valid_file(self):
        """Test reading valid tags file"""
        test_tags = "DET\nNOUN\nVERB\nADJ\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(test_tags)
            temp_filename = f.name
        
        try:
            result = read_tags(temp_filename)
            
            # Check that result is a frozenset
            assert isinstance(result, frozenset)
            
            # Check content
            expected_tags = {"DET", "NOUN", "VERB", "ADJ", ""}  # Empty string from final newline
            assert result == expected_tags
            
        finally:
            os.unlink(temp_filename)
    
    def test_read_tags_empty_file(self):
        """Test reading empty tags file"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("")
            temp_filename = f.name
        
        try:
            result = read_tags(temp_filename)
            assert isinstance(result, frozenset)
            assert result == frozenset([""])
        finally:
            os.unlink(temp_filename)
    
    def test_read_tags_file_not_found(self):
        """Test reading non-existent tags file"""
        with pytest.raises(FileNotFoundError):
            read_tags("non_existent_tags.txt")


class TestModel2Png:
    """Test the model2png function"""
    
    @patch('helpers.nx.drawing.nx_pydot.to_pydot')
    @patch('helpers.mplimg.imread')
    def test_model2png_basic(self, mock_imread, mock_to_pydot):
        """Test basic model2png functionality"""
        # Create a mock model
        mock_model = MagicMock()
        mock_model.start = "start_state"
        mock_model.end = "end_state"
        
        # Create mock nodes
        mock_node1 = MagicMock()
        mock_node1.name = "state1"
        mock_node2 = MagicMock()
        mock_node2.name = "state2"
        
        mock_model.graph.nodes.return_value = [mock_node1, mock_node2, mock_model.start, mock_model.end]
        mock_model.graph.subgraph.return_value.nodes.return_value = [mock_node1, mock_node2]
        
        # Mock pydot graph
        mock_pydot_graph = MagicMock()
        mock_pydot_graph.create_png.return_value = b"fake_png_data"
        mock_to_pydot.return_value = mock_pydot_graph
        
        # Mock imread
        mock_imread.return_value = np.array([[1, 2, 3]])
        
        # Test the function
        result = model2png(mock_model)
        
        # Verify calls
        mock_to_pydot.assert_called_once()
        mock_pydot_graph.set_rankdir.assert_called_once_with("LR")
        mock_pydot_graph.create_png.assert_called_once_with(prog='dot')
        mock_imread.assert_called_once()
        
        # Check result
        assert isinstance(result, np.ndarray)
    
    @patch('helpers.nx.drawing.nx_pydot.to_pydot')
    @patch('helpers.mplimg.imread')
    @patch('builtins.open', create=True)
    @patch('os.path.exists')
    def test_model2png_with_filename(self, mock_exists, mock_open, mock_imread, mock_to_pydot):
        """Test model2png with filename parameter"""
        mock_exists.return_value = False
        
        # Create a mock model
        mock_model = MagicMock()
        mock_model.start = "start_state"
        mock_model.end = "end_state"
        mock_model.graph.nodes.return_value = []
        mock_model.graph.subgraph.return_value.nodes.return_value = []
        
        # Mock pydot graph
        mock_pydot_graph = MagicMock()
        mock_pydot_graph.create_png.return_value = b"fake_png_data"
        mock_to_pydot.return_value = mock_pydot_graph
        
        # Mock imread
        mock_imread.return_value = np.array([[1, 2, 3]])
        
        # Test with filename
        result = model2png(mock_model, filename="test.png")
        
        # Verify file operations
        mock_exists.assert_called_once_with("test.png")
        mock_open.assert_called()


class TestShowModel:
    """Test the show_model function"""
    
    @patch('helpers.plt.figure')
    @patch('helpers.plt.imshow')
    @patch('helpers.plt.axis')
    @patch('helpers.model2png')
    def test_show_model(self, mock_model2png, mock_axis, mock_imshow, mock_figure):
        """Test show_model function"""
        mock_model = MagicMock()
        mock_model2png.return_value = np.array([[1, 2, 3]])
        
        show_model(mock_model, figsize=(10, 10))
        
        mock_figure.assert_called_once_with(figsize=(10, 10))
        mock_model2png.assert_called_once_with(mock_model)
        mock_imshow.assert_called_once()
        mock_axis.assert_called_once_with('off')


class TestSubset:
    """Test the Subset class"""
    
    def test_subset_creation(self):
        """Test creating a Subset"""
        # Create test sentences
        sentences = {
            "s1": Sentence(("The", "cat"), ("DET", "NOUN")),
            "s2": Sentence(("A", "dog"), ("DET", "NOUN")),
            "s3": Sentence(("Big", "house"), ("ADJ", "NOUN"))
        }
        
        keys = ["s1", "s2"]
        subset = Subset(sentences, keys)
        
        # Test basic properties
        assert len(subset) == 2
        assert subset.keys == keys
        assert "s1" in subset.sentences
        assert "s2" in subset.sentences
        assert "s3" not in subset.sentences
        
        # Test vocabulary
        expected_vocab = {"The", "cat", "A", "dog"}
        assert subset.vocab == expected_vocab
        
        # Test tagset
        expected_tagset = {"DET", "NOUN"}
        assert subset.tagset == expected_tagset
        
        # Test word count
        assert subset.N == 4  # "The", "cat", "A", "dog"
    
    def test_subset_iteration(self):
        """Test iterating over Subset"""
        sentences = {
            "s1": Sentence(("The", "cat"), ("DET", "NOUN")),
            "s2": Sentence(("A", "dog"), ("DET", "NOUN"))
        }
        
        keys = ["s1", "s2"]
        subset = Subset(sentences, keys)
        
        # Test iteration
        items = list(subset)
        assert len(items) == 2
        assert ("s1", sentences["s1"]) in items
        assert ("s2", sentences["s2"]) in items


class TestDataset:
    """Test the Dataset class"""
    
    def test_dataset_creation(self):
        """Test creating a Dataset"""
        # Create temporary files
        tags_content = "DET\nNOUN\nVERB"
        data_content = """s1

The	DET
cat	NOUN

s2

A	DET
dog	NOUN
runs	VERB

s3

Big	ADJ
house	NOUN
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tags_file:
            tags_file.write(tags_content)
            tags_filename = tags_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as data_file:
            data_file.write(data_content)
            data_filename = data_file.name
        
        try:
            dataset = Dataset(tags_filename, data_filename, train_test_split=0.6, seed=42)
            
            # Test basic properties
            assert len(dataset) == 3
            assert len(dataset.sentences) == 3
            
            # Test tagset
            expected_tagset = {"DET", "NOUN", "VERB", ""}  # Empty string from split
            assert dataset.tagset == expected_tagset
            
            # Test vocabulary
            expected_vocab = {"The", "cat", "A", "dog", "runs", "Big", "house"}
            assert dataset.vocab == expected_vocab
            
            # Test train/test split (with 60% split and 3 sentences, should be 1-2 split)
            assert len(dataset.training_set) >= 1
            assert len(dataset.testing_set) >= 1
            assert len(dataset.training_set) + len(dataset.testing_set) == 3
            
            # Test that training and testing sets are Subset instances
            assert isinstance(dataset.training_set, Subset)
            assert isinstance(dataset.testing_set, Subset)
            
        finally:
            os.unlink(tags_filename)
            os.unlink(data_filename)
    
    def test_dataset_iteration(self):
        """Test iterating over Dataset"""
        tags_content = "DET\nNOUN"
        data_content = """s1

The	DET
cat	NOUN
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as tags_file:
            tags_file.write(tags_content)
            tags_filename = tags_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as data_file:
            data_file.write(data_content)
            data_filename = data_file.name
        
        try:
            dataset = Dataset(tags_filename, data_filename)
            
            # Test iteration
            items = list(dataset)
            assert len(items) == 1
            assert items[0][0] == "s1"
            assert isinstance(items[0][1], Sentence)
            
        finally:
            os.unlink(tags_filename)
            os.unlink(data_filename)


if __name__ == "__main__":
    pytest.main([__file__])