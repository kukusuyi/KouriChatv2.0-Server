import requests
from typing import Dict, Any, Optional

class Http:
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = 30  # 默认超时时间

    def get(self, address: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """发送 GET 请求"""
        try:
            return requests.get(
                self.base_url + address,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            print(f"GET 请求失败: {str(e)}")
            raise

    def post(self, address: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        """发送 POST 请求"""
        try:
            return requests.post(
                self.base_url + address,
                json=json,
                headers=self.headers,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            print(f"POST 请求失败: {str(e)}")
            raise

    def put(self, address: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """发送 PUT 请求"""
        try:
            return requests.put(
                self.base_url + address,
                data=data,
                headers=self.headers,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            print(f"PUT 请求失败: {str(e)}")
            raise

    def delete(self, address: str) -> requests.Response:
        """发送 DELETE 请求"""
        try:
            return requests.delete(
                self.base_url + address,
                headers=self.headers,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            print(f"DELETE 请求失败: {str(e)}")
            raise

    def set_headers(self, headers: Dict[str, str]) -> None:
        """设置请求头"""
        self.headers.update(headers)

    def set_timeout(self, timeout: int) -> None:
        """设置超时时间"""
        self.timeout = timeout

    def download_file(self, address: str, save_path: str) -> bool:
        """下载文件"""
        try:
            response = requests.get(
                self.base_url + address,
                headers=self.headers,
                stream=True,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            return True
        except Exception as e:
            print(f"文件下载失败: {str(e)}")
            return False