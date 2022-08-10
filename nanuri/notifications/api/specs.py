from drf_spectacular.utils import OpenApiParameter, extend_schema

devices_api_specs = {
    "post": extend_schema(
        description="<h2>기기 정보를 등록합니다.</h2>",
        summary="Create a new device",
        tags=["Device"],
    ),
}


device_api_specs = {
    "get": extend_schema(
        description="<h2>특정 기기 정보를 조회합니다.</h2>",
        summary="Get a device",
        tags=["Device"],
    ),
    "put": extend_schema(
        description="<h2>특정 기기 정보를 수정합니다.</h2>",
        summary="Update a device",
        tags=["Device"],
    ),
    "patch": extend_schema(
        description="<h2>특정 기기 정보를 부분 수정합니다.</h2>",
        summary="Patch a device",
        tags=["Device"],
    ),
    "delete": extend_schema(
        description="<h2>특정 기기 정보를 삭제합니다.</h2>",
        summary="Delete a device",
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
    "delete": extend_schema(
        description="<h2>특정 구독을 삭제합니다.</h2>",
        summary="Delete a subscription",
        tags=["Subscription"],
    ),
}
