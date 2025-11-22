# Infering Relationships Between Iris Species and their Characteristics

## dsci-522-group-project
## Project summary

The Iris dataset includes measurements from 150 flowers, with each of the three species represented equally. The four recorded features capture sepal and petal dimensions, and these measurements vary noticeably among species—especially the petal attributes, which show the strongest separation. Because the dataset is clean and balanced, it provides a reliable foundation for classification. In this project, we built a Logistic Regression model to predict species and compared it against a simple baseline classifier. After scaling the features and tuning the model parameters, the final classifier reached high accuracy, correctly identifying most samples and showing only minor confusion between the two more similar species, versicolor and virginica. These results suggest that the measured flower characteristics contain enough structure to support effective species prediction, and additional modelling techniques could potentially refine performance further.

## Contributors

The following authors contributed to this project:

* **Aitong Wu** 
* **Manikanth Goud**
* **Sidharth Malik**
* **Derrick Jaskiel** 

## Dependencies

This project was implemented using Python and several open-source scientific computing libraries. The analysis, modelling pipeline, and visualizations rely on the following key packages:

* pandas – for loading, cleaning, and manipulating tabular data
* numpy – provides numerical operations used throughout the workflow
* scikit-learn – used for model training, feature scaling, cross-validation, hyperparameter tuning, and evaluation (Logistic Regression, DummyClassifier, RandomizedSearchCV, etc.)
* altair – for interactive visualizations including scatter plots, boxplots, and heatmaps
* matplotlib – used to display the confusion matrix and other static figures
* python – primary runtime environment for the project

## Dataset

**Iris Dataset**
- Source: scikit-learn sample datasets
- Features: 4 continuous morphological measurements — sepal length, sepal width, petal length, petal width
- Target: Species label — setosa, versicolor, virginica (3 balanced classes, 50 samples each)


## References

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., & Duchesnay, É. (2011). Iris dataset [Data set]. scikit-learn. https://scikit-learn.org/1.4/auto_examples/datasets/plot_iris_dataset.html

