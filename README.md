# Software Management Plans

[The Software Sustainability Institute](http://www.software.ac.uk) advice, guidance and services relating to Software Management Plans.

* [Issues](https://github.com/softwaresaved/software-management-plans/issues)
* [Software Management Plans](http://www.software.ac.uk/software-management-plans) web page on The Software Sustainability Institute web site.
* [DMPonline](https://dmponline.dcc.ac.uk/) service from [The Digital Curation Centre](http://www.dcc.ac.uk) which hosts Software Management Plan templates.

---

## Generate HTML and PDF

About these instructions:

* These instructions were tested on Ubuntu 14.04.4 LTS trusty.
* Other versions of the tools may also be usable.
* Installing tools requires you to have sudo access to install and configure software (or a local system administrator can do this for you):

```
$ sudo su -
```

Install [Git](https://git-scm.com/) version control tool:

```
$ apt-get install -y git
$ git --version
git version 1.9.1
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
$ apt-get install wkhtmltopdf
$ wkhtmltopdf -V
Name:
  wkhtmltopdf 0.9.6
```

Install [Node.js](https://nodejs.org/) JavaScript environment:

```
$ apt-get -y install nodejs
$ nodejs -v
v0.10.25
```

Create a symbolic link as third-party packages expect nodejs to be called node:

```
$ ln -s /usr/bin/nodejs /usr/bin/node
$ node -v
v0.10.25
```

Install [npm](https://www.npmjs.com/) Node.js package manager:

```
$ apt-get -y install npm
$ npm -v
1.3.10
```

Install [html-pdf](https://www.npmjs.com/package/html-pdf) Node.js package to convert HTML to PDF:

```
$ npm install -g html-pdf
```

Create HTML and PDF:

```
$ make pdf
```

### Notes

[Pandoc demos](http://pandoc.org/demos.html) use xelatex to convert MarkDown to PDF:

```
$ apt-get install texlive-xetex
$ pandoc --latex-engine=xelatex test.md -o test.pdf
```

I found that this gives PDFs that look like LaTeX documents, which I wasn't happy with the look of.

[markdown-pdf](https://www.npmjs.com/package/markdown-pdf) is a Node.js package to convert MarkDown to PDF:

```
$ npm install -g markdown-pdf
$ markdown-pdf test.md -o test.pdf
```

This didn't handle grid tables or hyperlinks well.
