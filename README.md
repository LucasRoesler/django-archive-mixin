[![Circle CI](https://circleci.com/gh/LucasRoesler/django-archive-mixin.svg?style=svg)](https://circleci.com/gh/LucasRoesler/django-archive-mixin)
[![Coverage Status](https://coveralls.io/repos/LucasRoesler/django-archive-mixin/badge.svg?branch=master&service=github)](https://coveralls.io/github/LucasRoesler/django-archive-mixin?branch=master)

# Django Archive Mixin

Implements a soft delete / archive capability for the Django ORM.

This project is inspired by other similar projects, such as

- https://github.com/scoursen/django-softdelete, or
- https://github.com/makinacorpus/django-safedelete, and
- any of the packages in https://www.djangopackages.com/packages/p/django-safedelete/

This implementation differs in that it not only safe marks an instance as
deleted, but it also implements that cascade logic so that relationships that
point to the recently "deleted" instance do not break you application.

We piggyback on Django's own delete logic/methodology to help guarentee that
it will cascade as expected and will abide by Django's `on_delete` api for
`ForeignKeys`.

## Testing

We test this against a postgres database, once you have postgres installed in
running, testing is as simple as

```
./runtests.sh
```
