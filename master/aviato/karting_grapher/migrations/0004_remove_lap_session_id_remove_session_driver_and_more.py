# Generated by Django 4.1 on 2022-08-30 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("karting_grapher", "0003_driver_lap_session_track_delete_blog_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="lap", name="session_id",),
        migrations.RemoveField(model_name="session", name="driver",),
        migrations.RemoveField(model_name="session", name="track_id",),
        migrations.DeleteModel(name="Driver",),
        migrations.DeleteModel(name="Lap",),
        migrations.DeleteModel(name="Session",),
        migrations.DeleteModel(name="Track",),
    ]
