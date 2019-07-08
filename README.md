# Checklist for a Software Management Plan

[The Software Sustainability Institute](https://www.software.ac.uk).

Sources and scripts for creating a software management plan checklist in various formats.

For more information see:

- [Software Management Plans](https://www.software.ac.uk/software-management-plans) web page on The Software Sustainability Institute web site.
- [DMPonline](http://dmponline.dcc.ac.uk/) service from [The Digital Curation Centre](https://www.dcc.ac.uk) which hosts Software Management Plan templates.

## Published versions

- The Software Sustainability Institute. (2018). Checklist for a Software Management Plan. v1.0\. doi:[10.5281/zenodo.2159713](https://doi.org/10.5281/zenodo.2159713)
- The Software Sustainability Institute. (2018). Checklist for a Software Management Plan. v0.2\. doi:[10.5281/zenodo.1460504](https://doi.org/10.5281/zenodo.1460504)
- The Software Sustainability Institute. (2016). Checklist for a Software Management Plan. v0.1\. doi:[10.5281/zenodo.1422657](https://doi.org/10.5281/zenodo.1422657)

--------------------------------------------------------------------------------

# Developer guide

## About these instructions

- These instructions were tested on Ubuntu 16.04.3 LTS xenial.
- Other versions of the tools may also be usable.
- Installing tools requires you to have sudo access to install and configure software (or a local system administrator to do this for you):

```bash
sudo su -
```

--------------------------------------------------------------------------------

## Install dependencies

### Pandoc

Install [Pandoc](https://pandoc.org/) document converter:

```bash
sudo apt-get install pandoc
pandoc --version
```

```
pandoc 1.16.0.2
```

### wkhtmltopdf

Install [wkhtmltopdf](https://wkhtmltopdf.org/) HTML-to-PDF converter (using latest stable version, 0.12.5, for Ubuntu 16.04 Xenial, on web site):

```bash
wget https://downloads.wkhtmltopdf.org/0.12/0.12.5/wkhtmltox_0.12.5-1.xenial_amd64.deb
sudo apt install ./wkhtmltox_0.12.5-1.xenial_amd64.deb
wkhtmltopdf  --version
```

```
wkhtmltopdf 0.12.5 (with patched qt)
```

### Python

Install [Python](https://www.python.org/)

- If you already have Python you can skip this step. If you don't have Python then we recommend [Miniconda Python](https://conda.io/miniconda.html).
- Either Python 2.7+ or Python 3.6+ can be used.

**Miniconda Python 2.7**

```bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda2.sh
bash miniconda2.sh -b -p $HOME/miniconda2
```

Set environment and check:

```bash
source $HOME/miniconda2/bin/activate
python -V
```

```
Python 2.7.15 :: Anaconda, Inc.
```

**Miniconda Python 3.6**

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3.sh
bash miniconda3.sh -b -p $HOME/miniconda3
```

Set environment and check:

```bash
source $HOME/miniconda3/bin/activate
python -V
```

```
Python 3.6.5 :: Anaconda, Inc.
```

### pyyaml

Install [pyyaml](https://pyyaml.org/):

- If you have Anaconda Python you can skip this step.

```bash
pip install pyyaml
```

### Microsoft TrueType core fonts:

Install Microsoft TrueType core fonts:

```bash
apt-get install ttf-mscorefonts-installer
```

### Python dev

This needs to be installed otherwise `python setup.py install` won't work below (pre-pend with sudo if your setup requires this)

```bash
apt-get install python-dev
```

### linkchecker

Install [linkchecker](https://github.com/linkchecker/linkchecker) 9.4:

```bash
wget https://github.com/linkchecker/linkchecker/archive/v9.4.0.tar.gz
tar -xf v9.4.0.tar.gz
cd linkchecker-9.4.0/
pip install -r requirements.txt
python setup.py install
linkchecker -V
```

```
LinkChecker 9.4.0 released xx.xx.xxxx
Copyright (C) 2000-2014 Bastian Kleineidam
```

--------------------------------------------------------------------------------

## Checkout the repository

You need to checkout the repository and then cd into the right directory (assumes git is installed and working)

```bash
git clone https://github.com/softwaresaved/software-management-plans.git
cd software-management-plans
```

--------------------------------------------------------------------------------

## Create HTML and PDF checklist papers

Create HTML and PDF checklist papers for publication online or depositing in Zenodo (for example).

Run:

```bash
make papers
```

This creates an intermediate Pandoc Markdown checklist, then converts this into HTML and PDF papers. The papers are placed in `build/papers/`.

--------------------------------------------------------------------------------

## Check HTML links

Run:

```bash
make check-links
```

This will display broken links, if any.

If you see an error e.g.

```
Makefile:66: recipe for target 'check-links' failed
make: [check-links] Error 1 (ignored)
```

then this can be ignored (an error code of 1 means that the `linkchecker` program encountered one or more broken links).

A full report is created in `build/link-check.txt`.

**Beware:** Certain links may be identified as broken when they in fact exist. See the Linkchecker FAQ, [Q:I still get an error, but the page is definitely ok](https://wummel.github.io/linkchecker/faq.html).

--------------------------------------------------------------------------------

## Create Markdown, Word and OpenOffice/LibreOffice checkist templates

Create Markdown (md), Word (docx) and OpenOffice/LibreOffice (odt) checklist templates for publication online so researchers can use these in their projects.

Run:

```bash
make templates
```

This will create an intermediate Pandoc Markdown checklist, then convert this into Word and OpenOffice/LibreOffice templates, and it will also create a Markdown checklist. The templates are placed in `build/templates/`.

--------------------------------------------------------------------------------

## See all available Make commands

Run:

```bash
make
```

--------------------------------------------------------------------------------

## Supported Languages

The software management plan is available in English and German. To change the language settings you have to switch language variables for `YAML` and `YAML_TO_MD` in `Makefile`:

- `YAML = data/checklist_en.yaml` or `YAML = data/checklist_de.yaml`
- `YAML_TO_MD = src/yaml_to_markdown_en.py` or `YAML_TO_MD = src/yaml_to_markdown_en.py`

If you want to translate the software management plan into your preferred language, do the following:

1. copy `data/checklist_en.yaml` and `src/yaml_to_markdown_en.py` to the same folder
2. rename it, e.g. for Spanish: `data/checklist_es.yaml` and `src/yaml_to_markdown_es.py`
3. translate the content

--------------------------------------------------------------------------------

## Styles

**Note:** read this whole section before you run any of the commands. It shows you how to change the template formatting. If you are happy with the current formatting then there is no need to run the `pandoc` commands below.

`templates/doc.html` and `css/styles.css` determine the style of HTML and PDF papers.

`templates/reference.docx` and `templates/reference.odt` determine the style of Word and OpenOffice/LibreOffice templates. These were generated using the commands:

```
pandoc --print-default-data-file reference.odt > templates/reference.odt
pandoc --print-default-data-file reference.docx > templates/reference.docx
```

They were then customised so that:

- Titles and level 1-3 headings are black, bold, non-italics.
- Body Text / Text Body content, used for boiler-plate guidance in the templates, is surrounded by a border.

--------------------------------------------------------------------------------

# Contributing

See [Contributing](./CONTRIBUTING.md).

--------------------------------------------------------------------------------

# Copyright and Licence

Copyright (c) 2014-2018, The University of Edinburgh

- Guidance (in `markdown/` directory): Creative Commons Attribution 4.0 International
- Source code: Apache License, Version 2.0, January 2004

For full details, see [LICENCE](./LICENCE).

The Software Sustainability Institute provides the checklist on an "as-is" basis, makes no warranties regarding any information provided within and disclaims liability for damages resulting from using this information. You are solely responsible for determining the appropriateness of any advice and guidance provided and assume any risks associated with your use of this advice and guidance. If you have any questions regarding the right licence for your code or any other legal issues relating to it, consult with a professional for advice relating to your individual circumstances.

--------------------------------------------------------------------------------

## Acknowledgements

The checklist has its origins in:

Chue Hong, Neil (2014) "Writing and using a software management plan", The Software Sustainability Institute <http://www.software.ac.uk/resources/guides/software-management-plans>.

The checklist has evolved in response to feedback from: Mario Antonioletti, The Software Sustainability Institute; Neil Chue Hong, The Software Sustainability Institute; Peter Cock, The James Hutton Institute; Steve Crouch, The Software Sustainability Institute; Robert Davey, The Genome Analysis Centre; Carole Goble, The Software Sustainability Institute; Catherine Jones, STFC; Sarah Jones, The Digital Curation Centre; Katrin Leinweber, Technische Informationsbibliothek; Mark Plumbley, Centre for Vision, Speech and Signal Processing, University of Surrey; Chris Rawlings, Rothamsted Research; Marta Ribeiro, The Digital Curation Centre; John Robinson, The Software Sustainability Institute; Shoaib Sufi, The Software Sustainability Institute.

We also acknowledge the valuable assistance and generosity of [The Digital Curation Centre](http://www.dcc.ac.uk), particularly Sarah Jones and Marta Ribeiro, in supporting the writing of of software management plans within [DMPonline](http://dmponline.dcc.ac.uk/).
