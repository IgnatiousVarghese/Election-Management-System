# Generated by Django 3.2.9 on 2021-11-18 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0002_candidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.candidate')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.post')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.voter')),
            ],
            options={
                'unique_together': {('voter', 'post')},
            },
        ),
    ]
