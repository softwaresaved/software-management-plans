#!/usr/bin/env python

"""
Program to read in a YAML software management plan advice and guidance 
file and print it out in MarkDown.

Each document in the YAML file corresponds to a single section of the
advice and guidance and is structured as follows:

    ---
    section: About your software - a minimal Software Management Plan
    intro:
    - Context
    - More context
    questions:
    - question: A question with sub-questions and guidance?
      consider: 
      - A sub-question?
      - Another sub-question?
      guidance:
      - Some guidance
      -
        - List for guidance   
        - List for guidance   
      - Some more guidance
    - question: A question with no guidance?
      consider: 
      - A sub-question?
      - Another sub-question?
    - question: A question with no sub-questions?
      guidance:
      - Some guidance
      - Some more guidance
    - question: A question with no guidance or sub-questions?

The following constraints are on each field:

* section: 1+ per document.
* intro: 0 or 1 per document. If provided then its sequence must
  have 1+ members.
* questions: 1 per document.
* question: 1+ per questions.
* consider: 0 or 1 per question. If provided then its sequence must
  have 1+ members.
* guidance: 0 or 1 per question. If provided then its sequence must
  have 1+ members.
* Colons, :, in text should be surrounded by text or, for a lead-in
  to a list a ",". Otherwise YAML will interpret it as a delimiter.
  - "Examples include:one, two, three"
  - "Examples include,"

The above renders into MarkDown as follows:

    ## About your software - a minimal Software Management Plan

    Context

    More context

    ### A question with sub-questions and guidance?

    **Questions to consider:**

    * A sub-question?
    * Another sub-question?

    **Guidance:**

    Some guidance

    * List for guidance
    * List for guidance

    Some more guidance

    ### A question with no guidance?

    **Questions to consider:**

    * A sub-question?
    * Another sub-question?

    ### A question with no sub-questions?

    Some guidance

    Some more guidance

    ### A question with no guidance or sub-questions?
    
    ---    
"""

import sys
import yaml

SECTION = "section"
INTRO = "intro"
QUESTIONS = "questions"
QUESTION = "question"
CONSIDER = "consider"
GUIDANCE = "guidance"

ADVICE_TEXT = "text"
ADVICE_TABLE = "table"

FUDGE = 20
"""
Fudge factor for first column. No word in the first column should be
wider than this word otherwise the MarkDown won't be in a
Pandoc-compatiblegrid table format.
"""

def convert_file(file_name, advice_format):
    """
    Read in a YAML software management plan advice and guidance
    file and print it out in MarkDown.
    """
    with open(file_name, "r") as stream:
        docs = yaml.load_all(stream)
        if (advice_format == ADVICE_TEXT):
            yaml_to_markdown(docs)
        else:
            yaml_to_markdown_table(docs)

def yaml_to_markdown(docs):
    """
    Read in a sequence of YAML documents, each corresponding to a
    single section and of software management plan advice and guidance
    and print out as MarkDown.
    """
    for doc in docs:
        print("## " + doc[SECTION] + "\n")
        if INTRO in doc.keys():
            for intro in doc[INTRO]:
                print(intro + "\n")
        for question in doc[QUESTIONS]:
            print("### " + question[QUESTION] + "\n")
            if CONSIDER in question.keys():
                print("**Questions to consider:**\n")
                for consider in question[CONSIDER]:
                    print("* " + consider)
                print("")
            if GUIDANCE in question.keys():
                print("**Guidance:**\n")
                for guidance in question[GUIDANCE]:
                    if (type(guidance) == list):
                        for element in guidance:
                            print("* " + element)
                        print("")
                    else:
                        print(guidance + "\n")

def print_left_cell(text):
    for word in text.split(" "):
        print("| " + word + ((FUDGE - len(word) - 2) * " ") +  " | |")

def print_right_cell(empty_cell, text):
    print(empty_cell + " " + text + " |")

def yaml_to_markdown_table(docs):
    """
    Read in a sequence of YAML documents, each corresponding to a
    single section and of software management plan advice and guidance
    and print out as MarkDown.
    """
    row = "+" + ("-" * FUDGE) + "+" + ("-" * (80 - FUDGE - 4)) + "+"
    empty_cell = "|" + (" " * FUDGE) + "|"
    blank_row = empty_cell + " |"
    for doc in docs:
        print("## " + doc[SECTION] + "\n")
        if INTRO in doc.keys():
            for intro in doc[INTRO]:
                print(intro + "\n")
        print(row)
        for question in doc[QUESTIONS]:
            print_left_cell(question[QUESTION])
            if CONSIDER in question.keys():
                print_right_cell(empty_cell, "**Questions to consider:**")
                print(blank_row)
                for consider in question[CONSIDER]:
                    print_right_cell(empty_cell, "* " + consider)
                print(blank_row)
            if GUIDANCE in question.keys():
                print_right_cell(empty_cell, "**Guidance:**")
                print(blank_row)
                for guidance in question[GUIDANCE]:
                    if (type(guidance) == list):
                        for element in guidance:
                            print_right_cell(empty_cell, "* " + element)
                    else:
                        print_right_cell(empty_cell, guidance)
                    print(blank_row)
                    print(row)
        print("\n")

from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [-f 'text' | 'table'] file")
    parser.add_option("-f", "--format",
                      default=ADVICE_TABLE,
                      dest="format",
                      help="Advice format ('text' or 'table')")
    (options, args) = parser.parse_args()
    if (len(args) == 0):
        parser.error("Missing file name")
    file_name = args[0]
    convert_file(file_name, options.format)
