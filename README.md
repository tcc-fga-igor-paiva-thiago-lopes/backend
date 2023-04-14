# Backend

[![codecov](https://codecov.io/gh/tcc-fga-igor-paiva-thiago-lopes/backend/branch/main/graph/badge.svg?token=AsxWX0BLTY)](https://codecov.io/gh/tcc-fga-igor-paiva-thiago-lopes/backend)

## How to run

You'll need docker and docker compose installed.

Older versions:

```
docker-compose up
```

Newer versions:

```
docker compose up
```

## How to run tests

Install this dependencies:

```
pip install -r requirements.txt
```

We are using tox for the tests, so it is good to install the tox:

```
pip install tox
```

Then you can run the tests using:

```
tox
```

if you want to especify the file use:

```
tox <PACKAGE OR FILE>
```

If it does not work, you can try to run before:

```
pip install pytest-mock
```

To run tests and check code coverage:

```
# Text
tox -- --cov=src

# The result will be printed on the screen

# HTML
tox -- --cov=src --cov-report=html:cov_html

# Check cov_html/index.html to see coverage info
```
