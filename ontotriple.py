from lexicon import Lexicon, LexicalEntry
import stanza
import nltk
from nltk.corpus import wordnet as wn
import pprint

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
def map_user_to_lexicon(lexicon, user_triple):
    print("=====from map_user_to_lexicon=====")
    x_lexicon = user_to_lexicon_subject(lexicon, user_triple[0])
    print("x_lexicon", x_lexicon['label'], x_lexicon['associated_predicate'], x_lexicon['associated_object'])
    z_lexicon = user_to_lexicon_object(lexicon, user_triple[2])
    print("z_lexicon", z_lexicon['label'], z_lexicon['associated_predicate'], z_lexicon['associated_subject'])
    if (x_lexicon['associated_object'] == z_lexicon['label'] or x_lexicon['associated_object'] == lexicon.entries[z_lexicon['label']].type) and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate']:
        print("Oh Yeah")
    else:
        print("Nay")

def user_to_lexicon_subject(input_lexicon, subject):
    min_med = 1000
    x_lexicon = ""
    pprint.pprint(input_lexicon.entries['Course'].ontotriples)
    for entry in input_lexicon.entries:
        for ontotriple in input_lexicon.entries[entry].ontotriples:
            if ontotriple['category'] == "subject":
                med = nltk.edit_distance(subject.lower(), input_lexicon.entries[entry].label.lower())
                if med < min_med:
                    min_med = med
                    x_lexicon = ontotriple
                    # x_lexicon = input_lexicon.entries[entry].label
    print(subject, x_lexicon)
    # z = input_lexicon.entries[x_lexicon].associated_object
    #
    # return input_lexicon.entries[x_lexicon]
    return x_lexicon

def user_to_lexicon_object(input_lexicon, obj):
    min_med = 1000
    z_lexicon = ""
    for entry in input_lexicon.entries:
        for ontotriple in input_lexicon.entries[entry].ontotriples:
            if ontotriple['category'] == "object":
                med = nltk.edit_distance(obj.lower(), input_lexicon.entries[entry].label.lower())
                if med < min_med:
                    min_med = med
                    z_lexicon = ontotriple
                    # z_lexicon = input_lexicon.entries[entry].label
    # return input_lexicon.entries[z_lexicon]
    return z_lexicon




# Constructing lexicon
lexicon = Lexicon()

instr_entry_args = {
    'label': 'Instructor',
    'part_of_speech': 'noun',
    'type': 'Class',
    'ontotriples':
    [
        {
            'label': 'Instructor',
            'category': 'subject',
            'associated_predicate': 'teaches',
            'associated_object': 'Course'
        },
        {
            'label': 'Instructor',
            'category': 'object',
            'associated_predicate': 'isTaughtBy',
            'associated_subject': 'Course'
        }
    ]
}

teach_entry_args = {
    'label': 'teaches',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'teaches',
            'category': 'predicate',
            'associated_subject': 'Instructor',
            'associated_object': 'Course'
        }
    ]
}

is_taught_by_entry_args = {
    'label': 'isTaughtBy',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isTaughtBy',
            'category': 'predicate',
            'associated_subject': 'course',
            'associated_object': 'instructor'
        }
    ]
}

course_entry_args = {
    'label': 'Course',
    'part_of_speech': 'noun',
    'type': 'class',
    'ontotriples':
    [
        {
            'label': 'Course',
            'category': 'object',
            'associated_predicate': 'teaches',
            'associated_subject': 'Instructor'
        },
        {
            'label': 'Course',
            'category': 'subject',
            'associated_predicate': 'isTaughtBy',
            'associated_object': 'Instructor'
        }
    ]
}

nlu_entry_args = {
    'label': 'NLU',
    'part_of_speech': 'noun',
    'type': 'Course',
    'ontotriples':
    [
        {
            'label': 'NLU',
            'category': 'object',
            'associated_predicate': 'teaches',
            'associated_subject': 'ProfDung'
        },
        {
            'label': 'NLU',
            'category': 'subject',
            'associated_predicate': 'isTaughtBy',
            'associated_object': 'ProfDung'
        }
    ]
}

dung_entry_args = {
    'label': 'ProfDung',
    'part_of_speech': 'noun',
    'type': 'instructor',
    'ontotriples':
    [
        {
            'label': 'ProfDung',
            'category': 'subject',
            'associated_predicate': 'teaches',
            'associated_object': 'NLU'
        },
        {
            'label': 'ProfDung',
            'category': 'object',
            'associated_predicate': 'isTaughtBy',
            'associated_subject': 'NLU'
        }
    ]
}

lexicon.add_entry(LexicalEntry(**instr_entry_args))
lexicon.add_entry(LexicalEntry(**teach_entry_args))
lexicon.add_entry(LexicalEntry(**course_entry_args))
lexicon.add_entry(LexicalEntry(**nlu_entry_args))
lexicon.add_entry(LexicalEntry(**dung_entry_args))

if __name__ == '__main__':

    input_target = "instructor"
    input_user_triple = ("instructor", "teaches", "NLU")
    # instructor = wn.synset(f'{input_user_triple[0]}.n.01')
    result = map_user_to_lexicon(lexicon, input_user_triple)
    # result = user_to_lexicon_subject(lexicon, input_user_triple[0])
    triple_subject = None

    # if result.ontotriple_category == "subject":
    #     triple_subject = result

    # triple_predicate = triple_subject.associated_predicate
    # triple_object = triple_subject.associated_object

    # query = f'select ?{input_target} where {{ {triple_subject.label} {triple_predicate} {triple_object} . }}'

    print("=========RESULTS=============")
    # print(query)
    print("End")
