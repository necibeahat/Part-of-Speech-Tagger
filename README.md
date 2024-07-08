## Introduction
Do you remember back in school when we learned about word classes? How you tried to understand the differences between nouns, verbs, adjectives, and adverbs? These word classes are now useful when a computer tries to understand written text. They help us extract data and ask important questions, like "what" and "why," so we can derive insights. And to think, you once thought you’d never use word classes in your adult life. 

## What is *Part of Speech Tagger*
Part of speech tagging (PoS) is labelling words in a sentence according to their word classes or lexical categories, if you want it to sounds fancy, or simply their part of speech. Tagging part of speech (PoS) helps us understand unstructured text (e.g. academic literature, social media post) better, allowing us to extract information by analysing the gramatical structure of a sentence. Each word is assigned with a lexical category (e.g. verb, noun, modal), enabling us to extract data and convert unstructured text to structured format. 

PoS taggers are powerful tools. They are predominantly used in grammar and spelling checks, but their applications are broader. 

One statistical method that shows promising results in tagging new text accurately is Hidden Markov Model (HMM). This notebook implement HMM for PoS and evaluates model acuracy in comparison to tagging words based on how frequently they have been tagged with a certain word class. 

To understand how PoS works, take a look at the this sample sentence: 
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

## Why do we need it? 
Let's look at the big picture. Why do we want to know the word class of text? We don't worry about whether a word is a noun or an adjective when we speak. This is because our brains tag words automatically. So when a friend says, "It’s an interesting book," we naturally think of a book 📚, and not a holiday they might be going to. 
ß
We need to spell it out for a computer. Once we do, we can start asking important questions about our data, like "What happened?" and "How did it happen?" We can make predictions by asking, "Why did it happen?" and ultimately figure out how we can make something happen or prevent it from happening.

This is one of the methods for turning unstructured text into a structured format that serves as the foundation.

## Data
The dataset comes from the [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus) that can be downloaded from NLTK library. To keep the tags simple and avoid complication, NLKT introduced the universal tag set. I used the universal tags that are given in tags-universal.txt

## Method 
This notebook uses Hidden Markov Model (HMM) to determine the tag in a given text. I am comparing the performance of HMM model to a base line model that counts the frequency of each word in the training set to asses the tag in the test set. 

Counting the frequency of tags is simple to understand and implement, but has its limitation. What if the same word is used in different meanings? Take a look at this example:
- It’s an interesting **book**. (noun)
- We ought to **book** a holiday soon. (verb)

We don't want the word 'book' in the second sentence to be tagged a a verb just because there are more 'books' that are nouns in the corpora. 

For this reason, we use HMM model. 

__HMM__ is a probabilistic model that calculates the likelyhood of a tag and a word. The likelyhood is determined based on the transitional and emissional probabilities. 
- Transitional probability: how likely is a noun followed by a verb, verb followed by a model, and so on
- Emissional probability: how likely is for a noun to be 'medicine' (form example above), and a verb to be treat. 

## How to run it 
Check out the Jupiter notebook with name '_HiddenMarkovModelforPOS.ipynb_' 

## Library 
There are two main python libraries used in this project
- I am using the [pomegranate](https://pomegranate.readthedocs.io/en/latest/) library  that has HMM implementation. 
- NLTK: The data is downloaded from the [NLTK library](https://www.nltk.org/book/ch05.html). 

## Acknowledgement
I've completed a nanodegree in Natural Language Processing from Udacity. The tutors were amazing, and I learned a lot! This notebook uses the template I got as part of the course. The script has changed a lot since my submission, but the credit definately goes to the [Udacity team](@udacity/active-public-content) for their brilliant content. 
