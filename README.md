

# Introduction

`edfdb` is a minimal python library to read and write the [European Data
Format](https://www.edfplus.info/) (EDF).  The main aim of `edflib` is the fast
and accurate handling of EEG signals stored in EDF.  The library is designed to
be able to read from [MongoDB Grid
files](https://docs.mongodb.com/manual/core/gridfs/).

# Install

To install the module enter

```
pip install -r requirements.txt
python setup.py install
```

# Development and Contribution

Contributions are welcome.  Please create your own fork of `edfdb` and a pull
request to the master branch starting with a title '[WIP] ...' that describes
what you are working on.  We'll review the changes once you switch the title
form '[WIP]' to '[MRG]'.  Make sure to run the tests before submitting and
switching the title.  We also use [SemaphoreCI](https://semaphoreci.com/).

To run the tests, first install the requirements-dev.txt file using 

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

This installs `pytest`.  Before testing the package first install.

```
pip install -e .
make check
```

# Contributors

The module was initially created by John C. Snyder and is now maintained by
Justus Schwabedal.

# License

The software is released under the MIT license.
