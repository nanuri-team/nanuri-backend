from rest_framework import serializers

from ..models import KakaoAccount


class KakaoAccountSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        slug_field="email",
        read_only=True,
    )

    class Meta:
        model = KakaoAccount
        fields = ["user", "kakao_id", "created_at", "updated_at"]
