## What is Part of Speech Tagger
Tagging part of speech (PoS) helps us understand unstructured text better and gives us the ability to extract information by looking at the gramatical structure of a sentence. Each word is assigned with a grammatical tag (e.g. verb, noun, modal), allowing us to understand the words based on there they are located in a sentence. This also allows to distinguish words that are the same, but have different meaning (for example 'I love Spot' vs 'I spot a bird'). 

PoS taggers are powerful. They are predominantly used in grammar and spelling checks, however their applications are wider. 

To understand how PoS word, take a look at the this sample sentence: 
 "This medicine is used to treat lung cancer"

 Let's assign tags to each word: 
    This (DT) - Determiner
    medicine (NN) - Noun, singular
    is (VBZ) - Verb, present tense, 3rd person singular
    used (VBN) - Verb, past participle
    to (TO) - Particle, infinitive marker
    treat (VB) - Verb, base form
    lung (NN) - Noun, singular (functioning as an adjective here, known as a noun adjunct)
    cancer (NN) - Noun, singular

## How to Run it 
Check out the Jupiter notebook with name '_HiddenMarkovModelforPOS.ipynb_'

## Data
The dataset comes from the [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus) that can be downloaded from NLTK library. The tags are the universal tags given in tags-universal.txt file. 

## Method 
This notebook uses Hidden Markov Model (HMM) to determine the tag in a given text. I am comparing the performance of HMM model to a base line model that simply counts the frequency of each word in the training set to asses the tag in the test set. 

Hidden Markov Model (HMM) is a probabilistic model that calculates the likelyhood of a tag and a word. The likelyhood is determined based on the transitional and emissional probabilities. 
    Transitional probability: how likely is a noun followed by a verb, verb followed by a model, and so on
    Emissional probability: how likely is for a noun to be 'medicine' (form example above), and a verb to be treat. 

## Library 
I am using the [pomegranate](https://pomegranate.readthedocs.io/en/latest/) library  that has HMM implementation.  

This site was built using [GitHub Pages](https://pages.github.com/).
