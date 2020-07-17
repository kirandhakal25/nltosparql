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
    type_declaration = (variable, "rdf:type", target.capitalize())

    triple_list = list(triple)
    triple_list.pop(target_position)
    triple_list.insert(target_position, variable)

    return type_declaration, tuple(triple_list)


if __name__ == '__main__':
    input_target = "instructor"
    input_ontology_triple = ("?who", "teaches", "NLU")

    # triple_subject = None
    #
    # sample_ontology_triple = ("Instructor", "teaches", "NLU")
    #
    # triples = evaluate_type(sample_ontology_triple, input_target)
    #
    # # If multiple triples, make a list of triples and pass iteratively
    #
    # query = f'SELECT ?{input_target} WHERE {{ {triples[0]} }}'

    if not input_ontology_triple[0].startswith("?who"):
        ontology_triple = evaluate_type(input_ontology_triple, input_target)
    else:
        ontology_triple = input_ontology_triple

    print("===========RESULTS============")
    print(ontology_triple)
    print("=============End==============")