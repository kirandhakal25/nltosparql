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

rep_entry_args = {
    'label': 'Representative',
    'part_of_speech': 'noun',
    'type': 'Class',
    'ontotriples':
    [
        {
            'label': 'Representative',
            'category': 'subject',
            'associated_predicate': 'represent',
            'associated_object': 'Course'
        },
    {
            'label': 'Representative',
            'category': 'subject',
            'associated_predicate': 'isRepresentativeOf',
            'associated_object': 'Course'
        },
        {
            'label': 'Representative',
            'category': 'object',
            'associated_predicate': 'isRepresentedBy',
            'associated_subject': 'Course'
        }
    ]
}

dept_entry_args = {
    'label': 'Department',
    'part_of_speech': 'noun',
    'type': 'Class',
    'ontotriples':
    [
        {
            'label': 'Department',
            'category': 'subject',
            'associated_predicate': 'offers',
            'associated_object': 'Course'
        },
        {
            'label': 'Department',
            'category': 'object',
            'associated_predicate': 'isOfferedBy',
            'associated_subject': 'Course'
        },
        {
            'label': 'Department',
            'category': 'object',
            'associated_predicate': 'isCourseIn',
            'associated_subject': 'Course'
        }
    ]
}

integer_entry_args = {
    'label': 'integer',
    'part_of_speech': 'verb',
    'type': 'object',
    'ontotriples':
    [
        {
            'label': 'integer',
            'category': 'object',
            'associated_subject': 'Instructor',
            'associated_predicate': 'age'
        }
    ]
}

age_entry_args = {
    'label': 'age',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'age',
            'category': 'predicate',
            'associated_subject': 'Instructor',
            'associated_object': 'integer'
        }
    ]
}

offers_entry_args = {
    'label': 'offers',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'offers',
            'category': 'predicate',
            'associated_subject': 'Department',
            'associated_object': 'Course'
        }
    ]
}

is_offered_by_args = {
    'label': 'isOfferedBy',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isOfferedBy',
            'category': 'predicate',
            'associated_subject': 'Course',
            'associated_object': 'Department'
        }
    ]
}

is_course_in_entry_args = {
    'label': 'isCourseIn',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isCourseIn',
            'category': 'predicate',
            'associated_subject': 'Course',
            'associated_object': 'Department'
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
            'associated_subject': 'Instructor',
            'associated_object': 'Course'
        }
    ]
}

is_rep_of_entry_args = {
    'label': 'isRepresentativeOf',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isRepresentativeOf',
            'category': 'predicate',
            'associated_subject': 'Representative',
            'associated_object': 'Course'
        }
    ]
}

is_instructor_in_entry_args = {
    'label': 'isInstructorIn',
    'part_of_speech': 'verb',
    'type': 'predicate',
    'ontotriples':
    [
        {
            'label': 'isInstructorIn',
            'category': 'predicate',
            'associated_subject': 'Instructor',
            'associated_object': 'Department'
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
        },
        {
            'label': 'Course',
            'category': 'subject',
            'associated_predicate': 'isOfferedBy',
            'associated_object': 'Department'
        },
        {
            'label': 'Course',
            'category': 'subject',
            'associated_predicate': 'isCourseIn',
            'associated_object': 'Department'
        },
        {
            'label': 'Course',
            'category': 'object',
            'associated_predicate': 'offers',
            'associated_subject': 'Department'
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
            'associated_predicate': 'offers',
            'associated_subject': 'ICT'
        },
        {
            'label': 'NLU',
            'category': 'subject',
            'associated_predicate': 'isOfferedBy',
            'associated_object': 'ICT'
        },
        {
            'label': 'NLU',
            'category': 'subject',
            'associated_predicate': 'isCourseIn',
            'associated_object': 'ICT'
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
        },
        {
            'label': 'NLU',
            'category': 'object',
            'associated_predicate': 'isRepresentativeOf',
            'associated_subject': 'Watsamon'
        }
    ]
}

ict_entry_args = {
    'label': 'ICT',
    'part_of_speech': 'noun',
    'type': 'Department',
    'ontotriples':
    [
        {
            'label': 'ICT',
            'category': 'object',
            'associated_predicate': 'isOfferedBy',
            'associated_subject': 'NLU'
        },
        {
            'label': 'ICT',
            'category': 'object',
            'associated_predicate': 'isCourseIn',
            'associated_subject': 'NLU'
        },
        {
            'label': 'ICT',
            'category': 'subject',
            'associated_predicate': 'offers',
            'associated_object': 'NLU'
        }
    ]
}

matt_entry_args = {
    'label': 'ProfMatt',
    'part_of_speech': 'noun',
    'type': 'Instructor',
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
    'type': 'Instructor',
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

jou_entry_args = {
    'label': 'Watsamon',
    'part_of_speech': 'noun',
    'type': 'Representative',
    'ontotriples':
    [
        {
            'label': 'Watsamon',
            'category': 'subject',
            'associated_predicate': 'represents',
            'associated_object': 'NLU'
        },
        {
            'label': 'Watsamon',
            'category': 'subject',
            'associated_predicate': 'isRepresentativeOf',
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
    wae_entry_args,
    dept_entry_args,
    offers_entry_args,
    is_offered_by_args,
    is_course_in_entry_args,
    rep_entry_args,
    jou_entry_args,
    is_rep_of_entry_args
])
