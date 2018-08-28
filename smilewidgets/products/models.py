from django.core.exceptions import ValidationError
from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, db_index=True, help_text='Internal facing reference to product')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class ProductPrice(models.Model):
    duration = models.CharField(max_length=30, db_index=True, help_text='Event or period name price in effect')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    date_start = models.DateField(default='2018-07-01')
    date_end = models.DateField(blank=True, null=True)

    @property
    def formatted_price(self):
        return '${0:.2f}'.format(self.price / 100)

    def __str__(self):
        return '{} - {} - {}'.format(self.duration, self.product.name, self.price)

    def clean(self):
        try:
            if self.date_start >= self.date_end:
                raise ValidationError({
                    'date_start': ValidationError(_('Start date must be less than end date'), code='invalid'),
                    'date_end': ValidationError(_('End date must be greater than start date'), code='invalid'),
                })
        except NameError:
            pass  # date_end is not set no need to validate


class GiftCard(models.Model):
    code = models.CharField(max_length=30, db_index=True)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)
    
    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    def clean(self):
        try:
            if self.date_start >= self.date_end:
                raise ValidationError({
                    'date_start': ValidationError(_('Start date must be less than end date'), code='invalid'),
                    'date_end': ValidationError(_('End date must be greater than start date'), code='invalid'),
                })
        except NameError:
            pass  # date_end is not set no need to validate

