from django.db import models
from django.core.exceptions import ValidationError

class Status(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=64)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name} ({self.type.name})"

class SubCategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class CashFlowRecord(models.Model):
    created_at = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)
    custom_date = models.DateField(null=True, blank=True, help_text="Можно изменить дату записи вручную")

    def clean(self):
        if self.category.type != self.type:
            raise ValidationError("Выбранная категория не относится к выбранному типу.")
        if self.subcategory.category != self.category:
            raise ValidationError("Выбранная подкатегория не относится к выбранной категории.")

    def __str__(self):
        return f"{self.created_at} | {self.amount}₽ | {self.status.name}"
