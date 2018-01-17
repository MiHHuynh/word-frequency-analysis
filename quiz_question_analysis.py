import json
import re
from pprint import pprint
import operator
from collections import OrderedDict
import math

stop_words_set = set(open('stop_words_nltk.txt').read().replace('\n', ' ').replace('\r', '').split())
cutoff_percentage = 0.5

##########

def reduce_word_sets_to_one(list_of_questions):
	# not very reusable since it requires a specific data structure pertaining to this problem
	# list_of_questions is a list of dicts, as such: [{'words': {this is a set}}, {'words': {this is another set}}, ...]

	unique_words = set()
	for entry in list_of_questions:
		unique_words = unique_words.union(entry['words'])
	return unique_words

def get_words_unique_to_set(set_of_words1, set_of_words2):
	return set_of_words1.difference(set_of_words2)

def get_word_frequency_across_questions(entire_questions_list, set_of_words_to_check_with):
	# get frequency of each word across all questions

	word_freq_counter = {}

	for question in entire_questions_list:
		for word in question['words']:
			if word in set_of_words_to_check_with:
				if word not in word_freq_counter:
					word_freq_counter[word] = 0
				word_freq_counter[word] += 1

	return word_freq_counter

def separate_questions(json_file_name, cutoff_percentage):
	with open(json_file_name) as json_file:
		quiz_questions = json.loads(json_file.read())

	questions_with_percentage_below_cutoff = []
	questions_with_percentage_above_cutoff = []

	for question in quiz_questions:
		processed_question = create_dict_of_significant_words(question['text'])

		if question['percent_correct'] > cutoff_percentage:
			questions_with_percentage_above_cutoff.append(processed_question)
		else:
			questions_with_percentage_below_cutoff.append(processed_question)

	json_file.close()

	return {'questions_with_percentage_below_cutoff': questions_with_percentage_below_cutoff, 
			'questions_with_percentage_above_cutoff': questions_with_percentage_above_cutoff}

def extract_words_and_lowercase(a_string):
	# removes punctuation, \r, \n, white space and returns a generator
	return [elem.lower() for elem in re.split('\W+', a_string) if elem]

def remove_stop_words(list_of_words):
	# removes stop words and returns a list
	return [word for word in list_of_words if word not in stop_words_set]

def create_dict_of_significant_words(a_string):
	words = extract_words_and_lowercase(a_string)
	words = remove_stop_words(words)
	result = set(words)
	return {'words': result}


# separation = separate_questions('quiz_questions.json', cutoff_percentage)

# below_word_set = reduce_word_sets_to_one(separation['questions_with_percentage_below_cutoff'])
# above_word_set = reduce_word_sets_to_one(separation['questions_with_percentage_above_cutoff'])

# unique_words_for_below = get_words_unique_to_set(below_word_set, above_word_set)
# unique_words_for_above = get_words_unique_to_set(above_word_set, below_word_set)

# below_freq = get_word_frequency_across_questions(separation['questions_with_percentage_below_cutoff'], unique_words_for_below)
# above_freq = get_word_frequency_across_questions(separation['questions_with_percentage_above_cutoff'], unique_words_for_above)

# below_freq = sorted([(key, value) for (key, value) in below_freq.items()], key=operator.itemgetter(1),reverse=True)
# above_freq = sorted([(key, value) for (key, value) in above_freq.items()], key=operator.itemgetter(1),reverse=True)

# output_file = open('results.txt', 'w')
# output_file.write("Frequency for all words of questions below threshold.\n")
# output_file.write(json.dumps(below_freq, indent=4))
# output_file.write("\n\n\n\n\n")
# output_file.write("Frequency for all words of questions above threshold.\n")
# output_file.write(json.dumps(above_freq, indent=4))

##########

separation = separate_questions('quiz_questions.json', cutoff_percentage)

below_word_set = reduce_word_sets_to_one(separation['questions_with_percentage_below_cutoff'])
above_word_set = reduce_word_sets_to_one(separation['questions_with_percentage_above_cutoff'])
entire_word_set = below_word_set.union(above_word_set)

below_freq = get_word_frequency_across_questions(separation['questions_with_percentage_below_cutoff'], entire_word_set)
above_freq = get_word_frequency_across_questions(separation['questions_with_percentage_above_cutoff'], entire_word_set)

below_freq = sorted([(key, value) for (key, value) in below_freq.items()], key=operator.itemgetter(1),reverse=True)
above_freq = sorted([(key, value) for (key, value) in above_freq.items()], key=operator.itemgetter(1),reverse=True)

joined_freq_counter = dict()
for word in entire_word_set:
	joined_freq_counter[word] = { "frequency_in_questions_below_threshold": 0, "frequency_in_questions_above_threshold": 0, "ratio_freq_above_vs_below": 0}

for word, freq in below_freq:
	joined_freq_counter[word]["frequency_in_questions_below_threshold"] = freq

for word, freq in above_freq:
	joined_freq_counter[word]["frequency_in_questions_above_threshold"] = freq

	if joined_freq_counter[word]["frequency_in_questions_below_threshold"] == 0:
		joined_freq_counter[word]["ratio_freq_above_vs_below"] = float("inf")
	else:
		joined_freq_counter[word]["ratio_freq_above_vs_below"] = float(joined_freq_counter[word]["frequency_in_questions_above_threshold"]) / float(joined_freq_counter[word]["frequency_in_questions_below_threshold"])


od = OrderedDict()
for word, freqs in sorted(joined_freq_counter.items(), 
	                      key = lambda kv: kv[1]['ratio_freq_above_vs_below'],
	                      reverse = True):
	od[word] = freqs

print(json.dumps(od, indent=4))

# analyzed_data_generator = ({'word': key, 'stats': value} for (key, value) in joined_freq_counter.items())
# analyzed_data = sorted(analyzed_data_generator, 
# 	                   key = lambda word_entry:  # word_entry ~ {'word': ..., 'stats': {'freq...': ..., }}
# 	                                word_entry['stats']['ratio_freq_above_vs_below'], reverse=True)


# analyzed_data = sorted(({'word': key, 'stats': value} 
# 	                    for (key, value) in joined_freq_counter.items()),
# 	                     key = lambda (word, stats): stats['ratio_freq_above_vs_below'], reverse=True)

# output_file = open('results.txt', 'w')
# output_file.write(json.dumps(analyzed_data, indent=4))
# output_file.close()
# output_file.write("\n\n\n\n\n")
# output_file.write("Frequency for all words of questions above threshold.\n")
# output_file.write(json.dumps(above_freq, indent=4))
# output_file.write("\n\n\n\n\n")
# output_file.write("Frequency comparison:")
# output_file.write(json.dumps(joined_freq_counter, indent=4))

# pprint("PERCENT BELOW")
# pprint(below_freq)
# pprint("PERCENT ABOVE")
# pprint(above_freq)
# print("PERCENT BELOW")
# print("PERCENT BELOW")
# print("PERCENT BELOW")
# print("PERCENT BELOW")
# freq = get_word_frequency_across_questions(separation['questions_with_percentage_below_cutoff'])
# rep = [(key, value) for (key, value) in sorted(freq.items())]
# # pprint(sorted(rep, key=operator.itemgetter(1),reverse=True))

# print("PERCENT ABOVE")
# print("PERCENT ABOVE")
# print("PERCENT ABOVE")
# print("PERCENT ABOVE")
# freq2 = get_word_frequency_across_questions(separation['questions_with_percentage_above_cutoff'])
# rep2 = [(key, value) for (key, value) in sorted(freq2.items())]
# # pprint(sorted(rep2, key=operator.itemgetter(1),reverse=True))