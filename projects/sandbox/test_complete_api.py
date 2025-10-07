#!/usr/bin/env python3
import requests
import json
import time

# API端点
API_BASE = "http://localhost:3005/sandbox"

def test_basic_function():
    """测试基本函数调用"""
    print("🧪 测试基本函数调用...")
    
    data = {
        "code": """def main(data1, data2):
    return {
        "result": data1,
        "data2": data2
    }""",
        "variables": {"data1": 1, "data2": 2}
    }
    
    response = requests.post(f"{API_BASE}/python", json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 基本函数调用成功")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # 检查返回格式
        if 'codeReturn' in result and 'result' in result['codeReturn'] and 'data2' in result['codeReturn']:
            print("✅ 返回格式正确")
            return True
        else:
            print("❌ 返回格式不正确")
            return False
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return False

def test_matplotlib_chinese():
    """测试matplotlib中文字体"""
    print("\n🧪 测试matplotlib中文字体...")
    
    data = {
        "code": """import matplotlib.pyplot as plt
import numpy as np

# 示例数据
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

# 绘制图形
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='正弦波')
plt.title('中文字体测试 - 正弦波函数')
plt.xlabel('X轴 (弧度)')
plt.ylabel('Y轴 (振幅)')
plt.legend()
plt.grid(True, alpha=0.3)

# 显示图形
plt.show()""",
        "variables": {}
    }
    
    response = requests.post(f"{API_BASE}/python", json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ matplotlib测试成功")
        
        if 'codeReturn' in result and 'matplotlib_images' in result['codeReturn']:
            images = result['codeReturn']['matplotlib_images']
            if images and len(images) > 0:
                print(f"✅ 成功生成图片，数量: {len(images)}")
                print(f"图片数据长度: {len(images[0])}")
                return True
            else:
                print("❌ 未生成图片")
                return False
        else:
            print("❌ 响应中未包含图片数据")
            return False
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return False

def test_complex_calculation():
    """测试复杂计算"""
    print("\n🧪 测试复杂计算...")
    
    data = {
        "code": """import numpy as np
import pandas as pd

def main(data1, data2):
    # 创建数据
    df = pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100)
    })
    
    # 计算统计信息
    stats = {
        'mean_x': float(df['x'].mean()),
        'std_x': float(df['x'].std()),
        'correlation': float(df['x'].corr(df['y']))
    }
    
    # 返回结果
    return {
        'result': data1 + data2,
        'statistics': stats,
        'data_shape': list(df.shape)
    }""",
        "variables": {"data1": 10, "data2": 20}
    }
    
    response = requests.post(f"{API_BASE}/python", json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 复杂计算成功")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return True
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return False

def test_security():
    """测试安全性"""
    print("\n🧪 测试安全性...")
    
    # 测试危险导入
    dangerous_code = """import os
def main():
    return {"result": "dangerous import test"}"""
    
    data = {"code": dangerous_code, "variables": {}}
    response = requests.post(f"{API_BASE}/python", json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if 'error' in result.get('codeReturn', {}):
            print("✅ 危险导入被正确阻止")
            return True
        else:
            print("❌ 危险导入未被阻止")
            return False
    else:
        print(f"❌ 请求失败: {response.status_code}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始测试增强版Python沙盒...")
    print("=" * 60)
    
    tests = [
        test_basic_function,
        test_matplotlib_chinese,
        test_complex_calculation,
        test_security
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
        
        time.sleep(1)  # 避免请求过快
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！Python沙盒增强完成！")
    else:
        print("⚠️ 部分测试失败，需要进一步调试")

if __name__ == "__main__":
    main()
