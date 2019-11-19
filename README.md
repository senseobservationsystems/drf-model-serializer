# drf-model-serializer

## Description
The scope of this module is to enhance DRF's [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) class, and provide object-level validation out of the box. 

The idea is that the model defines its object-level validation in its `clean` method. The serializer class `ModelSerializer` provided by this module, overrides its `validate` method so that it invokes the model's `clean` method. Therefore whenever invoking the serializer's `is_valid` method, the `validate` method runs and provides the object-level validation.

This way, object-level validation is defined once in the model and is used automatically by the Django admin, the model when explicitly invoking `full_clean` and the serializer whenever invoking `is_valid`. This follows the convention for *field-level* validation. When defined correctly using *[model validators](https://docs.djangoproject.com/en/2.2/ref/validators/)*, the field-level validation is used out of the box by the Django admin, serializer and model.


## Installation
```bash
$ pip install drf-model-serializer
```
or add this on your `requirements.txt`
```
drf-model-serializer==0.0.1
```
