# Generated by Django 4.0.6 on 2022-07-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_color_remove_card_colors_card_colors'),
    ]

    operations = [
        migrations.AddField(
            model_name='color',
            name='color',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='color',
            name='element',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='card',
            name='colors',
            field=models.ManyToManyField(blank=True, to='cards.color'),
        ),
        migrations.RemoveField(
            model_name='deck',
            name='colors',
        ),
        migrations.AddField(
            model_name='deck',
            name='colors',
            field=models.ManyToManyField(blank=True, to='cards.color'),
        ),
    ]
