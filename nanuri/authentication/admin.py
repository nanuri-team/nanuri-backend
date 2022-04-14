from django.contrib import admin

from .models import KakaoAccount


class KakaoAccountAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'kakao_id',
    ]


admin.site.register(KakaoAccount, KakaoAccountAdmin)
