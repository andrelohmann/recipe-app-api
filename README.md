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

Test db availability

```
python manage.py wait_for_db
```

## REST Auth

* https://django-rest-registration.readthedocs.io/
* https://django-rest-framework-simplejwt.readthedocs.io/
* https://jazzband.github.io/django-rest-knox/auth/
* https://django-oauth-toolkit.readthedocs.io/en/latest/
* https://saasitive.com/tutorial/django-rest-framework-register-user-email-verification/
* https://dj-rest-auth.readthedocs.io/
* https://www.youtube.com/watch?v=mDosRuqDG5o
* https://dev.to/jkaylight/django-rest-framework-authentication-with-dj-rest-auth-4kli
* https://drf-social-oauth2.readthedocs.io/en/latest/
* https://testdriven.io/blog/django-rest-auth/#:~:text=django%2Dallauth%20addresses%20authentication%2C%20registration,registration%20and%20other%20authentication%20tasks.
* https://www.youtube.com/watch?v=2pZmxh8Tf78
* https://docs.digitalocean.com/developer-center/deploy-a-django-app-on-app-platform/

### Idea:

* Implement registration and simple jwt
* Create OAuth Provider as standalone service