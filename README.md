# Word and Phrase Frequency Analysis

## Introduction

Analysis of word frequencies and patterns in quiz questions via Python from scratch, to answer the following questions.

### The Problem

Provided with a UTF-8 encoded `.json` file containing data about quiz questions presented to students (data includes the question itself and the percent of students that got it correct), what words or phrases appear more frequently in questions that students tend to do poorly on, and what appear more frequently in questions that students do well on? 

If you get different results using different methods you may include any that you find interesting in your response.

Consider how many appearances of a word there needs to be in order to say something about it. There may be words that should be excluded or sanitized.

## Getting Started

### Prerequisites

The only dependences that this solution has are:

* Python 3
* the original `.json` file being formatted as such:

```
[
	{"text": "Which statement BEST supports Obama's goal for the minimum wage?", "percent_correct": 0.6551724137931034}, 
	{"text": "Read the sentence from the passage. <blockquote>Air Force One will be back in the skies on Friday, as Obama returns to his old neighborhood in Chicago to talk more about his proposals to help middle and working class families.</blockquote> How does Obama plan to help the middle- and working-class families? ", "percent_correct": 0.5689655172413793}, 
	{"text": "What can we conclude Obama hoped to gain by inviting Gabby Giffords to his State of the Union address?", "percent_correct": 0.6551724137931034}, 
	{"text": "Read this sentence from the passage. <blockquote>\"Every dollar we invest in high-quality early education can save more than seven dollars later on \u2013 boosting graduation rates, reducing teen pregnancy, reducing violent crime.\"</blockquote> What can we conclude is the BEST reason Obama makes this claim? ", "percent_correct": 0.5862068965517241},
	...
]
```

* a list of stop words. `stop_words_nltk.txt` was sourced from [a Gist for English stopwords from NLTK](https://gist.github.com/sebleier/554280). It has been manually edited by me to be less restrictive. `stop_words.txt` was sourced from [Rank.nl's English stop words list](https://www.ranks.nl/stopwords). I've included both for reference. The solution uses my own edited list of stop words, manually picked after running the program to get some results. It is named `stop_words_short.txt`.

### Installing

Clone and `cd` into the directory via the terminal.

```
git clone https://github.com/MiHHuynh/word-frequency-analysis.git
cd Quiz_Questions_Analysis
```

Files must be in this structure:

```
.
├── README.md
├── quiz_question_analysis.py
├── quiz_questions.json
├── results.txt
├── stop_words.txt
└── stop_words_nltk.txt
```

Run from your terminal:

```
python3 quiz_questions_analysis.py
```

There will be an approximately 55 second stall (more on this later, under the discussion of time complexity and drawbacks) before your terminal is free again. The program will not output anything to the console. Rather, it will write to a file named `results.txt` which should exist in the same directory.

A sampling of the data written to the file:

```
{
    "article": {
        "freq_below_cutoff": 0.011038565113561303,
        "freq_above_cutoff": 0.009921660700937503,
        "ratio_above_vs_below": 0.8988179712550103,
        "count_below_cutoff": 1738,
        "count_above_cutoff": 3013
    },
    "which": {
        "freq_below_cutoff": 0.006344951984147147,
        "freq_above_cutoff": 0.00604915058334623,
        "ratio_above_vs_below": 0.9533800410877851,
        "count_below_cutoff": 999,
        "count_above_cutoff": 1837
    },
    "select": {
        "freq_below_cutoff": 0.0061544128855241095,
        "freq_above_cutoff": 0.0049163755149351784,
        "ratio_above_vs_below": 0.7988374531223055,
        "count_below_cutoff": 969,
        "count_above_cutoff": 1493
    },
    "following": {
        "freq_below_cutoff": 0.0055954981962298665,
        "freq_above_cutoff": 0.005746199111561879,
        "ratio_above_vs_below": 1.0269325286233766,
        "count_below_cutoff": 881,
        "count_above_cutoff": 1745
    },
    "paragraph": {
        "freq_below_cutoff": 0.005220771302271226,
        "freq_above_cutoff": 0.003520164384102951,
        "ratio_above_vs_below": 0.674261364900537,
        "count_below_cutoff": 822,
        "count_above_cutoff": 1069
    },
    "sentence": {
        "freq_below_cutoff": 0.0046809105228392866,
        "freq_above_cutoff": 0.0053115296085669405,
        "ratio_above_vs_below": 1.1347214570008788,
        "count_below_cutoff": 737,
        "count_above_cutoff": 1613
    },
    "what": {
        "freq_below_cutoff": 0.0044078044814796,
        "freq_above_cutoff": 0.006447597627758258,
        "ratio_above_vs_below": 1.462768517716545,
        "count_below_cutoff": 694,
        "count_above_cutoff": 1958
    },
    ...
}

```
The rest of the results can be viewed from the `results.txt` file.

## Solution

### Approach

In order to comment on particular words or phrases that showed up more in certain questions, I needed to compare the frequency of specific terms in questions with a failing percentage and questions of a passing percentage.

Originally, I thought I could find words that were specific to each category to see if there were some kind of pattern there. This approach turned out to be restrictive, as finding terms and phrases that existed in only one category and not the other removed the majority of words, leaving only content-specific terms that did not give me much insight.

What I wanted to do:

* Gather significant terms for *each* question (remove "meaningless" words, or words that don't hold much value, such as "a," "the," "I," etc., also known as stopwords.
* Gather N-grams, or batches of N words that occur frequently together, for *each question*. I gathered 2-grams and 3-grams, as these are costly in terms of time complexity.
* Consolidate all of the significant terms across all questions in that percentile.
* Create a dict initialized to zero for each one (to be used later to count) of significant terms and phrases for failing questions, and another for passing questions.
* Tally up all terms for each percentile.
* Compare frequencies of shared terms in each percentile.

### Things to Consider

#### How do we determine which words to exclude (words without much meaning nor significance: stop words)?

In both of the stop word lists I referenced, question words (e.g. "who," "what," "when," etc.) were listed in both. In other texts, perhaps these words may not hold much meaning nor significance, but because of the particular context of the text we're analyzing here (questions), I manually went in and removed those from the stop words.

#### How do we capture significant phrases alongside individual words?

Here, I had to think about n-grams: words that frequently occur in a sequence of n words (e.g. "red wine," "President Obama"). I thought to gather and include 2-grams and 3-grams.


* Determining importance of a word or phrase (TF-IDF)
* Are there other subtle things that can be valuable for the analysis but will be lost through the processing, such as the length of questions?

### Time Complexity?

Where is the bottleneck? Technical debt? remove infinites, remove stop words, remove html words, remove stuff that aren't significant

O(n*m) to get all words, with n being average length of a single question and m being the number of questions

O((n-K) * m) to get all n-grams, where n is average length of single question, K is n in n-grams, and m is number of questions

many more linear operations to go through, build up frequency counter

O(nlogn) to sort the ordered dict


## Analysis

I tried several approaches in an attempt to find the best way to display data for gathering insight.

words that only appear in one set vs. another

number of counts in one set compared to in the other set

% frequency of the words (so number of occurrences of particular word divided by total number of words for that set) comparison



## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Built With

* Python 3.6.2

## Acknowledgments

* List of stop words from [a Gist for English stopwords from NLTK](https://gist.github.com/sebleier/554280)
* List of stop words from from [Rank.nl's English stop words list](https://www.ranks.nl/stopwords)