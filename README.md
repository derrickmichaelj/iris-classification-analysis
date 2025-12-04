# Iris Species Classification  
**DSCI 522 Group Project – Milestone 2**

A reproducible, containerized machine‑learning pipeline that classifies Iris flower species from morphological measurements.  
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
- A tuned `LogisticRegression` model with feature scaling, cross‑validation, and hyperparameter optimization  

The final model yields high accuracy, effectively distinguishing most samples, with minor confusion between *versicolor* and *virginica*.  
This demonstrates that simple morphological measurements provide sufficient signal for accurate species prediction.

---

## Contributors

- Aitong Wu  
- Manikanth Goud  
- Sidharth Malik  
- Derrick Jaskiel  

We adopt a **GitHub Flow** workflow:  
feature branches, pull requests, peer reviews, and proper commit history for collaboration and transparency.

---

## Repository Structure

```
dsci-522-group-project/
│
├── data/                           # Raw and processed datasets (ignored by Git)
├── src/
│   └── data_validation_iris.py     # Python script for enforcing data quality checks
├── reports/
│   └── iris_classification.ipynb   # Main Jupyter Notebook for analysis and modeling
├── environment.yml                 # Conda environment definition (dependencies)
├── conda-lock.yml                  # Lock file for cross-platform reproducibility (linux-64)
├── Dockerfile                      # Instructions for building the project Docker image
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

To ensure consistency for all collaborators and graders, the project provides a Docker‑based environment. Using Docker is the most reproducible way to run this project, guaranteeing the exact environment used by the developers.

### Prerequisites 

You must have Docker Desktop installed and running on your system.

## DockerFile

```bash
# Stage 1: Use a minimal Conda image as the base
# We choose miniconda3 for a lighter image size.
FROM continuumio/miniconda3:24.3.0-0

# Set a non-root user for security best practices (optional but recommended)
# We will still run commands as root during the build for installation.

# 1. Set environment variables
ENV CONDA_DIR=/opt/conda \
    PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_PORT=8888

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the Conda lock file and environment definition
# Using the lock file (conda-lock.yml) ensures identical dependencies across builds.
COPY conda-lock.yml environment.yml ./

# 4. Install the Conda environment using the lock file
# We use 'explicit' to list exact package versions, and 'quiet' to reduce build output.
# The 'mamba' solver is much faster than 'conda' if available, but 'conda' is standard in the base image.
RUN conda update -n base conda -y && \
    conda env create --name 522_group_project_env --file conda-lock.yml --quiet && \
    conda clean --all -f -y

# 5. Activate the environment for subsequent commands
# This ensures that all following RUN commands use the installed environment packages.
SHELL ["conda", "run", "-n", "522_group_project_env", "/bin/bash", "-c"]

# 6. Copy all project files into the container's working directory (/app)
# This includes the source code, reports, and data (if any small, committed data).
# Note: Sensitive or large data files should be volume mounted, not copied.
COPY . .

# 7. Expose the port for JupyterLab
EXPOSE $JUPYTER_PORT

# 8. Define the default command to run when the container starts
# This launches JupyterLab, making it listen on all interfaces (0.0.0.0) and uses the token
# to ensure secure access.
CMD ["conda", "run", "-n", "522_group_project_env", "jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--NotebookApp.token='dsci522'"] # Set a simple, predictable token for easy access
```

## How to Run the container 

Option 1: Run Pre-Built Image (Fastest)
Pull the image directly from DockerHub and run the container, which will start JupyterLab on port 8888.

```
# 1. Pull the official, pre-built image
docker pull derrickj11/dsci-522-group-project:latest

# 2. Run the container. The '--rm' flag ensures it is cleaned up upon exit.
# The '-p 8888:8888' maps the container's JupyterLab port to your host machine's port.
docker run -it --rm -p 8888:8888 derrickj11/dsci-522-group-project:latest

```
Once the container is running, open your web browser and navigate to the printed URL (usually http://127.0.0.1:8888/lab?token=...).

Option 2: Build and Run Locally (For Developers)
If you need to ensure the build process or have made changes to the Dockerfile, use the docker-compose.yml file.

```bash
# Clone the repository first if you haven't already
git clone https://github.com/derrickmichaelj/dsci-522-group-project.git
cd dsci-522-group-project

# 1. Build the Docker image (this may take a few minutes)
docker-compose build

# 2. Run the container service (starts JupyterLab)
docker-compose up
```

Access JupyterLab at http://localhost:8888. To stop the container, press Ctrl+C in the terminal where docker-compose up is running.

### Using the Container

Open Docker Desktop then run the following lines in your console to pull and run the container:

```bash
#Run the code below in CLI 
docker pull derrickj11/dsci-522-group-project:latest

#Upon pulling the image, run: 
docker run -it --rm -p 8888:8888 derrickj11/dsci-522-group-project:latest
```

### Updating the Container

1. Add new dependencies to the `environment.yml` file and push to a new branch in the repository
2. Run `conda-lock -k explicit --file environment.yml -p linux-64` to update the `conda-linux-64.lock` file
3. Update the Dockerfile locally and test it to make sure that it bulds/runs properly
4. Push these changes to your branch, the updated Docker image will then be created and pushed to DockerHub automatically
5. Create a pull request to merge the changes into the main branch

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

The environment.yml file contains all necessary dependencies.

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

---

## Key Dependencies

- Core: `python`  
- Data Handling: `pandas`, `numpy`
- Modelling: `scikit-learn`, `scipy`
- Validation: `pandera`,  
- Visualisation: `altair`, `matplotlib`
- Environment: `jupyterlab`, `docker` (for containerization)

All managed via: `environment.yml`, `conda-lock.yml`, and Docker.

---

## Licenses

- This project is released under the **MIT License.**

---

## References

Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56C76.

Thyagharajan, K. K., & Kiruba Raji, I. (2018). A Review of Visual Descriptors and Classification Techniques Used in Leaf Species Identification. Archives of Computational Methods in Engineering, 26(4), 933–960. https://doi.org/10.1007/s11831-018-9266-3

Joly, A., Goëau, H., Bonnet, P., Bakić, V., Barbe, J., Selmi, S., Yahiaoui, I., Carré, J., Mouysset, E., Molino, J.-F., Boujemaa, N., & Barthélémy, D. (2014). Interactive Plant Identification Based on Social Image Data. Ecological Informatics, 23, 22–34. https://doi.org/10.1016/j.ecoinf.2013.07.006

Yanikoglu, B., Aptoula, E., & Tirkaz, C. (2014). Automatic Plant Identification from Photographs. Machine Vision and Applications, 25(6), 1369–1383. https://doi.org/10.1007/s00138-014-0612-7
