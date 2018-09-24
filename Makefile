DOC_PREFIX = SoftwareManagementPlanChecklist
DATA_DIR = data
DATA_YAML = $(DATA_DIR)/checklist.yaml
DATA_HDR_MD = $(DATA_DIR)/header.md
YAML_TO_MD = src/yaml_to_markdown.py

IMAGES = $(wildcard images/*.png)
TEMPLATE = templates/doc.html
CSS = css/style.css
PANDOC = pandoc
WKHTMLTOPDF = wkhtmltopdf --disable-smart-shrinking
LINK_CHECKER = linkchecker --check-extern --no-robots

BUILD_DIR = build
BUILD_MD_DIR = $(BUILD_DIR)/markdown
BUILD_HTML_DIR = $(BUILD_DIR)/html
BUILD_PDF_DIR = $(BUILD_DIR)/pdf
BUILD_DOCX_DIR = $(BUILD_DIR)/docx
BUILD_MD = $(BUILD_MD_DIR)/$(DOC_PREFIX).md
BUILD_HTML = $(BUILD_HTML_DIR)/$(DOC_PREFIX).html
BUILD_PDF = $(BUILD_PDF_DIR)/$(DOC_PREFIX).pdf
BUILD_DOCX = $(BUILD_DOCX_DIR)/$(DOC_PREFIX).docx
LINK_REPORT = $(BUILD_DIR)/link-check.txt

# Default action is to show what commands are available.
.PHONY : all
all : commands

## clean       : Clean up temporary and auto-generated files.
.PHONY : clean
clean :
	@rm -rf $(BUILD_DIR)
	@rm -rf $$(find . -name '*~' -print)

## markdown    : Create Markdown document.
.PHONY : markdown
markdown : $(BUILD_MD)

## html        : Create HTML document.
.PHONY : html
html : $(BUILD_HTML)

## pdf         : Create PDF document.
.PHONY : pdf
pdf : $(BUILD_PDF)

## docx        : Create DOCX document.
.PHONY : docx
docx : $(BUILD_DOCX)

# Create Markdown document.
$(BUILD_MD) : $(DATA_YAML) $(DATA_HDR_MD) $(YAML_TO_MD)
	mkdir -p $(BUILD_MD_DIR)
	cp $(DATA_HDR_MD) $@
	python $(YAML_TO_MD) -f $< -o text >> $@

# Convert Markdown to HTML.
$(BUILD_HTML) : $(BUILD_MD) $(IMAGES) $(TEMPLATE) $(CSS)
	mkdir -p $(BUILD_HTML_DIR)
	cp -r images/ $(BUILD_HTML_DIR)
	cp -r css/ $(BUILD_HTML_DIR)
	# $(PANDOC) -t html -o $@ $<
	$(PANDOC) -t html -c $(CSS) --template=$(TEMPLATE) -o $@ $<

# Convert HTML to PDF.
$(BUILD_PDF) : $(BUILD_HTML)
	mkdir -p $(BUILD_PDF_DIR)
	$(WKHTMLTOPDF) $< $@

# Convert Markdown to DOCX.
$(BUILD_DOCX) : $(BUILD_MD)
	mkdir -p $(BUILD_DOCX_DIR)
	$(PANDOC) -t docx -o $@ $<

## check-links : Check HTML links.
# linkchecker fails with exit code 1 if there are broken. The
# Makefile will continue to exit the remaining action to filter
# the link report even if linkchecker fails in this way.
.PHONY : check-links
check-links : $(HTML)
	-$(LINK_CHECKER) -Ftext/$(LINK_REPORT) $(BUILD_HTML_DIR)/*.html
	@echo Extracting broken links from link report $(LINK_REPORT)
	@echo Broken links:
	@grep Real $(LINK_REPORT) | sort | uniq

## commands    : Display available commands.
.PHONY : commands
commands : Makefile
	@sed -n 's/^##//p' $<

## settings    : Show variables and settings.
.PHONY : settings
settings :
	@echo 'DOC_PREFIX:' $(DOC_PREFIX)
	@echo 'DATA_DIR:' $(DATA_DIR)
	@echo 'DATA_YAML:' $(DATA_YAML)
	@echo 'DATA_HDR_MD:' $(DATA_HDR_MD)
	@echo 'YAML_TO_MD' $(YAML_TO_MD)
	@echo 'IMAGES:' $(IMAGES)
	@echo 'TEMPLATE:' $(TEMPLATE)
	@echo 'CSS:' $(CSS)
	@echo 'PANDOC:' $(PANDOC)
	@echo 'WKHTMLTOPDF:' $(WKHTMLTOPDF)
	@echo 'LINK_CHECKER:' $(LINK_CHECKER)
	@echo 'BUILD_DIR:' $(BUILD_DIR)
	@echo 'BUILD_MD_DIR:' $(BUILD_MD_DIR)
	@echo 'BUILD_MD:' $(BUILD_MD)
	@echo 'BUILD_HTML_DIR:' $(BUILD_HTML_DIR)
	@echo 'BUILD_HTML:' $(BUILD_HTML)
	@echo 'BUILD_PDF_DIR:' $(BUILD_PDF_DIR)
	@echo 'BUILD_PDF:' $(BUILD_PDF)
	@echo 'BUILD_DOCX_DIR:' $(BUILD_DOCX_DIR)
	@echo 'BUILD_DOCX:' $(BUILD_DOCX)
	@echo 'LINK_REPORT:' $(LINK_REPORT)
