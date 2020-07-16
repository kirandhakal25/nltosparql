import stanza
import re

def get_user_triples(doc):
    subjects = []
    predicates = []
    objs = []

    is_compound, rule = compound_non_reln(doc)

    if is_compound:
        queries = break_compound_non_reln(doc, rule)
        for query in queries:
            ss, ps, os = generate_triple_non_reln(query)
            subjects = subjects + ss
            predicates = predicates + ps
            objs = objs + os
        return (queries)
    else:
        print("tadaaa")

def compound_non_reln(doc):
    upos_string = ""
    compound_flag = False
    rule = 0

    compound_upos_patterns_rule_1 = [
        "AUX (DET)? NOUN CCONJ NOUN",
    ]

    compound_upos_patterns_rule_2 = [
        "ADJ CCONJ ADJ NOUN"
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
    return compound_flag, rule

def break_compound_non_reln(doc, rule):
    if rule == 1:
        queries = []
        wd = ""
        wf = ""
        wg = ""
        wk = ""
        cop_flag = True
        nsubj_flag = True
        cc_flag = True
        conj_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.deprel == 'cop' and cop_flag:
                    wd = word
                    cop_flag = False
                # print (word.id, word.text, word.head, sentence.words[word.head - 1].text, '-', word.deprel)
                if word.deprel == 'nsubj' and nsubj_flag:
                    wf = word
                    nsubj_flag = False
                if word.deprel == 'cc' and cc_flag:
                    wg = word
                    cc_flag = False
                if word.deprel == 'conj' and conj_flag:
                    wk = word
                    conj_flag = False
        s1 = ""
        s1_flag = True
        s2 = ""
        s2_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                # Conditions to change the flags
                if word.text == wf.text:
                    s2_flag = False

                # Add words to Question s1
                if s1_flag:
                    s1 = s1 + " " + word.text

                # Add words to Question s2
                if s2_flag:
                    s2 = s2 + " " + word.text

                # Conditions to change the flags
                if word.text == wf.text:
                    s1_flag = False

                if word.text == wk.text:
                    s1_flag = True

                if word.text == wg.text:
                    s2_flag = True

        queries.append(s1.strip())
        queries.append(s2.strip())
        print(s1)
        print(s2)
        return queries

    elif rule == 2:
        queries = []
        wi = ""
        wh = ""
        wj = ""
        cc_flag = True
        conj_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.deprel == 'cc' and cc_flag:
                    wi = word
                    cc_flag = False
                if word.deprel == 'conj' and conj_flag:
                    wh = sentence.words[word.head - 1]
                    wj = word
                    conj_flag = False

        s1 = ""
        s1_flag = True
        s2 = ""
        s2_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                # Conditions to change the flags
                if word.text == wh.text:
                    s2_flag = False

                if word.text == wj.text:
                    s2_flag = True

                # Add words to Question s1
                if s1_flag:
                    s1 = s1 + " " + word.text

                # Add words to Question s2
                if s2_flag:
                    s2 = s2 + " " + word.text

                # Conditions to change the flags
                if word.text == wh.text:
                    s1_flag = False

                if word.text == wj.text:
                    s1_flag = True

        queries.append(s1.strip())
        queries.append(s2.strip())
        print(s1)
        print(s2)
        return queries

def generate_triple_non_reln(query):

if __name__ == '__main__':
    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }
    nlp = stanza.Pipeline(**param_dict)
    # doc = nlp("What is the population and area of the most populated state?")
    doc = nlp("Which is the shortest and longest river in America?")
    # doc = nlp("Which is the highest mountain in Germany?")
    # doc = nlp("What is Angela's birth name?")
    # doc = nlp("Which rivers and lakes traverse Alaska")

    triples = get_user_triples(doc)
    print("===================TRIPLES=====================")
    for subject, predicate, obj in triples:
        print(subject.text, predicate, obj.text)
    print("===============================================")