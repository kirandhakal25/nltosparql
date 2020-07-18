import stanza
import re


def get_user_triples_relational(doc, pipeline):
    subjects = []
    predicates = []
    objs = []
    upos_sentence = ""
    query_ending_with_verb_pattern = "ADP .* (PROPN)|(NOUN) VERB$"
    for sentence in doc.sentences:
        for word in sentence.words:
            upos_sentence += word.upos + " "
    upos_sentence = upos_sentence.strip()
    query_ending_with_verb = bool(re.search(query_ending_with_verb_pattern, upos_sentence))
    print(upos_sentence)
    print(query_ending_with_verb)

    is_compound, rule = compound_relational(doc)
    if is_compound:
        queries = break_compound_relational(doc, rule)
        # print(queries)
        for query in queries:
            if not query.lower().startswith("wh"):
                ss, ps, os = generate_triple_relational(query, pipeline)
                subjects = subjects + ss
                predicates = predicates + ps
                objs = objs + os
            else:
                ss, ps, os = generate_triple_who_relational(query, pipeline)
                subjects = subjects + ss
                predicates = predicates + ps
                objs = objs + os
    elif doc.text.capitalize().startswith("Wh"):
        ss, ps, os = generate_triple_who_relational(doc.text, pipeline)
        subjects = subjects + ss
        predicates = predicates + ps
        objs = objs + os
    else:
        ss, ps, os = generate_triple_relational(doc.text, pipeline)
        subjects = subjects + ss
        predicates = predicates + ps
        objs = objs + os
    return zip(subjects, predicates, objs)

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
    if rule == 1:
        queries = break_with_rule_1(doc)
    elif rule == 2:
        queries = break_with_rule_2(doc)
    elif rule == 3:
        queries = break_with_rule_3(doc)
    elif rule == 4:
        # This requires handling adjective part
        # The queries are successfully broken into two but the triples aren't extracted. Encountered error.
        queries = break_with_rule_4(doc)

    return queries


def break_with_rule_1(doc):
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

def break_with_rule_2(doc):
    queries = []
    we = wh = wi = wj = ""
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel == "obj":
                we = sentence.words[word.head-1]
                wh = word
            elif word.deprel == "cc":
                wj = sentence.words[word.head-1]
                wi = word
    s1 = ""
    s2 = ""
    s1_flag = True
    s2_flag = True

    for sentence in doc.sentences:
        for word in sentence.words:
            if word.text == wh.text:
                s2_flag = False
            elif word.text == wj.text:
                s2_flag = True
            if s1_flag:
                s1 = s1 + " " + word.text
            if s2_flag:
                s2 = s2 + " " + word.text
            if word.text == wh.text:
                s1_flag = False
            elif word.text == wj.text:
                s2_flag = False

    queries.append(s1.strip())
    queries.append(s2.strip())
    return queries


def break_with_rule_3(doc):
    queries = []
    we = wh = wi = wj = ""
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel == "nsubj":
                we = sentence.words[word.head - 1]
                wh = word
            elif word.deprel == "cc":
                wh = sentence.words[word.head - 1]
                wi = word
            elif word.deprel == "conj":
                wh = sentence.words[word.head - 1]
                wj = word

    s1 = ""
    s2 = ""
    s1_flag = True
    s2_flag = True
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.text == we.text:
                s1_flag = True
            elif word.text == wh.text:
                s2_flag = False
            elif word.text == wj.text:
                s2_flag = True

            if s1_flag:
                s1 = s1 + " " + word.text
            if s2_flag:
                s2 = s2 + " " + word.text

            if word.text == wh.text:
                s1_flag = False

    queries.append(s1.strip())
    queries.append(s2.strip())
    return queries

def break_with_rule_4(doc):
    queries = []
    we = wh = wi = wj = ""
    advmod_flag = 0
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel == "advmod" and advmod_flag == 0:
                we = sentence.words[word.head - 1]
                wh = word
                advmod_flag += 1
            elif word.deprel == "advmod" and advmod_flag == 1:
                wj = word
                advmod_flag += 1
            elif word.deprel == "cc":
                wj = sentence.words[word.head - 1]
                wi = word
            elif word.deprel == "conj":
                wh = sentence.words[word.head - 1]
                wj = word

    s1 = ""
    s2 = ""
    s1_flag = True
    s2_flag = True
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.text == wh.text:
                s2_flag = False
            elif word.text == wj.text:
                s2_flag = True

            if s1_flag:
                s1 = s1 + " " + word.text
            if s2_flag:
                s2 = s2 + " " + word.text

            if word.text == wh.text:
                s1_flag = False
            elif word.text == wj.text:
                s1_flag = True

    queries.append(s1.strip())
    queries.append(s2.strip())
    return queries


def generate_triple_relational(query, pipeline):
    doc = pipeline(query)
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
                    subjects.append(word.text)
                    subject_flag = False
                elif not subject_flag:
                    objs.append(word.text)
                    predicates.append(predicate)
                    predicate = ""
                    subject_flag = True
                    obj = word.text
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
            # If next head noun should be object
            elif not subject_flag:
                # But if the word is a verb then it is the first part of predicate
                if word.upos == "VERB":
                    predicate += word.text
                # If the word is a preposition then it gets added in the predicate
                elif word.upos == "ADP":
                    predicate += word.text.capitalize()
    return subjects, predicates, objs


def generate_triple_who_relational(query, pipeline):
    doc = pipeline(query)
    subjects = []
    objs = []
    predicates = []
    predicate = ""
    subject_flag = True

    for sentence in doc.sentences:
        for word in sentence.words:
            print(f'{word.text} \t {sentence.words[word.head - 1].text} \t {word.deprel}')
            if word.deprel == 'nsubj':
                subjects.append("?" + word.text.lower())
            if word.deprel == 'obj':
                objs.append(word.text)
            if word.deprel == 'root':
                predicates.append(word.text.lower())
            # if (word.deprel == 'conj') and sentence.words[word.head - 1].text == targets[0].text:
            #     targets.append(word)

    return subjects, predicates, objs

# def generate_triple_relational_verbend(query):
#     doc = nlp(query)
#     subjects = []
#     objs = []
#     predicates = []
#     predicate = ""
#
#     for sentence in doc.sentences:
#         for word in sentence.words:
#             print(f'{word.text} \t {sentence.words[word.head - 1].text} \t {word.deprel}')
#



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
    doc = nlp("Which rivers traverse Mississippi or Alaska")
    doc = nlp("who killed Caesar?")
    doc = nlp("In which continent does the Nile traverse")
    # doc = nlp("Which is the least and most populated state in America") # Dependency relation not correctly given by stanza
    # Needs handling adjective part to handle most populated state and least populated state.
    # doc = nlp("Which is the most and least populated state in America") # However, dependency relation given by stanza for this is correct
    # for sentence in doc.sentences:
    #     for word in sentence.words:
    #         print(f'{word.text} \t {sentence.words[word.head-1].text} \t {word.deprel}')
    triples = get_user_triples(doc, nlp)
    print("===================TRIPLES=====================")
    for subject, predicate, obj in triples:
        print(subject, predicate, obj)
    print("===============================================")


