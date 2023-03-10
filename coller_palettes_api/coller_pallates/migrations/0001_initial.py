# Generated by Django 3.2.18 on 2023-03-10 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorPalette',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('dominant_color1', models.CharField(max_length=7)),
                ('dominant_color2', models.CharField(blank=True, max_length=7, null=True)),
                ('accent_colors1', models.CharField(max_length=7)),
                ('accent_colors2', models.CharField(max_length=7)),
                ('accent_colors3', models.CharField(blank=True, max_length=7, null=True)),
                ('accent_colors4', models.CharField(blank=True, max_length=7, null=True)),
                ('is_public', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_palattes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]