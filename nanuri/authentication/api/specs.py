from drf_spectacular.utils import extend_schema

kakao_accounts_api_specs = {
    "post": extend_schema(
        description="<h2>카카오 계정 정보를 등록하는 API</h2>",
        summary="Create a new Kakao user",
        tags=["Kakao Account"],
    ),
}
