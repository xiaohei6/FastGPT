#!/usr/bin/env python3
"""
测试增强的沙盒功能
包括自动安装库、matplotlib图片生成和中文字体支持
"""

import requests
import json

# 测试数据
test_data = {
    "code": '''
def main(variables):
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 创建中文图表
    plt.figure(figsize=(10, 6))
    
    # 生成示例数据
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # 绘制图表
    plt.plot(x, y1, label='正弦函数', linewidth=2)
    plt.plot(x, y2, label='余弦函数', linewidth=2)
    
    # 设置中文标题和标签
    plt.title('三角函数图表', fontsize=16, fontweight='bold')
    plt.xlabel('角度 (弧度)', fontsize=12)
    plt.ylabel('函数值', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # 返回数据
    return {
        "message": "图表生成成功",
        "data_points": len(x),
        "functions": ["sin", "cos"]
    }
''',
    "variables": {
        "test_var": "Hello World"
    }
}

def test_sandbox():
    """测试沙盒功能"""
    try:
        # 发送请求到沙盒服务
        response = requests.post(
            'http://localhost:3000/sandbox/python',
            json=test_data,
            timeout=60  # 增加超时时间以支持库安装
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 沙盒测试成功!")
            print(f"返回结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查是否包含matplotlib图片
            if 'codeReturn' in result and 'matplotlib_images' in result['codeReturn']:
                print(f"✅ 检测到 {len(result['codeReturn']['matplotlib_images'])} 个matplotlib图片")
                print("图片已转换为base64格式，可在前端直接显示")
            else:
                print("ℹ️  未检测到matplotlib图片")
                
        else:
            print(f"❌ 沙盒测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到沙盒服务，请确保服务已启动")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")

def test_auto_install():
    """测试自动安装库功能"""
    test_data_install = {
        "code": '''
def main(variables):
    # 尝试导入一个不常用的库
    import wordcloud
    import jieba
    
    # 创建词云数据
    text = "Python 机器学习 人工智能 数据分析 可视化"
    
    # 分词
    words = jieba.lcut(text)
    word_freq = {}
    for word in words:
        if len(word) > 1:  # 过滤单字符
            word_freq[word] = word_freq.get(word, 0) + 1
    
    return {
        "message": "自动安装库测试成功",
        "imported_libraries": ["wordcloud", "jieba"],
        "word_frequency": word_freq
    }
''',
        "variables": {}
    }
    
    try:
        response = requests.post(
            'http://localhost:3000/sandbox/python',
            json=test_data_install,
            timeout=120  # 更长的超时时间用于安装库
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 自动安装库测试成功!")
            print(f"返回结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 自动安装库测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 自动安装库测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    print("🚀 开始测试增强的沙盒功能...")
    print("=" * 50)
    
    print("\n1. 测试基础沙盒功能...")
    test_sandbox()
    
    print("\n2. 测试自动安装库功能...")
    test_auto_install()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")
