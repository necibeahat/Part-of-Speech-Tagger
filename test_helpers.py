"""
Unit tests for helpers.py module

This module contains basic unit tests for the helper functions used in the
NLP Part of Speech tagging project.
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from collections import namedtuple

import helpers


class TestHelpers(unittest.TestCase):
    """Test cases for helper functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_data_content = """sentence1
word1	TAG1
word2	TAG2

sentence2
word3	TAG3
word4	TAG4"""
        
        self.test_tags_content = "TAG1\nTAG2\nTAG3\nTAG4"

    def test_sentence_namedtuple(self):
        """Test Sentence namedtuple creation"""
        words = ("word1", "word2")
        tags = ("TAG1", "TAG2")
        sentence = helpers.Sentence(words, tags)
        
        self.assertEqual(sentence.words, words)
        self.assertEqual(sentence.tags, tags)

    def test_read_data(self):
        """Test read_data function"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(self.test_data_content)
            temp_file = f.name

        try:
            result = helpers.read_data(temp_file)
            
            # Check that we got an OrderedDict
            self.assertIsInstance(result, dict)
            
            # Check that we have the expected sentences
            self.assertIn('sentence1', result)
            self.assertIn('sentence2', result)
            
            # Check sentence1 content
            sentence1 = result['sentence1']
            self.assertEqual(sentence1.words, ('word1', 'word2'))
            self.assertEqual(sentence1.tags, ('TAG1', 'TAG2'))
            
            # Check sentence2 content
            sentence2 = result['sentence2']
            self.assertEqual(sentence2.words, ('word3', 'word4'))
            self.assertEqual(sentence2.tags, ('TAG3', 'TAG4'))
            
        finally:
            os.unlink(temp_file)

    def test_read_tags(self):
        """Test read_tags function"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(self.test_tags_content)
            temp_file = f.name

        try:
            result = helpers.read_tags(temp_file)
            
            # Check that we got a frozenset
            self.assertIsInstance(result, frozenset)
            
            # Check that we have the expected tags
            expected_tags = {'TAG1', 'TAG2', 'TAG3', 'TAG4'}
            self.assertEqual(result, expected_tags)
            
        finally:
            os.unlink(temp_file)

    def test_subset_creation(self):
        """Test Subset class creation"""
        # Create mock sentences
        sentences = {
            'sent1': helpers.Sentence(('word1', 'word2'), ('TAG1', 'TAG2')),
            'sent2': helpers.Sentence(('word3', 'word4'), ('TAG3', 'TAG4'))
        }
        keys = ['sent1', 'sent2']
        
        subset = helpers.Subset(sentences, keys)
        
        # Check basic properties
        self.assertEqual(len(subset), 2)
        self.assertEqual(subset.keys, keys)
        
        # Check vocabulary
        expected_vocab = {'word1', 'word2', 'word3', 'word4'}
        self.assertEqual(subset.vocab, expected_vocab)
        
        # Check tagset
        expected_tagset = {'TAG1', 'TAG2', 'TAG3', 'TAG4'}
        self.assertEqual(subset.tagset, expected_tagset)
        
        # Check word count
        self.assertEqual(subset.N, 4)

    @patch('helpers.read_tags')
    @patch('helpers.read_data')
    @patch('random.seed')
    @patch('random.shuffle')
    def test_dataset_creation(self, mock_shuffle, mock_seed, mock_read_data, mock_read_tags):
        """Test Dataset class creation"""
        # Mock the file reading functions
        mock_sentences = {
            'sent1': helpers.Sentence(('word1', 'word2'), ('TAG1', 'TAG2')),
            'sent2': helpers.Sentence(('word3', 'word4'), ('TAG3', 'TAG4')),
            'sent3': helpers.Sentence(('word5', 'word6'), ('TAG1', 'TAG3')),
            'sent4': helpers.Sentence(('word7', 'word8'), ('TAG2', 'TAG4'))
        }
        mock_read_data.return_value = mock_sentences
        mock_read_tags.return_value = frozenset(['TAG1', 'TAG2', 'TAG3', 'TAG4'])
        
        # Mock random.shuffle to have predictable behavior
        def mock_shuffle_func(lst):
            # Keep the order for predictable testing
            pass
        mock_shuffle.side_effect = mock_shuffle_func
        
        dataset = helpers.Dataset('tags.txt', 'data.txt', train_test_split=0.5, seed=42)
        
        # Check that file reading functions were called
        mock_read_tags.assert_called_once_with('tags.txt')
        mock_read_data.assert_called_once_with('data.txt')
        mock_seed.assert_called_once_with(42)
        
        # Check basic properties
        self.assertEqual(len(dataset), 4)
        self.assertIsInstance(dataset.training_set, helpers.Subset)
        self.assertIsInstance(dataset.testing_set, helpers.Subset)
        
        # Check split (50% split of 4 sentences = 2 each)
        self.assertEqual(len(dataset.training_set), 2)
        self.assertEqual(len(dataset.testing_set), 2)

    def test_dataset_iteration(self):
        """Test Dataset iteration"""
        with patch('helpers.read_tags') as mock_read_tags, \
             patch('helpers.read_data') as mock_read_data:
            
            mock_sentences = {
                'sent1': helpers.Sentence(('word1',), ('TAG1',)),
                'sent2': helpers.Sentence(('word2',), ('TAG2',))
            }
            mock_read_data.return_value = mock_sentences
            mock_read_tags.return_value = frozenset(['TAG1', 'TAG2'])
            
            dataset = helpers.Dataset('tags.txt', 'data.txt')
            
            # Test iteration
            items = list(dataset)
            self.assertEqual(len(items), 2)
            
            # Check that we can iterate over sentences
            for key, sentence in dataset:
                self.assertIn(key, mock_sentences)
                self.assertEqual(sentence, mock_sentences[key])


class TestModelVisualization(unittest.TestCase):
    """Test cases for model visualization functions"""

    @patch('helpers.mplimg.imread')
    @patch('helpers.nx.drawing.nx_pydot.to_pydot')
    @patch('helpers.nx.relabel_nodes')
    def test_model2png_basic(self, mock_relabel, mock_to_pydot, mock_imread):
        """Test basic model2png functionality"""
        # Create a mock model
        mock_model = MagicMock()
        mock_model.graph.nodes.return_value = ['node1', 'node2']
        mock_model.start = 'start'
        mock_model.end = 'end'
        
        # Mock the pydot graph
        mock_pydot_graph = MagicMock()
        mock_pydot_graph.create_png.return_value = b'fake_png_data'
        mock_to_pydot.return_value = mock_pydot_graph
        
        # Mock imread
        mock_imread.return_value = 'fake_image_array'
        
        result = helpers.model2png(mock_model)
        
        # Check that the function returns the image array
        self.assertEqual(result, 'fake_image_array')
        
        # Check that pydot graph methods were called
        mock_pydot_graph.set_rankdir.assert_called_once_with("LR")
        mock_pydot_graph.create_png.assert_called_once_with(prog='dot')

    @patch('helpers.plt.figure')
    @patch('helpers.plt.imshow')
    @patch('helpers.plt.axis')
    @patch('helpers.model2png')
    def test_show_model(self, mock_model2png, mock_axis, mock_imshow, mock_figure):
        """Test show_model function"""
        mock_model = MagicMock()
        mock_model2png.return_value = 'fake_image_array'
        
        helpers.show_model(mock_model, figsize=(10, 8))
        
        # Check that matplotlib functions were called correctly
        mock_figure.assert_called_once_with(figsize=(10, 8))
        mock_imshow.assert_called_once_with('fake_image_array')
        mock_axis.assert_called_once_with('off')
        mock_model2png.assert_called_once_with(mock_model)


if __name__ == '__main__':
    unittest.main()