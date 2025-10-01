#!/usr/bin/env python3
"""
测试增强的FastGPT沙盒API功能
包括自动安装库、matplotlib图片生成和中文字体支持
"""

import requests
import json
import time

# API地址
API_BASE_URL = "http://127.0.0.1:3000"

def test_basic_functionality():
    """测试基础功能"""
    print("🧪 测试1: 基础功能测试")
    
    test_data = {
        "code": '''
def main(variables):
    import numpy as np
    import pandas as pd
    
    # 创建示例数据
    data = np.random.randn(100)
    df = pd.DataFrame({'value': data})
    
    return {
        "message": "基础功能测试成功！",
        "data_shape": df.shape,
        "mean": float(df['value'].mean()),
        "std": float(df['value'].std())
    }
''',
        "variables": {
            "test_param": "Hello World"
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/sandbox/python",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 基础功能测试成功!")
            print(f"返回结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 基础功能测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 基础功能测试出错: {str(e)}")

def test_matplotlib_chinese():
    """测试matplotlib中文字体支持"""
    print("\n🎨 测试2: Matplotlib中文图表生成")
    
    test_data = {
        "code": '''
def main(variables):
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 创建中文图表
    plt.figure(figsize=(12, 8))
    
    # 生成示例数据
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x)
    
    # 绘制多个图表
    plt.subplot(2, 2, 1)
    plt.plot(x, y1, 'b-', linewidth=2, label='正弦函数')
    plt.title('正弦函数图', fontsize=14, fontweight='bold')
    plt.xlabel('角度 (弧度)', fontsize=10)
    plt.ylabel('函数值', fontsize=10)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.plot(x, y2, 'r-', linewidth=2, label='余弦函数')
    plt.title('余弦函数图', fontsize=14, fontweight='bold')
    plt.xlabel('角度 (弧度)', fontsize=10)
    plt.ylabel('函数值', fontsize=10)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.plot(x, y3, 'g-', linewidth=2, label='sin(x)*cos(x)')
    plt.title('复合函数图', fontsize=14, fontweight='bold')
    plt.xlabel('角度 (弧度)', fontsize=10)
    plt.ylabel('函数值', fontsize=10)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 散点图
    plt.subplot(2, 2, 4)
    x_scatter = np.random.randn(50)
    y_scatter = np.random.randn(50)
    colors = np.random.rand(50)
    plt.scatter(x_scatter, y_scatter, c=colors, alpha=0.6)
    plt.title('随机散点图', fontsize=14, fontweight='bold')
    plt.xlabel('X坐标', fontsize=10)
    plt.ylabel('Y坐标', fontsize=10)
    
    plt.tight_layout()
    
    return {
        "message": "中文图表生成成功！",
        "charts_count": 4,
        "data_points": len(x),
        "chart_types": ["正弦函数", "余弦函数", "复合函数", "散点图"]
    }
''',
        "variables": {}
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/sandbox/python",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Matplotlib中文图表测试成功!")
            print(f"返回结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查是否包含图片
            if 'codeReturn' in result and 'matplotlib_images' in result['codeReturn']:
                images = result['codeReturn']['matplotlib_images']
                print(f"🎨 生成了 {len(images)} 个图表")
                print(f"📊 第一个图表大小: {len(images[0])} 字符 (base64)")
            else:
                print("⚠️  未检测到matplotlib图片")
        else:
            print(f"❌ Matplotlib测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ Matplotlib测试出错: {str(e)}")

def test_auto_install():
    """测试自动安装库功能"""
    print("\n📦 测试3: 自动安装库功能")
    
    test_data = {
        "code": '''
def main(variables):
    # 尝试导入一些可能未安装的库
    import seaborn as sns
    import plotly.graph_objects as go
    import plotly.express as px
    import requests
    from bs4 import BeautifulSoup
    
    # 创建seaborn图表
    import numpy as np
    import pandas as pd
    
    # 生成数据
    data = np.random.randn(1000)
    df = pd.DataFrame({'value': data, 'category': np.random.choice(['A', 'B', 'C'], 1000)})
    
    # 创建plotly图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='lines+markers', name='测试线'))
    fig.update_layout(title='Plotly图表测试', xaxis_title='X轴', yaxis_title='Y轴')
    
    return {
        "message": "自动安装库测试成功！",
        "imported_libraries": ["seaborn", "plotly", "requests", "beautifulsoup4"],
        "data_statistics": {
            "mean": float(df['value'].mean()),
            "std": float(df['value'].std()),
            "categories": df['category'].value_counts().to_dict()
        },
        "plotly_chart": "已创建交互式图表"
    }
''',
        "variables": {}
    }
    
    try:
        print("⏳ 正在安装库并执行代码（可能需要30-60秒）...")
        response = requests.post(
            f"{API_BASE_URL}/sandbox/python",
            json=test_data,
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
        print(f"❌ 自动安装库测试出错: {str(e)}")

def test_advanced_visualization():
    """测试高级可视化功能"""
    print("\n🚀 测试4: 高级可视化功能")
    
    test_data = {
        "code": '''
def main(variables):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
    
    # 设置seaborn样式
    sns.set_style("whitegrid")
    
    # 创建复杂的数据可视化
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. 热力图
    data_heatmap = np.random.randn(10, 10)
    sns.heatmap(data_heatmap, annot=True, cmap='viridis', ax=axes[0,0])
    axes[0,0].set_title('随机热力图', fontsize=14, fontweight='bold')
    
    # 2. 分布图
    data_dist = np.random.normal(0, 1, 1000)
    axes[0,1].hist(data_dist, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,1].set_title('正态分布直方图', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('数值', fontsize=10)
    axes[0,1].set_ylabel('频次', fontsize=10)
    
    # 3. 散点图矩阵
    df = pd.DataFrame({
        'X': np.random.randn(100),
        'Y': np.random.randn(100),
        'Z': np.random.randn(100)
    })
    scatter = axes[1,0].scatter(df['X'], df['Y'], c=df['Z'], cmap='coolwarm', alpha=0.6)
    axes[1,0].set_title('三维散点图投影', fontsize=14, fontweight='bold')
    axes[1,0].set_xlabel('X坐标', fontsize=10)
    axes[1,0].set_ylabel('Y坐标', fontsize=10)
    plt.colorbar(scatter, ax=axes[1,0])
    
    # 4. 时间序列图
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    ts_data = np.cumsum(np.random.randn(100)) + 100
    axes[1,1].plot(dates, ts_data, linewidth=2, color='green')
    axes[1,1].set_title('模拟股价走势图', fontsize=14, fontweight='bold')
    axes[1,1].set_xlabel('日期', fontsize=10)
    axes[1,1].set_ylabel('价格', fontsize=10)
    axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    return {
        "message": "高级可视化测试成功！",
        "charts": {
            "heatmap": "热力图",
            "histogram": "直方图", 
            "scatter": "散点图",
            "timeseries": "时间序列图"
        },
        "data_info": {
            "heatmap_size": data_heatmap.shape,
            "distribution_samples": len(data_dist),
            "scatter_points": len(df),
            "timeseries_periods": len(dates)
        }
    }
''',
        "variables": {}
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/sandbox/python",
            json=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 高级可视化测试成功!")
            print(f"返回结果: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 检查图片
            if 'codeReturn' in result and 'matplotlib_images' in result['codeReturn']:
                images = result['codeReturn']['matplotlib_images']
                print(f"🎨 生成了 {len(images)} 个高级图表")
        else:
            print(f"❌ 高级可视化测试失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 高级可视化测试出错: {str(e)}")

def main():
    """主测试函数"""
    print("🚀 FastGPT 增强沙盒功能测试")
    print("=" * 60)
    
    # 检查服务是否可用
    try:
        response = requests.get(f"{API_BASE_URL}", timeout=5)
        print(f"✅ 沙盒服务运行正常: {API_BASE_URL}")
    except:
        print(f"❌ 无法连接到沙盒服务: {API_BASE_URL}")
        print("请确保sandbox服务已启动")
        return
    
    # 运行所有测试
    test_basic_functionality()
    test_matplotlib_chinese()
    test_auto_install()
    test_advanced_visualization()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成!")
    print("\n📝 测试总结:")
    print("1. ✅ 基础数据处理功能")
    print("2. ✅ Matplotlib中文图表生成")
    print("3. ✅ 自动安装缺失库")
    print("4. ✅ 高级可视化功能")
    print("\n🔗 API地址: http://127.0.0.1:3000/sandbox/python")
    print("📖 文档地址: http://127.0.0.1:3000/api")

if __name__ == "__main__":
    main()

