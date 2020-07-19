import stanza
import re
import target


def get_user_triples_non_relational(doc, pipeline, targets):
    subjects = []
    predicates = []
    objs = []

    is_compound, rule = compound_non_reln(doc)
    # for sentence in doc.sentences:
    #     for word in sentence.words:
    #         print(word.text, word.upos)

    if is_compound:
        queries, cc = break_compound_non_reln(doc, rule)
        # print(queries)
        for query in queries:
            ss, ps, os = generate_triple_non_reln(query, pipeline, targets[0])
            # print(ss)
            # print(ps)
            subjects = subjects + ss
            predicates = predicates + ps
            objs = objs + os
    else:
        ss, ps, os = generate_triple_non_reln(doc.text, pipeline, targets[0])
        # print(ss)
        # print(ps)
        subjects = subjects + ss
        predicates = predicates + ps
        objs = objs + os
    return zip(subjects, predicates, objs)

def compound_non_reln(doc):
    upos_string = ""
    compound_flag = False
    rule = 0

    compound_upos_patterns_rule_1 = [
        "AUX (DET)? NOUN CCONJ NOUN",
        "AUX (DET)? NOUN CCONJ PROPN",
        "AUX (DET)? PROPN CCONJ NOUN",
        "AUX (DET)? PROPN CCONJ PROPN"
    ]

    compound_upos_patterns_rule_2 = [
        "ADJ CCONJ ADJ NOUN"
    ]

    compound_upos_patterns_rule_3 = [
        "AUX (DET)? NOUN ADP PROPN CCONJ PROPN"
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
        cc = wg
        return queries, cc

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
        cc = wi

        return queries, cc

    elif rule == 3:
        queries = []
        wi = ""
        wh = ""
        wj = ""
        cc_flag = True
        conj_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                # print(word.text, '-', sentence.words[word.head - 1].text, word.deprel)

                if word.deprel == 'cc' and cc_flag:
                    wi = word
                    # print('------------')
                    # print(wi)
                    # print(wi.text)
                    cc_flag = False
                if word.deprel == 'conj' and conj_flag:
                    wh = sentence.words[word.head - 1]
                    wj = word
                    # print(wh.text, wj.text)
                    conj_flag = False

        s1 = ""
        s1_flag = True
        s2 = ""
        s2_flag = True
        for sentence in doc.sentences:
            for word in sentence.words:
                # print(word.text, word.upos, word.deprel, '-', word.head, '-', sentence.words[word.head - 1].text)

        #         # Conditions to change the flags
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
        cc = wi
        # print(s1)
        # print(s2)

        return queries, cc


def generate_triple_non_reln(query, pipeline, target):
    doc = pipeline(query)
    subjects = []
    objects = []
    predicates = []
    pred = ""
    subject_flag = True
    prep_flag = True
    cop_flag = True
    wz= ''
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel == 'root':
                root = word

            if word.deprel == 'nsubj' and subject_flag:
                if word.upos == 'NOUN':
                    wx = word
                elif word.upos == 'PRON':
                    wx = root
                subject_flag = False
    for sentence in doc.sentences:
        for word in sentence.words:
            # print(word.text, word.deprel, '-', word.head, '-', sentence.words[word.head - 1].text)
            if word.deprel == 'case' and prep_flag:
                if word.text == 'of':
                    wz = sentence.words[word.head - 1].text
                    wy = word.text
                    prep_flag = False
                    pred = wx.text + '_' + wy
                    objects.append(wz)
                elif word.text == 'in':
                    pred = wx.text
                    wz = sentence.words[word.head - 1].text

                    objects.append(wz)
                    # print('--------')
                    # print(word.deprel, word.text, '-', word.head, '-', sentence.words[word.head - 1].text)
                elif word.text == "'s":
                    wy = sentence.words[word.head - 1]
                    if sentence.words[wy.head - 1].text == wx.text:
                        pred = wx.text
                        objects.append(wy.text)

        predicates.append(pred)
        subjects.append(target.capitalize())

    # print(subjects)
    # print(predicates)
    # print(objects)

    return subjects, predicates, objects


if __name__ == '__main__':

    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }
    nlp = stanza.Pipeline(**param_dict)
    # doc = nlp("What is the population and area of the most populated state?")
    # doc = nlp("Which is the shortest and longest river in America?")
    # doc = nlp("Who are the professors of NLU and DSA?")
    doc = nlp("Which is the highest mountain in Germany?")
    # doc = nlp("What is Angela's birth name?")
    # doc = nlp("Which rivers and lakes traverse Alaska")
    # doc = nlp("Who is the professor and TA of NLU?")
    # doc = nlp("What is the salary of Dung?")
    # doc = nlp("Who are the TA and professors of NLU and DSA?")

    target_words = target.get_targets(doc)
    targets = []
    for target_word in target_words:
        targets.append(target_word.text.lower())
    triples = get_user_triples_non_relational(doc, nlp, targets)
    print("===================TRIPLES=====================")
    for subject, predicate, obj in triples:
        print(subject, predicate, obj)
    print("===============================================")