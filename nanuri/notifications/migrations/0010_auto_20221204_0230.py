# Generated by Django 3.2.16 on 2022-12-04 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0009_remove_device_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_token',
            field=models.TextField(blank=True, help_text='기기마다 고유한 문자열 값입니다. iOS 기기인 경우 APNs를 통해 얻을 수 있습니다.', null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='endpoint_arn',
            field=models.TextField(blank=True, help_text='Amazon SNS에서 사용되는 모바일 엔드포인트 ARN 주소입니다.', null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='opt_in',
            field=models.BooleanField(default=True, help_text='모바일 푸시 알림 수신 여부를 나타냅니다.'),
        ),
    ]
