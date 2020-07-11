import stanza

def get_user_triples(doc):
    triples = []
    if compound(doc):
        queries = break_compound(doc)
        print(queries)
        for query in queries:
            triple = generate_triple(query)
            triples.append(triple)

    return triples

def compound(doc):
    return True

def break_compound(doc):
    queries = []
    queries.append(doc)
    return queries

def generate_triple(doc):
    triple = []
    triple_flag = 0
    for sentence in doc.sentences:
        for word in sentence.words:
            print(f'{word.text} \t {sentence.words[word.head-1].text} \t {word.deprel} \t {word.upos} \t {word.xpos}')
            if word.upos == 'NOUN' or word.upos == "PROPN":
                if triple_flag == 0:
                    triple.append(word)
                    triple_flag = 1
                elif triple_flag == 1:
                    triple.append(word)
                    triple_flag = 0
            elif word.upos == "VERB" and triple_flag == 1:
                triple.append(word)

    return triple


if __name__ == '__main__':
    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }
    nlp = stanza.Pipeline(**param_dict)
    doc = nlp("Which professor teaches NLU?")
    triples = get_user_triples(doc)
    print("===================TRIPLES=====================")
    for triple in triples:
        for word in triple:
            print(word.text, end =" ")
    print()
    print("===============================================")


