from django.core.validators import MinValueValidator
from django.db import models

from enumchoicefield import ChoiceEnum, EnumChoiceField


class Cover(ChoiceEnum):
    soft = "Soft"
    hard = "Hard"


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = EnumChoiceField(Cover, default=Cover.hard)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    daily_fee = models.DecimalField(decimal_places=2, max_digits=5)
    need_to_refill = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean_inventory(self):
        if self.inventory == 0:
            self.need_to_refill = True
