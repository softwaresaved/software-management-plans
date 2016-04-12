SRC ?= SMP_Checklist
SRC_YAML ?= $(SRC).yaml
HDR_MD ?= $(SRC).header.md
YAML_MD ?= yaml_to_markdown.py
YAML_MD_FLAGS ?= -f text
PY_YAML_MD ?= python $(YAML_MD)
PANDOC ?= pandoc
PANDOC_FLAGS = --smart
PANDOC_TOC ?=
HTML_PDF ?= html-pdf
WKHTMLTOPDF ?= wkhtmltopdf

# Markdown files.
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

# Build MarkDown pages.
$(DST_MD) : $(SRC_YAML) $(HDR_MD) $(YAML_MD)
	cp $(HDR_MD) $@
	$(PY_YAML_MD) $(YAML_MD_FLAGS) $< >> $@

# Build HTML pages.
$(DST_HTML) : $(DST_MD) _layouts/page.html $(FILTERS)
	$(PANDOC) -s $(PANDOC_TOC) -t html \
	    $(PANDOC_FLAGS) \
	    --template=_layouts/page \
	    -o $@ $<

# Build PDF documents.
$(DST_PDF) : $(DST_HTML)
	$(WKHTMLTOPDF) $< $@

## commands : Display available commands.
commands : Makefile
	@sed -n 's/^##//p' $<

## settings : Show variables and settings.
settings :
	@echo 'YAML_MD:' $(YAML_MD)
	@echo 'YAML_MD_FLAGS:' $(YAML_MD_FLAGS)
	@echo 'PY_YAML_MD:' $(PY_YAML_MD)
	@echo 'PANDOC:' $(PANDOC)
	@echo 'PANDOC_TOC:' $(TOC)
	@echo 'HTML_PDF:' $(HTML_PDF)
	@echo 'WKHTMLTOPDF:' $(WKHTMLTOPDF)
	@echo 'SRC:' $(SRC)
	@echo 'SRC_YAML:' $(SRC_YAML)
	@echo 'HDR_MD:' $(HDR_MD)
	@echo 'DST_MD:' $(DST_MD)
	@echo 'DST_HTML:' $(DST_HTML)
	@echo 'DST_PDF:' $(DST_PDF)
