import stanza
import re

def get_user_triples(doc):
    subjects = []
    predicates = []
    objs = []

    is_compound, rule = compound_relational(doc)
    if is_compound:
        queries = break_compound_relational(doc, rule)
        print(queries)
        for query in queries:
            ss, ps, os = generate_triple_relational(query)
            subjects = subjects + ss
            predicates = predicates + ps
            objs = objs + os
    return subjects, predicates, objs

def compound_relational(doc):
    upos_string = ""
    compound_flag = False
    rule = 0
    compound_upos_patterns_rule_1 = [
        #RULE 1
        "VERB ADP NOUN CCONJ VERB",
        "VERB ADP PROPN CCONJ VERB",
        "VERB ADP DET NOUN CCONJ VERB",

        "VERB ADP NOUN CCONJ AUX VERB",
        "VERB ADP PROPN CCONJ AUX VERB",
        "VERB ADP DET NOUN CCONJ AUX VERB"
    ]

        #RULE 2
    compound_upos_patterns_rule_2 = [
        "VERB NOUN CCONJ NOUN",
        "VERB NOUN CCONJ PROPN",
        "VERB PROPN CCONJ NOUN",
        "VERB PROPN CCONJ PROPN"
    ]
        #RULE 3
    compound_upos_patterns_rule_3 = [
        "NOUN CCONJ NOUN VERB"
    ]

        #RULE 4
    compound_upos_patterns_rule_4 = [
        "ADJ CCONJ ADJ VERB",
        "ADJ CCONJ ADV VERB",
        "ADV CCONJ ADJ VERB",
        "ADV CCONJ ADV VERB"
    ]

    for sentence in doc.sentences:
        for word in sentence.words:
            upos_string += word.upos + " "
    for pattern in compound_upos_patterns_rule_1:
        comp = re.search(pattern, upos_string)
        if comp:
            compound_flag = bool(comp)
            rule = 1
    for pattern in compound_upos_patterns_rule_2:
        comp = re.search(pattern, upos_string)
        if comp:
            compound_flag = bool(comp)
            rule = 2
    for pattern in compound_upos_patterns_rule_3:
        comp = re.search(pattern, upos_string)
        if comp:
            compound_flag = bool(comp)
            rule = 3
    for pattern in compound_upos_patterns_rule_4:
        comp = re.search(pattern, upos_string)
        if comp:
            compound_flag = bool(comp)
            rule = 4

    return compound_flag, rule
    # return True

def break_compound_relational(doc, rule):
    queries = []
    case_flag = True
    obl_flag = True
    cc_flag = True
    conj_flag = True
    we = ""
    wh = ""
    wi = ""
    wj = ""
    wk = ""
    if rule == 1:
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.deprel == "case" and case_flag:
                    wi = sentence.words[word.head-1]
                    wh = word
                    case_flag = False
                elif word.deprel == "obl" and obl_flag:
                    we = sentence.words[word.head-1]
                    wi = word
                    obl_flag = False
                elif word.deprel == "cc" and cc_flag:
                    wk = sentence.words[word.head-1]
                    wj = word
                    cc_flag = False
                elif word.deprel == "conj" and conj_flag:
                    we = sentence.words[word.head-1]
                    wk = word
                    conj_flag = False
        s1 = ""
        s1_flag = True
        s2 = ""
        s2_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                # Conditions to change the flags
                if word.text == we.text:
                    s2_flag = False

                # Add words to Question s1
                if s1_flag:
                    s1 = s1 + " " + word.text

                # Add words to Question s2
                if s2_flag:
                    s2 = s2 + " " + word.text

                # Conditions to change the flags
                if word.text == wi.text:
                    s1_flag = False
                if word.text == wj.text:
                    s2_flag = True

        queries.append(s1.strip())
        queries.append(s2.strip())
    return queries

def generate_triple_relational(query):
    doc = nlp(query)
    print("==================Generate Triple RElation=====================")
    print(doc.text)
    subjects = []
    objs = []
    predicates = []
    predicate = ""
    subject_flag = True
    for sentence in doc.sentences:
        for word in sentence.words:
            # if the word is a head noun (noun or proper noun)
            if word.upos == 'NOUN' or word.upos == "PROPN":
                if subject_flag:
                    subjects.append(word)
                    subject_flag = False
                elif not subject_flag:
                    objs.append(word)
                    predicates.append(predicate)
                    predicate = ""
                    subject_flag = True
                    obj = word
            # if next head noun should be subject
            elif subject_flag:
                # But if the word is verb then last obj should be the next subject as well
                # and the verb should be first part of predicate
                if word.upos == "VERB":
                    subjects.append(obj)
                    predicate += word.text
                    subject_flag = False
                # If the word is a preposition then it gets added in the predicate
                elif word.upos == "ADP":
                    predicate += word.text.capitalize()
                    print("predicate", end=" ")
                    print(predicate)
            # If next head noun should be object
            elif not subject_flag:
                # But if the word is a verb then it is the first part of predicate
                if word.upos == "VERB":
                    predicate += word.text
                # If the word is a preposition then it gets added in the predicate
                elif word.upos == "ADP":
                    predicate += word.text.capitalize()
        print("========Subject, Object==========")
        print_triples(subjects, predicates, objs)
    return subjects, predicates, objs

def print_triples(subjects, predicates, objs):
    for (subject, predicate, obj) in zip(subjects, predicates, objs):
        print(subject.text, predicate, obj.text)


if __name__ == '__main__':
    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }
    nlp = stanza.Pipeline(**param_dict)
    doc = nlp("Which professor teaches us NLU?")
    doc = nlp("Which professor teaches about Natural Language Understanding?")
    doc = nlp("Which female actor played in Casablanca and is married to writer born in Rome?")
    # doc = nlp("Which female actor is married to writer born in Rome and played in Casablanca")
    # doc = nlp("Which river traverses Mississippi or Alaska")
    # doc = nlp("Which rivers and lakes traverse Alaska")
    # doc = nlp("Which is the least and most populated state in America")
    triples = get_user_triples(doc)
    print("===================TRIPLES=====================")
    for subject, predicate, obj in triples:
        pass
        # print(predicate)
    # print("===============================================")


