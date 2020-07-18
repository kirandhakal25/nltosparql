from lexicon import Lexicon, LexicalEntry
import stanza
import nltk
from lexicon_ontology import lexicon
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
    # print("x_lexicon", x_lexicon['label'], x_lexicon['associated_predicate'], x_lexicon['associated_object'])
    y_lexicon = user_to_lexicon_predicate(lexicon, user_triple[1])
    x_lexicon = user_to_lexicon_subject(lexicon, user_triple[0], y_lexicon['label'])
    z_lexicon = user_to_lexicon_object(lexicon, user_triple[2], y_lexicon['label'])
    print("")
    # print("z_lexicon", z_lexicon['associated_subject'], z_lexicon['associated_predicate'], z_lexicon['label'])
    if x_lexicon['associated_object'] == z_lexicon['label'] and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate'] and \
            x_lexicon['associated_predicate'] == y_lexicon['label']:
        return(x_lexicon['label'], x_lexicon['associated_predicate'], x_lexicon['associated_object'])

    elif x_lexicon['associated_object'] == lexicon.entries[z_lexicon['label']].type and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate'] and \
            x_lexicon['associated_predicate'] == y_lexicon['label']:
        return(x_lexicon['label'], x_lexicon['associated_predicate'], z_lexicon['label'])

    elif lexicon.entries[x_lexicon['associated_object']].type == z_lexicon['label'] and \
            x_lexicon['associated_predicate'] == z_lexicon['associated_predicate'] and \
            x_lexicon['associated_predicate'] == y_lexicon['label']:
        return(x_lexicon['label'], x_lexicon['associated_predicate'], z_lexicon['label'])
    elif (user_triple[0].startswith("?wh")) or (user_triple[0].startswith("?how")):
        if z_lexicon['associated_predicate'] == y_lexicon['label']:
            return (user_triple[0], z_lexicon['associated_predicate'], z_lexicon['label'])
    else:
        raise Exception("We don't understand your language. Please update the ontology")

def user_to_lexicon_subject(input_lexicon, subject, predicate):
    min_med = 1000
    x_lexicon = ""
    for entry in input_lexicon.entries:
        for ontotriple in input_lexicon.entries[entry].ontotriples:
            if ontotriple['category'] == "subject" and ontotriple['associated_predicate'] == predicate:
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


def user_to_lexicon_object(input_lexicon, obj, predicate):
    min_med = 1000
    z_lexicon = ""
    for entry in input_lexicon.entries:
        for ontotriple in input_lexicon.entries[entry].ontotriples:
            if ontotriple['category'] == "object" and ontotriple['associated_predicate'] == predicate:
                med = nltk.edit_distance(obj.lower(), input_lexicon.entries[entry].label.lower())
                if med < min_med:
                    min_med = med
                    z_lexicon = ontotriple
    return z_lexicon


# Constructing lexicon
# moved to lexicon_ontology.py


if __name__ == '__main__':
    input_target = "instructor"
    input_user_triple = ("?who", "instructor_of", "NLU")

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
