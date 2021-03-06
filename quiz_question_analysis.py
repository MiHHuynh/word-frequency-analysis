import json
import re
from pprint import pprint
from collections import OrderedDict
import math

# stop_words_set = set(open('stop_words_short.txt').read().replace('\n', ' ').replace('\r', '').split())
stop_words_set = set(open('stop_words_nltk.txt').read().replace('\n', ' ').replace('\r', '').split())
cutoff_percentage = 0.5

##################################################################
### Functions to clean up, extract, and gather words and terms ###
##################################################################

def extract_N_grams(N_num, list_of_terms):
	'''
	Input: This takes a number, N_num, which determines how many N-grams you want to generate, and a list of terms.
	Output: Returns a generator for a list of n-grams represented as tuples. "red wine" --> ("red", "wine")
	Info: A 2-gram is a phrase of 2 words that frequently go together. 3-gram is a phrase of 3 words, etc.
	'''
	return (tuple(list_of_terms[i:i+N_num]) for i in range(len(list_of_terms)-N_num))

def extract_words_and_lowercase(a_string):
	'''
	Input: a string
	Output: list of terms, retaining original order in the sentence, with removal of punctuation, \r, \n, and white space
	'''
	return [elem.lower() for elem in re.split('\W+', a_string) if elem]

def remove_stop_words(list_of_words):
	'''
	Input: a list of strings
	Output: returns a list of words minus stop words as indicated in the stop_words_set; relies on set from outside of function
	'''
	return [word for word in list_of_words if word not in stop_words_set]

def create_dict_of_significant_terms(a_string):
	'''
	Input: a string	
	Output: a dict containing a set of unique terms, including 2-grams and 3-grams
	and excluding stop words, and the number of terms
	'''
	terms = extract_words_and_lowercase(a_string)

	two_grams = extract_N_grams(2, terms)
	three_grams = extract_N_grams(3, terms)

	terms.extend(two_grams)
	terms.extend(three_grams)

	terms = remove_stop_words(terms)

	result = set(terms)
	return {'terms': result, 'terms_count': len(terms) }

################################################################################
### Functions to process the text, split them into groups, count frequencies ###
################################################################################

def separate_questions(json_file_name, cutoff_percentage):
	'''
	Input: json file containing questions, formatted as [{"text": ..., "percent_correct": X }, ...],
	and a cutoff percentage given as a float (e.g. 0.4, 0.5)

	What this does: separate_questions opens the file and reads from it, goes through every question
	in the file and converts it into a set of terms and pushes it to a list depending on whether it is
	above or below the cutoff. It also counts the total number of terms for each half (above the cutoff
	and below the cutoff).
	
	Output: Returns a dict containing all the questions below and above the cutoff, represented as sets of
	terms, and the total number of terms for each category as well.
	'''
	with open(json_file_name) as json_file:
		quiz_questions = json.loads(json_file.read())

	qs_below_cutoff = []
	qs_above_cutoff = []

	total_terms_below_cutoff = 0
	total_terms_above_cutoff = 0
	for question in quiz_questions:
		processed_question = create_dict_of_significant_terms(question['text']) # {'terms': {...}, 'terms_count': X }

		if question['percent_correct'] > cutoff_percentage:
			total_terms_above_cutoff += processed_question['terms_count']
			qs_above_cutoff.append(processed_question)
		else:
			total_terms_below_cutoff += processed_question['terms_count']
			qs_below_cutoff.append(processed_question)

	json_file.close()

	return {'qs_below_cutoff': qs_below_cutoff, 
			'total_terms_below_cutoff': total_terms_below_cutoff,
			'qs_above_cutoff': qs_above_cutoff,
			'total_terms_above_cutoff': total_terms_above_cutoff}

def get_word_frequency_across_questions(entire_questions_list, set_of_words_to_check_with):
	'''
	Input: a list of questions that have already been processed into term sets, formatted
	as [{'terms': result, 'terms_count': X }, {'terms': result, 'terms_count': Y }, ...], and
	a set of other words to check against

	Output: A dict counter containing information on the term and how many occurrences it has
	'''

	word_freq_counter = {}

	for question in entire_questions_list:
		for term in question['terms']:
			if term in set_of_words_to_check_with:
				if term not in word_freq_counter:
					word_freq_counter[str(term)] = 0
				word_freq_counter[str(term)] += 1

	return word_freq_counter

###############################################
### Some helpers for creating sets of terms ###
###############################################

def reduce_word_sets_to_one(list_of_questions):
	'''
	This takes a list of questions, formatted as term sets a reduced, single set of terms
	'''
	unique_words = set()
	for entry in list_of_questions:
		unique_words = unique_words.union(entry['terms'])
	return unique_words

def get_words_unique_to_set(set_of_words1, set_of_words2):
	'''
	Gets the difference between two sets of terms.
	'''
	return set_of_words1.difference(set_of_words2)

############
### Main ###
############

def main():
	separation = separate_questions('quiz_questions.json', cutoff_percentage)

	below_word_set = reduce_word_sets_to_one(separation['qs_below_cutoff'])
	above_word_set = reduce_word_sets_to_one(separation['qs_above_cutoff'])
	entire_word_set = below_word_set.union(above_word_set)

	below_freq = get_word_frequency_across_questions(separation['qs_below_cutoff'], entire_word_set) # returns a dict
	above_freq = get_word_frequency_across_questions(separation['qs_above_cutoff'], entire_word_set)

	joined_freq_counter = dict()
	for term in entire_word_set:
		joined_freq_counter[str(term)] = { 'freq_below_cutoff': 0, 
					           'freq_above_cutoff': 0, 
						   'ratio_above_vs_below': 0,
						   'count_below_cutoff': 0,
						   'count_above_cutoff': 0,
						   'diff_above_vs_below': 0}

	for term, val in below_freq.items():
		joined_freq_counter[term]['count_below_cutoff'] = val
		joined_freq_counter[term]['freq_below_cutoff'] = float(val / separation['total_terms_below_cutoff'])

	for term, val in above_freq.items():
		joined_freq_counter[term]['count_above_cutoff'] = val
		joined_freq_counter[term]['freq_above_cutoff'] = float(val / separation['total_terms_above_cutoff'])
		joined_freq_counter[term]['diff_above_vs_below'] = math.fabs(joined_freq_counter[term]['freq_above_cutoff'] - joined_freq_counter[term]['freq_below_cutoff'])
		if joined_freq_counter[term]['freq_below_cutoff'] == 0:
			continue
		else:
			joined_freq_counter[term]['ratio_above_vs_below'] = float(joined_freq_counter[term]['freq_above_cutoff'] / joined_freq_counter[term]['freq_below_cutoff'])

	ordered_joined_freq_counter = OrderedDict()

	for term, data in sorted(joined_freq_counter.items(), key = lambda kv: kv[1]['diff_above_vs_below'], reverse = True):
		# not much value in words that don't show up at all in one or more sets
		if data['freq_below_cutoff'] > 0 and data['freq_above_cutoff'] > 0:
			ordered_joined_freq_counter[term] = data

	output_file = open('results_sorted_by_diff_desc.json', 'w')
	output_file.write(json.dumps(ordered_joined_freq_counter, indent=4))
	output_file.close()


	ordered_joined_freq_counter = OrderedDict()
	for term, data in sorted(joined_freq_counter.items(), key = lambda kv: kv[1]['freq_below_cutoff'], reverse = True):
		# not much value in words that don't show up at all in one or more sets
		if data['freq_below_cutoff'] > 0 and data['freq_above_cutoff'] > 0:
			ordered_joined_freq_counter[term] = data

	output_file = open('results_sorted_by_freq_below_desc.json', 'w')
	output_file.write(json.dumps(ordered_joined_freq_counter, indent=4))
	output_file.close()


	ordered_joined_freq_counter = OrderedDict()
	for term, data in sorted(joined_freq_counter.items(), key = lambda kv: kv[1]['freq_above_cutoff'], reverse = True):
		# not much value in words that don't show up at all in one or more sets
		if data['freq_below_cutoff'] > 0 and data['freq_above_cutoff'] > 0:
			ordered_joined_freq_counter[term] = data

	output_file = open('results_sorted_by_freq_above_desc.json', 'w')
	output_file.write(json.dumps(ordered_joined_freq_counter, indent=4))
	output_file.close()


if __name__ == '__main__':
	main()

