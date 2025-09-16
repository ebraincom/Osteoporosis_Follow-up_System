import requests
import json

def debug_api_auth():
    """调试API认证逻辑"""
    base_url = "http://localhost:8000"
    
    # 登录李一御
    print("=== 登录李一御 ===")
    login_data = {"username": "李一御", "password": "xiaoyu988"}
    login_response = requests.post(f"{base_url}/v1/personal-auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"登录失败: {login_response.text}")
        return
    
    login_result = login_response.json()
    token = login_result["token"]
    user_info = login_result["user"]
    
    print(f"登录成功:")
    print(f"  用户ID: {user_info.get('id')}")
    print(f"  用户名: {user_info.get('username')}")
    print(f"  姓名: {user_info.get('name')}")
    print(f"  Token: {token[:50]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 测试获取当前用户信息
    print("\n=== 测试获取当前用户信息 ===")
    me_response = requests.get(f"{base_url}/v1/personal-auth/me", headers=headers)
    print(f"状态码: {me_response.status_code}")
    if me_response.status_code == 200:
        me_data = me_response.json()
        print(f"当前用户信息: {json.dumps(me_data, ensure_ascii=False, indent=2)}")
    else:
        print(f"错误: {me_response.text}")
    
    # 测试患者列表API
    print("\n=== 测试患者列表API ===")
    patients_response = requests.get(f"{base_url}/v1/patients/", headers=headers)
    print(f"状态码: {patients_response.status_code}")
    if patients_response.status_code == 200:
        patients_data = patients_response.json()
        print(f"患者列表: {json.dumps(patients_data, ensure_ascii=False, indent=2)}")
    else:
        print(f"错误: {patients_response.text}")

if __name__ == "__main__":
    debug_api_auth()