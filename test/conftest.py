from http.client import responses

import pytest
from allure_commons import fixture
from certifi import contents

from utils.config import load_config      # 加载配置文件的工具
# from utils.data_factory import user_payload  # 生成测试用户数据的工厂函数
from utils.http_client import ApiClient    # 自定义的HTTP客户端类
from utils.data_store import load_data, save_data
from utils.data_factory import admin_payload
from data.testdata.data_read import Test1

@pytest.fixture(scope="session")
def config() -> dict:
    return load_config()

@pytest.fixture(scope="session")
def api_client(config: dict) -> ApiClient:
    return ApiClient(config["api_base_url"], timeout=config["timeout_seconds"])


@pytest.fixture(scope="session")
def admin_account():
    return

# saas登录
@pytest.fixture(scope="session")
def temp_session_id_save(api_client):
    response = api_client.post(
        "/xx/n/login",
        json={"account": "xxx", "passwd": "xxx"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("code") == 200
    assert payload.get("success"), "登录失败"
    temp_session_id = payload.get("content", {}).get("tempSessionId")
    return temp_session_id


# saas登录验证
@pytest.fixture(scope="session")
def session_id_save(api_client, temp_session_id_save):
    response = api_client.post(
        "/xx/n/confirmLogin",
        json={"tempSessionId": temp_session_id_save},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("code") == 200
    assert payload.get("success"), "登录失败"
    session_id = payload.get("content", {}).get("sessionId")
    api_client.session_id = session_id
    return session_id


# 获取闻道世界数据
@pytest.fixture(scope="session")
def instance_target_save(api_client, session_id_save):
    response = api_client.post(
        "/xx/e/seniorQuery",
        params={"page": 1, "size": 10},
        json={
            "templateClassifyCode": None,
            "templateCode": None,
            "classifyType": None,
            "classifyCode": None,
            "sortType": "1",
            "typeCode": [],
            "queryChildrenDTOList": []
        }
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("code") == 200
    assert payload.get("success"), "登录失败"

    instanceModuleCode = payload.get("content", {}).get("t", {}).get("queryInfoList")[0].get("instanceModuleCode")
    targetCode = payload.get("content", {}).get("t", {}).get("queryInfoList")[0].get("targetCode")
    return {
        "instanceModuleCode": instanceModuleCode,
        "targetCode": targetCode
    }



@pytest.fixture(scope="session")
def global_data():
    """
    全局数据存储中心
    """

    # 启动pytest时读取文件
    data = load_data()

    yield data

    # pytest结束自动保存
    save_data(data)

    return {}


# cms登录
@pytest.fixture(scope="session")
def admin_session_save(api_client):
    admin = admin_payload()
    account = admin.get("account")
    password = admin.get("password")
    response = api_client.post(
        "/xx/admin/login",
        json={
            "account":account,
            "password":password
        },
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload.get("code") ==200
    assert payload.get("success"), "登录失败"
    admin_session_id = payload.get("content", {}).get("adminSessionId")
    api_client.admin_session_id = admin_session_id
    return admin_session_id


# 新建实例
@pytest.fixture(scope="session")
def batch_create_instanceCode_save(api_client, admin_session_save,global_data):
    if "instanceCode" in global_data:
        return global_data["instanceCode"]

    print("创建 instanceCode...")
    response = api_client.post(
        "/xx/admin/researchInstance/batchCreate",
        json={
            "instances": [
                {
                    "id": "3ed706b26f5ac04ff76beaafe980cd67",
                    "instanceName": "同义词-任务-测试",
                    "templateCode": "57ce5f58c0a1441aa9408bc26b5ed88e", #模板templateCode
                    "industryClassifyCodes": [
                        "be3cd0f163b74d68b93a9e4b5f3dbccf"
                    ],  #industryClassifyCodes为申万行业code
                    "entCodes": [],
                    "customClassifyCodes": [
                        "d8ffb38192e0486d835c9238b799752f",
                        "b848af986db04c13888d0cce78d649c8",
                    ],# customClassifyCodes为主题code
                }
            ]
        },
    )
    payload = response.json()
    assert response.status_code == 200
    assert str(payload.get("success")).lower() in {"true", "1", "yes"}
    instanceCode = payload.get("content")
    global_data["instanceCode"] = instanceCode
    return global_data["instanceCode"]

# 获取实例的instanceCode，根据instanceCode去获取实例内的moduleCode
@pytest.fixture(scope="session")
def research_instance(api_client, admin_session_save,global_data):
    instance_code = global_data["instanceCode"][0]
    response = api_client.get(
            f"/xx/admin/researchInstance/{instance_code}"
    )
    payload = response.json()
    module_tree = payload.get("content", {}).get("template",{}).get("moduleTree",[])
    result = []

    def recurse(nodes):
        for node in nodes:
            children = node.get("children",[])
            if not children:
                result.append(node.get("moduleCode"))
            else:
                recurse(children)

    recurse(module_tree)
    global_data["moduleCode"] = result

# 获取新建任务的taskCode
@pytest.fixture(scope="session")
def task_code_save(api_client,admin_session_save,global_data):
    response = api_client.get(
        "/xx/admin/task/manager/listOfInstance",
        params={"instanceCode": global_data["instanceCode"][0]}
    )
    payload = response.json()
    content = payload.get("content",[])
    taskCode = []
    for item in content:
        taskCode.append(item.get("taskCode"))
    global_data["taskCode"] = taskCode
    return taskCode


# 获取生产人员和审批人员的nodeCode
@pytest.fixture(scope="session")
def verify_task_nodes_save(api_client,admin_session_save):
    response = api_client.get(
        "xx/admin/task/manager/verifyTaskNodes",
        params={"page": 1,"size": 10}
    )
    payload = response.json()
    content = payload.get("content",[])
    nodeCode = []
    for item in content:
        nodeCode.append(item.get("nodeCode"))
    return nodeCode


# 获取执行人员的accountCode
@pytest.fixture(scope="session")
def producers_accountCode_save(api_client,admin_session_save):
    response = api_client.post(
        "/xx/admin/task/producers",
        json={"taskNodeCode": ""}
    )
    payload = response.json()
    content = payload.get("content",[])
    for item in content:
        if item["name"] == "测试组长，总监11":
            accountCode = item.get("accountCode")
            return accountCode


@pytest.fixture(scope="session")
def login_data():
    return Test1().a1_data(sheet="login")