## Ideas
# Then can run word2vec on the non named entities to cluster
# Clustering the named entities is tougher, but they might be broken down enough that manual is practical

# Notes
# Gonna scrape the MonkeyLearn API for NER (https://app.monkeylearn.com/main/extractors/ex_isnnZRbS/tab/demo/)
# Works of art are a notable weakness here
# https://medium.com/analytics-vidhya/basics-of-using-pre-trained-glove-vectors-in-python-d38905f356db
# https://github.com/wsuh60/nlp_jeopardy
# Named Entity Recognition
# https://www.aclweb.org/anthology/W15-1830.pdf
# https://patents.google.com/patent/US20080071519

from most_common_utils import get_most_common, initially_populate_table, process_api_response, update_entity_columns

most_common_obj = get_most_common()
api_string = most_common_obj['api_string']
initial_insertions = most_common_obj['initial_insertions']
initially_populate_table(initial_insertions)

# api_string then gets manually processed (because I don't want to pay for their API) at this link (https://app.monkeylearn.com/main/extractors/ex_isnnZRbS/tab/demo/)
# Then the JSON API response gets manually saved to a file (monkey_learn.json)

process_api_response()
update_entity_columns()