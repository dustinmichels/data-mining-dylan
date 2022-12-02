# Data Mining Dylan: Analysis

Some code for scraping Dylan lyrics, and quantifying references to places.

## Installation

```bash
# create virtual environment
conda create --no-default-packages -n dylan python
source activate dylan

# upgrade pip
pip install --upgrade pip

# install jupyter, then exit/enter environment
conda install jupyter
conda install -c conda-forge jupyterlab
source deactivate
source activate dylan

# install bokeh and its jupyterlab extension
conda install bokeh
jupyter labextension install jupyterlab_bokeh

# add geojson extension
jupyter labextension install @jupyterlab/geojson-extension

# install spacy and its english language module
conda install -c conda-forge spacy
python -m spacy download en

# more
conda install pandas
```
