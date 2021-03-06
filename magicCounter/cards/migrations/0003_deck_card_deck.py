# Generated by Django 4.0.6 on 2022-07-05 15:08

from django.db import migrations, models
import django.db.models.deletion
from user.models import CustomUser


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_alter_card_defense_alter_card_power'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cards', models.JSONField(blank=True)),
                ('colors', models.JSONField(default={'black', 'white'})),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cards.deck'),
        ),
    ]
