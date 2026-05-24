import pytest
import requests
import allure
import json

BASE_URL = "https://reqres.in/api"
API_KEY = "free_user_3EB0UbftyiJ75A85PLhPcHXM5y9"
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# 多组测试数据
create_user_data = [
    {"name": "morpheus", "job": "leader", "expected_name": "morpheus", "expected_job": "leader"},
    {"name": "neo", "job": "the one", "expected_name": "neo", "expected_job": "the one"},
    {"name": "trinity", "job": "hacker", "expected_name": "trinity", "expected_job": "hacker"},
    {"name": "agent_smith", "job": "virus", "expected_name": "agent_smith", "expected_job": "virus"},
]


@allure.feature("用户管理")
@allure.story("创建用户-数据驱动")
class TestUserCreateDataDriven:

    @allure.title("创建用户: {data[name]}")
    @pytest.mark.parametrize("data", create_user_data)
    def test_create_user_with_data(self, data):
        with allure.step(f"步骤1：发送POST请求，创建用户 {data['name']}"):
            response = requests.post(
                f"{BASE_URL}/users",
                json={"name": data["name"], "job": data["job"]},
                headers=HEADERS
            )
            allure.attach(
                json.dumps({"name": data["name"], "job": data["job"]}, indent=2),
                name="请求数据",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step("步骤2：校验状态码201"):
            assert response.status_code == 201

        with allure.step("步骤3：校验返回数据"):
            result = response.json()
            assert result["name"] == data["expected_name"]
            assert result["job"] == data["expected_job"]
            assert "id" in result
            assert "createdAt" in result

            allure.attach(
                json.dumps(result, indent=2),
                name="响应数据",
                attachment_type=allure.attachment_type.JSON
            )


# 登录测试数据：包含预期结果
login_data = [
    {
        "case_name": "正确的用户名密码",
        "payload": {"email": "eve.holt@reqres.in", "password": "cityslicka"},
        "expected_status": 200,
        "expected_field": "token",
        "description": "登录成功应返回token"
    },
    {
        "case_name": "缺少密码",
        "payload": {"email": "peter@klaven"},
        "expected_status": 400,
        "expected_field": "error",
        "description": "缺少密码应返回错误"
    },
    # 修改这条：reqres.in 对不存在用户返回 400
    {
        "case_name": "不存在的用户",
        "payload": {"email": "notexist@reqres.in", "password": "123456"},
        "expected_status": 400,
        "expected_field": "error",
        "description": "用户不存在应返回错误"
    },
    # 新增：空密码
    {
        "case_name": "空密码",
        "payload": {"email": "eve.holt@reqres.in", "password": ""},
        "expected_status": 400,
        "expected_field": "error",
        "description": "空密码应返回错误"
    },
]


@allure.feature("认证模块")
@allure.story("登录-数据驱动")
class TestLoginDataDriven:

    @allure.title("登录测试: {data[case_name]}")
    @pytest.mark.parametrize("data", login_data)
    def test_login_with_data(self, data):
        with allure.step(f"场景: {data['case_name']}"):
            allure.attach(data["description"], name="测试说明", attachment_type=allure.attachment_type.TEXT)

        with allure.step("步骤1：发送登录请求"):
            response = requests.post(
                f"{BASE_URL}/login",
                json=data["payload"],
                headers=HEADERS
            )
            allure.attach(
                json.dumps(data["payload"], indent=2),
                name="请求参数",
                attachment_type=allure.attachment_type.JSON
            )

        with allure.step(f"步骤2：校验状态码为{data['expected_status']}"):
            assert response.status_code == data["expected_status"], \
                f"期望状态码{data['expected_status']}, 实际{response.status_code}"

        with allure.step(f"步骤3：校验返回包含{data['expected_field']}"):
            result = response.json()
            assert data["expected_field"] in result, \
                f"期望包含字段'{data['expected_field']}', 实际响应: {result}"

            allure.attach(
                json.dumps(result, indent=2),
                name="响应结果",
                attachment_type=allure.attachment_type.JSON
            )


# 分页查询测试数据
page_data = [
    {"page": 1, "expected_first_id": 1, "description": "第1页第一个用户id应为1"},
    {"page": 2, "expected_first_id": 7, "description": "第2页第一个用户id应为7"},
]


@allure.feature("用户管理")
@allure.story("分页查询-数据驱动")
class TestUserPageDataDriven:

    @allure.title("查询第{data[page]}页用户")
    @pytest.mark.parametrize("data", page_data)
    def test_get_users_page(self, data):
        with allure.step(f"步骤1：查询第{data['page']}页"):
            response = requests.get(
                f"{BASE_URL}/users",
                params={"page": data["page"]},
                headers=HEADERS
            )

        with allure.step("步骤2：校验数据"):
            assert response.status_code == 200
            result = response.json()
            assert result["data"][0]["id"] == data["expected_first_id"]

            allure.attach(
                f"第{data['page']}页第一个用户ID: {result['data'][0]['id']}",
                name="校验结果",
                attachment_type=allure.attachment_type.TEXT
            )