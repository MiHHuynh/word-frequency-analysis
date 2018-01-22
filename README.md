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

```
{
    "article": {
        "freq_below_cutoff": 0.0114123618598604,
        "freq_above_cutoff": 0.010272373010217823,
        "ratio_above_vs_below": 0.9001092969499899,
        "count_below_cutoff": 1738,
        "count_above_cutoff": 3013
    },
    "which": {
        "freq_below_cutoff": 0.006559809837744844,
        "freq_above_cutoff": 0.006262976840282158,
        "ratio_above_vs_below": 0.9547497557391493,
        "count_below_cutoff": 999,
        "count_above_cutoff": 1837
    },
    "select": {
        "freq_below_cutoff": 0.0063628185513260795,
        "freq_above_cutoff": 0.005090160273566283,
        "ratio_above_vs_below": 0.7999851374836768,
        "count_below_cutoff": 969,
        "count_above_cutoff": 1493
    },
    "following": {
        "freq_below_cutoff": 0.005784977444497705,
        "freq_above_cutoff": 0.005949316595695354,
        "ratio_above_vs_below": 1.028407915635688,
        "count_below_cutoff": 881,
        "count_above_cutoff": 1745
    },
    "paragraph": {
        "freq_below_cutoff": 0.005397561247874136,
        "freq_above_cutoff": 0.0036445956680792742,
        "ratio_above_vs_below": 0.6752300716392466,
        "count_below_cutoff": 822,
        "count_above_cutoff": 1069
    },
    "sentence": {
        "freq_below_cutoff": 0.004839419269687638,
        "freq_above_cutoff": 0.005499282331722984,
        "ratio_above_vs_below": 1.1363517036369402,
        "count_below_cutoff": 737,
        "count_above_cutoff": 1613
    },
    "what": {
        "freq_below_cutoff": 0.004557065092487409,
        "freq_above_cutoff": 0.006675508248923497,
        "ratio_above_vs_below": 1.4648700673441042,
        "count_below_cutoff": 694,
        "count_above_cutoff": 1958
    },
    "best": {
        "freq_below_cutoff": 0.0037428344419565174,
        "freq_above_cutoff": 0.0025501941625101004,
        "ratio_above_vs_below": 0.6813537178996942,
        "count_below_cutoff": 570,
        "count_above_cutoff": 748
    },
    "read": {
        "freq_below_cutoff": 0.0030336658108489666,
        "freq_above_cutoff": 0.0034332159380316457,
        "ratio_above_vs_below": 1.13170538618783,
        "count_below_cutoff": 462,
        "count_above_cutoff": 1007
    },
    "not": {
        "freq_below_cutoff": 0.0025411875948020564,
        "freq_above_cutoff": 0.0020967505480530904,
        "ratio_above_vs_below": 0.8251065573993623,
        "count_below_cutoff": 387,
        "count_above_cutoff": 615
    },
    "why": {
        "freq_below_cutoff": 0.002153771398178487,
        "freq_above_cutoff": 0.0028365796032197906,
        "ratio_above_vs_below": 1.3170290986400766,
        "count_below_cutoff": 328,
        "count_above_cutoff": 832
    },
    "except": {
        "freq_below_cutoff": 0.0021472050219645284,
        "freq_above_cutoff": 0.0018342305607358742,
        "ratio_above_vs_below": 0.8542409979358625,
        "count_below_cutoff": 327,
        "count_above_cutoff": 538
    },
    "section": {
        "freq_below_cutoff": 0.0020421430025411875,
        "freq_above_cutoff": 0.001592166676326493,
        "ratio_above_vs_below": 0.779654840207196,
        "count_below_cutoff": 311,
        "count_above_cutoff": 467
    },
    "idea": {
        "freq_below_cutoff": 0.0018714172209782587,
        "freq_above_cutoff": 0.0014660207083948436,
        "ratio_above_vs_below": 0.7833745954461724,
        "count_below_cutoff": 285,
        "count_above_cutoff": 430
    },
    "shows": {
        "freq_below_cutoff": 0.001766355201554918,
        "freq_above_cutoff": 0.0015273890171183487,
        "ratio_above_vs_below": 0.8647122706541651,
        "count_below_cutoff": 269,
        "count_above_cutoff": 448
    },
    "word": {
        "freq_below_cutoff": 0.0017269569442711651,
        "freq_above_cutoff": 0.0027342990886806153,
        "ratio_above_vs_below": 1.5833047243888196,
        "count_below_cutoff": 263,
        "count_above_cutoff": 802
    },
    "how": {
        "freq_below_cutoff": 0.0017203905680572063,
        "freq_above_cutoff": 0.0020387915898142247,
        "ratio_above_vs_below": 1.1850748473450308,
        "count_below_cutoff": 262,
        "count_above_cutoff": 598
    },
    "describes": {
        "freq_below_cutoff": 0.0015102665292105245,
        "freq_above_cutoff": 0.0011455417628387615,
        "ratio_above_vs_below": 0.7585030461064254,
        "count_below_cutoff": 230,
        "count_above_cutoff": 336
    },
    "author": {
        "freq_below_cutoff": 0.001431470014643019,
        "freq_above_cutoff": 0.0009102965793986587,
        "ratio_above_vs_below": 0.6359173228128492,
        "count_below_cutoff": 218,
        "count_above_cutoff": 267
    },
    "contains": {
        "freq_below_cutoff": 0.0012279123520102962,
        "freq_above_cutoff": 0.0012035007210776274,
        "ratio_above_vs_below": 0.9801194027467003,
        "count_below_cutoff": 187,
        "count_above_cutoff": 353
    },
    "sentences": {
        "freq_below_cutoff": 0.0012147795995823786,
        "freq_above_cutoff": 0.0011080389075077306,
        "ratio_above_vs_below": 0.9121316392608637,
        "count_below_cutoff": 185,
        "count_above_cutoff": 325
    },
    "main": {
        "freq_below_cutoff": 0.0011950804709405021,
        "freq_above_cutoff": 0.001213728772531545,
        "ratio_above_vs_below": 1.015604222514294,
        "count_below_cutoff": 182,
        "count_above_cutoff": 356
    },
    "important": {
        "freq_below_cutoff": 0.001168814966084667,
        "freq_above_cutoff": 0.0011625885152619574,
        "ratio_above_vs_below": 0.9946728515604424,
        "count_below_cutoff": 178,
        "count_above_cutoff": 341
    },
    "summary": {
        "freq_below_cutoff": 0.0011556822136567493,
        "freq_above_cutoff": 0.0010432612482995864,
        "ratio_above_vs_below": 0.9027232884363199,
        "count_below_cutoff": 176,
        "count_above_cutoff": 306
    },
    "evidence": {
        "freq_below_cutoff": 0.0011031512039450788,
        "freq_above_cutoff": 0.00041253140864133973,
        "ratio_above_vs_below": 0.3739572663892754,
        "count_below_cutoff": 168,
        "count_above_cutoff": 121
    },
    "according": {
        "freq_below_cutoff": 0.00109658482773112,
        "freq_above_cutoff": 0.0019535578276982453,
        "ratio_above_vs_below": 1.781492665496967,
        "count_below_cutoff": 167,
        "count_above_cutoff": 573
    },
    "supports": {
        "freq_below_cutoff": 0.0010571865704473672,
        "freq_above_cutoff": 0.0007091449008049477,
        "ratio_above_vs_below": 0.6707850067607843,
        "count_below_cutoff": 161,
        "count_above_cutoff": 208
    },
    "include": {
        "freq_below_cutoff": 0.0010243546893775731,
        "freq_above_cutoff": 0.001015986444422473,
        "ratio_above_vs_below": 0.991830715432967,
        "count_below_cutoff": 156,
        "count_above_cutoff": 298
    },
    "explains": {
        "freq_below_cutoff": 0.0010112219369496555,
        "freq_above_cutoff": 0.0007227823027435044,
        "ratio_above_vs_below": 0.714761296539682,
        "count_below_cutoff": 154,
        "count_above_cutoff": 212
    },
    "provides": {
        "freq_below_cutoff": 0.000998089184521738,
        "freq_above_cutoff": 0.0005727708814193807,
        "ratio_above_vs_below": 0.5738674361989402,
        "count_below_cutoff": 152,
        "count_above_cutoff": 168
    },
    "people": {
        "freq_below_cutoff": 0.0009324254223821499,
        "freq_above_cutoff": 0.0010978108560538132,
        "ratio_above_vs_below": 1.1773712188682484,
        "count_below_cutoff": 142,
        "count_above_cutoff": 322
    },
    "least": {
        "freq_below_cutoff": 0.0008864607888844384,
        "freq_above_cutoff": 0.0006580046435353601,
        "ratio_above_vs_below": 0.7422828531010631,
        "count_below_cutoff": 135,
        "count_above_cutoff": 193
    },
    "reason": {
        "freq_below_cutoff": 0.0008864607888844384,
        "freq_above_cutoff": 0.001036442547330308,
        "ratio_above_vs_below": 1.1691916442628143,
        "count_below_cutoff": 135,
        "count_above_cutoff": 304
    },
    "used": {
        "freq_below_cutoff": 0.0008470625316006856,
        "freq_above_cutoff": 0.001213728772531545,
        "ratio_above_vs_below": 1.4328679728496243,
        "count_below_cutoff": 129,
        "count_above_cutoff": 356
    },
    "means": {
        "freq_below_cutoff": 0.0008470625316006856,
        "freq_above_cutoff": 0.0008216534667980403,
        "ratio_above_vs_below": 0.9700033186987624,
        "count_below_cutoff": 129,
        "count_above_cutoff": 241
    },
    "support": {
        "freq_below_cutoff": 0.0007879651456750563,
        "freq_above_cutoff": 0.00044662491348773143,
        "ratio_above_vs_below": 0.5668079558330009,
        "count_below_cutoff": 120,
        "count_above_cutoff": 131
    },
    "central": {
        "freq_below_cutoff": 0.0007682660170331799,
        "freq_above_cutoff": 0.0005284493251190716,
        "ratio_above_vs_below": 0.6878468048863977,
        "count_below_cutoff": 117,
        "count_above_cutoff": 155
    },
    "text": {
        "freq_below_cutoff": 0.0007682660170331799,
        "freq_above_cutoff": 0.0005079932222112365,
        "ratio_above_vs_below": 0.6612204769553113,
        "count_below_cutoff": 117,
        "count_above_cutoff": 149
    },
    "one": {
        "freq_below_cutoff": 0.0007682660170331799,
        "freq_above_cutoff": 0.0008011973638902053,
        "ratio_above_vs_below": 1.042864510634216,
        "count_below_cutoff": 117,
        "count_above_cutoff": 235
    },
    "first": {
        "freq_below_cutoff": 0.0007485668883913035,
        "freq_above_cutoff": 0.000715963601774226,
        "ratio_above_vs_below": 0.9564457269982336,
        "count_below_cutoff": 114,
        "count_above_cutoff": 210
```



## Time and Space Complexity

O(n*m) to get all words, with n being average length of a single question and m being the number of questions

O((n-K) * m) to get all n-grams, where n is average length of single question, K is n in n-grams, and m is number of questions

many more linear operations to go through, build up frequency counter

O(nlogn) to sort the ordered dict

## What's Next

For future exploration, I'd like to take into consideration the actual length of questions, as perhaps longer questions are more convoluted or lose the reader's focus. Longer questions also tend to have passages, which add complexity to the question asked. Alongside that, I would like to generate comparisons for multiple cutoffs to see if there are more obvious patterns across more restrictive cutoff percentages (90% failing vs 10% passing, for example).

For the technical side, improving time and space complexity and code flexibility and adding unit tests would be high in priority for the next step. As of now, the code is slow, very rigid and has some hardcoded values (such as file names and the cutoff percentage). It does not have proper tests either.

## Built With

* Python 3.6.2

## Acknowledgments

* List of stop words from [a Gist for English stopwords from NLTK](https://gist.github.com/sebleier/554280)
* List of stop words from from [Rank.nl's English stop words list](https://www.ranks.nl/stopwords)