import argparse
from target import get_targets
from user_triple_relational import get_user_triples
from ontotriple import map_user_to_lexicon, lexicon
from query_construction import construct_query
import stanza
import re


def type_of_question(doc):
    relational_patterns = [
        "DET NOUN VERB PROPN",
        "PRON VERB PROPN",
        "NOUN VERB ADP PROPN",
        "PRON VERB ADP PROPN",
        "NOUN VERB ADP DET NOUN",
        "CCONJ NOUN VERB PROPN"
    ]
    non_relational_patterns = [
        "PRON AUX PROPN PART NOUN",
        "PRON AUX DET ADJ CCONJ ADJ NOUN"
    ]
    rel = False
    upos_sentence = ""
    for sentence in doc.sentences:
        for word in sentence.words:
            upos_sentence = upos_sentence + word.upos + " "
    upos_sentence = upos_sentence.strip()
    for pattern in relational_patterns:
        rel = bool(re.search(pattern, upos_sentence))
        if rel:
            return "relational"
    for pattern in non_relational_patterns:
        rel = bool(re.search(pattern, upos_sentence))
        if rel:
            return "non_relational"
    return rel



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NL to SPARQL interface.')
    parser.add_argument('--input', type=str,
                        help='The input question.')

    args = parser.parse_args()

    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }

    nlp = stanza.Pipeline(**param_dict)
    text = args.input
    text.strip('?')
    text = nlp(text)
    rel = type_of_question(text)
    # Identify targets
    # and extract string from word object
    target_words = get_targets(text)
    targets = []
    for target_word in target_words:
        targets.append(target_word.text.lower())

    print("\nStarting program...")
    print("\nGot input question: ", args.input)

    print("")
    [print("Targets identified: ", target) for target in targets]



    # Get user triples
    triples = get_user_triples(text, nlp)

    user_triples = []
    print("\nUser triples: ")
    for subject, predicate, obj in triples:
        user_triple = (subject, predicate, obj)
        user_triples.append(user_triple)
        print(user_triple)

    # get ontology triples
    ontology_triples = []
    print("\nOntology triples: ")
    for user_triple in user_triples:
        ontology_triple = map_user_to_lexicon(lexicon, user_triple)
        ontology_triples.append(ontology_triple)
        print(ontology_triple)

    # construct query
    print("\nConstructing queries...\n")
    print(construct_query(ontology_triples, targets))

    print("\nFinished conversion.")


