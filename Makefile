SMP ?= SMP_Checklist
SRC_YAML ?= $(SMP).yaml
HDR_MD ?= $(SMP).header.md

YAML_MD_SRC ?= yaml_to_markdown.py
YAML_MD ?= python $(YAML_MD_SRC)
PANDOC ?= pandoc
PANDOC_FLAGS = --smart
HTML_PDF ?= html-pdf
WKHTMLTOPDF ?= wkhtmltopdf

# Markdown files.
# SRC_YAML = $(wildcard *.yaml)
DST_MD = $(patsubst %.yaml,%.md,$(SRC_YAML))
DST_HTML = $(patsubst %.yaml,%.html,$(SRC_YAML))
DST_PDF = $(patsubst %.yaml,%.pdf,$(SRC_YAML))

# Default action is to show what commands are available.
all : commands

## clean    : Clean up temporary and auto-generated files.
clean :
	@rm -f $(DST_MD)
	@rm -f $(DST_HTML)
	@rm -f $(DST_PDF)
	@rm -rf $$(find . -name '*~' -print)

## md       : Build MarkDown pages.
md : $(DST_MD)

## html     : Build HTML pages.
html : $(DST_HTML)

## pdf      : Build PDF documents.
pdf : $(DST_PDF)

# Pattern to build MarkDown document.
%.md : %.yaml $(YAML_MD_SRC)
	cp $(HDR_MD) $@
	$(YAML_MD) $< >> $@

# Pattern to build HTML page.
%.html : %.md _layouts/page.html $(FILTERS)
	${PANDOC} -s --toc -t html \
	    ${PANDOC_FLAGS} \
	    --template=_layouts/page \
	    -o $@ $<

# Pattern to build PDF document.
%.pdf : %.html
	${WKHTMLTOPDF} $< $@

## commands : Display available commands.
commands : Makefile
	@sed -n 's/^##//p' $<

## settings : Show variables and settings.
settings :
	@echo 'YAML_MD:' $(YAML_MD)
	@echo 'PANDOC:' $(PANDOC)
	@echo 'HTML_PDF:' $(HTML_PDF)
	@echo 'WKHTMLTOPDF:' $(WKHTMLTOPDF)
	@echo 'SMP:' $(SMP)
	@echo 'SRC_YAML:' $(SRC_YAML)
	@echo 'HDR_MD:' $(HDR_MD)
	@echo 'DST_MD:' $(DST_MD)
	@echo 'DST_HTML:' $(DST_HTML)
	@echo 'DST_PDF:' $(DST_PDF)
