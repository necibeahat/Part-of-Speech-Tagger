#!/usr/bin/env python3
"""
Test script to verify the architecture diagram has been properly added to README.md
and that the main components are accessible.
"""

import os
import sys
import unittest
from pathlib import Path

# Add the workspace to the path to import helpers
sys.path.insert(0, '/workspace')

try:
    import helpers
except ImportError as e:
    print(f"Warning: Could not import helpers module: {e}")
    helpers = None


class TestArchitectureDiagram(unittest.TestCase):
    """Test cases to verify the architecture diagram integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.readme_path = Path('/workspace/README.md')
        self.data_dir = Path('/workspace/data')
        
    def test_readme_exists(self):
        """Test that README.md file exists."""
        self.assertTrue(self.readme_path.exists(), "README.md file should exist")
        
    def test_architecture_section_exists(self):
        """Test that the Architecture section has been added to README.md."""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn('## Architecture', content, 
                     "README.md should contain an Architecture section")
        
    def test_architecture_diagram_exists(self):
        """Test that the architecture diagram is present in README.md."""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key components of the diagram
        diagram_elements = [
            'DATA LAYER',
            'CORE PROCESSING LAYER', 
            'MODEL LAYER',
            'EVALUATION & OUTPUT LAYER',
            'EXTERNAL DEPENDENCIES',
            'Brown Corpus',
            'Universal Tags',
            'Dataset Class',
            'SimpleTagger',
            'Hidden Markov Model',
            'helpers.py'
        ]
        
        for element in diagram_elements:
            self.assertIn(element, content, 
                         f"Architecture diagram should contain '{element}'")
            
    def test_component_relationships_section_exists(self):
        """Test that the Component Relationships section exists."""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn('### Component Relationships', content,
                     "README.md should contain Component Relationships section")
        self.assertIn('**Data Flow:**', content,
                     "README.md should contain Data Flow description")
        self.assertIn('**Key Interactions:**', content,
                     "README.md should contain Key Interactions description")
        
    def test_data_files_exist(self):
        """Test that the referenced data files exist."""
        tags_file = self.data_dir / 'tags-universal.txt'
        brown_file = self.data_dir / 'brown-universal.txt'
        
        self.assertTrue(tags_file.exists(), 
                       "tags-universal.txt should exist in data directory")
        self.assertTrue(brown_file.exists(), 
                       "brown-universal.txt should exist in data directory")
        
    def test_helpers_module_components(self):
        """Test that the main components mentioned in the diagram are accessible."""
        if helpers is None:
            self.skipTest("helpers module not available")
            
        # Test that key classes exist
        self.assertTrue(hasattr(helpers, 'Dataset'), 
                       "helpers module should have Dataset class")
        self.assertTrue(hasattr(helpers, 'Subset'), 
                       "helpers module should have Subset class")
        
        # Test that key functions exist
        expected_functions = [
            'read_data', 'read_tags', 'model2png', 'show_model'
        ]
        
        for func_name in expected_functions:
            self.assertTrue(hasattr(helpers, func_name),
                           f"helpers module should have {func_name} function")
            
    def test_notebook_files_exist(self):
        """Test that the notebook files mentioned in the diagram exist."""
        hmm_notebook = Path('/workspace/HiddenMarkovModelforPOS.ipynb')
        download_notebook = Path('/workspace/DownloadDataset.ipynb')
        
        self.assertTrue(hmm_notebook.exists(),
                       "HiddenMarkovModelforPOS.ipynb should exist")
        self.assertTrue(download_notebook.exists(),
                       "DownloadDataset.ipynb should exist")
        
    def test_readme_structure_maintained(self):
        """Test that the original README structure is maintained."""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check that original sections still exist
        original_sections = [
            '## Introduction',
            '## What is *Part of Speech Tagger*',
            '## Why do we need it?',
            '## Data',
            '## Method',
            '## How to run it locally',
            '## Library',
            '## Acknowledgement'
        ]
        
        for section in original_sections:
            self.assertIn(section, content,
                         f"Original section '{section}' should be preserved")
            
        # Check that Architecture section is positioned correctly
        # (after Introduction, before What is Part of Speech Tagger)
        intro_pos = content.find('## Introduction')
        arch_pos = content.find('## Architecture')
        pos_tagger_pos = content.find('## What is *Part of Speech Tagger*')
        
        self.assertGreater(arch_pos, intro_pos,
                          "Architecture section should come after Introduction")
        self.assertLess(arch_pos, pos_tagger_pos,
                       "Architecture section should come before POS Tagger explanation")


def run_tests():
    """Run all tests and return the result."""
    unittest.main(verbosity=2, exit=False)


if __name__ == '__main__':
    print("Testing Architecture Diagram Integration...")
    print("=" * 50)
    run_tests()