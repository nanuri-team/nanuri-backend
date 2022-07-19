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


class AuthTokenSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=32)
    token = serializers.CharField(max_length=2048)
    uuid = serializers.UUIDField()

    # NotImplementedError 발생시키도록 구현되어 있음
    # 이 정보를 DB에 등록할 것이 아니므로 사실상 필요없는 메서드
    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    # NotImplementedError 발생시키도록 구현되어 있음
    # 이 정보를 DB에 등록할 것이 아니므로 사실상 필요없는 메서드
    def create(self, validated_data):
        super().create(validated_data)
