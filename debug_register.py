import requests
import json
import traceback

# 测试机构用户注册 - 详细调试
def debug_institutional_register():
    url = "http://localhost:8000/api/v1/auth/register"
    data = {
        "username": "debug_inst_user",
        "password": "test123456",
        "name": "调试机构用户",
        "phone": "13800138000",
        "user_type": "institutional",
        "institution": "调试医院",
        "department": "骨科"
    }
    
    print("=== 调试机构用户注册 ===")
    print("请求URL:", url)
    print("请求数据:", json.dumps(data, ensure_ascii=False, indent=2))
    
    try:
        response = requests.post(url, json=data)
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 机构用户注册成功")
        else:
            print("❌ 机构用户注册失败")
            # 尝试解析错误详情
            try:
                error_detail = response.json()
                print("错误详情:", json.dumps(error_detail, ensure_ascii=False, indent=2))
            except:
                print("无法解析错误详情")
                
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        traceback.print_exc()

# 测试不同的数据组合
def test_different_data():
    url = "http://localhost:8000/api/v1/auth/register"
    
    # 测试1: 最小数据
    data1 = {
        "username": "minimal_user",
        "password": "test123456",
        "name": "最小用户",
        "user_type": "institutional"
    }
    
    print("\n=== 测试最小数据 ===")
    try:
        response = requests.post(url, json=data1)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"异常: {e}")
    
    # 测试2: 包含email
    data2 = {
        "username": "email_user",
        "password": "test123456",
        "name": "邮箱用户",
        "email": "test@example.com",
        "user_type": "institutional"
    }
    
    print("\n=== 测试包含邮箱 ===")
    try:
        response = requests.post(url, json=data2)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"异常: {e}")

if __name__ == "__main__":
    debug_institutional_register()
    test_different_data()