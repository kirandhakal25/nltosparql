def find_target_position(user_triple, target):
    result = None
    position = 0

    for idx, term in enumerate(user_triple):
        if target == term.lower():
            position = idx
            result = term
    return result, position


def evaluate_type(triple, target):
    _, target_position = find_target_position(triple, target)

    variable = "?" + triple[target_position].lower()
    type_declaration = (variable, "rdf:type", target.strip("s").capitalize())

    triple_list = list(triple)
    triple_list.pop(target_position)
    triple_list.insert(target_position, variable)

    return [type_declaration, tuple(triple_list)]


def construct_query(triples, targets):
    # make query triples for inside where clause {}
    query_triples = []
    # not enough target for query -> Which instructor teaches NLU and WAE?

    if len(targets) == len(triples):
        for input_triple, target in zip(triples, targets):
            if not input_triple[0].startswith("?wh"):
                # if not wh question
                ontology_triple = evaluate_type(input_triple, target)
            else:
                # if other questions
                ontology_triple = input_triple

            query_triples.append(ontology_triple)
    elif len(targets) == 1:
        for input_triple in triples:
            if not input_triple[0].startswith("?wh"):
                # if not wh question
                ontology_triple = evaluate_type(input_triple, targets[0])
            else:
                # if other questions
                ontology_triple = input_triple

            query_triples.append(ontology_triple)

    # concatenate targets into ?x ?y for before where clause
    target_string = ""
    for target in targets:
        target_string += f"?{target} "

    target_string.strip()

    main_query = f"SELECT {target_string} WHERE " + "{\n"
    triple_string = None
    for query_triple in query_triples:
        if type(query_triple) is list:
            for qt in query_triple:
                triple_string = ' '.join(qt) + " .\n"
                main_query += triple_string
        else:
            triple_string = ' '.join(query_triple) + " .\n"
            main_query += triple_string

    main_query += "}"

    return main_query


if __name__ == '__main__':
    input_targets = ["instructor"]
    input_ontology_triple = ("Instructor", "teaches", "NLU")
    input_ontology_triple2 = ("Instructor", "teaches", "WAE")

    input_triples = [input_ontology_triple, input_ontology_triple2]

    # triple_subject = None
    #
    # sample_ontology_triple = ("Instructor", "teaches", "NLU")
    #
    # triples = evaluate_type(sample_ontology_triple, input_target)
    #
    # # If multiple triples, make a list of triples and pass iteratively
    #
    # query = f'SELECT ?{input_target} WHERE {{ {triples[0]} }}'

    print("===========RESULTS============")
    print(construct_query(input_triples, input_targets))
    print("=============End==============")