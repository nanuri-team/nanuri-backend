# Generated by Django 3.2.14 on 2022-08-02 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20220731_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='topic',
            field=models.CharField(choices=[('TO_ALL', '공지사항'), ('TO_POST_WRITER', '공동구매 진행자에게 보내는 푸시 알림'), ('TO_POST_WRITERS', '공동구매 참여자에게 보내는 푸시 알림'), ('TO_CHAT_ROOM', '채팅방 참가자에게 보내는 푸시 알림')], default=None, max_length=255, null=True),
        ),
    ]
