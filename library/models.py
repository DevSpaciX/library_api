from django.db import models


class Book(models.Model):
    class Enum(models.IntegerChoices):
        HARD = 0
        SOFT = 1

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    cover = models.BooleanField(choices=Enum.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    need_to_refill = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def clean_inventory(self):
        if self.inventory == 0:
            self.need_to_refill = True
