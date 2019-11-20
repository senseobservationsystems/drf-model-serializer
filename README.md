# drf-model-serializer

## Description
The scope of this module is to enhance DRF's [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) class, and provide object-level validation out of the box. 

The idea is that the model defines its object-level validation in its `clean` method. The serializer class `ModelSerializer` provided by this module, overrides its `validate` method so that it invokes the model's `clean` method. Therefore whenever invoking the serializer's `is_valid` method, the `validate` method runs and provides the object-level validation.

This way, object-level validation is defined once in the model and is used automatically by the Django admin, the model when explicitly invoking `full_clean` and the serializer whenever invoking `is_valid`. This follows the convention for *field-level* validation. When defined correctly using *[model validators](https://docs.djangoproject.com/en/2.2/ref/validators/)*, the field-level validation is used out of the box by the Django admin, serializer and model.

## Proving the validation idea
In this module, we also provide a Django project that will show you how the object level validations works together with Django admin, Serializer, and a model by implementing `drf-model-serializer` and model `clean()` method. A main focus of the test project lives on create/update actions over any drinks or main dishes recipe, which all any incoming data either from Admin or Serializer must be validated. See the [Recipe model](https://github.com/senseobservationsystems/drf-model-serializer/blob/master/test_project/test_app/models.py) and the [tests section](https://github.com/senseobservationsystems/drf-model-serializer/tree/master/test_project/test_app/tests) to understand it in more detail.

### Prerequisite
Ensure pip installed on your local machine. If you don't have it, you can follow the installation guide [here](https://pip.pypa.io/en/stable/installing/).

### How to run the tests
1. Open terminal and go to the root directory of where the package live, for instance: `$ cd Documents/py-projects/drf-model-serializer`.
2. Run `$ ./scripts/requirement-install.sh` from your command line.
3. Run `$ ./scripts/checker.sh`.

### How to run the test project
Currently only Recipe admin page that available to be explored, and to try it out you can follow these steps:
1. Open terminal and go to the root directory of where the package live, for instance: `$ cd Documents/py-projects/drf-model-serializer`.
3. Run `$ ./scripts/requirement-install.sh` from your command line (you can skip this if you already did it when running the tests).
4. Run `$ source venv/bin/activate && cd test_project && python manage.py migrate`.
5. Create admin user, run `$ python manage.py createsuperuser --email admin@mail.com --username admin`.
6. Run `$ python manage.py runserver 0.0.0.0:8000` and when server is ready, open the admin page and logged in with the previous Admin account.


## Installation
```bash
$ pip install drf-model-serializer
```
or add this on your `requirements.txt`
```
drf-model-serializer==0.0.1
```

## Get involved!

We are happy to receive bug reports, fixes, documentation enhancements, and other improvements.

Please report bugs via the github [issue tracker](https://github.com/senseobservationsystems/drf-model-serializer/issues).

Master git repository [drf-model-serializer](https://github.com/senseobservationsystems/drf-model-serializer).
