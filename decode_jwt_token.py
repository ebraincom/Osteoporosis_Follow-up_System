import jwt
import json

def decode_jwt_token():
    """解码JWT token查看内容"""
    
    # 从之前的测试中获取的token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJcdTY3NGVcdTRlMDBcdTVmYTEiLCJ1c2VyX3R5cGUiOiJwZXJzb25hbCIsImV4cCI6MTc1ODAwNDU2OX0.VkY5UTCoRl91L1bGNwyrMPANxe4O_WPiRmy"
    
    print("=== 解码JWT Token ===")
    print(f"Token: {token}")
    
    try:
        # 不验证签名，只解码payload
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"解码结果: {json.dumps(decoded, ensure_ascii=False, indent=2)}")
        
        # 检查用户名
        username = decoded.get("sub")
        print(f"用户名: {username}")
        print(f"用户名类型: {type(username)}")
        print(f"用户名长度: {len(username) if username else 0}")
        
        # 检查每个字符
        if username:
            print("用户名字符分析:")
            for i, char in enumerate(username):
                print(f"  位置{i}: '{char}' (Unicode: {ord(char)})")
                
    except Exception as e:
        print(f"解码失败: {e}")

if __name__ == "__main__":
    decode_jwt_token()