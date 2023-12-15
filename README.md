# recipe-app-api

## VSCode Rest Client

* https://www.youtube.com/watch?v=RcxvrhQKv8I
* https://www.codingninjas.com/studio/library/rest-client-in-vs-code-pycharm-and-intellij
* https://www.youtube.com/watch?v=VxxS9STojhc

## OpenAPI Extensions

* https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi
* https://www.youtube.com/watch?v=jc8v_DpAbEk
* https://github.com/tfranzel/drf-spectacular/

## Startup

reopen in container and create django app

```
django-admin startproject app .
```

Run flake8 linting

```
flake8
```

Run tests

```
python manage.py test
```

## DB Race Condition

To avoid race conditions, of a not ready startet db, we can create a wait_for_db routine.

Therefor a special app will be crated called "core" including these kind of core functionalities.

```
python manage.py startapp core
```

