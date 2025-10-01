#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import subprocess
import json

def test_api():
    """测试API"""
    print("🧪 测试FastGPT沙盒API")
    
    # 测试数据
    test_data = {
        "code": '''
def main():
    import numpy as np
    import json
    
    # 创建示例数据
    data = np.random.randn(100)
    
    return {
        "message": "基础功能测试成功！",
        "data_length": len(data),
        "mean": float(np.mean(data)),
        "std": float(np.std(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data))
    }
''',
        "variables": {}
    }
    
    # 使用curl测试
    curl_cmd = [
        "curl", "-X", "POST", "http://127.0.0.1:3000/sandbox/python",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(test_data)
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print("✅ API调用成功!")
            print(f"响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ API调用失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")

def test_matplotlib():
    """测试matplotlib功能"""
    print("\n🎨 测试Matplotlib功能")
    
    test_data = {
        "code": '''
def main():
    import numpy as np
    
    # 测试基础数学运算
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    return {
        "message": "数学计算测试成功！",
        "function": "sin(x)",
        "x_range": [0, 10],
        "y_min": float(np.min(y)),
        "y_max": float(np.max(y))
    }
''',
        "variables": {}
    }
    
    curl_cmd = [
        "curl", "-X", "POST", "http://127.0.0.1:3000/sandbox/python",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(test_data)
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print("✅ 数学计算测试成功!")
            print(f"响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 测试失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试出错: {str(e)}")

if __name__ == "__main__":
    print("🚀 FastGPT 沙盒API测试")
    print("=" * 50)
    
    test_api()
    test_matplotlib()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")
    print("\n📝 API地址:")
    print("POST http://127.0.0.1:3000/sandbox/python")
    print("\n📖 文档地址:")
    print("GET http://127.0.0.1:3000/api")

