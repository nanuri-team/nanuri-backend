from drf_spectacular.utils import extend_schema

kakao_accounts_api_specs = {
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
