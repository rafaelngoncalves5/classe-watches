# Generated by Django 4.2.1 on 2023-05-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='apartment',
            field=models.CharField(default='', help_text='Anule, se não tiver', null=True, verbose_name='Número da residência'),
        ),
        migrations.AddField(
            model_name='order',
            name='floor',
            field=models.CharField(default='', max_length=6, null=True, verbose_name='Andar'),
        ),
        migrations.AlterField(
            model_name='order',
            name='city',
            field=models.CharField(max_length=50, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='order',
            name='district',
            field=models.CharField(help_text='Anule, se não tiver', max_length=25, verbose_name='Bairro'),
        ),
    ]
