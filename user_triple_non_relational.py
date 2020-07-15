import stanza
import re

def get_user_triples:
    subjects = []
    predicates = []
    objs = []

    is_compound, rule = compound_non_reln(doc)
    if is_compound:
        queries = break_compound_non_reln(doc, rule)
        print(queries)
        for query in queries:
            ss, ps, os = generate_triple_non_reln(query)
            subjects = subjects + ss
            predicates = predicates + ps
            objs = objs + os
    return zip(subjects, predicates, objs)

def compound_non_reln:
    upos_string = ""
    compound_flag = False
    rule = 0



if __name__ == '__main__':
    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }
    nlp = stanza.Pipeline(**param_dict)
    doc = nlp("What is the population and area of the most populated state?")
    doc = nlp("Which is the shortest and longest river in America?")
    doc = nlp("Which is the highest mountain in Germany?")
    doc = nlp("What is Angela's birth name?")
    # doc = nlp("Which rivers and lakes traverse Alaska")

    triples = get_user_triples(doc)
    print("===================TRIPLES=====================")
    for subject, predicate, obj in triples:
        print(subject.text, predicate, obj.text)
    print("===============================================")