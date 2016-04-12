# Software Management Plans

[The Software Sustainability Institute](http://www.software.ac.uk) advice, guidance and services relating to Software Management Plans.

* [Issues](https://github.com/softwaresaved/software-management-plans/issues)
* [Software Management Plans](http://www.software.ac.uk/software-management-plans) web page on The Software Sustainability Institute web site.
* [DMPonline](https://dmponline.dcc.ac.uk/) service from [The Digital Curation Centre](http://www.dcc.ac.uk) which hosts Software Management Plan templates.

---

## Create HTML and PDF documents

About these instructions:

* These instructions were tested on Ubuntu 14.04.4 LTS trusty.
* Other versions of the tools may also be usable.
* Installing tools requires you to have sudo access to install and configure software (or a local system administrator can do this for you):

```
$ sudo su -
```

### Install dependencies

Install [Git](https://git-scm.com/) version control tool:

```
$ apt-get install -y git
$ git --version
git version 1.9.1
```

Install [pyyaml](http://pyyaml.org/) YAML parser for Python:

```
$ pip install pyyaml
```

Install [Pandoc](http://pandoc.org/) document converter:

```
$ wget https://github.com/jgm/pandoc/releases/download/1.17.0.2/pandoc-1.17.0.2-1-amd64.deb
$ dpkg -i pandoc-1.17.0.2-1-amd64.deb
$ pandoc --version
pandoc 1.17.0.2
```

Install [wkhtmltopdf](http://wkhtmltopdf.org/) HTML-to-PDF converter:

```
$ wget http://download.gna.org/wkhtmltopdf/0.12/0.12.3/wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
$ tar -xf wkhtmltox-0.12.3_linux-generic-amd64.tar.xz
$ export PATH=$PWD/wkhtmltox/bin:$PATH
$ wkhtmltopdf --version
wkhtmltopdf 0.12.3 (with patched qt)
```

### Create documents

Create SMP_Checklist.html and SMP_Checklist.pdf:

```
$ make pdf
```

Create documents with tables of contents:

```
$ PANDOC_TOC=--toc make pdf
```

Create HTML document with tabular checklist format:

```
$ YAML_MD_FLAGS="-f table" make html
```

Create HTML document with tabular checklist format and table of contents:

```
$ PANDOC_TOC=--toc YAML_MD_FLAGS="-f table" make html
```

Create HTML document with tabular checklist format, consisting of the key sections and questions only with no advice and guidance:

```
$ YAML_MD_FLAGS="-f summary" make html
```

**Note:** while PDFs can be created from the HTML with tabular checklists, the tables do not currently get converted correctly by wkhtmltopdf (0.12.3).

### Notes

[Pandoc demos](http://pandoc.org/demos.html) use xelatex to convert MarkDown to PDF:

```
$ apt-get install texlive-xetex
$ pandoc --latex-engine=xelatex test.md -o test.pdf
```

I found that this gives PDFs that look like LaTeX documents, which I wasn't happy with the look of.
