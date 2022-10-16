from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from .serializers import DeviceSerializer

devices_api_specs = {
    "post": extend_schema(
        summary="모바일 기기 정보를 추가합니다.",
        description="모바일 기기 정보를 추가합니다.",
        tags=["Device"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                value={
                    "device_token": "a1d8683b74b02fb064d288a9652763707c1e255d607fbc7e30f003da11384999",
                },
                description="디바이스 토큰은 기기마다 고유한 값을 가집니다. iOS 기기인 경우 APNs를 통해 얻을 수 있습니다.",
                request_only=True,
            )
        ],
        responses={
            201: OpenApiResponse(
                response=DeviceSerializer,
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "uuid": "4ed3e784-c1b4-4819-bcd7-fa316c2cade3",
                            "user": "user@example.com",
                            "device_token": "a1d8683b74b02fb064d288a9652763707c1e255d607fbc7e30f003da11384999",
                            "endpoint_arn": "arn:aws:sns:ap-northeast-2:000000000000:endpoint/APNS/TestApplication/6a8d5d65-9418-43a8-bb81-f09449f90602",
                            "opt_in": True,
                        },
                        response_only=True,
                        description="opt_in 값이 `false` 인 경우, endpoint_arn 값은 `null`로 설정됩니다.",
                    )
                ],
            )
        },
    ),
}


device_api_specs = {
    "get": extend_schema(
        summary="특정 모바일 기기 정보를 조회합니다.",
        description="특정 모바일 기기 정보를 조회합니다.",
        tags=["Device"],
        responses={
            200: OpenApiResponse(
                response=DeviceSerializer,
                description="",
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "uuid": "9c7c33ea-227a-45e1-b1dd-2ad93d0dcf4a",
                            "user": "user@example.com",
                            "device_token": "e29e4f187b06ef4a892eab2b13eb34cf79054ff0ca3ed8b234874a08c0b19416",
                            "endpoint_arn": "arn:aws:sns:ap-northeast-2:000000000000:endpoint/APNS/TestApplication/12119d3e-1dd7-4754-bf77-0ef653c35bed",
                            "opt_in": True,
                        },
                        response_only=True,
                    )
                ],
            )
        },
    ),
    "put": extend_schema(
        summary="특정 모바일 기기 정보를 수정합니다.",
        description="특정 모바일 기기 정보를 수정합니다.",
        tags=["Device"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                value={
                    "device_token": "f20b417a6ef6631abe171606a16c683f68d70ffea300f515105ccb51f34e8655",
                    "opt_in": False,
                },
                request_only=True,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=DeviceSerializer,
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "uuid": "36c624f6-5b64-44f7-905c-2fa6ecb17674",
                            "user": "user@example.com",
                            "device_token": "f20b417a6ef6631abe171606a16c683f68d70ffea300f515105ccb51f34e8655",
                            "endpoint_arn": None,
                            "opt_in": False,
                        },
                        response_only=True,
                        description="opt_in 값이 `false` 인 경우 endpoint_arn 값은 `null`로 설정됩니다.",
                    )
                ],
            )
        },
    ),
    "patch": extend_schema(
        summary="특정 모바일 기기 정보를 부분 수정합니다.",
        description="특정 모바일 기기 정보를 부분 수정합니다.",
        tags=["Device"],
        examples=[
            OpenApiExample(
                name="요청 예시",
                value={"opt_in": False},
                request_only=True,
                description="전체 모바일 푸시 알림을 수신거부하는 예시입니다.",
            )
        ],
        responses={
            200: OpenApiResponse(
                response=DeviceSerializer,
                examples=[
                    OpenApiExample(
                        name="응답 예시",
                        value={
                            "uuid": "36c624f6-5b64-44f7-905c-2fa6ecb17674",
                            "user": "user@example.com",
                            "device_token": "f20b417a6ef6631abe171606a16c683f68d70ffea300f515105ccb51f34e8655",
                            "endpoint_arn": None,
                            "opt_in": False,
                        },
                        description="opt_in 값이 `False`인 경우 endpoint_arn 값은 `null`로 설정됩니다.",
                    )
                ],
            )
        },
    ),
    "delete": extend_schema(
        summary="특정 모바일 기기 정보를 삭제합니다.",
        description="특정 모바일 기기 정보를 삭제합니다.",
        tags=["Device"],
    ),
}

subscriptions_api_specs = {
    "get": extend_schema(
        description="<h2>구독 목록을 조회합니다.</h2>",
        summary="Get list of subscriptions",
        tags=["Subscription"],
        parameters=[
            OpenApiParameter(
                name="device",
                location=OpenApiParameter.QUERY,
                description="Device UUID",
                required=False,
                type=str,
            )
        ],
    ),
    "post": extend_schema(
        description="<h2>구독을 생성합니다.</h2>",
        summary="Create a new subscription",
        tags=["Subscription"],
    ),
}


subscription_api_specs = {
    "get": extend_schema(
        description="<h2>특정 구독을 조회합니다.</h2>",
        summary="Get a subscription",
        tags=["Subscription"],
    ),
    "put": extend_schema(
        description="<h2>특정 구독을 수정합니다.</h2>",
        summary="Update a subscription",
        tags=["Subscription"],
    ),
    "patch": extend_schema(
        description="<h2>특정 구독을 부분 수정합니다.</h2>",
        summary="Patch a subscription",
        tags=["Subscription"],
    ),
    "delete": extend_schema(
        description="<h2>특정 구독을 삭제합니다.</h2>",
        summary="Delete a subscription",
        tags=["Subscription"],
    ),
}


messages_api_specs = {
    "post": extend_schema(
        description="""<h2>푸시 알림 메시지를 발행합니다.</h2>
        <p>topic이 `TO_ALL`일 때는 group_code를 `null`로 설정해도 무방합니다.</p>
        <p>topic이 `TO_POST_WRITER`, `TO_POST_PARTICIPANTS`, `TO_CHAT_ROOM`일 때는 해당 글의 UUID를 group_code 필드의 값으로 설정해야 합니다.</p>
        """,
        summary="Publish push notification message",
        tags=["Message"],
    )
}
