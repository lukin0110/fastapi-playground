# FastAPI Playground

Deployed on [immense-shelf-72787.herokuapp.com](https://immense-shelf-72787.herokuapp.com/docs).

## Install, setup & run

```shell
pip install poetry
poetry install
poetry run api
```

API becomes available on [0.0.0.0:8000](http://0.0.0.0:8000)

### Generate `requirments.txt`
```shell
poetry export -f requirements.txt --output requirements.txt
```

## Push to heroku

```shell
git push heroku main
```

View logs:
```shell
heroku logs --tail
```


## TODO

- Investigate nested models
- Where to put validators? Mixins?
- Where to put computer fields? Mixins?
