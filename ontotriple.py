from lexicon import Lexicon, LexicalEntry
import stanza
import nltk
from nltk.corpus import wordnet as wn

"""
Convert user triple to ontology triples.

Reference case 1:
    {
    State population_of ?x
    }

    =============>


    select ?x where
    {
        State :hasPopulation ?x .
    }

Reference case 2:
    {
    instructor teaches NLU
    }

    =============>


    select ?instructor where
    {
        ?instructor a :Instructor
        ?instructor :teaches NLU .
    }
"""

# nltk.download('wordnet')


def map_user2lexicon(input_lexicon, subject):
    for entry in input_lexicon.entries:
        med = nltk.edit_distance(subject, input_lexicon.entries[entry].label)
        # print(med)

        if med == 0:
            print("Found exact match!")
            return input_lexicon.entries[entry]


# Constructing lexicon
lexicon = Lexicon()

instr_entry_args = {
    'label': 'Instructor',
    'part_of_speech': 'noun',
    'type': 'Class',
    'ontotriple_category': 'subject',
    'associated_predicate': 'teaches',
    'associated_object': 'Course'
}

teach_entry_args = {
    'label': 'teaches',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriple_category': 'predicate',
    'associated_subject': 'Instructor',
    'associated_object': 'Course'
}

is_taught_by_entry_args = {
    'label': 'isTaughtBy',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriple_category': 'predicate',
    'associated_subject': 'course',
    'associated_object': 'instructor'
}

course_entry_args = {
    'label': 'Course',
    'part_of_speech': 'noun',
    'type': 'class',
    'ontotriple_category': 'object',
    'associated_predicate': 'teaches',
    'associated_subject': 'Instructor'
}

nlu_entry_args = {
    'label': 'NLU',
    'part_of_speech': 'noun',
    'type': 'Course',
    'ontotriple_category': 'object',
    'associated_predicate': 'isTaughtBy',
    'associated_subject': 'Dung'
}

dung_entry_args = {
    'label': 'Dung',
    'part_of_speech': 'noun',
    'type': 'instructor',
    'ontotriple_category': 'subject',
    'associated_predicate': 'teaches',
    'associated_subject': 'NLU'
}

lexicon.add_entry(LexicalEntry(**instr_entry_args))
lexicon.add_entry(LexicalEntry(**teach_entry_args))
lexicon.add_entry(LexicalEntry(**course_entry_args))
lexicon.add_entry(LexicalEntry(**nlu_entry_args))
lexicon.add_entry(LexicalEntry(**dung_entry_args))

input_target = "instructor"
input_user_triple = ("instructor", "teaches", "NLU")

instructor = wn.synset(f'{input_user_triple[0]}.n.01')

result = map_user2lexicon(lexicon, input_user_triple[0])
triple_subject = None

if result.ontotriple_category == "subject":
    triple_subject = result

triple_predicate = triple_subject.associated_predicate
triple_object = triple_subject.associated_object

query = f'select ?{input_target} where {{ {triple_subject.label} {triple_predicate} {triple_object} . }}'

print("=========RESULTS=============")
print(query)
print("End")
