#!/usr/bin/env python

"""
Read in YAML file with software management plan advice and guidance
and print it out in MarkDown.

    usage: python yaml_to_markdown.py [-h] [-f FILE] [-o FORMAT]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  YAML configuration file
      -o FORMAT, --output FORMAT
                            Output format ('text' | 'table' | 'list')

The YAML file must hold a single document. The document must be
structured as follows:

    ---
    metadata:
      title: Title.
      author: Author.
      date-meta: Data for HTML meta-data tag.
      citation-date: Human-readable date.
      version: Version number.
      doi: DOI of document being produced.
      website: URL of web site associated with document.
      keywords: list of keywords.
      licence: licence information.
    intro: Introductory text.
    usage: Usage conditions.
    acks: Acknowledgements.
    sections:
    - section: Section name e.g. About your software
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
    - section: Another section name.
      ...

The following constraints hold for each field:

* metadata: 1
* title: 1
* author: 1
* date-meta: 1
* citation-date: 1
* version: 1
* doi: 1
* website: 1
* keywords: 0+
* licence: 1
* sections: 1
* section: 0+
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

from argparse import ArgumentParser
import yaml

METADATA = "metadata"
INTRO = "intro"
USAGE = "usage"
ACKS = "acks"
SECTIONS = "sections"
SECTION = "section"
QUESTIONS = "questions"
QUESTION = "question"
CONSIDER = "consider"
GUIDANCE = "guidance"

FORMAT_TEXT = "text"
FORMAT_TABLE = "table"
FORMAT_LIST = "list"

FUDGE = 20
"""
FUDGE as a fudge factor for first column for Pandoc-compatible grid
table format in MarkDown (see Extension:grid_tables in
http://pandoc.org/README.html), the format needed to include
paragraphs and bulleted lists within table cells. No word in the first
column of a grid table should be wider than this.
"""


def read_file(file_name):
    """
    Read YAML file and return contents.

    :param file_name: file name
    :type file_name: str or unicode
    :return: document
    :rtype: dict
    """
    document = None
    with open(file_name, "r") as stream:
        document = yaml.load(stream)
    return document


def write_markdown(document, output_format):
    """
    Write out software management plan as Markdown.

    :param document: software management plan
    :type document: dict
    :param output_format: one of FORMAT_TEXT (default), FORMAT_TABLE,
    FORMAT_LIST
    :type output_format: str or unicode
    """
    sections = document[SECTIONS]
    if output_format == FORMAT_TABLE:
        write_markdown_tables(sections)
    elif output_format == FORMAT_LIST:
        write_markdown_list(sections)
    else:
        print("---")
        for (key, value) in list(document[METADATA].items()):
            print((key + ": " + str(value)))
        print("---\n")
        print("## Introduction\n")
        print((document[INTRO] + "\n"))
        print("## Use of this checklist\n")
        print((document[USAGE] + "\n"))
        print("## Acknowledgements\n")
        print((document[ACKS] + "\n"))
        write_markdown_text(sections)


def write_left_cell(text):
    """
    Write cell for left-hand column.

    :param text: cell text
    :type text: str or unicode
    """
    for word in text.split(" "):
        print(("| " + word + ((FUDGE - len(word) - 2) * " ") + " | |"))


def write_right_cell(empty_cell, text):
    """
    Write cell for right-hand column.

    :param text: cell text
    :type text: str or unicode
    """
    print((empty_cell + " " + text + " |"))


def write_header():
    """
    Write checklist header.
    """
    checklist = "Checklist"
    print(("| " + checklist + ((FUDGE - len(checklist) - 2) * " ") +
           " | Guidance and Questions to consider |"))


def write_markdown_tables(sections):
    """
    Process a list of dictionaries, each corresponding to a single
    section of a software management plan, and output these as
    Markdown, with each section being rendered as a table.
    Each table has a row for each question and its associated
    questions to consider and  guidance. If the section has
    introductory paragraphs then these are rendered before the table.

    This function uses FUDGE as a fudge factor for first column for
    Pandoc-compatible grid table format in MarkDown.

    :param sections: sections
    :type sections: list of dict
    """
    row = "+" + ("-" * FUDGE) + "+" + ("-" * (80 - FUDGE - 4)) + "+"
    header_row = "+" + ("=" * FUDGE) + "+" + ("=" * (80 - FUDGE - 4)) + "+"
    empty_cell = "|" + (" " * FUDGE) + "|"
    blank_row = empty_cell + " |"
    for section in sections:
        print(("## " + section[SECTION] + "\n"))
        if INTRO in list(section.keys()):
            for intro in section[INTRO]:
                print((intro + "\n"))
        print(row)
        write_header()
        print(header_row)
        for question in section[QUESTIONS]:
            write_left_cell(question[QUESTION])
            if CONSIDER in list(question.keys()):
                write_right_cell(empty_cell, "**Questions to consider:**")
                print(blank_row)
                for consider in question[CONSIDER]:
                    write_right_cell(empty_cell, "* " + consider)
                print(blank_row)
            if GUIDANCE in list(question.keys()):
                write_right_cell(empty_cell, "**Guidance:**")
                print(blank_row)
                for guidance in question[GUIDANCE]:
                    if isinstance(guidance, list):
                        for element in guidance:
                            write_right_cell(empty_cell, "* " + element)
                    else:
                        write_right_cell(empty_cell, guidance)
                    print(blank_row)
            print(row)
        print("\n")


def write_markdown_list(sections):
    """
    Process a list of dictionaries, each corresponding to a
    single section of a software management plan, and output these as
    a Markdown table, with a row for each section name, and each
    question within a section.

    Associated questions to consider, guidance and introductory
    paragraphs are not rendered.

    Tables are in the Pandoc-compatible pipe table format in Markdown
    (see Extension:pipe_tables in http://pandoc.org/README.html).

    :param sections: sections
    :type sections: list of dict
    """
    print(("| Checklist |"))
    print(("|" + 80 * "-" + "|"))
    for section in sections:
        print(("| **" + section[SECTION] + "** |"))
        for question in section[QUESTIONS]:
            print(("| " + question[QUESTION] + " |"))


def write_markdown_text(sections):
    """
    Process a list of dictionaries, each corresponding to a single
    section of a software management plan and output these as
    Markdown, with each question being rendered as a text with its
    questions to consider and guidance as bulleted lists and
    paragraphs within that section.

    :param sections: sections
    :type sections: list of dict
    """
    for section in sections:
        print(("## " + section[SECTION] + "\n"))
        if INTRO in list(section.keys()):
            for intro in section[INTRO]:
                print((intro + "\n"))
        for question in section[QUESTIONS]:
            print(("### " + question[QUESTION] + "\n"))
            if CONSIDER in list(question.keys()):
                print("**Questions to consider:**\n")
                for consider in question[CONSIDER]:
                    print(("* " + consider))
                print("")
            if GUIDANCE in list(question.keys()):
                print(("**Guidance:**\n"))
                for guidance in question[GUIDANCE]:
                    if isinstance(guidance, list):
                        for element in guidance:
                            print(("* " + element))
                        print("")
                    else:
                        print((guidance + "\n"))


def parse_command_line_arguments():
    """
    Parse command-line arguments, printing usage information if there
    are any problems.

    :return: command-line arguments
    :rtype: argparse.Namespace
    """
    parser = ArgumentParser("python yaml_to_markdown.py")
    parser.add_argument("-f", "--file",
                        dest="file",
                        help="YAML configuration file")
    parser.add_argument("-o", "--output",
                        default=FORMAT_TEXT,
                        dest="format",
                        help="Output format ('text' | 'table' | 'list')")
    args = parser.parse_args()
    if not args.file:
        parser.error("Missing file name")
    return args


def yaml_to_markdown(file_name, output_format):
    """
    Set up command-line arguments and parse these, printing usage
    information if there are any problems, or processing the YAML file
    otherwise.

    :param file_name: file name
    :type file_name: str or unicode
    :param output_format: one of FORMAT_TEXT (default), FORMAT_TABLE,
    FORMAT_LIST
    :type output_format: str or unicode
    """
    document = read_file(file_name)
    write_markdown(document, output_format)


if __name__ == '__main__':
    command_line_args = parse_command_line_arguments()
    yaml_to_markdown(command_line_args.file, command_line_args.format)
