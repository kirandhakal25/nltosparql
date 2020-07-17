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
    # print("=====from map_user_to_lexicon=====")
    x_lexicon = user_to_lexicon_subject(lexicon, user_triple[0])
    # print("x_lexicon", x_lexicon['label'], x_lexicon['associated_predicate'], x_lexicon['associated_object'])
    y_lexicon = user_to_lexicon_predicate(lexicon, user_triple[1])
    z_lexicon = user_to_lexicon_object(lexicon, user_triple[2])
    # print("z_lexicon", z_lexicon['associated_subject'], z_lexicon['associated_predicate'], z_lexicon['label'])
    if x_lexicon['associated_object'] == z_lexicon['label'] and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate']:
        return(x_lexicon['label'], x_lexicon['associated_predicate'], x_lexicon['associated_object'])

    elif x_lexicon['associated_object'] == lexicon.entries[z_lexicon['label']].type and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate']:
        return(x_lexicon['label'], x_lexicon['associated_predicate'], z_lexicon['label'])

    elif lexicon.entries[x_lexicon['associated_object']].type == z_lexicon['label'] and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate']:
        return(x_lexicon['label'], x_lexicon['associated_predicate'], z_lexicon['label'])
    elif (user_triple[0].startswith("?wh")) or (user_triple[0].startswith("?how")):
        if z_lexicon['associated_predicate'] == y_lexicon['label']:
            return (user_triple[0], z_lexicon['associated_predicate'], z_lexicon['label'])
    else:
        print("We don't understand your language. Please update the ontology")

def user_to_lexicon_subject(input_lexicon, subject):
    min_med = 1000
    x_lexicon = ""
    for entry in input_lexicon.entries:
        for ontotriple in input_lexicon.entries[entry].ontotriples:
            if ontotriple['category'] == "subject":
                med = nltk.edit_distance(subject.lower(), input_lexicon.entries[entry].label.lower())
                if med < min_med:
                    min_med = med
                    x_lexicon = ontotriple
    return x_lexicon


def user_to_lexicon_predicate(input_lexicon, pred):
    min_med = 1000
    y_lexicon = ""
    for entry in input_lexicon.entries:
        for ontotriple in input_lexicon.entries[entry].ontotriples:
            if ontotriple['category'] == "predicate":
                med = nltk.edit_distance(pred.lower(), input_lexicon.entries[entry].label.lower())
                if med < min_med:
                    min_med = med
                    y_lexicon = ontotriple
    return y_lexicon


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
    return z_lexicon


def find_target_position(user_triple, target):
    result = None
    position = 0

    for idx, term in enumerate(user_triple):
        if target == term.lower():
            position = idx
            result = term
    return result, position


def evaluate_type(triple, target):
    _, target_position = find_target_position(triple, target)

    variable = "?" + triple[target_position].lower()
    type_declaration = (variable, "rdf:type", target.capitalize())

    triple_list = list(triple)
    triple_list.pop(target_position)
    triple_list.insert(target_position, variable)

    return type_declaration, tuple(triple_list)


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

    # triple_subject = None
    #
    # sample_ontology_triple = ("Instructor", "teaches", "NLU")
    #
    # triples = evaluate_type(sample_ontology_triple, input_target)
    #
    # # If multiple triples, make a list of triples and pass iteratively
    #
    # query = f'SELECT ?{input_target} WHERE {{ {triples[0]} }}'

    ontology_triple = map_user_to_lexicon(lexicon, input_user_triple)

    print("===========RESULTS============")
    print(ontology_triple)
    print("=============End==============")
