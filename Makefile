PAPER_PREFIX = SoftwareManagementPlanChecklist
TEMPLATE_PREFIX = SoftwareManagementPlanTemplate

# Available languages: en, de
YAML = data/checklist_en.yaml
HTML_LAYOUT = templates/doc.html
IMAGES = $(wildcard images/*.png)
CSS = css/style.css
DOCX_STYLE = templates/reference.docx
ODT_STYLE = templates/reference.odt

# Available languages: en, de
YAML_TO_MD = src/yaml_to_markdown_en.py
PANDOC = pandoc
WKHTMLTOPDF = wkhtmltopdf --disable-smart-shrinking
LINK_CHECKER = linkchecker --check-extern --no-robots

BUILD = build
BUILD_PAPER = $(BUILD)/papers
HTML_PAPER_DIR = $(BUILD_PAPER)/html
PANDOC_MD_PAPER = $(BUILD_PAPER)/$(PAPER_PREFIX).md
HTML_PAPER = $(HTML_PAPER_DIR)/$(PAPER_PREFIX).html
PDF_PAPER = $(BUILD_PAPER)/$(PAPER_PREFIX).pdf

BUILD_TEMPLATE = $(BUILD)/templates
PANDOC_MD_TEMPLATE = $(BUILD_TEMPLATE)/$(TEMPLATE_PREFIX).tmp.md
MD_TEMPLATE = $(BUILD_TEMPLATE)/$(TEMPLATE_PREFIX).md
DOCX_TEMPLATE = $(BUILD_TEMPLATE)/$(TEMPLATE_PREFIX).docx
ODT_TEMPLATE = $(BUILD_TEMPLATE)/$(TEMPLATE_PREFIX).odt

LINK_REPORT = $(BUILD)/link-check.txt

# Default action is to show what commands are available.
.PHONY : all
all : commands

## clean         : Clean up temporary and auto-generated files.
.PHONY : clean
clean :
	@rm -rf $(BUILD)
	@rm -rf $$(find . -name '*~' -print)

## html-paper    : Create HTML paper.
.PHONY : html-paper
html-paper : $(HTML_PAPER)

## pdf-paper     : Create PDF paper.
.PHONY : pdf-paper
pdf-paper : $(PDF_PAPER)

## papers        : Create HTML and PDF papers.
.PHONY : papers
papers : html-paper pdf-paper

## md-template   : Create Markdown template.
.PHONY : md-template
md-template : $(MD_TEMPLATE)

## docx-template : Create DOCX template.
.PHONY : docx-template
docx-template : $(DOCX_TEMPLATE)

## odt-template  : Create ODT template.
.PHONY : odt-template
odt-template : $(ODT_TEMPLATE)

## templates     : Create Markdown, DOCX and ODT templates.
.PHONY : templates
templates : md-template docx-template odt-template

# Create Pandoc Markdown for creating paper.
$(PANDOC_MD_PAPER) : $(YAML) $(YAML_TO_MD)
	mkdir -p $(BUILD_PAPER)
	python $(YAML_TO_MD) -f $< -t paper > $@

# Convert Pandoc Markdown to HTML paper.
$(HTML_PAPER) : $(PANDOC_MD_PAPER) $(IMAGES) $(HTML_LAYOUT) $(CSS)
	mkdir -p $(HTML_PAPER_DIR)
	cp -r images/ $(HTML_PAPER_DIR)
	cp -r css/ $(HTML_PAPER_DIR)
	$(PANDOC) -t html -c $(CSS) --template=$(HTML_LAYOUT) -o $@ $<

# Convert HTML to PDF paper.
$(PDF_PAPER) : $(HTML_PAPER)
	mkdir -p $(BUILD_PAPER)
	$(WKHTMLTOPDF) $< $@

# Create Pandoc Markdown for creating template.
$(PANDOC_MD_TEMPLATE) : $(YAML) $(YAML_TO_MD)
	mkdir -p $(BUILD_TEMPLATE)
	python $(YAML_TO_MD) -f $< -t template > $@

# Create Markdown template.
$(MD_TEMPLATE) : $(YAML) $(YAML_TO_MD)
	mkdir -p $(BUILD_TEMPLATE)
	python $(YAML_TO_MD) -f $< -t markdown-template > $@

# Convert Pandoc Markdown to DOCX template.
$(DOCX_TEMPLATE) : $(PANDOC_MD_TEMPLATE) $(DOCX_STYLE)
	mkdir -p $(BUILD_TEMPLATE)
	$(PANDOC) -t docx --reference-doc=$(DOCX_STYLE) -o $@ $<

# Convert Pandoc Markdown to ODT template.
$(ODT_TEMPLATE) : $(PANDOC_MD_TEMPLATE) $(ODT_STYLE)
	mkdir -p $(BUILD_TEMPLATE)
	$(PANDOC) -t odt --reference-odt=$(ODT_STYLE) -o $@ $<

## check-links   : Check HTML links.
# linkchecker fails with exit code 1 if there are broken. The
# Makefile will continue to exit the remaining action to filter
# the link report even if linkchecker fails in this way.
.PHONY : check-links
check-links : $(HTML_PAPER)
	-$(LINK_CHECKER) -Ftext/$(LINK_REPORT) $(HTML_PAPER_DIR)/*.html
	@echo Extracting broken links from link report $(LINK_REPORT)
	@echo Broken links:
	@grep Real $(LINK_REPORT) | sort | uniq

## commands      : Display available commands.
.PHONY : commands
commands : Makefile
	@sed -n 's/^##//p' $<

## settings      : Show variables and settings.
.PHONY : settings
settings :
	@echo 'PAPER_PREFIX:' $(PAPER_PREFIX)
	@echo 'TEMPLATE_PREFIX:' $(TEMPLATE_PREFIX)
	@echo 'YAML:' $(YAML)
	@echo 'HTML_LAYOUT:' $(HTML_LAYOUT)
	@echo 'IMAGES:' $(IMAGES)
	@echo 'CSS:' $(CSS)
	@echo 'ODT_STYLE' $(ODT_STYLE)
	@echo 'YAML_TO_MD' $(YAML_TO_MD)
	@echo 'PANDOC:' $(PANDOC)
	@echo 'WKHTMLTOPDF:' $(WKHTMLTOPDF)
	@echo 'LINK_CHECKER:' $(LINK_CHECKER)
	@echo 'BUILD:' $(BUILD)
	@echo 'BUILD_PAPER:' $(BUILD_PAPER)
	@echo 'HTML_PAPER_DIR:' $(HTML_PAPER_DIR)
	@echo 'PANDOC_MD_PAPER:' $(PANDOC_MD_PAPER)
	@echo 'HTML_PAPER:' $(HTML_PAPER)
	@echo 'PDF_PAPER:' $(PDF_PAPER)
	@echo 'BUILD_TEMPLATE:' $(BUILD_TEMPLATE)
	@echo 'PANDOC_MD_TEMPLATE:' $(PANDOC_MD_TEMPLATE)
	@echo 'MD_TEMPLATE:' $(MD_TEMPLATE)
	@echo 'DOCX_TEMPLATE:' $(DOCX_TEMPLATE)
	@echo 'ODT_TEMPLATE:' $(ODT_TEMPLATE)
	@echo 'LINK_REPORT:' $(LINK_REPORT)
