# AirBnB Analysis
Analysis of open AirBnB data. This project has an associated [Medium Story](https://medium.com/@miguel.tasende/this-data-will-make-you-enjoy-the-best-airbnb-vacations-of-your-life-47858d00895e).

## Installations
This project was created using Python 3. To create the conda environment, and start working:
```
conda env create -f data.yml
source activate data
python -m ipykernel install --user --name data --display-name "data"
```
The notebook `007-mt-q4-best-value.ipynb` uses a different environment, called geo
(geo has functions to show the maps of Seattle). It can be installed this way:
```
conda env create -f geo.yml
source activate geo
python -m ipykernel install --user --name geo --display-name "geo"
```
No extra libraries are needed.

## Project Motivation
This project is based on Kaggle's ["Seattle AirBnB Open Data"](https://www.kaggle.com/airbnb/seattle). The aim is to find insights that help a person decide how to choose a place, through AirBnB, to stay in Seattle, based on that dataset.

## File Descriptions

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │   │                     the creator's initials, and a short `-` delimited description, e.g.
    │   │                     `1.0-jqp-initial-data-exploration`.
    │   │
    │   └── scratchpad     <- Only for internal use. Messy and unconventional notebooks.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── data.yml           <- The conda env file, generated with `conda env export > data.yml`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


## How to interact with the project
The results of the analysis can be found in the `reports` folder.

Also, the notebooks in the `notebooks` folder can be run, in order, to obtain the analysis results. (The `scratchpad` folder contains notebooks that should be ignored. They are just used to record the process of development).

Finally, you can run the script `(data)hostname$ python src/data/make_dataset.py` to create and preprocess the dataset, from the raw data. That is not necessary for running the notebooks as they already can create the dataset (you will normally find a commented cell that creates the dataset in the notebooks; just uncomment it).


## Licensing, Authors, Acknowledgements
Code released under the [MIT](https://github.com/mtasende/airbnb-analysis/blob/master/LICENSE) license.

This project was authored by Miguel Tasende.

Thanks to Kaggle and AirBnB for the ["Seattle AirBnB Open Data"](https://www.kaggle.com/airbnb/seattle) dataset.

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
