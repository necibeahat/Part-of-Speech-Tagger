# Part-of-Speech Tagger

![Documentation](https://github.com/necibeahat/Part-of-Speech-Tagger/workflows/Validate%20README%20and%20Documentation/badge.svg)
![Python CI](https://github.com/necibeahat/Part-of-Speech-Tagger/workflows/Python%20CI/badge.svg)
![Security Scan](https://github.com/necibeahat/Part-of-Speech-Tagger/workflows/Security%20Scan/badge.svg)

## Introduction

Do you remember back in school when we learned about word classes? How you tried to understand the differences
between nouns, verbs, adjectives, and adverbs? These word classes are now useful when a computer tries to
understand written text. They help us extract data and ask important questions, like "what" and "why," so we
can derive insights. And to think, you once thought you'd never use word classes in your adult life.

## What is *Part of Speech Tagger*

Part of speech tagging (PoS) is labelling words in a sentence according to their word classes or lexical
categories, if you want it to sounds fancy, or simply their part of speech. Tagging part of speech (PoS) helps
us understand unstructured text (e.g. academic literature, social media post) better, allowing us to extract
information by analysing the gramatical structure of a sentence. Each word is assigned with a lexical category
(e.g. verb, noun, modal), enabling us to extract data and convert unstructured text to structured format.

To understand part of speech taggings, take a look at the this sample sentence:
"This medicine is used to treat lung cancer"

Let's assign tags to each word:

- This (DT) - Determiner
- medicine (NN) - Noun, singular
- is (VBZ) - Verb, present tense, 3rd person singular
- used (VBN) - Verb, past participle
- to (TO) - Particle, infinitive marker
- treat (VB) - Verb, base form
- lung (NN) - Noun, singular (functioning as an adjective here, known as a noun adjunct)
- cancer (NN) - Noun, singular

PoS taggers are powerful tools. By understanding the gramatical structure of a text, we can improve the search
relevance as we will take into account the context of queries. In question and answering systems, the
gramatical structure of the question can give us a better extraction of answer from the knowledge base.

One statistical method that shows promising results in tagging new text accurately is Hidden Markov Model (HMM).
This notebook implement HMM for PoS and evaluates model acuracy in comparison to tagging words based on how
frequently they have been tagged with a certain word class.

## Why do we need it?

Let's look at the big picture. Why do we want to know the word class of text? We don't worry about whether a
word is a noun or an adjective when we speak. This is because our brains tag words automatically. So when a
friend says, "It's an interesting book," we naturally think of a book 📚, and not a holiday they might be
going to.

We need to spell it out for a computer. Once we do, we can start asking important questions about our data,
like "What happened?" and "How did it happen?" We can make predictions by asking, "Why did it happen?" and
ultimately figure out how we can make something happen or prevent it from happening.

This is one of the methods for turning unstructured text into a structured format that serves as the foundation.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Quick Installation

1. Clone the repository:

```bash
git clone https://github.com/necibeahat/Part-of-Speech-Tagger.git
cd Part-of-Speech-Tagger
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download required NLTK data:

```bash
python -c "import nltk; nltk.download('brown'); nltk.download('universal_tagset')"
```

### Development Installation

For development work, install additional tools:

```bash
# Install development dependencies
make install-dev

# Or manually:
pip install pytest pytest-cov flake8 black isort jupyter notebook
```

## Usage

### Running the Jupyter Notebook

The main analysis is contained in the Jupyter notebook:

```bash
# Start Jupyter notebook server
jupyter notebook

# Open HiddenMarkovModelforPOS.ipynb in your browser
```

### Using the Helper Functions

The project provides utility functions for working with POS tagging data:

```python
from helpers import read_data, read_tags, Dataset

# Load the universal tagset
tagset = read_tags('data/tags-universal.txt')

# Load the Brown corpus data
sentences = read_data('data/brown-universal.txt')

# Create a dataset with train/test split
dataset = Dataset('data/tags-universal.txt', 'data/brown-universal.txt', train_test_split=0.8)

# Access training and testing data
training_data = dataset.training_set
testing_data = dataset.testing_set
```

### Command Line Usage

Use the provided Makefile for common tasks:

```bash
# Run all tests
make test

# Check code quality
make lint

# Format code
make format

# Run all checks (format, lint, test)
make check

# Clean temporary files
make clean
```

## Data

The dataset comes from the [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus) that can be downloaded
from NLTK library. To keep the tags simple and avoid complication, NLKT introduced the universal tag set.
I used the universal tags that are given in tags-universal.txt

## Method

This notebook uses Hidden Markov Model (HMM) to determine the tag in a given text. I am comparing the
performance of HMM model to a base line model that counts the frequency of each word in the training set to
asses the tag in the test set.

Counting the frequency of tags is simple to understand and implement, but has its limitation. What if the same
word is used in different meanings? Take a look at this example:

- It's an interesting **book**. (noun)
- We ought to **book** a holiday soon. (verb)

We don't want the word 'book' in the second sentence to be tagged as a noun, even thought it should be verb,
just because there are more 'books' that are nouns in the corpora.

For this reason, we use HMM model.

**HMM** is a probabilistic model that calculates the likelihood of a tag and a word. The likelihood is
determined based on the transitional and emissional probabilities.

- Transitional probability: how likely is a noun followed by a verb, verb followed by a model, and so on
- Emissional probability: how likely is for a noun to be 'medicine' (form example above), and a verb to be treat.

### Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download NLTK data: `make download-data`
4. Run the notebook: `jupyter notebook HiddenMarkovModelforPOS.ipynb`

### Using Make Commands

The project includes a Makefile with convenient commands:

- `make install` - Install production dependencies
- `make install-dev` - Install development dependencies
- `make test` - Run tests with coverage
- `make lint` - Run code linting
- `make format` - Format code with black and isort
- `make check` - Run all quality checks
- `make clean` - Clean temporary files
- `make run-notebook` - Start Jupyter notebook server
- `make docs-check` - Check documentation quality

### Development Setup

For contributors and developers:

```bash
# Set up development environment
make setup-dev

# Run all checks before committing
make check

# Simulate CI pipeline locally
make simulate-ci
```

### Workflow Status

The project uses GitHub Actions for continuous integration:

- **Documentation Validation**: Checks README formatting and completeness
- **Python CI**: Tests code across multiple Python versions
- **Security Scanning**: Checks for vulnerabilities in dependencies
- **Release Management**: Automates release creation

## Testing

The project includes comprehensive tests:

- `test_helpers.py`: Unit tests for helper functions and classes

Run tests with:

```bash
make test
# or
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Library

There are two main python libraries used in this project:

- I am using the [pomegranate](https://pomegranate.readthedocs.io/en/latest/) library that has HMM
  implementation.
- NLTK: The data is downloaded from the [NLTK library](https://www.nltk.org/book/ch05.html).

Additional libraries:

- [matplotlib](https://matplotlib.org/) - For plotting and visualization
- [pandas](https://pandas.pydata.org/) - For data manipulation
- [numpy](https://numpy.org/) - For numerical computations

## Project Structure

```text
Part-of-Speech-Tagger/
├── .github/
│   └── workflows/          # GitHub Actions workflows
│       ├── documentation.yml
│       ├── python-ci.yml
│       ├── security.yml
│       └── release.yml
├── data/
│   ├── brown-universal.txt # Brown corpus data
│   └── tags-universal.txt  # Universal POS tags
├── tests/
│   ├── __init__.py
│   └── test_helpers.py     # Unit tests
├── helpers.py              # Utility functions
├── requirements.txt        # Python dependencies
├── Makefile               # Development commands
├── pyproject.toml         # Tool configurations
├── .flake8               # Linting configuration
├── .markdownlint.json    # Markdown linting rules
├── .markdown-link-check.json # Link checking config
├── HiddenMarkovModelforPOS.ipynb # Main analysis notebook
├── DownloadDataset.ipynb # Data preparation notebook
├── GITHUB_ACTIONS_DOCUMENTATION.md # Workflow documentation
└── README.md             # This file
```

## Acknowledgement

I've completed a nanodegree in Natural Language Processing from Udacity. The tutors were amazing, and I learned
a lot! This notebook uses the template I got as part of the course. The script has changed a lot since my
submission, but the credit definately goes to the Udacity team for their brilliant content.