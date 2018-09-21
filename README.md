# Software Management Plans

[The Software Sustainability Institute](https://www.software.ac.uk).

Sources and scripts for creating software management plan checklists in various formats.

For more information see:

* [Software Management Plans](https://www.software.ac.uk/software-management-plans) web page on The Software Sustainability Institute web site.
* [DMPonline](http://dmponline.dcc.ac.uk/) service from [The Digital Curation Centre](https://www.dcc.ac.uk) which hosts Software Management Plan templates.

---

## About these instructions

* These instructions were tested on Ubuntu 16.04.3 LTS xenial.
* Other versions of the tools may also be usable.
* Installing tools requires you to have sudo access to install and configure software (or a local system administrator to do this for you):

```bash
sudo su -
```

---

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

* If you already have Python you can skip this step. If you don't have Python then we recommend [Miniconda Python](https://conda.io/miniconda.html).
* Either Python 2.7+ or Python 3.6+ can be used.

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

* If you have Anaconda Python you can skip this step.

```bash
pip install pyyaml
```

### Microsoft TrueType core fonts:

Install Microsoft TrueType core fonts:

```bash
apt-get install ttf-mscorefonts-installer
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

---

## Create Markdown checklist

Run:

```bash
make pdf
```

This will process the files in `data/` and create a Markdown checklist in `build/markdown/`.

---

## Create HTML checklist

Run:

```bash
make html
```

This will create a Markdown checklist, as above, then convert this into an HTML checklist in `build/html/`.

---

## Check links

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

---

## Create PDF checklist

Run:

```bash
make pdf
```

This will create an HTML checklist, as above, then convert this into a PDF checklist in `build/pdf/`.

**Troubleshooting**

If you see an error like:

```
terminate called after throwing an instance of 'std::bad_alloc'Page 2 of 5
  what():  std::bad_alloc
Makefile:57: recipe for target 'build/pdf/<FILENAME>.pdf' failed
make: *** [build/pdf/<FILENAME>.pdf] Aborted (core dumped)
make: *** Deleting file 'build/pdf/<FILENAME>.pdf'
```

then it may be that one or more image files used in the guide are too big and causing `wkhtmltopdf`, which creates PDFs, to run out of memory. Try resizing the images and try again.

---

## Deposit in Zenodo (sample metadata, for information only)

Zenodo metadata:

* Communities: Zenodo
* Upload type: Publication (for guides), Software (for source)
* Publication type: Working paper
* Click Digital Object Identifier => Reserve DOI
* Publication date: YYYY-MM-DD
* Title:
* Authors: 
* Description:
* Version: X.Y
* Keywords:
  - research software
  - research outputs
  - software management plan
  - software sustainability
  - software sustainability institute
* Additional notes: The Software Sustainability Institute is supported by EPSRC grant EP/H043160/1 and EPSRC/BBSRC and ESRC grant EP/N006410/1.
* Funding: delete default entry.

---

## Contributing

See [Contributing](./CONTRIBUTING.md).

---

## Copyright and Licence

Copyright (c) 2014-2018, The University of Edinburgh

* Guidance (in markdown/ directory): Creative Commons Attribution 4.0 International
* Source code: Apache License, Version 2.0, January 2004

For full details, see [LICENCE](./LICENCE).
