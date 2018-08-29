# Generated by Django 2.0.7 on 2018-08-28 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180827_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprice',
            name='date_end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productprice',
            name='date_start',
            field=models.DateField(default='2018-07-01'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='duration',
            field=models.CharField(db_index=True, default='Flash', help_text='Event or period name price in effect', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='giftcard',
            name='code',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(db_index=True, help_text='Internal facing reference to product', max_length=10),
        ),
    ]
