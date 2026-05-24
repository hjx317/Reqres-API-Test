import requests
import pytest
import allure
import json

BASE_URL = "https://reqres.in/api"
API_KEY = "free_user_3EB0UbftyiJ75A85PLhPcHXM5y9"
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}


@allure.feature("用户管理")
@allure.story("查询用户")
class TestUserQuery:

    @allure.title("分页查询第2页用户")
    @allure.description("""
    验证分页查询接口：
    1. 状态码 200
    2. 每页返回6条数据
    3. 字段完整性校验
    4. 第2页第一个用户id为7
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_users_page2(self):
        with allure.step("步骤1：发送GET请求，查询第2页用户"):
            response = requests.get(
                f"{BASE_URL}/users",
                params={"page": 2},
                headers=HEADERS
            )
            allure.attach(
                f"URL: {response.url}\nStatus: {response.status_code}",
                name="请求信息",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("步骤2：校验状态码为200"):
            assert response.status_code == 200
            allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤3：校验响应数据结构"):
            data = response.json()

            # 校验分页字段
            required_fields = ["page", "per_page", "total", "total_pages", "data", "support"]
            for field in required_fields:
                assert field in data, f"缺少字段: {field}"

            # 校验用户字段
            user_fields = ["id", "email", "first_name", "last_name", "avatar"]
            for user in data["data"]:
                for field in user_fields:
                    assert field in user, f"用户对象缺少字段: {field}"

            allure.attach(
                json.dumps(data, indent=2, ensure_ascii=False),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("步骤4：校验业务数据"):
            assert len(data["data"]) == 6
            assert data["data"][0]["id"] == 7
            allure.attach(f"数据条数: {len(data['data'])}\n第一个用户ID: {data['data'][0]['id']}",
                          name="业务校验结果", attachment_type=allure.attachment_type.TEXT)


@allure.feature("用户管理")
@allure.story("创建用户")
class TestUserCreate:

    @allure.title("创建新用户")
    @allure.description("验证创建用户接口：状态码201、返回id和createdAt、数据一致性")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user(self):
        payload = {"name": "morpheus", "job": "leader"}

        with allure.step("步骤1：准备请求数据"):
            allure.attach(
                json.dumps(payload, indent=2),
                name="请求体",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("步骤2：发送POST请求"):
            response = requests.post(
                f"{BASE_URL}/users",
                json=payload,
                headers=HEADERS
            )

        with allure.step("步骤3：校验创建结果"):
            assert response.status_code == 201
            data = response.json()

            assert "id" in data, "响应缺少id字段"
            assert "createdAt" in data, "响应缺少createdAt字段"
            assert data["name"] == payload["name"], f"name不匹配: 期望{payload['name']}, 实际{data['name']}"
            assert data["job"] == payload["job"], f"job不匹配: 期望{payload['job']}, 实际{data['job']}"

            allure.attach(
                json.dumps(data, indent=2),
                name="创建结果",
                attachment_type=allure.attachment_type.JSON
            )


@allure.feature("用户管理")
@allure.story("更新用户")
class TestUserUpdate:

    @allure.title("更新用户信息")
    @allure.description("验证PUT更新接口：状态码200、返回updatedAt、job更新成功")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_user(self):
        payload = {"name": "morpheus", "job": "zion resident"}

        with allure.step("步骤1：发送PUT请求更新用户2"):
            response = requests.put(
                f"{BASE_URL}/users/2",
                json=payload,
                headers=HEADERS
            )

        with allure.step("步骤2：校验更新结果"):
            assert response.status_code == 200
            data = response.json()

            assert "updatedAt" in data, "响应缺少updatedAt字段"
            assert data["job"] == "zion resident", f"job未更新: 实际{data['job']}"

            allure.attach(
                json.dumps(data, indent=2),
                name="更新结果",
                attachment_type=allure.attachment_type.JSON
            )


@allure.feature("用户管理")
@allure.story("删除用户")
class TestUserDelete:

    @allure.title("删除用户")
    @allure.description("验证DELETE删除接口：状态码204、无返回内容")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user(self):
        with allure.step("步骤1：发送DELETE请求删除用户2"):
            response = requests.delete(
                f"{BASE_URL}/users/2",
                headers=HEADERS
            )

        with allure.step("步骤2：校验删除结果"):
            assert response.status_code == 204
            allure.attach(f"状态码: {response.status_code}\n响应内容为空",
                          name="删除结果", attachment_type=allure.attachment_type.TEXT)


@allure.feature("认证模块")
@allure.story("登录")
class TestAuth:

    @allure.title("登录成功")
    @allure.description("验证登录成功：状态码200、返回token")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self):
        payload = {
            "email": "eve.holt@reqres.in",
            "password": "cityslicka"
        }

        with allure.step("步骤1：发送登录请求"):
            response = requests.post(
                f"{BASE_URL}/login",
                json=payload,
                headers=HEADERS
            )
            allure.attach(
                json.dumps(payload, indent=2),
                name="登录参数",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("步骤2：校验登录成功"):
            assert response.status_code == 200
            data = response.json()
            assert "token" in data, "登录成功但未返回token"

            allure.attach(
                json.dumps(data, indent=2),
                name="登录响应",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.title("登录失败-缺少密码")
    @allure.description("验证登录失败：状态码400、返回错误信息")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_failure(self):
        payload = {"email": "peter@klaven"}

        with allure.step("步骤1：发送缺少密码的登录请求"):
            response = requests.post(
                f"{BASE_URL}/login",
                json=payload,
                headers=HEADERS
            )

        with allure.step("步骤2：校验登录失败"):
            assert response.status_code == 400
            data = response.json()
            assert "error" in data, "未返回错误信息"

            allure.attach(
                json.dumps(data, indent=2),
                name="错误响应",
                attachment_type=allure.attachment_type.JSON
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])