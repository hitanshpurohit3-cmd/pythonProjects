# Word Frequency Counter

A text analysis tool that finds the most common meaningful words in any passage.
## Features
-Cleans and tokenizes raw text input
-Filters common stopwords (the, a, is, etc.)
-Ranks words by freuqency 
-Easily extendable to accept file or user input

## Concept used
-Dictionary frequency counting with .get()
-Sets for 0(1) stopword lookup
-sorted() with lambda key functions
-enumerate() for ranked output
-string cleaning and tokenization

## How to run 
python word_counter.py

##Extension Ideas
-Accept a .txt file as input
-Export results to CSV
-Add more languages stopwords