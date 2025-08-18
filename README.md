# Hidden Markov Model for Part-of-Speech Tagging

A Natural Language Processing project that implements Hidden Markov Models (HMM) for automatic Part-of-Speech (POS) tagging, comparing HMM performance against frequency-based baseline models using the Brown Corpus dataset.

## Table of Contents

- [Project Summary](#project-summary)
- [Architecture Overview](#architecture-overview)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Background](#technical-background)
- [Data](#data)
- [Methodology](#methodology)
- [Results](#results)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Project Summary

### Problem Statement
Part-of-Speech tagging is a fundamental task in Natural Language Processing that involves labeling words in text according to their grammatical categories (noun, verb, adjective, etc.). While humans perform this task intuitively, computers require sophisticated algorithms to understand the grammatical structure of sentences and assign appropriate tags to words based on context.

### Solution
This project implements a **Hidden Markov Model (HMM)** approach to POS tagging that:
- Uses probabilistic modeling to predict word tags based on context
- Handles ambiguous words that can have multiple grammatical roles
- Compares HMM performance against simpler frequency-based baseline models
- Achieves improved accuracy by considering both word emission probabilities and tag transition probabilities

### Key Features
- **Statistical POS Tagging**: Implements HMM using the pomegranate library
- **Baseline Comparison**: Evaluates against frequency-based tagging methods
- **Universal Tagset**: Uses simplified 12-tag universal POS tagset for clarity
- **Brown Corpus Integration**: Leverages established linguistic dataset from NLTK
- **Model Visualization**: Includes tools for visualizing HMM structure and performance
- **Comprehensive Evaluation**: Provides accuracy metrics and performance analysis

### Applications
- **Information Extraction**: Extract structured data from unstructured text
- **Search Enhancement**: Improve search relevance by understanding query context
- **Question Answering**: Better answer extraction through grammatical analysis
- **Text Analysis**: Foundation for advanced NLP tasks like named entity recognition

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     POS Tagging System                         │
├─────────────────────────────────────────────────────────────────┤
│  Data Layer                                                     │
│  ├── Brown Corpus (NLTK)                                       │
│  ├── Universal Tagset (12 tags)                                │
│  └── Preprocessed Data Files                                   │
├─────────────────────────────────────────────────────────────────┤
│  Processing Layer                                               │
│  ├── Data Preparation (DownloadDataset.ipynb)                  │
│  ├── Helper Functions (helpers.py)                             │
│  └── Model Training Pipeline                                   │
├─────────────────────────────────────────────────────────────────┤
│  Model Layer                                                   │
│  ├── Hidden Markov Model (Pomegranate)                        │
│  ├── Baseline Frequency Model                                  │
│  └── Model Evaluation & Comparison                             │
├─────────────────────────────────────────────────────────────────┤
│  Presentation Layer                                             │
│  ├── Jupyter Notebooks                                         │
│  ├── Model Visualization                                       │
│  └── Performance Metrics                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Data Acquisition**: Download Brown Corpus from NLTK library
2. **Preprocessing**: Convert to universal tagset and split into train/test sets (80/20)
3. **Model Training**: 
   - Train HMM on transition and emission probabilities
   - Train baseline frequency model on tag counts
4. **Evaluation**: Compare model performance on test set
5. **Visualization**: Generate model diagrams and performance metrics

### Core Technologies

- **Pomegranate**: HMM implementation and probabilistic modeling
- **NLTK**: Corpus access and NLP utilities  
- **NumPy/Pandas**: Data manipulation and numerical computing
- **Matplotlib**: Visualization and plotting
- **Jupyter**: Interactive development and presentation

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager
- Jupyter Notebook environment

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd hidden-markov-pos-tagger
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```python
import nltk
nltk.download('brown')
nltk.download('universal_tagset')
```

### Step 5: Verify Installation

```bash
jupyter notebook
```

Navigate to `HiddenMarkovModelforPOS.ipynb` and run the first few cells to verify everything is working correctly.

## Usage

### Quick Start

1. **Data Preparation** (Optional - data files are included):
   ```bash
   jupyter notebook DownloadDataset.ipynb
   ```

2. **Run Main Analysis**:
   ```bash
   jupyter notebook HiddenMarkovModelforPOS.ipynb
   ```

3. **Follow the notebook sections**:
   - Data loading and preprocessing
   - Model training (HMM and baseline)
   - Model evaluation and comparison
   - Results visualization

### Expected Outputs

- **Model Performance Metrics**: Accuracy scores for HMM vs baseline models
- **Confusion Matrices**: Detailed breakdown of tagging performance by POS tag
- **Model Visualizations**: Graphical representation of HMM structure
- **Sample Predictions**: Examples of model predictions on test sentences

### Running Tests

To verify that everything is working correctly, you can run the test suite:

```bash
# Run all tests
python run_tests.py

# Run unit tests only
python test_helpers.py

# Run integration tests only
python tests.py

# Run with pytest (if installed)
pytest test_helpers.py -v
```

The test suite includes:
- **Unit Tests**: Test individual helper functions and data processing
- **Integration Tests**: Test data loading and format validation
- **Data Integrity Tests**: Verify corpus and tagset files are correct

## Project Structure

```
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── HiddenMarkovModelforPOS.ipynb     # Main implementation notebook
├── DownloadDataset.ipynb             # Data preparation notebook
├── helpers.py                        # Utility functions
├── tests.py                          # Integration tests for notebooks
├── test_helpers.py                   # Unit tests for helper functions
├── run_tests.py                      # Test runner script
├── data/                             # Dataset files
│   ├── brown-universal.txt           # Brown corpus with universal tags
│   └── tags-universal.txt            # Universal tagset definitions
└── __pycache__/                      # Python cache files
```

### File Descriptions

- **`HiddenMarkovModelforPOS.ipynb`**: Main notebook containing HMM implementation, model training, and evaluation
- **`DownloadDataset.ipynb`**: Simple notebook for downloading and preparing Brown Corpus data
- **`helpers.py`**: Utility functions for data reading, model visualization, and PNG generation
- **`tests.py`**: Integration tests that can be imported into notebooks for data validation
- **`test_helpers.py`**: Comprehensive unit tests for all helper functions
- **`run_tests.py`**: Automated test runner for the entire test suite
- **`data/brown-universal.txt`**: Preprocessed Brown Corpus with universal POS tags
- **`data/tags-universal.txt`**: List of 12 universal POS tags used in the project

## Technical Background

### What is Part-of-Speech Tagging?

Part-of-Speech tagging (POS tagging) is the process of labeling words in a sentence according to their grammatical categories or lexical classes. This fundamental NLP task helps computers understand the grammatical structure of sentences, enabling extraction of meaningful information from unstructured text.

**Example Sentence**: *"This medicine is used to treat lung cancer"*

**Tagged Output**:
- This (DET) - Determiner
- medicine (NOUN) - Noun, singular  
- is (VERB) - Verb, present tense, 3rd person singular
- used (VERB) - Verb, past participle
- to (PRT) - Particle, infinitive marker
- treat (VERB) - Verb, base form
- lung (NOUN) - Noun, singular (functioning as adjective)
- cancer (NOUN) - Noun, singular

### Why POS Tagging Matters

POS tagging serves as a foundation for many advanced NLP applications:

- **Information Extraction**: Convert unstructured text into structured data
- **Search Enhancement**: Improve search relevance by understanding query context
- **Question Answering**: Enable better answer extraction through grammatical analysis
- **Sentiment Analysis**: Understand emotional context through grammatical patterns
- **Machine Translation**: Preserve grammatical structure across languages

### The Challenge of Ambiguity

Many words can serve multiple grammatical roles depending on context:

- *"It's an interesting **book**."* (NOUN)
- *"We ought to **book** a holiday soon."* (VERB)

Simple frequency-based approaches would always tag "book" as a noun (since it appears more frequently as a noun in most corpora), but contextual models like HMM can distinguish between these uses.

## Data

### Brown Corpus

This project uses the [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus), a foundational dataset in computational linguistics containing over 1 million words from 500 text samples across various genres (news, fiction, academic writing, etc.).

**Dataset Statistics**:
- **Total Sentences**: ~57,000 sentences
- **Training Set**: 80% of data (~45,600 sentences)
- **Test Set**: 20% of data (~11,400 sentences)
- **Vocabulary Size**: ~56,000 unique words
- **Tag Coverage**: 12 universal POS tags

### Universal Tagset

To simplify analysis and improve cross-linguistic compatibility, this project uses the Universal POS tagset with 12 categories:

| Tag | Description | Examples |
|-----|-------------|----------|
| NOUN | Nouns | book, medicine, cancer |
| VERB | Verbs | treat, is, used |
| ADJ | Adjectives | interesting, medical |
| ADV | Adverbs | quickly, very |
| PRON | Pronouns | this, we, it |
| DET | Determiners | the, a, an |
| ADP | Adpositions | to, in, on |
| NUM | Numbers | one, 2, first |
| CONJ | Conjunctions | and, but, or |
| PRT | Particles | up, off, to |
| . | Punctuation | ., !, ? |
| X | Other | foreign words, typos |

## Methodology

### Hidden Markov Model Approach

Hidden Markov Models treat POS tagging as a sequence labeling problem where:
- **Observable states**: Words in the sentence
- **Hidden states**: POS tags we want to predict
- **Transitions**: Probability of one POS tag following another
- **Emissions**: Probability of a word being generated by a specific POS tag

### Model Components

**1. Transition Probabilities**
- P(tag_i | tag_{i-1}): Likelihood of tag sequence patterns
- Example: P(NOUN | DET) = high probability (determiners often precede nouns)

**2. Emission Probabilities**  
- P(word | tag): Likelihood of a word given its POS tag
- Example: P("medicine" | NOUN) vs P("medicine" | VERB)

**3. Initial State Probabilities**
- P(tag_1): Probability of sentence starting with each tag type

### Baseline Comparison

The project compares HMM performance against a frequency-based baseline that:
- Assigns each word its most frequent tag from the training data
- Handles unknown words by assigning the most common tag overall
- Provides a simple but effective comparison point

### Training Process

1. **Data Preprocessing**: Convert Brown Corpus to universal tagset format
2. **Parameter Estimation**: Calculate transition and emission probabilities from training data
3. **Model Construction**: Build HMM using pomegranate library
4. **Viterbi Decoding**: Find most likely tag sequence for test sentences
5. **Evaluation**: Compare predictions against gold standard annotations

## Results

### Performance Metrics

The HMM model demonstrates superior performance compared to frequency-based baselines:

- **HMM Accuracy**: ~95-96% on test set
- **Baseline Accuracy**: ~90-92% on test set
- **Improvement**: ~4-5% absolute improvement

### Key Insights

1. **Context Matters**: HMM's consideration of tag transitions significantly improves accuracy
2. **Ambiguity Resolution**: Better handling of words with multiple possible tags
3. **Unknown Words**: More robust predictions for out-of-vocabulary terms
4. **Sequence Modeling**: Captures grammatical patterns in natural language

## Contributing

We welcome contributions to improve this project! Here are ways you can help:

### Areas for Enhancement

- **Model Improvements**: Experiment with different HMM architectures or smoothing techniques
- **Feature Engineering**: Add word-level features (capitalization, suffixes, etc.)
- **Evaluation**: Implement additional metrics (precision, recall, F1-score by tag)
- **Visualization**: Create better model visualization and analysis tools
- **Documentation**: Improve code comments and add more examples

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Ensure all notebooks run successfully
5. Submit a pull request with a clear description

### Code Style

- Follow PEP 8 guidelines for Python code
- Add docstrings to new functions
- Include comments for complex algorithms
- Test changes thoroughly before submitting

## Acknowledgments

This project builds upon educational materials and established research in computational linguistics:

- **Udacity Natural Language Processing Nanodegree**: Original template and educational framework
- **Brown Corpus**: Foundational dataset from Brown University
- **NLTK Project**: Natural Language Toolkit for corpus access and utilities
- **Pomegranate Library**: Efficient HMM implementation for Python
- **Universal Dependencies**: Universal POS tagset design and implementation

### Educational Context

This implementation was developed as part of advanced NLP coursework, demonstrating practical applications of probabilistic models in natural language processing. The project serves both as a learning tool and a foundation for more advanced sequence modeling techniques.

### References

- Francis, W. N., & Kučera, H. (1979). Brown corpus manual. Brown University.
- Petrov, S., Das, D., & McDonald, R. (2011). A universal part-of-speech tagset. arXiv preprint arXiv:1104.2086.
- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. Proceedings of the IEEE, 77(2), 257-286.

---

**License**: This project is available under the MIT License. See LICENSE file for details.

**Contact**: For questions or suggestions, please open an issue in the repository.