# cli_for_ds_masterclass
An introduction to Bash &amp; Line Command Utilities for Data Scientists


# Makefile command

```
Available recipes:
  check-installation:  Validate environment for missing dependencies.

 Local project recipes
  copy-env:  Create .env file
  install:  Install project dependencies.
  create-venv:  Create virtualenv
  delete-venv:  Delete virtualenv
  spacy-spanish-embedding:  Installing Spacy es_core_news_sm
  train-model:  Traning the Conversation Model
  students:  Generate Fake Student data
  install-poetry:  Install poetry system-wide.
  clean:  Clean temporary files.
  test:  Run tests and generate coverage report.
  autoformat:  Autoformat code. Don't be lazy and do it by yourself.
  lint:  Lint code.
  serve:  Start the local Uvicorn server.
  prediction-taurus:  Create a prediction for taurus
```

## How to run the project

```
make delete-venv # Optional
make copy-env
make create-env 
make install-poetry
make check-installation
make spacy-spanish-embedding
make train-model
make serve
```
