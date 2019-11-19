from django.core.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer as DRFModelSerializer, as_serializer_error


class ModelSerializer(DRFModelSerializer):

    def validate(self, data):
        # Use existing model instance when it's an update operation or
        # initiate new instance when it's a create operation
        instance = self.instance if self.instance else self.Meta.model()
        for key, value in data.items():
            setattr(instance, key, value)

        # Validate data model
        try:
            instance.clean()
        except ValidationError as exc:
            raise ValidationError(message=as_serializer_error(exc))

        return data
