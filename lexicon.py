class LexicalEntry:
    def __init__(self, **kwargs):
        self.label = kwargs.get("label")

        self.part_of_speech = kwargs.get("part_of_speech")
        self.type = kwargs.get("type")
        self.ontotriples = kwargs.get("ontotriples")

        self.associated_predicate = kwargs.get("associated_predicate")
        self.associated_object = kwargs.get("associated_object")
        self.associated_subject = kwargs.get("associated_subject")

        self.canonical_form = CanonicalForm(written_rep=kwargs.get("written_rep"))
        self.lexical_sense = LexicalSense(reference=kwargs.get("reference"))


class CanonicalForm:
    def __init__(self, **kwargs):
        self.written_rep = kwargs.get("written_rep")


class LexicalSense:
    def __init__(self, **kwargs):
        self.reference = kwargs.get("reference")


class Lexicon:
    def __init__(self):
        self.entries = {}

    def add_entry(self, entry: LexicalEntry):
        self.entries[entry.label] = entry
