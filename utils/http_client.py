import requests
from utils.allure_helper import attach_http

class ApiClient:
    def __init__(self, base_url: str, timeout: int = 20) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session_id = None
        self.admin_session_id = None

    def request(
            self,
            method: str,
            endpoint: str,
            params: dict | None = None,
            data: dict | None = None,
            json: dict | None = None,
            headers: dict | None = None,
    ) -> requests.Response:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}/{endpoint.lstrip('/')}"

        headers = headers or {}
        if self.session_id:
            headers["sessionId"] = self.session_id

        if self.admin_session_id:
            headers["adminSessionId"] = self.admin_session_id

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=self.timeout,
        )
        attach_http(method, url, params, data, json, response)
        return response

    def get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: dict | None = None, json: dict | None = None, headers: dict | None = None, params: dict | None = None) -> requests.Response:
        return self.request("POST", endpoint, data=data, json=json, params=params, headers=headers)

    def put(self, endpoint: str, data: dict | None = None) -> requests.Response:
        return self.request("PUT", endpoint, data=data)

    def delete(self, endpoint: str, data: dict | None = None) -> requests.Response:
        return self.request("DELETE", endpoint, data=data)