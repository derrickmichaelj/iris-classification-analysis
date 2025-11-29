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
├── data/                     
├── src/
│   └── data_validation_iris.py
├── reports/
│   └── iris_classification.ipynb
├── environment.yml
├── conda-lock.yml
├── Dockerfile
├── docker-compose.yml
├── LICENSE.md
└── README.md
```

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

## Containerized & Reproducible Environment

To ensure consistency for all collaborators and graders, the project provides a Docker‑based environment.


## Local Development

```bash
git clone https://github.com/derrickmichaelj/dsci-522-group-project.git
cd dsci-522-group-project
git checkout wuaitong-data-validation

conda env create -f environment.yml
conda activate 522_group_project_env

jl
```

Open:

```
reports/iris_classification.ipynb
```

---

## Key Dependencies

- python  
- pandas  
- numpy  
- scikit-learn  
- matplotlib  
- altair  
- pandera  
- scipy  
- jupyterlab  
- docker  

All managed via: `environment.yml`, `conda-lock.yml`, and Docker.

---

## Dataset Information

**Iris Dataset**  
Source: scikit‑learn  
Balanced dataset with 4 numerical features and 3 species.

---

## References

Fisher, R. (1936). Iris [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56C76.

Thyagharajan, K. K., & Kiruba Raji, I. (2018). A Review of Visual Descriptors and Classification Techniques Used in Leaf Species Identification. Archives of Computational Methods in Engineering, 26(4), 933–960. https://doi.org/10.1007/s11831-018-9266-3

Joly, A., Goëau, H., Bonnet, P., Bakić, V., Barbe, J., Selmi, S., Yahiaoui, I., Carré, J., Mouysset, E., Molino, J.-F., Boujemaa, N., & Barthélémy, D. (2014). Interactive Plant Identification Based on Social Image Data. Ecological Informatics, 23, 22–34. https://doi.org/10.1016/j.ecoinf.2013.07.006

Yanikoglu, B., Aptoula, E., & Tirkaz, C. (2014). Automatic Plant Identification from Photographs. Machine Vision and Applications, 25(6), 1369–1383. https://doi.org/10.1007/s00138-014-0612-7
