# Word and Phrase Frequency Analysis

## Introduction

Analysis of word frequencies and patterns in quiz questions via Python, to answer the following questions.

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

There will be an approximately 1 minute (more on this later, under the discussion of time complexity and drawbacks) before your terminal is free again. The program will not output anything to the console. Rather, it will write to three different files:

* `results_sorted_by_diff_desc.txt` Results, a list of words, listed by the difference in frequencies from greatest difference to smallest difference

```
{
    "what": {
        "freq_below_cutoff": 0.004557065092487409,
        "freq_above_cutoff": 0.006675508248923497,
        "ratio_above_vs_below": 1.4648700673441042,
        "count_below_cutoff": 694,
        "count_above_cutoff": 1958,
        "diff_above_vs_below": 0.0021184431564360883
    },
    "paragraph": {
        "freq_below_cutoff": 0.005397561247874136,
        "freq_above_cutoff": 0.0036445956680792742,
        "ratio_above_vs_below": 0.6752300716392466,
        "count_below_cutoff": 822,
        "count_above_cutoff": 1069,
        "diff_above_vs_below": 0.0017529655797948614
    },
    "select": {
        "freq_below_cutoff": 0.0063628185513260795,
        "freq_above_cutoff": 0.005090160273566283,
        "ratio_above_vs_below": 0.7999851374836768,
        "count_below_cutoff": 969,
        "count_above_cutoff": 1493,
        "diff_above_vs_below": 0.0012726582777597964
    },
    "best": {
        "freq_below_cutoff": 0.0037428344419565174,
        "freq_above_cutoff": 0.0025501941625101004,
        "ratio_above_vs_below": 0.6813537178996942,
        "count_below_cutoff": 570,
        "count_above_cutoff": 748,
        "diff_above_vs_below": 0.001192640279446417
    },
    ...
```
* `results_sorted_by_freq_above_desc.txt` Results listing words that are most to least frequent in questions ABOVE cutoff

```
{
    "article": {
        "freq_below_cutoff": 0.0114123618598604,
        "freq_above_cutoff": 0.010272373010217823,
        "ratio_above_vs_below": 0.9001092969499899,
        "count_below_cutoff": 1738,
        "count_above_cutoff": 3013,
        "diff_above_vs_below": 0.0011399888496425765
    },
    "what": {
        "freq_below_cutoff": 0.004557065092487409,
        "freq_above_cutoff": 0.006675508248923497,
        "ratio_above_vs_below": 1.4648700673441042,
        "count_below_cutoff": 694,
        "count_above_cutoff": 1958,
        "diff_above_vs_below": 0.0021184431564360883
    },
    "which": {
        "freq_below_cutoff": 0.006559809837744844,
        "freq_above_cutoff": 0.006262976840282158,
        "ratio_above_vs_below": 0.9547497557391493,
        "count_below_cutoff": 999,
        "count_above_cutoff": 1837,
        "diff_above_vs_below": 0.0002968329974626857
    },
    "following": {
        "freq_below_cutoff": 0.005784977444497705,
        "freq_above_cutoff": 0.005949316595695354,
        "ratio_above_vs_below": 1.028407915635688,
        "count_below_cutoff": 881,
        "count_above_cutoff": 1745,
        "diff_above_vs_below": 0.00016433915119764848
    },
    ...
```

* `results_sorted_by_freq_below_desc.txt` Results listing words that are most to least frequent in questions BELOW cutoff

```
{
    "article": {
        "freq_below_cutoff": 0.0114123618598604,
        "freq_above_cutoff": 0.010272373010217823,
        "ratio_above_vs_below": 0.9001092969499899,
        "count_below_cutoff": 1738,
        "count_above_cutoff": 3013,
        "diff_above_vs_below": 0.0011399888496425765
    },
    "which": {
        "freq_below_cutoff": 0.006559809837744844,
        "freq_above_cutoff": 0.006262976840282158,
        "ratio_above_vs_below": 0.9547497557391493,
        "count_below_cutoff": 999,
        "count_above_cutoff": 1837,
        "diff_above_vs_below": 0.0002968329974626857
    },
    "select": {
        "freq_below_cutoff": 0.0063628185513260795,
        "freq_above_cutoff": 0.005090160273566283,
        "ratio_above_vs_below": 0.7999851374836768,
        "count_below_cutoff": 969,
        "count_above_cutoff": 1493,
        "diff_above_vs_below": 0.0012726582777597964
    },
    "following": {
        "freq_below_cutoff": 0.005784977444497705,
        "freq_above_cutoff": 0.005949316595695354,
        "ratio_above_vs_below": 1.028407915635688,
        "count_below_cutoff": 881,
        "count_above_cutoff": 1745,
        "diff_above_vs_below": 0.00016433915119764848
    },
    ...
```

The rest of the results can be viewed from the files.

## Solution

### Approach

In order to comment on particular words or phrases that showed up more in certain questions, I needed to compare the frequency of specific terms in questions below and above the cutoff percentage (designated at 50%).

What I wanted to do:

* Gather significant terms for *each* question (remove "meaningless" words, or words that don't hold much value, such as "a," "the," "I," etc., also known as stopwords.
* Gather N-grams, or batches of N words that occur frequently together, for *each question*. I gathered 2-grams and 3-grams, as generating and adding these to the overall list of terms is costly in time complexity.
* Consolidate all of the significant terms across all questions in that percentile.
* Create a dict initialized to zero for each one (to be used later to count) of significant terms and phrases for failing questions, and another for passing questions.
* Tally up all terms for each percentile.
* Compare frequencies of shared terms in each percentile.

Afterwards, it was a matter of figuring out the best way to display the resulting information.

I tried a couple of approaches in an attempt to find the best way to display data for gathering insight.

* Words that only appear in one set vs. another: This was flawed, as it was too restrictive and ended up with very few words per set. The words were very specific to the topic, so getting this data did not answer the question.
* Number of counts of a single word, one set compared to the other: This gives a bit more insight, but we lose information on how frequent a particular word appears relative to its own set. The most frequently appearing word in the "below" set can still appear fewer times than in the "above" set.

Finally, I decided to show the frequency of a word as a percentage of how often it appears in questions of its particular set relative to the total number of words and terms along with the raw number of how many occurrences it has.

### Things to Consider

**How do we determine which words to exclude (words without much meaning nor significance: stop words)?**

In both of the stop word lists I referenced, question words (e.g. "who," "what," "when," etc.) were listed in both. In other texts, perhaps these words may not hold much meaning nor significance, but because of the particular context of the text we're analyzing here (questions), I manually went in and removed those from the stop words.

**How do we capture significant phrases alongside individual words?**

Here, I had to think about n-grams: words that frequently occur in a sequence of n words (e.g. "red wine," "President Obama"). I thought to gather and include 2-grams and 3-grams.

**Other**

Are there other subtle things that can be valuable for the analysis but will be lost through the processing, such as the length of questions?

## Analysis
Some words that showed up more frequently in questions below the cutoff compared to above are:

* "article"
* "which"
* "select"
* "paragraph"
* "best"
* "not"
* "except"
* "section"
* "idea"
* "shows"
* "describes"
* "author"
* "contains"
* "sentences"
* "important"
* "summary"
* "evidence"
* "supports"
* "explains"
* "provides"
* "least"
* "pro"
* "information"
* "help"
* "phrase"
* "could"
* "reasons"
* "use"
* "antonym"


## Time and Space Complexity

O(n*m) to get all words, with n being average length of a single question and m being the number of questions

O((n-K) * m) to get all n-grams, where n is average length of single question, K is n in n-grams, and m is number of questions

many more linear operations to go through, build up frequency counter

O(nlogn) to sort the ordered dict

## What's Next

For future exploration, I'd like to take into consideration the actual length of questions, as perhaps longer questions are more convoluted or lose the reader's focus. Longer questions also tend to have passages, which add complexity to the question asked. Alongside that, I would like to generate comparisons for multiple cutoffs to see if there are more obvious patterns across more restrictive cutoff percentages (90% failing vs 10% passing, for example).

I'd also like to implement a better ranking/scoring system exploring TF-IDF that will judge and pull out terms for me.

For the technical side, improving time and space complexity and code flexibility and adding unit tests would be high in priority for the next step. As of now, the code is slow, very rigid and has some hardcoded values (such as file names and the cutoff percentage). It does not have proper tests either.

## Built With

* Python 3.6.2

## Acknowledgments

* List of stop words from [a Gist for English stopwords from NLTK](https://gist.github.com/sebleier/554280)
* List of stop words from from [Rank.nl's English stop words list](https://www.ranks.nl/stopwords)