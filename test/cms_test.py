from http.client import responses

import allure
import pytest

from utils.data_factory import admin_payload
from utils.data_factory import content
from utils.log import log

# # cms登录
# def test_cms_login(api_client):
#     admin = admin_payload()
#     account = admin.get("account")
#     password = admin.get("password")
#     response = api_client.post(
#         "/xx/admin/login", json={"account": account, "password": password}
#     )
#     payload = response.json()
#     assert response.status_code == 200
#     assert payload.get("code") == 200
#     assert payload.get("success"), "登录失败"
#     adminSession = payload.get("content", {}).get("adminSessionId")
#     print(adminSession)
#
#
# # 新建实例
# def test_batch_create(api_client, admin_session_save,global_data):
#     response = api_client.post(
#         "/xx/admin/researchInstance/batchCreate",
#         json={
#             "instances": [
#                 {
#                     "id": "3ed706b26f5ac04ff76beaafe980cd67",
#                     "instanceName": "自动测试02",
#                     "templateCode": "57ce5f58c0a1441aa9408bc26b5ed88e",
#                     "industryClassifyCodes": [
#                         "ee285a2d6eed4a70b3de7fb2022d2c28",
#                         "201977c81ed04ea487496853603115f3",
#                         "a5ad99086cd54f12a17062a1cbae2db6",
#                     ],
#                     "entCodes": [],
#                     "customClassifyCodes": [
#                         "d8ffb38192e0486d835c9238b799752f",
#                         "b848af986db04c13888d0cce78d649c8",
#                     ],
#                 }
#             ]
#         },
#     )
#     payload = response.json()
#     assert response.status_code == 200
#     assert str(payload.get("success")).lower() in {"true", "1", "yes"}
#     content = payload.get("content")
#     global_data["instanceCode"] = content
#
#
# 获取实例中的instance
# def test_research_instance(api_client, admin_session_save,batch_create_instanceCode_save):
#     instance_code = batch_create_instanceCode_save[0]
#     response = api_client.get(
#             f"/xx/admin/researchInstance/{instance_code}"
#     )
#     payload = response.json()
#     module_tree = payload.get("content", {}).get("template",{}).get("moduleTree",[])
#     result = []
#
#     def recurse(nodes):
#         for node in nodes:
#             children = node.get("children",[])
#             if not children:
#                 result.append(node.get("moduleCode"))
#             else:
#                 recurse(children)
#
#     recurse(module_tree)
#     print(result)



# 创建公告任务
@allure.title("API-001 创建公告任务")
@pytest.mark.api
def test_create_single_task(api_client, admin_session_save, batch_create_instanceCode_save, research_instance, global_data):
    instance_code = batch_create_instanceCode_save[0]
    log.info("开始创建公告任务")
    response = api_client.post(
        "/xx/admin/researchInstance/createSingleTask",
        json={
            "instanceCode":instance_code,
            "moduleCode":global_data["moduleCode"][0]
        }
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["errMsg"] is None
    content = payload.get("content",{})
    global_data["instanceModuleCode"]=content.get("instanceModuleCode")
    global_data["taskCode"] = content.get("taskCode")


# 委派任务
@allure.title("API-002 委派任务")
@pytest.mark.api
def test_assign_to_dept(api_client,admin_session_save,verify_task_nodes_save,producers_accountCode_save,global_data):
    log.info("开始委派任务")
    response = api_client.post(
        "/xx/admin/task/manager/assignToDept",
        json={
            "taskCodes": [global_data["taskCode"]],
            "producerAccountCode": producers_accountCode_save,
             "verify": [
        {
            "nodeCode": verify_task_nodes_save[0],
            "nodeName": "分配任务",
            "processUserCode": producers_accountCode_save
        },
        {
            "nodeCode": verify_task_nodes_save[1],
            "nodeName": "生产任务",
            "processUserCode": producers_accountCode_save
        },
        {
            "nodeCode": verify_task_nodes_save[2],
            "nodeName": "一级审批",
            "processUserCode": producers_accountCode_save
        },
        {
            "nodeCode": verify_task_nodes_save[3],
            "nodeName": "二级审批",
            "processUserCode": producers_accountCode_save
        }
    ]
        }
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["errMsg"] is None

# 保存正文内容
@allure.title("API-003 保存正文内容")
@pytest.mark.api
def test_content_save(api_client,admin_session_save,global_data):
    log.info("开始保存正文内容")
    response = api_client.post(
        "/xx/admin/task/content",
        json={
            "contentData":content(),
            "taskCode":global_data["taskCode"]
        }
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["errMsg"] is None



# 提交审核
@allure.title("API-004 提交审核")
@pytest.mark.api
def test_confirm(api_client,admin_session_save,global_data):
    log.info("开始提交审核")
    response = api_client.post(
        "/xx/admin/task/confirm",
        json={"taskCode":global_data["taskCode"]}
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["errMsg"] is None

# 发布正文
@allure.title("API-005 发布正文")
@pytest.mark.api
def test_launch(api_client,admin_session_save,global_data):
    log.info("开始发布正文")
    response = api_client.post(
        "/xx/admin/task/manager/launch",
        json={"taskCodes": [global_data["taskCode"]]}
    )
    payload = response.json()
    assert response.status_code == 200
    assert payload["errMsg"] is None