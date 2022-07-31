# Generated by Django 3.2.14 on 2022-07-31 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20220726_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='opt_in',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='group_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='opt_in',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='topic',
            field=models.CharField(choices=[('To all', '공지사항'), ('To post writer', '공동구매 진행자에게 보내는 푸시 알림'), ('To post participants', '공동구매 참여자에게 보내는 푸시 알림'), ('To participants of chat room', '채팅방 참가자에게 보내는 푸시 알림')], default=None, max_length=255, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('device', 'topic', 'group_code')},
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='post',
        ),
    ]
