# import csv

# file_in = '../data/core_unique.csv'
# file_out = '../decoded_data/core_unique.csv'

# with open(file_in, encoding='utf-8', errors='ignore') as f:
#     reader = csv.reader(f)
#     with open(file_out, 'w') as ff:
#         writer = csv.writer(ff)
#         writer.writerows(reader)
import spacy
nlp = spacy.load('en_core_web_sm')
parsed_text = nlp(u"What members does Ekofisk formation have?")

#get token dependencies
for text in parsed_text:
    #subject would be
    print(text, text.pos_)

# spacy.find
# print(subject)
# print(direct_object)
# print(indirect_object)