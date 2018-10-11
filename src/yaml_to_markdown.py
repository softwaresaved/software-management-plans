#!/usr/bin/env python

"""
Read in YAML file with software management plan advice and guidance
and print it out in Markdown.

    usage: python yaml_to_markdown.py [-h] [-f FILE] [-t TYPE]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  YAML configuration file
      -t TYPE, --type TYPE  Document type
                            ('paper' | 'template' | 'markdown-template')

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
      licence-tag: licence tag, from SPDX, https://spdx.org/licenses/.
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
* licence-tag: 1
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
TITLE = "title"
VERSION = "version"
INTRO = "intro"
USAGE = "usage"
ACKS = "acks"
SECTIONS = "sections"
SECTION = "section"
QUESTIONS = "questions"
QUESTION = "question"
CONSIDER = "consider"
GUIDANCE = "guidance"

PAPER = "paper"
MARKDOWN_TEMPLATE = "markdown-template"
TEMPLATE = "template"


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


def write_paper(document):
    """
    Write out software management plan paper as Markdown.

    :param document: software management plan
    :type document: dict
    """
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
    write_paper_body(document[SECTIONS])


def write_paper_body(sections):
    """
    Write out software management plan paper body as Markdown.

    Process given list of dictionaries, each corresponding to a single
    section of a software management plan and output these as
    Markdown.

    * Each section title is represented as a level 2 heading.
    * Introductory text, if any, follows as paragraphs.
    * Each question is represented as a level 3 heading.
    * Each question's questions to consider and guidance are
      represented as bulleted lists.

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


def write_template(document):
    """
    Write out software management plan template as Markdown.

    This Markdown is intended to be used as an intermediary before
    onward conversion into another format e.g. to docx, odt or
    html, using, for example, pandoc.

    The Markdown starts with:

        ---
        title: PROJECT-NAME Software Management Plan
        ---

    :param document: software management plan
    :type document: dict
    """
    print("---")
    print((TITLE + ": PROJECT-NAME Software Management Plan"))
    print("---\n")
    write_template_body(document[SECTIONS])


def write_template_body(sections):
    """
    Write out software management plan template body as Markdown.

    Process given list of dictionaries, each corresponding to a single
    section of a software management plan and output these as
    Markdown.

    * Each section title is represented as a level 2 heading.
    * Each question is represented as a level 3 paragraph.
    * Each question's questions to consider are represented as
      plain text on separate lines.

    This Markdown is intended to be used as an intermediary before
    onward conversion into another format e.g. to docx, odt or
    html, using, for example, pandoc.

    :param sections: sections
    :type sections: list of dict
    """
    for section in sections:
        print(("## " + section[SECTION] + "\n"))
        for question in section[QUESTIONS]:
            print(("### " + question[QUESTION] + "\n"))
            if CONSIDER in list(question.keys()):
                print("Questions to consider:\n")
                for consider in question[CONSIDER]:
                    print((consider + "\n"))
            else:
                # Insert non-breaking spaces into Markdown so that
                # they are not ignored during downstream conversion.
                print("&nbsp;\n\n&nbsp;\n\n&nbsp;\n\n")


def write_markdown_template(document):
    """
    Write out software management plan template as Markdown.

    This Markdown is intended to be used as a standalone
    Markdown document.

    :param document: software management plan
    :type document: dict
    """
    print(("# PROJECT-NAME Software Management Plan\n"))
    write_markdown_template_body(document[SECTIONS])


def write_markdown_template_body(sections):
    """
    Write out software management plan template body as Markdown.

    Process given list of dictionaries, each corresponding to a single
    section of a software management plan and output these as
    Markdown.

    * Each section title is represented as a level 2 heading.
    * Each question is represented as a level 3 paragraph.
    * Each question's questions to consider are represented as
      a bulleted list on separate lines, embedded within a block
      quote.

    :param sections: sections
    :type sections: list of dict
    """
    for section in sections:
        print(("## " + section[SECTION] + "\n"))
        for question in section[QUESTIONS]:
            print(("### " + question[QUESTION] + "\n"))
            if CONSIDER in list(question.keys()):
                print("> Questions to consider:")
                print(">")
                for consider in question[CONSIDER]:
                    print(("> * " + consider))
            else:
                print("> ...")
            print("")


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
    parser.add_argument("-t", "--type",
                        default=PAPER,
                        dest="type",
                        help="Document type ('paper' | 'template')")
    args = parser.parse_args()
    if not args.file:
        parser.error("Missing file name")
    return args


def yaml_to_markdown(args):
    """
    Process YAML file and output desired file.

    :param args: command-line arguments.
    :type args: argparse.Namespace
    """
    file_name = args.file
    doc_type = args.type
    document = read_file(file_name)
    if doc_type == TEMPLATE:
        write_template(document)
    elif doc_type == MARKDOWN_TEMPLATE:
        write_markdown_template(document)
    else:
        write_paper(document)


if __name__ == '__main__':
    command_line_args = parse_command_line_arguments()
    yaml_to_markdown(command_line_args)
