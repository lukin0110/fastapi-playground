# FastAPI Playground

Deployed on [immense-shelf-72787.herokuapp.com](https://immense-shelf-72787.herokuapp.com/docs).

## Install, setup & run

```shell
# Use conda if you don't want to rely on the system's python interpreter
conda create --name playground python=3.8.12
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
- Try patchable prop

### Caveats with `Annotated`
- Only available in `Python 3.9`
- `default` attribute is not allowed in conjuction with `Annotated`. But with default_factory it is possible
- `Optional[Annotated[str, Field(..., example="Hello World)]]` doesn't render example values in `openapi.json`
