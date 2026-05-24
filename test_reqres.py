import requests
import pytest

BASE_URL = "https://reqres.in/api"

# 替换为你的实际 API Key
API_KEY = "free_user_3EB0UbftyiJ75A85PLhPcHXM5y9"

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}


class TestReqresAPI:

    def test_get_users_page2(self):
        """测试分页查询用户"""
        response = requests.get(
            f"{BASE_URL}/users",
            params={"page": 2},
            headers=HEADERS
        )

        # 1. 状态码断言
        assert response.status_code == 200

        data = response.json()

        # 2. 数据条数校验
        assert len(data["data"]) == 6

        # 3. 字段完整性校验
        required_fields = ["page", "per_page", "total", "total_pages", "data", "support"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        # 校验每个用户对象
        user_fields = ["id", "email", "first_name", "last_name", "avatar"]
        for user in data["data"]:
            for field in user_fields:
                assert field in user, f"User missing field: {field}"

        # 4. 业务数据校验
        assert data["data"][0]["id"] == 7

    def test_create_user(self):
        """测试创建用户"""
        payload = {
            "name": "morpheus",
            "job": "leader"
        }

        response = requests.post(
            f"{BASE_URL}/users",
            json=payload,
            headers=HEADERS
        )

        assert response.status_code == 201
        data = response.json()

        assert "id" in data
        assert "createdAt" in data
        assert data["name"] == "morpheus"
        assert data["job"] == "leader"

    def test_update_user(self):
        """测试更新用户"""
        payload = {
            "name": "morpheus",
            "job": "zion resident"
        }

        response = requests.put(
            f"{BASE_URL}/users/2",
            json=payload,
            headers=HEADERS
        )

        assert response.status_code == 200
        data = response.json()
        assert "updatedAt" in data
        assert data["job"] == "zion resident"

    def test_delete_user(self):
        """测试删除用户"""
        response = requests.delete(
            f"{BASE_URL}/users/2",
            headers=HEADERS
        )
        assert response.status_code == 204

    def test_login_success(self):
        """测试登录成功"""
        payload = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }

        response = requests.post(
            f"{BASE_URL}/login",
            json=payload,
            headers=HEADERS
        )

        assert response.status_code == 200
        data = response.json()
        assert "token" in data

    def test_login_failure(self):
        """测试登录失败"""
        payload = {
            "email": "peter@klaven"
        }

        response = requests.post(
            f"{BASE_URL}/login",
            json=payload,
            headers=HEADERS
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v"])