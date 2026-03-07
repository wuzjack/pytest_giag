import json
from typing import Any

try:
    import allure
except Exception:
    allure = None

def attach_http(method: str, url: str, params:dict | None, data:dict | None, json_body:dict |None, response: Any) -> None:
    request_payload = {
        "method": method,
        "url": url,
        "params": params or {},
        "data": data or {},
        "json":json_body or {}
    }

    allure.attach(
        json.dumps(request_payload, ensure_ascii=False, indent=2),
        name="request",
        attachment_type=allure.attachment_type.JSON,
    )

    content_type = response.headers.get("Content-Type", "") if hasattr(response, "headers") else ""
    if "application/json" in content_type:
        attachment_type = allure.attachment_type.JSON
    else:
        attachment_type = allure.attachment_type.TEXT

    allure.attach(
        getattr(response, "text", ""),
        name="response",
        attachment_type=attachment_type,
    )
