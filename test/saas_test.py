import allure
import pytest
from utils.data_factory import cusComment

@allure.title("API-001 闻道世界数据")
@pytest.mark.api
def test_seniorQuery(api_client,session_id_save,global_data):
    response = api_client.post(
        "/xx/e/seniorQuery",
        params={"page": 1,"size":10},
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
    instanceModuleCode = payload.get("content", {}).get("t",{}).get("queryInfoList")[0].get("instanceModuleCode")
    print(instanceModuleCode)
    global_data["instanceModuleCode"] = instanceModuleCode
    targetCode = payload.get("content", {}).get("t", {}).get("queryInfoList")[0].get("targetCode")
    print(targetCode)
    global_data["targetCode"] = targetCode
    print(global_data)


# 在闻道世界第一个实例的第一个任务进行评论
def test_cusComment(api_client,session_id_save,instance_target_save):
    print(instance_target_save)
    response = api_client.post(
        "/xx/mindscapes/cusComment",
        json={
            "content": cusComment(),
            "dataType": 1,
            "instanceModuleCode": instance_target_save["instanceModuleCode"],
            "page": 1,
            "relationCode": instance_target_save["targetCode"],
            "size": 10
        }
    )
    print(response.json())


# 展示评论内容
def test_cus_list(api_client,session_id_save,instance_target_save):
    responses = api_client.post(
        "/xx/mindscapes/cusComment/list",
        params={"page": 1,"size":10},
        json={
            "instanceModuleCode": instance_target_save["instanceModuleCode"],
            "relationCode": instance_target_save["targetCode"],
            "dataType": 1
        }
    )
    payload = responses.json()
    content_list = [
        item.get("content")
        for item in payload.get("content", {}).get("commentList", [])
    ]
    print(content_list)

def test_login(api_client,login_data):
    print(login_data[1]['account'],login_data[1]['passwd'])
    response = api_client.post(
        "/xx/n/login",
        json={
            "account": login_data[0]['account'],
            "passwd": login_data[0]['passwd']
        }
    )
    payload = response.json()
    print(payload)