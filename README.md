## Introduction
Do you remember back in school when we learned about word classes? How you tried to understand the differences between nouns, verbs, adjectives, and adverbs? These word classes are now useful when a computer tries to understand written text. They help us extract data and ask important questions, like "what" and "why," so we can derive insights. And to think, you once thought you’d never use word classes in your adult life. 

## What is *Part of Speech Tagger*
Part of speech tagging (PoS) is labelling words in a sentence according to their word classes or lexical categories, if you want it to sounds fancy, or simply their part of speech. Tagging part of speech (PoS) helps us understand unstructured text (e.g. academic literature, social media post) better, allowing us to extract information by analysing the gramatical structure of a sentence. Each word is assigned with a lexical category (e.g. verb, noun, modal), enabling us to extract data and convert unstructured text to structured format. 

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

PoS taggers are powerful tools. By understanding the gramatical structure of a text, we can improve the search relevance as we will take into account the context of queries. In question and answering systems, the gramatical structure of the question can give us a better extraction of answer from the knowledge base. 

One statistical method that shows promising results in tagging new text accurately is Hidden Markov Model (HMM). This notebook implement HMM for PoS and evaluates model acuracy in comparison to tagging words based on how frequently they have been tagged with a certain word class. 

## Why do we need it? 
Let's look at the big picture. Why do we want to know the word class of text? We don't worry about whether a word is a noun or an adjective when we speak. This is because our brains tag words automatically. So when a friend says, "It’s an interesting book," we naturally think of a book 📚, and not a holiday they might be going to. 

We need to spell it out for a computer. Once we do, we can start asking important questions about our data, like "What happened?" and "How did it happen?" We can make predictions by asking, "Why did it happen?" and ultimately figure out how we can make something happen or prevent it from happening.

This is one of the methods for turning unstructured text into a structured format that serves as the foundation.

## Data
The dataset comes from the [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus) that can be downloaded from NLTK library. To keep the tags simple and avoid complication, NLKT introduced the universal tag set. I used the universal tags that are given in tags-universal.txt

## Method 
This notebook uses Hidden Markov Model (HMM) to determine the tag in a given text. I am comparing the performance of HMM model to a base line model that counts the frequency of each word in the training set to asses the tag in the test set. 

Counting the frequency of tags is simple to understand and implement, but has its limitation. What if the same word is used in different meanings? Take a look at this example:
- It’s an interesting **book**. (noun)
- We ought to **book** a holiday soon. (verb)

We don't want the word 'book' in the second sentence to be tagged as a noun, even thought it should be verb, just because there are more 'books' that are nouns in the corpora. 

For this reason, we use HMM model. 

__HMM__ is a probabilistic model that calculates the likelihood of a tag and a word. The likelihood is determined based on the transitional and emissional probabilities. 
- Transitional probability: how likely is a noun followed by a verb, verb followed by a model, and so on
- Emissional probability: how likely is for a noun to be 'medicine' (form example above), and a verb to be treat. 

## How to run it locally

### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download NLTK data: `python -c "import nltk; nltk.download('brown'); nltk.download('universal_tagset')"`
4. Run the Jupyter notebook: `jupyter notebook HiddenMarkovModelforPOS.ipynb`

### Using Make Commands
This project includes a Makefile for convenient development tasks:

```bash
# Install dependencies and set up environment
make install

# Run all tests
make test

# Format code and run quality checks
make all

# Start Jupyter notebook server
make notebook

# See all available commands
make help
```

### Development Setup
For development work:
```bash
# Set up development environment with pre-commit hooks
make dev-setup

# Run tests with coverage
make test-coverage

# Check code formatting and security
make format-check lint security
```

## GitHub Actions CI/CD

This project includes comprehensive GitHub Actions workflows for:

- **Continuous Integration**: Automated testing across multiple Python versions and operating systems
- **Code Quality**: Automated linting, formatting checks, and security scanning
- **Documentation**: Automatic documentation building and deployment
- **Release Management**: Automated package publishing and Docker image building

### Workflow Status
The following workflows run automatically on push and pull requests:

- ✅ **CI Pipeline**: Tests, linting, notebook validation, data integrity checks
- 🔒 **Security Scanning**: Dependency vulnerability scanning, CodeQL analysis
- 📚 **Documentation**: API docs generation, README validation
- 🚀 **Release**: Automated releases on version tags

For detailed information about the GitHub Actions setup, see [GITHUB_ACTIONS_DOCUMENTATION.md](GITHUB_ACTIONS_DOCUMENTATION.md).

## Testing

The project includes comprehensive test coverage:

```bash
# Run unit tests
make test-unit

# Run integration tests with real data
make test-integration

# Run all tests with coverage report
make test-coverage
```

Test files:
- `test_helpers.py`: Unit tests for helper functions
- `test_integration.py`: Integration tests with actual Brown Corpus data

## Library 
The main Python libraries used in this project:
- [pomegranate](https://pomegranate.readthedocs.io/en/latest/): HMM implementation
- [NLTK](https://www.nltk.org/book/ch05.html): Natural language processing and Brown Corpus data
- [matplotlib](https://matplotlib.org/): Data visualization
- [pandas](https://pandas.pydata.org/): Data manipulation
- [numpy](https://numpy.org/): Numerical computing

## Project Structure
```
├── .github/workflows/          # GitHub Actions CI/CD workflows
├── data/                       # Brown Corpus and universal tags data
├── helpers.py                  # Core utility functions
├── test_helpers.py            # Unit tests
├── test_integration.py        # Integration tests
├── HiddenMarkovModelforPOS.ipynb  # Main implementation notebook
├── DownloadDataset.ipynb      # Data download notebook
├── requirements.txt           # Python dependencies
├── Makefile                   # Development commands
└── GITHUB_ACTIONS_DOCUMENTATION.md  # CI/CD documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Run quality checks: `make all`
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature/new-feature`
7. Create a Pull Request

The GitHub Actions workflows will automatically run tests and quality checks on your pull request.

## Acknowledgement
I've completed a nanodegree in Natural Language Processing from Udacity. The tutors were amazing, and I learned a lot! This notebook uses the template I got as part of the course. The script has changed a lot since my submission, but the credit definitely goes to the [Udacity team](@udacity/active-public-content) for their brilliant content. 
