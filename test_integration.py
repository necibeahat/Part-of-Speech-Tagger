"""
Integration tests for the NLP POS Tagging project

This module contains integration tests that verify the complete workflow
from data loading to model training and evaluation using the actual
Brown Corpus data files.
"""

import pytest
import os
from helpers import Dataset, read_data, read_tags


class TestDataIntegration:
    """Integration tests using actual data files"""
    
    def test_data_files_exist(self):
        """Test that required data files exist"""
        assert os.path.exists("data/brown-universal.txt"), "Brown corpus file missing"
        assert os.path.exists("data/tags-universal.txt"), "Tags file missing"
    
    def test_tags_file_content(self):
        """Test that tags file contains expected universal tags"""
        tags = read_tags("data/tags-universal.txt")
        
        # Expected universal tagset
        expected_tags = {'.', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'X'}
        
        # Remove empty strings that might come from file parsing
        tags_clean = {tag for tag in tags if tag.strip()}
        
        assert tags_clean == expected_tags, f"Expected {expected_tags}, got {tags_clean}"
    
    def test_brown_corpus_format(self):
        """Test that Brown corpus file has expected format"""
        # Read first few lines to check format
        with open("data/brown-universal.txt", 'r') as f:
            lines = [f.readline().strip() for _ in range(20)]
        
        # Should have sentence identifiers (lines without tabs)
        sentence_ids = [line for line in lines if line and '\t' not in line]
        assert len(sentence_ids) > 0, "No sentence identifiers found"
        
        # Should have word-tag pairs (lines with tabs)
        word_tag_pairs = [line for line in lines if '\t' in line]
        assert len(word_tag_pairs) > 0, "No word-tag pairs found"
        
        # Check that word-tag pairs have exactly one tab
        for pair in word_tag_pairs[:5]:  # Check first 5 pairs
            parts = pair.split('\t')
            assert len(parts) == 2, f"Invalid word-tag pair format: {pair}"
            assert parts[0].strip(), f"Empty word in pair: {pair}"
            assert parts[1].strip(), f"Empty tag in pair: {pair}"
    
    def test_dataset_creation_with_real_data(self):
        """Test creating Dataset with actual data files"""
        dataset = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=42)
        
        # Basic validation
        assert len(dataset) > 0, "Dataset is empty"
        assert len(dataset.sentences) > 1000, "Dataset too small (expected >1000 sentences)"
        
        # Check vocabulary size (should be substantial for Brown corpus)
        assert len(dataset.vocab) > 10000, f"Vocabulary too small: {len(dataset.vocab)}"
        
        # Check tagset
        expected_tags = {'.', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'X'}
        tags_in_data = {tag for tag in dataset.tagset if tag.strip()}
        assert expected_tags.issubset(tags_in_data), f"Missing expected tags: {expected_tags - tags_in_data}"
        
        # Check train/test split
        total_sentences = len(dataset.sentences)
        train_size = len(dataset.training_set)
        test_size = len(dataset.testing_set)
        
        assert train_size + test_size == total_sentences, "Train/test split doesn't add up"
        assert train_size > test_size, "Training set should be larger than test set"
        
        # Check that split is approximately 80/20
        train_ratio = train_size / total_sentences
        assert 0.75 <= train_ratio <= 0.85, f"Train ratio {train_ratio} not close to 0.8"
    
    def test_dataset_reproducibility(self):
        """Test that dataset creation is reproducible with same seed"""
        dataset1 = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=42)
        dataset2 = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=42)
        
        # Should have identical train/test splits
        assert dataset1.training_set.keys == dataset2.training_set.keys
        assert dataset1.testing_set.keys == dataset2.testing_set.keys
        
        # Should have identical vocabulary and tagsets
        assert dataset1.vocab == dataset2.vocab
        assert dataset1.tagset == dataset2.tagset
    
    def test_dataset_different_seeds(self):
        """Test that different seeds produce different splits"""
        dataset1 = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=42)
        dataset2 = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=123)
        
        # Should have different train/test splits
        assert dataset1.training_set.keys != dataset2.training_set.keys
        
        # But should have same vocabulary and tagsets (same data)
        assert dataset1.vocab == dataset2.vocab
        assert dataset1.tagset == dataset2.tagset
    
    def test_subset_functionality(self):
        """Test that Subset objects work correctly with real data"""
        dataset = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=42)
        
        training_set = dataset.training_set
        testing_set = dataset.testing_set
        
        # Test training set
        assert len(training_set) > 0
        assert training_set.N > 0  # Word count
        assert len(training_set.vocab) > 0
        assert len(training_set.tagset) > 0
        
        # Test testing set
        assert len(testing_set) > 0
        assert testing_set.N > 0
        assert len(testing_set.vocab) > 0
        assert len(testing_set.tagset) > 0
        
        # Test that subsets are proper subsets of full dataset
        assert training_set.vocab.issubset(dataset.vocab)
        assert testing_set.vocab.issubset(dataset.vocab)
        assert training_set.tagset.issubset(dataset.tagset)
        assert testing_set.tagset.issubset(dataset.tagset)
    
    def test_data_quality(self):
        """Test data quality and consistency"""
        dataset = Dataset("data/tags-universal.txt", "data/brown-universal.txt", train_test_split=0.8, seed=42)
        
        # Check for empty sentences
        empty_sentences = [key for key, sentence in dataset.sentences.items() 
                          if len(sentence.words) == 0 or len(sentence.tags) == 0]
        assert len(empty_sentences) == 0, f"Found empty sentences: {empty_sentences[:5]}"
        
        # Check for mismatched word/tag counts
        mismatched = []
        for key, sentence in list(dataset.sentences.items())[:100]:  # Check first 100
            if len(sentence.words) != len(sentence.tags):
                mismatched.append(key)
        assert len(mismatched) == 0, f"Found sentences with mismatched word/tag counts: {mismatched[:5]}"
        
        # Check for invalid tags
        valid_tags = read_tags("data/tags-universal.txt")
        valid_tags_clean = {tag.strip() for tag in valid_tags if tag.strip()}
        
        invalid_tags = set()
        for sentence in list(dataset.sentences.values())[:100]:  # Check first 100
            for tag in sentence.tags:
                if tag not in valid_tags_clean:
                    invalid_tags.add(tag)
        
        assert len(invalid_tags) == 0, f"Found invalid tags: {invalid_tags}"


class TestWorkflowIntegration:
    """Test complete workflow integration"""
    
    def test_complete_data_pipeline(self):
        """Test the complete data processing pipeline"""
        # Step 1: Load tags
        tags = read_tags("data/tags-universal.txt")
        assert len(tags) > 0
        
        # Step 2: Load data
        sentences = read_data("data/brown-universal.txt")
        assert len(sentences) > 0
        
        # Step 3: Create dataset
        dataset = Dataset("data/tags-universal.txt", "data/brown-universal.txt")
        assert len(dataset) == len(sentences)
        
        # Step 4: Access training and testing data
        training_data = dataset.training_set
        testing_data = dataset.testing_set
        
        assert len(training_data) > 0
        assert len(testing_data) > 0
        
        # Step 5: Verify data integrity throughout pipeline
        total_words_original = sum(len(s.words) for s in sentences.values())
        total_words_dataset = dataset.N
        total_words_subsets = training_data.N + testing_data.N
        
        assert total_words_original == total_words_dataset == total_words_subsets
    
    @pytest.mark.slow
    def test_large_dataset_performance(self):
        """Test performance with full dataset (marked as slow test)"""
        import time
        
        start_time = time.time()
        dataset = Dataset("data/tags-universal.txt", "data/brown-universal.txt")
        load_time = time.time() - start_time
        
        # Should load reasonably quickly (adjust threshold as needed)
        assert load_time < 30, f"Dataset loading took too long: {load_time:.2f} seconds"
        
        # Should have substantial data
        assert len(dataset) > 5000, f"Dataset smaller than expected: {len(dataset)} sentences"
        assert dataset.N > 100000, f"Word count smaller than expected: {dataset.N} words"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])