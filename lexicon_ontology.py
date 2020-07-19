"""
Stores the actual ontology used.
"""

from lexicon import LexicalEntry, Lexicon


lexicon = Lexicon()

instr_entry_args = {
    'label': 'Instructor',
    'part_of_speech': 'noun',
    'type': 'Class',
    'ontotriples':
    [
        {
            'label': 'Instructor',
            'category': 'subject',
            'associated_predicate': 'teaches',
            'associated_object': 'Course'
        },
        {
            'label': 'Instructor',
            'category': 'object',
            'associated_predicate': 'isTaughtBy',
            'associated_subject': 'Course'
        },
        {
            'label': 'Instructor',
            'category': 'subject',
            'associated_predicate': 'isInstructorOf',
            'associated_object': 'Course'
        }
    ]
}

assistant_entry_args = {
    'label': 'Assistant',
    'part_of_speech': 'noun',
    'type': 'Class',
    'ontotriples':
    [
        {
            'label': 'Assistant',
            'category': 'subject',
            'associated_predicate': 'teaches',
            'associated_object': 'Course'
        },
        {
            'label': 'Assistant',
            'category': 'object',
            'associated_predicate': 'isTaughtBy',
            'associated_subject': 'Course'
        },
        {
            'label': 'Assistant',
            'category': 'subject',
            'associated_predicate': 'isAssistantOf',
            'associated_object': 'Course'
        }
    ]
}

teach_entry_args = {
    'label': 'teaches',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'teaches',
            'category': 'predicate',
            'associated_subject': 'Instructor',
            'associated_object': 'Course'
        }
    ]
}

is_taught_by_entry_args = {
    'label': 'isTaughtBy',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isTaughtBy',
            'category': 'predicate',
            'associated_subject': 'Course',
            'associated_object': 'Instructor'
        }
    ]
}

is_instructor_of_entry_args = {
    'label': 'isInstructorOf',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isInstructorOf',
            'category': 'predicate',
            'associated_subject': 'Assistant',
            'associated_object': 'Course'
        }
    ]
}

is_assistant_of_entry_args = {
    'label': 'isAssistantOf',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isAssistantOf',
            'category': 'predicate',
            'associated_subject': 'Assistant',
            'associated_object': 'Course'
        }
    ]
}

assist_entry_args = {
    'label': 'assists',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'assists',
            'category': 'predicate',
            'associated_subject': 'Assistant',
            'associated_object': 'Course'
        }
    ]
}

is_assisted_by_entry_args = {
    'label': 'isAssistedBy',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isAssistedBy',
            'category': 'predicate',
            'associated_subject': 'course',
            'associated_object': 'Assistant'
        }
    ]
}

course_entry_args = {
    'label': 'Course',
    'part_of_speech': 'noun',
    'type': 'class',
    'ontotriples':
    [
        {
            'label': 'Course',
            'category': 'object',
            'associated_predicate': 'teaches',
            'associated_subject': 'Instructor'
        },
        {
            'label': 'Course',
            'category': 'subject',
            'associated_predicate': 'isTaughtBy',
            'associated_object': 'Instructor'
        },
        {
            'label': 'Course',
            'category': 'object',
            'associated_predicate': 'isAssistantOf',
            'associated_subject': 'Assistant'
        }
    ]
}

nlu_entry_args = {
    'label': 'NLU',
    'part_of_speech': 'noun',
    'type': 'Course',
    'ontotriples':
    [
        {
            'label': 'NLU',
            'category': 'object',
            'associated_predicate': 'teaches',
            'associated_subject': 'ProfDung'
        },
        {
            'label': 'NLU',
            'category': 'subject',
            'associated_predicate': 'isTaughtBy',
            'associated_object': 'ProfDung'
        },
        {
            'label': 'NLU',
            'category': 'object',
            'associated_predicate': 'isInstructorOf',
            'associated_subject': 'ProfDung'
        },
        {
            'label': 'NLU',
            'category': 'object',
            'associated_predicate': 'isAssistantOf',
            'associated_subject': 'Joe'
        }
    ]
}

matt_entry_args = {
    'label': 'ProfMatt',
    'part_of_speech': 'noun',
    'type': 'instructor',
    'ontotriples':
        [
            {
                'label': 'ProfMatt',
                'category': 'subject',
                'associated_predicate': 'teaches',
                'associated_object': 'ML'
            },
            {
                'label': 'ProfMatt',
                'category': 'object',
                'associated_predicate': 'isTaughtBy',
                'associated_subject': 'ML'
            },
            {
                'label': 'ProfMatt',
                'category': 'subject',
                'associated_predicate': 'teaches',
                'associated_object': 'WAE'
            },
            {
                'label': 'ProfMatt',
                'category': 'object',
                'associated_predicate': 'isTaughtBy',
                'associated_subject': 'WAE'
            },
            {
                'label': 'ProfMatt',
                'category': 'subject',
                'associated_predicate': 'isInstructorOf',
                'associated_object': 'WAE'
            },
            {
                'label': 'ProfMatt',
                'category': 'subject',
                'associated_predicate': 'teaches',
                'associated_object': 'MachineVision'
            },
            {
                'label': 'ProfMatt',
                'category': 'object',
                'associated_predicate': 'isTaughtBy',
                'associated_subject': 'MachineVision'
            }
        ]
}

wae_entry_args = {
    'label': 'WAE',
    'part_of_speech': 'noun',
    'type': 'Course',
    'ontotriples':
    [
        {
            'label': 'WAE',
            'category': 'object',
            'associated_predicate': 'teaches',
            'associated_subject': 'ProfMatt'
        },
        {
            'label': 'WAE',
            'category': 'subject',
            'associated_predicate': 'isTaughtBy',
            'associated_object': 'ProfMatt'
        },
        {
            'label': 'WAE',
            'category': 'object',
            'associated_predicate': 'isInstructorOf',
            'associated_subject': 'ProfMatt'
        }
    ]
}

dung_entry_args = {
    'label': 'ProfDung',
    'part_of_speech': 'noun',
    'type': 'instructor',
    'ontotriples':
    [
        {
            'label': 'ProfDung',
            'category': 'subject',
            'associated_predicate': 'teaches',
            'associated_object': 'NLU'
        },
        {
            'label': 'ProfDung',
            'category': 'object',
            'associated_predicate': 'isTaughtBy',
            'associated_subject': 'NLU'
        },
        {
            'label': 'ProfDung',
            'category': 'subject',
            'associated_predicate': 'isInstructorOf',
            'associated_object': 'NLU'
        }
    ]
}

lexicon.add_entries([
    instr_entry_args,
    teach_entry_args,
    course_entry_args,
    nlu_entry_args,
    dung_entry_args,
    matt_entry_args,
    assistant_entry_args,
    is_instructor_of_entry_args,
    is_assistant_of_entry_args,
    wae_entry_args
])
