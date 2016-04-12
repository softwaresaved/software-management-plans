#!/usr/bin/env python

"""
Read in YAML file with software management plan advice and guidance
and print it out in MarkDown.

    Usage: yaml_to_markdown.py [-f 'text' | 'table' | 'checklist' ] file

    Options:
      -h, --help            show this help message and exit
      -f FORMAT, --format=FORMAT
                            Advice format ('text' or 'table' or
                            'checklist')

Each document in the YAML file should correspond to a single section
of advice and guidance and be structured as follows:

    ---
    section: Section name e.g. About your software
    intro:
    - Context
    - Each entry corresponds to a paragraph.
    questions:
    - question: A question.
      consider: 
      - A sub-question to consider.
      - Another sub-question to consider.
      guidance:
      - Some guidance.
      - Each entry corresponds to a paragraph.
      -
        - Bulleted list entry within guidance.
        - Bulleted list entry within guidance.
      - Some more guidance.
    - question: A question with no guidance.
      consider: 
      - A sub-question to consider.
      - Another sub-question to consider.
    - question: A question with no sub-questions.
      guidance:
      - Some guidance.
      - Each entry corresponds to a paragraph.
    - question: A question with no guidance or sub-questions.

The following constraints hold for each field:

* section: 1
* intro: 0 or 1. If provided then its sequence must have 1+ entries.
* questions: 1
* question: 1+
* consider: 0 or 1 per question. If provided then its sequence must
  have 1+ entries.
* guidance: 0 or 1 per question. If provided then its sequence must
  have 1+ entries.
* Colons, :, in text should be surrounded by text or, for a lead-in
  to a list use a ",". Otherwise YAML will interpret the colon as
  its delimiter. As an example:

    - guidance:
      - Examples of this approach include:one, two, three
      - Other examples include,
      -
        - four.
        - five.
"""

from optparse import OptionParser
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
ADVICE_CHECKLIST = "checklist"

FUDGE = 20
"""
FUDGE as a fudge factor for first column for Pandoc-compatible grid
table format in MarkDown (see Extension:grid_tables in
http://pandoc.org/README.html), the format needed to include
paragraphs and bulleted lists within table cells. No word in the first
column of a grid table should be wider than this.
"""

def convert_file(file_name, advice_format):
    """
    Read YAML software management plan file and print it out in
    MarkDown.
    """
    with open(file_name, "r") as stream:
        sections = yaml.load_all(stream)
        if (advice_format == ADVICE_TEXT):
            output_text(sections)
            output_table(sections)
        elif (advice_format == ADVICE_TABLE):
            output_table(sections)
        else:
            output_summary(sections)


def output_text(sections):
    """
    Read in a sequence of YAML documents, each corresponding to a
    single section of a software management plan and print out as
    MarkDown, with each question being rendered as a section with
    its questions to consider and guidance as bulleted lists and
    paragraphs within that section.
    """
    for section in sections:
        print("## " + section[SECTION] + "\n")
        if INTRO in section.keys():
            for intro in section[INTRO]:
                print(intro + "\n")
        for question in section[QUESTIONS]:
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


def print_header():
     checklist = "Checklist"
     print("| " + checklist + ((FUDGE - len(checklist) - 2) * " ") +
           " | Guidance and Questions to consider |")


def output_table(sections):
    """
    Read in a sequence of YAML documents, each corresponding to a
    single section of a software management plan and print out as
    MarkDown, with each section being rendered as a table, with a row
    for each question and its associated questions to consider and
    guidance. If the section has introductory paragraphs then these
    are rendered before the table. 

    This function uses FUDGE as a fudge factor for first column for
    Pandoc-compatible grid table format in MarkDown.
    """
    row = "+" + ("-" * FUDGE) + "+" + ("-" * (80 - FUDGE - 4)) + "+"
    header_row = "+" + ("=" * FUDGE) + "+" + ("=" * (80 - FUDGE - 4)) + "+"
    empty_cell = "|" + (" " * FUDGE) + "|"
    blank_row = empty_cell + " |"
    for section in sections:
        print("## " + section[SECTION] + "\n")
        if INTRO in section.keys():
            for intro in section[INTRO]:
                print(intro + "\n")
        print(row)
        print_header()
        print(header_row)
        for question in section[QUESTIONS]:
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


def output_summary(sections):
    """
    Read in a sequence of YAML documents, each corresponding to a
    single section of a software management plan and print out as
    MarkDown table, with a row for each section name, and each
    question within a section. Associated questions to consider,
    guidance and introductory paragraphs are not rendered.

    Tables are in the Pandoc-compatible pipe table format in Markdown
    (see Extension:pipe_tables in http://pandoc.org/README.html).
    """
    print "| Checklist |"
    print "|" + 80 * "-" + "|"
    for section in sections:
        print("| **" + section[SECTION] + "** |")
        for question in section[QUESTIONS]:
            print("| " + question[QUESTION] + " |")


def yaml_to_markdown():
    """
    Set up command-line arguments and parse these, printing usage
    information if there are any problems, or processing the
    YAML file otherwise.
    """
    parser = OptionParser(
        usage="%prog [-f 'text' | 'table' | 'checklist' ] file")
    parser.add_option("-f", "--format",
                      default=ADVICE_TABLE,
                      dest="format",
                      help="Advice format ('text' or 'table' or 'checklist')")
    (options, args) = parser.parse_args()
    if (len(args) == 0):
        parser.error("Missing file name")
    file_name = args[0]
    convert_file(file_name, options.format)


if __name__ == '__main__':
    yaml_to_markdown();
