PANDOC ?= pandoc
PANDOC_FLAGS = --smart
HTML_PDF ?= html-pdf

# Markdown files.
ALL_MD = $(wildcard *.md)
EXCLUDE_MD = README.md LICENSE.md
SRC_MD = $(filter-out $(EXCLUDE_MD),$(ALL_MD))

# Outputs.
DST_HTML = $(patsubst %.md,%.html,$(SRC_MD))
DST_PDF = $(patsubst %.md,%.pdf,$(SRC_MD))

# Default action is to show what commands are available.
all : commands

## clean    : Clean up temporary and auto-generated files.
clean :
	@rm -f $(DST_HTML)
	@rm -f $(DST_PDF)
	@rm -rf $$(find . -name '*~' -print)

## html     : Build HTML pages.
html : $(DST_HTML)

## pdf      : Build PDF documents.
pdf : $(DST_PDF)

# Pattern to build HTML page.
%.html : %.md _layouts/page.html $(FILTERS)
	${PANDOC} -s -t html \
	    ${PANDOC_FLAGS} \
	    --template=_layouts/page \
	    -o $@ $<

# Pattern to build PDF document.
%.pdf : %.html
	${HTML_PDF} $< $@

## commands : Display available commands.
commands : Makefile
	@sed -n 's/^##//p' $<

## settings : Show variables and settings.
settings :
	@echo 'PANDOC:' $(PANDOC)
	@echo 'HTML_PDF:' $(HTML_PDF)
	@echo 'SRC_MD:' $(SRC_MD)
	@echo 'DST_HTML:' $(DST_HTML)
	@echo 'DST_PDF:' $(DST_PDF)
