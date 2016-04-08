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

file_name = sys.argv[1]

def convert_file(file_name):
    """
    Read in a YAML software management plan advice and guidance
    file and print it out in MarkDown.
    """
    with open(file_name, "r") as stream:
        docs = yaml.load_all(stream)
        yaml_to_markdown(docs)

def yaml_to_markdown(docs):
    """
    Read in a sequence of YAML documents, each corresponding to a
    single section and of software management plan advice and guidance
    and print out as MarkDown.
    """
    print("---")
    print("title: Checklist for a Software Management Plan v0.1")
    print("---")

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

if __name__ == '__main__':
    file_name = sys.argv[1]
    convert_file(file_name)
