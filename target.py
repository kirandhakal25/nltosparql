import stanza
from user_triple_relational import verbend


def get_targets(doc):
    targets = []
    is_verb_end = verbend(doc)

    if not is_verb_end:
        for sentence in doc.sentences:
            for word in sentence.words:
                print(f'{word.text} \t {sentence.words[word.head-1].text} \t {word.deprel}')
                if word.deprel == 'nsubj':
                    targets.append(word)
                if word.deprel == 'nsubj:pass':
                    targets.append(word)
                if(word.deprel == 'conj') and sentence.words[word.head-1].text == targets[0].text:
                    targets.append(word)
    else:
        for sentence in doc.sentences:
            for word in sentence.words:
                print(f'{word.text} \t {sentence.words[word.head-1].text} \t {word.deprel}')
                if word.deprel == 'obj':
                    targets.append(word)
    return targets


if __name__ == '__main__':
    param_dict = {
        'lang': 'en',
        'processors': 'pos, lemma, tokenize, depparse',
        'use_gpu': True,
        'pos_batch_size': 3000
    }

    nlp = stanza.Pipeline(**param_dict)

    # doc = nlp("Who teaches NLU?")
    doc = nlp("What is the prerequisite of NLU?")  # Question for Equation 1a
    doc = nlp("What is the prerequisite, textbook and resource of NLU?")  # Question for Equation 1b
    doc = nlp("Who is the instructor, TA and secretary of NLU?")
    # doc = nlp("Which German actor was killed in a road crash?")                           #Question for Equation 2a
    # doc = nlp("Which German actor and musician and artist was killed in a road crash?")   #Question for Equation 2b
    doc = nlp("Who is oldest instructor?")
    print(doc.text)
    targets = get_targets(doc)
    print("===============TARGETS IDENTIFIED====================")
    for target in targets:
        print(target.text)
    print("=====================================================")
