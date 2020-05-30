# Generated by Django 3.0.6 on 2020-05-28 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stars', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='exercises.Exercise')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stars.Star')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
