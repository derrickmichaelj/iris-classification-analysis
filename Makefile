PYTHON = conda run -n 522_group_project_env python

RAW_DATA=data/raw/iris.csv
PROCESSED_DATA=data/processed/iris_clean.csv
FIGURES_DIR=results/figures
METRICS_DIR=results/metrics
REPORT=reports/iris_classification.qmd

# Cache directories in /tmp to avoid Docker permission issues
MPLCACHE=/tmp/.cache/matplotlib
QUARTOCACHE=/tmp/.cache/quarto
DENOCACHE=/tmp/.cache/deno

# Ensure output and cache directories exist
$(shell mkdir -p data/raw data/processed results/figures results/metrics \
    $(MPLCACHE) $(QUARTOCACHE) $(DENOCACHE))

# Default pipeline (without report)
all: download process eda model

# Full pipeline including report
full: all report

# Download raw data
download:
	@echo "Running download script..."
	$(PYTHON) src/download.py --output $(RAW_DATA)

# Process / clean & validate data
process:
	@echo "Running data validation and cleaning..."
	$(PYTHON) src/process.py --input $(RAW_DATA) --output $(PROCESSED_DATA)

# Run EDA
eda:
	@echo "Running EDA..."
	$(PYTHON) src/eda.py --input $(PROCESSED_DATA) --output-dir $(FIGURES_DIR)

# Train model and save metrics
model:
	@echo "Running modeling..."
	$(PYTHON) src/model.py --input $(PROCESSED_DATA) --output-dir $(METRICS_DIR)

# Render Quarto report
report: $(PROCESSED_DATA)
	@echo "Rendering Quarto report..."
	@env \
	    HOME=/tmp \
	    XDG_CACHE_HOME=/tmp/.cache \
	    MPLCONFIGDIR=$(MPLCACHE) \
	    QUARTO_CACHE_DIR=$(QUARTOCACHE) \
	    DENO_DIR=$(DENOCACHE) \
	    QUARTO_PANDOC_USE_CACHE=false \
	    QUARTO_PYTHON_USE_CACHE=false \
	    quarto render $(REPORT) --to html

# Clean intermediate and output files (keep folders)
clean:
	@echo "Cleaning outputs..."
	rm -rf data/raw/* data/processed/*
	rm -rf results/figures/* results/metrics/*
	rm -rf reports/*.html
	rm -rf /tmp/.cache/*

# Phony targets
.PHONY: all full download process eda model report clean
