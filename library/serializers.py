from rest_framework import serializers
from library.models import Book, Cover



class BookSerializer(serializers.ModelSerializer):
    cover = serializers.ChoiceField(choices=("Hard", "Soft"))

    class Meta:
        model = Book
        fields = ("id","cover","title","author","inventory","daily_fee")

    def hide(self):

        self.instance.hidden = True
        self.instance.save()

