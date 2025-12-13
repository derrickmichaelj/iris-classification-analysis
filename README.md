# Iris Species Classification  
**DSCI 522 Group Project – Milestone 2**

A reproducible, containerized machine-learning pipeline that classifies Iris flower species from morphological measurements.  
This version includes full data validation, modular code structure, and Docker-based environment reproducibility.

---

## Project Overview

The project uses the classic Iris dataset (150 samples, 3 species, balanced).  
Each sample has four continuous features:

- Sepal length  
- Sepal width  
- Petal length  
- Petal width  

We preprocess, validate, and analyze the data, then build and evaluate classification models:

- A baseline classifier (`DummyClassifier`)  
- A tuned `LogisticRegression` model with feature scaling, cross-validation, and hyperparameter optimization  

The final model yields high accuracy, effectively distinguishing most samples, with minor confusion between *versicolor* and *virginica*.  
This demonstrates that simple morphological measurements provide sufficient signal for accurate species prediction.

---

## Contributors

- Aitong Wu  
- Manikanth Goud  
- Sidharth Malik  
- Derrick Jaskiel  

We adopt a **GitHub Flow** workflow:  
feature branches, pull requests, peer reviews, and proper commit history for collaboration and transparency.

---

## Repository Structure

```text
dsci-522-group-project/
│
├── data/                           # Raw and processed datasets (ignored by Git)
├── src/
│   ├── download.py                 # Download the Iris dataset
│   ├── process.py                  # Run data validation and preprocessing
│   ├── eda.py                      # Generate EDA figures
│   ├── model.py                    # Train and evaluate models
│   └── data_validation_iris.py     # Helper functions for data quality checks
├── reports/
│   └── iris_classification.ipynb   # Main Jupyter Notebook for analysis and modeling
├── environment.yml                 # Conda environment definition (dependencies)
├── conda-lock.yml                  # Lock file for cross-platform reproducibility (linux-64)
├── Dockerfile                      # Instructions for building the project Docker image
├── Makefile                        # Automation commands for building, running, and cleaning the project
├── docker-compose.yml              # Orchestration for running the Docker service (JupyterLab)
├── LICENSE.md                      # MIT License details
└── README.md                       # This project documentation
```

---

## Dataset Information 

The project utilizes the classic Iris Dataset (Fisher, 1936), readily available via scikit-learn.

- Size: 150 samples
- Features (4, continuous): Sepal Length, Sepal Width, Petal Length, Petal Width
- Target (3, species): Iris-setosa, Iris-versicolor, Iris-virginica
- Balance: The dataset is perfectly balanced (50 samples per species).

---

## Data Validation (Milestone 2)

We enforce a robust data validation pipeline via `src/data_validation_iris.py`. Checks include:

- Schema validation  
- Duplicate and missing value checks  
- Outlier detection  
- Species category verification  
- Target class balance  
- Feature–target consistency  
- Feature–feature correlation warnings  

These checks run automatically at the beginning of the analysis pipeline.

---

## Containerized & Reproducible Environment (Recommended)

To ensure consistency for all collaborators and graders, the project provides a Docker-based environment. Using Docker is the most reproducible way to run this project, guaranteeing the exact environment used by the developers.

### Prerequisites 

You must have Docker Desktop installed and running on your system.

## How to Run the container 

**Option 1: Run Pre-Built Image (Fastest)**  
Pull the image directly from DockerHub and run the container, which will start JupyterLab on port 8888.

Open Docker Desktop then run the following lines in your console to pull and run the container:

```bash
# 1. Pull the official, pre-built image
docker pull derrickj11/dsci-522-group-project:latest

# 2. Run the container. The '--rm' flag ensures it is cleaned up upon exit.
# The '-p 8888:8888' maps the container's JupyterLab port to your host machine's port.
# Upon pulling the image, run: 
docker run -it --rm -p 8888:8888 derrickj11/dsci-522-group-project:latest
```

Once the container is running, open your web browser and navigate to the printed URL (usually `http://127.0.0.1:8888/lab?token=...`).

**Option 2: Build and Run Locally (For Developers)**  
If you need to ensure the build process or have made changes to the Dockerfile, use the `docker-compose.yml` file.

```bash
# Clone the repository first if you haven't already
git clone https://github.com/derrickmichaelj/dsci-522-group-project.git
cd dsci-522-group-project

# 1. Build the Docker image (this may take a few minutes)
docker-compose build

# 2. Run the container service (starts JupyterLab)
docker-compose up
```

Access JupyterLab at `http://localhost:8888`. To stop the container, press `Ctrl+C` in the terminal where `docker-compose up` is running.



### Updating the Container

1. Add new dependencies to the `environment.yml` file and push to a new branch in the repository  
2. Run `conda-lock lock -f environment.yml --platform linux-64 --platform osx-64 --platform osx-arm64 --platform win-64` to update the `conda-linux-64.lock` file  
3. Update the Dockerfile locally and test it to make sure that it builds/runs properly  
4. Push these changes to your branch, the updated Docker image will then be created and pushed to DockerHub automatically  
5. Create a pull request to merge the changes into the main branch  

---

## Local Development

If you prefer to run the project without Docker, you can set up the environment locally using Conda.

### Prerequisites
- Git
- Conda (Miniconda or Anaconda)

### Setup Instructions

#### 1. Clone the Repository and Checkout Branch: 

Using CLI, in your desired folder: 

```bash
git clone https://github.com/derrickmichaelj/dsci-522-group-project.git
cd dsci-522-group-project
```

#### 2. Create and Activate Conda Environment:

The `environment.yml` file contains all necessary dependencies.

```bash
# Create the environment named '522_group_project_env'
conda env create -f environment.yml

# Activate the newly created environment
conda activate 522_group_project_env
```

#### 3. Launch Jupyter Lab

```bash
# Launch JupyterLab
jupyter lab
# or the shorthand alias, if set up:
jl
```

#### 4. Open the Notebook

In the JupyterLab interface, navigate to and open: `reports/iris_classification.ipynb`

## Follow these steps after Activating the Environment from either of the ways mentioned above:



### Running the Codes in the Command-Line of JL Docker Container or Local Development 

```bash

#If the folders already contain all the figures and tables run: 
make clean

#The previous command cleans all the folders, the next step is to run: 
make all
#make all includes re-rendering of quarto document to update the HTML file

#(optional) manual command for the quarto document to update the HTML file:
quarto render reports/iris_classification.qmd --to html

#Additional Step only use if required
#If you encounter an error in rendering the document such as "No such kernel named 522_group_project_env", run: 
python -m ipykernel install --user --name 522_group_project_env --display-name "522_group_project_env"
```



This script will:

1. Split the data into train/test sets  
2. Train and cross-validate the dummy baseline; save its CV results  
3. Build a preprocessing + logistic regression pipeline  
4. Perform randomized search over `C` (log-uniform prior)  
5. Print train/test accuracy for the best model  
6. Save:

   - `results/metrics/dummy_cv_results.csv` — baseline CV results  
   - `results/metrics/cv_results.csv` — tuned model CV results  
   - `results/metrics/confusion_matrix.png` — confusion matrix for the best model  
   - `results/metrics/logreg_model.pickle` — trained model artifact  

### End-to-End Example

To run the **entire pipeline** from scratch (assuming empty `data/` and `results/` folders), execute:

```bash
# 1. Download raw data
python src/download.py --output data/raw/iris.csv

# 2. Validate & process
python src/process.py --input data/raw/iris.csv --output data/processed/iris_clean.csv

# 3. Generate EDA figures
python src/eda.py --input data/processed/iris_clean.csv --output-dir results/figures

# 4. Train & evaluate models
python src/model.py --input data/processed/iris_clean.csv --output-dir results/metrics
```

After these commands complete, you will have:

- Validated raw and processed datasets in `data/`  
- EDA visualizations in `results/figures/`  
- Model metrics, confusion matrix, and trained model artifacts in `results/metrics/`  


### Clean up

1. To shut down the container and clean up the resources, 
type `Cntrl` + `C` in the terminal
where you launched the container, and then type `docker compose rm`

---

## Key Dependencies

- Core: `python`  
- Data Handling: `pandas`, `numpy`
- Modelling: `scikit-learn`, `scipy`
- Validation: `pandera`  
- Visualisation: `altair`, `matplotlib`
- Environment: `jupyterlab`, `docker` (for containerization)

All managed via: `environment.yml`, `conda-lock.yml`, and Docker.

#### Developer dependencies
- `conda` (version 23.9.0 or higher)
- `conda-lock` (version 2.5.7 or higher)

---

## Licenses

- This project is released under the **MIT License.**

---

## References

Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56C76.

Thyagharajan, K. K., & Kiruba Raji, I. (2018). A Review of Visual Descriptors and Classification Techniques Used in Leaf Species Identification. Archives of Computational Methods in Engineering, 26(4), 933–960. https://doi.org/10.1007/s11831-018-9266-3

Joly, A., Goëau, H., Bonnet, P., Bakić, V., Barbe, J., Selmi, S., Yahiaoui, I., Carré, J., Mouysset, E., Molino, J.-F., Boujemaa, N., & Barthélémy, D. (2014). Interactive Plant Identification Based on Social Image Data. Ecological Informatics, 23, 22–34. https://doi.org/10.1016/j.ecoinf.2013.07.006

Yanikoglu, B., Aptoula, E., & Tirkaz, C. (2014). Automatic Plant Identification from Photographs. Machine Vision and Applications, 25(6), 1369–1383. https://doi.org/10.1007/s00138-014-0612-7
