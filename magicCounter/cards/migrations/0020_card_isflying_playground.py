# Generated by Django 4.0.6 on 2022-07-14 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cards', '0019_alter_deck_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='isFlying',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Playground',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Aire de jeu',
            },
        ),
    ]
