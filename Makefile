# DSCI 522 Iris project Makefile

PYTHON         = python

RAW_DATA       = data/raw/iris.csv
PROCESSED_DATA = data/processed/iris_clean.csv

FIGURES_DIR    = results/figures
METRICS_DIR    = results/metrics

FIGURES        = $(FIGURES_DIR)/scatter_petal.png \
                 $(FIGURES_DIR)/boxplots.png \
                 $(FIGURES_DIR)/correlation_heatmap.png

MODEL_ARTIFACT = $(METRICS_DIR)/logreg_model.pickle

REPORT_QMD     = reports/iris_classification.qmd
REPORT_HTML    = reports/iris_classification.html

$(shell mkdir -p data/raw data/processed $(FIGURES_DIR) $(METRICS_DIR))

all: $(REPORT_HTML)

$(REPORT_HTML): $(REPORT_QMD) $(FIGURES) $(MODEL_ARTIFACT)
	quarto render $(REPORT_QMD) --to html

$(FIGURES): $(PROCESSED_DATA) src/eda.py
	$(PYTHON) src/eda.py --input $(PROCESSED_DATA) --output-dir $(FIGURES_DIR)

$(MODEL_ARTIFACT): $(PROCESSED_DATA) src/model.py
	$(PYTHON) src/model.py --input $(PROCESSED_DATA) --output-dir $(METRICS_DIR)

$(PROCESSED_DATA): $(RAW_DATA) src/process.py src/data_validation_iris.py
	$(PYTHON) src/process.py --input $(RAW_DATA) --output $(PROCESSED_DATA)

$(RAW_DATA): src/download.py
	$(PYTHON) src/download.py --output $(RAW_DATA)

.PHONY: clean
clean:
	@echo "Cleaning generated data, results and report..."
	rm -rf data/raw/* data/processed/*
	rm -rf results/figures/* results/metrics/*
	rm -f $(REPORT_HTML)

.PHONY: data eda model report
data: $(PROCESSED_DATA)
eda: $(FIGURES)
model: $(MODEL_ARTIFACT)
report: $(REPORT_HTML)

.PHONY: all
