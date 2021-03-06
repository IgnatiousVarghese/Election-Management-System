# Generated by Django 3.2.8 on 2021-11-30 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0004_auto_20211130_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manage_post',
            name='ec',
        ),
        migrations.RemoveField(
            model_name='manage_post',
            name='post',
        ),
        migrations.RemoveField(
            model_name='candidate',
            name='id',
        ),
        migrations.AlterField(
            model_name='candidate',
            name='voter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='election.voter'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set(),
        ),
        migrations.DeleteModel(
            name='Manage_Candidate',
        ),
        migrations.DeleteModel(
            name='Manage_Post',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='post',
        ),
    ]
