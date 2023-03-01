from rest_framework import serializers
from enumchoicefield import ChoiceEnum, EnumChoiceField
from library.models import Book, Cover

# class CoverSerializer(serializers.Serializer):
#     value = serializers.CharField()
#
#     def to_representation(self, instance):
#         return {'value': instance.value}
#
#     def to_internal_value(self, data):
#         return Cover(data['value'])



class BookSerializer(serializers.ModelSerializer):
    cover = serializers.ChoiceField(choices=("Hard", "Soft"))

    class Meta:
        model = Book
        fields = '__all__'

