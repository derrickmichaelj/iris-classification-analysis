# DSCI 522 Iris Classification Project

# Python command using the project conda environment
PYTHON = conda run -n 522_group_project_env python

# Raw and processed data locations
RAW_DATA       = data/raw/iris.csv
PROCESSED_DATA = data/processed/iris_clean.csv

# Output directories
FIGURES_DIR    = results/figures
METRICS_DIR    = results/metrics

# EDA output figures
FIGURES = $(FIGURES_DIR)/scatter_petal.png \
          $(FIGURES_DIR)/boxplots.png \
          $(FIGURES_DIR)/correlation_heatmap.png

# Trained model artifact
MODEL_ARTIFACT = $(METRICS_DIR)/logreg_model.pickle

# Quarto report files
REPORT_QMD  = reports/iris_classification.qmd
REPORT_HTML = reports/iris_classification.html

# Ensure required directories exist
$(shell mkdir -p data/raw data/processed $(FIGURES_DIR) $(METRICS_DIR))

# Default target: build the final HTML report
all: $(REPORT_HTML)

# Render the Quarto report after figures and model are available
$(REPORT_HTML): $(REPORT_QMD) $(FIGURES) $(MODEL_ARTIFACT)
	quarto render $(REPORT_QMD) --to html

# Run exploratory data analysis and save figures
$(FIGURES): $(PROCESSED_DATA) src/eda.py
	$(PYTHON) src/eda.py --input $(PROCESSED_DATA) --output-dir $(FIGURES_DIR)

# Train the classification model and save metrics/artifacts
$(MODEL_ARTIFACT): $(PROCESSED_DATA) src/model.py
	$(PYTHON) src/model.py --input $(PROCESSED_DATA) --output-dir $(METRICS_DIR)

# Clean and validate the raw dataset
$(PROCESSED_DATA): $(RAW_DATA) src/process.py src/data_validation_iris.py
	$(PYTHON) src/process.py --input $(RAW_DATA) --output $(PROCESSED_DATA)

# Download the raw Iris dataset
$(RAW_DATA): src/download.py
	$(PYTHON) src/download.py --output $(RAW_DATA)

# Remove all generated files and reset the workspace
.PHONY: clean
clean:
	@echo "Cleaning generated data, results and report..."
	rm -rf data/raw/* data/processed/*
	rm -rf results/figures/* results/metrics/*
	rm -f $(REPORT_HTML)

# Convenience targets for individual pipeline stages
.PHONY: data eda model report
data: $(PROCESSED_DATA)
eda: $(FIGURES)
model: $(MODEL_ARTIFACT)
report: $(REPORT_HTML)

.PHONY: all
