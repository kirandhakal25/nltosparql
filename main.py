import argparse
from target import get_targets
import stanza

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

    targets = get_targets(nlp(args.input))

    print("")
    print("Got input question: ", args.input)

    [print("Targets identified: ", target.text) for target in targets]

    print("Finished conversion.")

