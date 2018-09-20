SRC_DIR = src
SRC_PREFIX = SMP_Checklist
SRC_YAML = $(SRC_DIR)/$(SRC_PREFIX).yaml
SRC_HDR_MD = $(SRC_DIR)/$(SRC_PREFIX).header.md
YAML_TO_MD = scripts/yaml_to_markdown.py

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
BUILD_MD = $(BUILD_MD_DIR)/$(SRC_PREFIX).md
BUILD_HTML = $(BUILD_HTML_DIR)/$(SRC_PREFIX).html
BUILD_PDF = $(BUILD_PDF_DIR)/$(SRC_PREFIX).pdf
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

# Create Markdown document.
$(BUILD_MD) : $(SRC_YAML) $(SRC_HDR_MD) $(YAML_TO_MD)
	mkdir -p $(BUILD_MD_DIR)
	cp $(SRC_HDR_MD) $@
	python $(YAML_TO_MD) -f text $< >> $@

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
	@echo 'SRC_DIR:' $(SRC_DIR)
	@echo 'SRC_PREFIX:' $(SRC_PREFIX)
	@echo 'SRC_YAML:' $(SRC_YAML)
	@echo 'SRC_HDR_MD:' $(SRC_HDR_MD)
	@echo 'YAML_TO_MD' $(YAML_TO_MD)
	@echo 'IMAGES:' $(IMAGES)
	@echo 'TEMPLATE:' $(TEMPLATE)
	@echo 'CSS:' $(CSS)
	@echo 'PANDOC:' $(PANDOC)
	@echo 'WKHTMLTOPDF:' $(WKHTMLTOPDF)
	@echo 'LINK_CHECKER:' $(LINK_CHECKER)
	@echo 'BUILD_DIR:' $(BUILD_DIR)
	@echo 'BUILD_MD:' $(BUILD_MD)
	@echo 'BUILD_HTML:' $(BUILD_HTML)
	@echo 'BUILD_PDF:' $(BUILD_PDF)
	@echo 'LINK_REPORT:' $(LINK_REPORT)
