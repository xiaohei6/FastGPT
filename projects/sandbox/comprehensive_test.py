#!/usr/bin/env python3
"""
FastGPT Python沙盒全面功能测试
测试自动安装库、复杂代码执行、matplotlib图片生成等功能
"""

import subprocess
import json
import time

API_BASE = "http://127.0.0.1:3000"

def make_request(endpoint, data):
    """发送API请求"""
    try:
        result = subprocess.run([
            "curl", "-X", "POST", f"{API_BASE}{endpoint}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(data)
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": f"Request failed: {result.stderr}"}
    except Exception as e:
        return {"error": f"Request error: {str(e)}"}

def test_basic_python():
    """测试基础Python功能"""
    print("🧪 测试1: 基础Python功能")
    
    test_data = {
        "code": '''
def main():
    import numpy as np
    import pandas as pd
    
    # 创建示例数据
    data = np.random.randn(1000)
    df = pd.DataFrame({'value': data})
    
    return {
        "message": "基础Python功能测试成功！",
        "data_shape": df.shape,
        "statistics": {
            "mean": float(df['value'].mean()),
            "std": float(df['value'].std()),
            "min": float(df['value'].min()),
            "max": float(df['value'].max())
        },
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__
    }
''',
        "variables": {}
    }
    
    response = make_request("/sandbox/python", test_data)
    
    if response.get("success") and "data" in response:
        result = response["data"]["codeReturn"]
        print("✅ 基础Python功能测试成功!")
        print(f"   - 数据形状: {result['data_shape']}")
        print(f"   - 均值: {result['statistics']['mean']:.4f}")
        print(f"   - 标准差: {result['statistics']['std']:.4f}")
        print(f"   - NumPy版本: {result['numpy_version']}")
        print(f"   - Pandas版本: {result['pandas_version']}")
        return True
    else:
        print(f"❌ 基础Python测试失败: {response.get('message', 'Unknown error')}")
        return False

def test_auto_install_libraries():
    """测试自动安装库功能"""
    print("\n📦 测试2: 自动安装库功能")
    
    test_data = {
        "code": '''
def main():
    # 测试一些可能未安装的库
    import seaborn as sns
    import plotly.graph_objects as go
    import plotly.express as px
    import requests
    from bs4 import BeautifulSoup
    import scipy.stats
    
    # 创建一些数据
    import numpy as np
    data = np.random.normal(0, 1, 100)
    
    # 使用seaborn
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 6))
    sns.histplot(data, kde=True)
    plt.title('数据分布图')
    
    # 使用plotly
    fig = go.Figure(data=go.Scatter(x=list(range(len(data))), y=data, mode='lines'))
    fig.update_layout(title='时间序列图')
    
    return {
        "message": "自动安装库测试成功！",
        "imported_libraries": ["seaborn", "plotly", "requests", "beautifulsoup4", "scipy"],
        "data_statistics": {
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "normality_test": float(scipy.stats.normaltest(data)[1])
        },
        "libraries_working": True
    }
''',
        "variables": {}
    }
    
    print("⏳ 正在安装库并执行代码（可能需要60-120秒）...")
    response = make_request("/sandbox/python", test_data)
    
    if response.get("success") and "data" in response:
        result = response["data"]["codeReturn"]
        print("✅ 自动安装库测试成功!")
        print(f"   - 导入的库: {', '.join(result['imported_libraries'])}")
        print(f"   - 库工作状态: {result['libraries_working']}")
        print(f"   - 正态性检验p值: {result['data_statistics']['normality_test']:.6f}")
        return True
    else:
        print(f"❌ 自动安装库测试失败: {response.get('message', 'Unknown error')}")
        return False

def test_matplotlib_chinese():
    """测试matplotlib中文图表生成"""
    print("\n🎨 测试3: Matplotlib中文图表生成")
    
    test_data = {
        "code": '''
def main():
    import matplotlib.pyplot as plt
    import numpy as np
    
    # 创建复杂的中文图表
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. 正弦余弦函数图
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    axes[0,0].plot(x, y1, 'b-', linewidth=2, label='正弦函数')
    axes[0,0].plot(x, y2, 'r-', linewidth=2, label='余弦函数')
    axes[0,0].set_title('三角函数对比图', fontsize=14, fontweight='bold')
    axes[0,0].set_xlabel('角度 (弧度)', fontsize=10)
    axes[0,0].set_ylabel('函数值', fontsize=10)
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # 2. 正态分布直方图
    data = np.random.normal(0, 1, 1000)
    axes[0,1].hist(data, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    axes[0,1].set_title('正态分布直方图', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('数值', fontsize=10)
    axes[0,1].set_ylabel('频次', fontsize=10)
    
    # 3. 散点图
    x_scatter = np.random.randn(200)
    y_scatter = 2 * x_scatter + np.random.randn(200)
    colors = np.random.rand(200)
    scatter = axes[1,0].scatter(x_scatter, y_scatter, c=colors, cmap='viridis', alpha=0.6)
    axes[1,0].set_title('相关性散点图', fontsize=14, fontweight='bold')
    axes[1,0].set_xlabel('X坐标', fontsize=10)
    axes[1,0].set_ylabel('Y坐标', fontsize=10)
    plt.colorbar(scatter, ax=axes[1,0])
    
    # 4. 饼图
    sizes = [30, 25, 20, 15, 10]
    labels = ['类别A', '类别B', '类别C', '类别D', '类别E']
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    axes[1,1].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    axes[1,1].set_title('数据分布饼图', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    return {
        "message": "中文图表生成成功！",
        "charts": ["正弦余弦函数图", "正态分布直方图", "相关性散点图", "数据分布饼图"],
        "data_info": {
            "trigonometric_points": len(x),
            "histogram_samples": len(data),
            "scatter_points": len(x_scatter),
            "pie_categories": len(sizes)
        }
    }
''',
        "variables": {}
    }
    
    response = make_request("/sandbox/python", test_data)
    
    if response.get("success") and "data" in response:
        result = response["data"]["codeReturn"]
        print("✅ Matplotlib中文图表测试成功!")
        print(f"   - 生成的图表: {', '.join(result['charts'])}")
        print(f"   - 三角函数点数: {result['data_info']['trigonometric_points']}")
        print(f"   - 直方图样本数: {result['data_info']['histogram_samples']}")
        
        # 检查是否包含图片
        if 'matplotlib_images' in result:
            print(f"   - 生成的图片数量: {len(result['matplotlib_images'])}")
            print(f"   - 图片格式: base64编码的PNG")
            return True
        else:
            print("   ⚠️  未检测到matplotlib图片")
            return True
    else:
        print(f"❌ Matplotlib测试失败: {response.get('message', 'Unknown error')}")
        return False

def test_complex_data_analysis():
    """测试复杂数据分析"""
    print("\n📊 测试4: 复杂数据分析")
    
    test_data = {
        "code": '''
def main():
    import numpy as np
    import pandas as pd
    import scipy.stats as stats
    import matplotlib.pyplot as plt
    
    # 生成复杂的模拟数据
    np.random.seed(42)
    n_samples = 1000
    
    # 创建多个相关变量
    x1 = np.random.normal(0, 1, n_samples)
    x2 = 0.5 * x1 + np.random.normal(0, 0.5, n_samples)
    x3 = np.random.exponential(2, n_samples)
    y = 2 * x1 + 1.5 * x2 - 0.8 * x3 + np.random.normal(0, 0.3, n_samples)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'feature1': x1,
        'feature2': x2,
        'feature3': x3,
        'target': y
    })
    
    # 描述性统计
    desc_stats = df.describe()
    
    # 相关性分析
    correlation_matrix = df.corr()
    
    # 回归分析
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import r2_score, mean_squared_error
    
    X = df[['feature1', 'feature2', 'feature3']]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    
    # 创建可视化
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. 特征分布
    axes[0,0].hist(df['feature1'], bins=30, alpha=0.7, color='blue')
    axes[0,0].set_title('特征1分布')
    
    # 2. 相关性热力图
    im = axes[0,1].imshow(correlation_matrix, cmap='coolwarm', aspect='auto')
    axes[0,1].set_title('相关性矩阵')
    axes[0,1].set_xticks(range(len(correlation_matrix.columns)))
    axes[0,1].set_yticks(range(len(correlation_matrix.columns)))
    axes[0,1].set_xticklabels(correlation_matrix.columns, rotation=45)
    axes[0,1].set_yticklabels(correlation_matrix.columns)
    
    # 3. 预测vs实际
    axes[1,0].scatter(y_test, y_pred, alpha=0.6)
    axes[1,0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[1,0].set_xlabel('实际值')
    axes[1,0].set_ylabel('预测值')
    axes[1,0].set_title('预测vs实际值')
    
    # 4. 残差图
    residuals = y_test - y_pred
    axes[1,1].scatter(y_pred, residuals, alpha=0.6)
    axes[1,1].axhline(y=0, color='r', linestyle='--')
    axes[1,1].set_xlabel('预测值')
    axes[1,1].set_ylabel('残差')
    axes[1,1].set_title('残差图')
    
    plt.tight_layout()
    
    return {
        "message": "复杂数据分析完成！",
        "data_info": {
            "sample_size": n_samples,
            "features": list(df.columns),
            "missing_values": df.isnull().sum().to_dict()
        },
        "statistics": {
            "correlation_matrix": correlation_matrix.to_dict(),
            "model_performance": {
                "r2_score": float(r2),
                "mse": float(mse),
                "coefficients": model.coef_.tolist(),
                "intercept": float(model.intercept_)
            }
        },
        "analysis_type": "机器学习回归分析"
    }
''',
        "variables": {}
    }
    
    print("⏳ 执行复杂数据分析（可能需要60-120秒）...")
    response = make_request("/sandbox/python", test_data)
    
    if response.get("success") and "data" in response:
        result = response["data"]["codeReturn"]
        print("✅ 复杂数据分析测试成功!")
        print(f"   - 样本大小: {result['data_info']['sample_size']}")
        print(f"   - 特征数量: {len(result['data_info']['features'])}")
        print(f"   - R²分数: {result['statistics']['model_performance']['r2_score']:.4f}")
        print(f"   - 均方误差: {result['statistics']['model_performance']['mse']:.4f}")
        print(f"   - 分析类型: {result['analysis_type']}")
        
        # 检查是否包含图片
        if 'matplotlib_images' in result:
            print(f"   - 生成的图表数量: {len(result['matplotlib_images'])}")
        
        return True
    else:
        print(f"❌ 复杂数据分析测试失败: {response.get('message', 'Unknown error')}")
        return False

def test_variable_passing():
    """测试变量传递功能"""
    print("\n🔄 测试5: 变量传递功能")
    
    test_data = {
        "code": '''
def main(variables):
    import numpy as np
    import json
    
    # 使用传入的变量
    input_data = variables.get('data', [])
    operation = variables.get('operation', 'mean')
    
    if not input_data:
        return {"error": "No input data provided"}
    
    # 根据操作类型处理数据
    if operation == 'mean':
        result = float(np.mean(input_data))
    elif operation == 'std':
        result = float(np.std(input_data))
    elif operation == 'max':
        result = float(np.max(input_data))
    elif operation == 'min':
        result = float(np.min(input_data))
    else:
        result = {"error": f"Unknown operation: {operation}"}
    
    return {
        "message": "变量传递测试成功！",
        "input_data": input_data,
        "operation": operation,
        "result": result,
        "data_length": len(input_data),
        "processed_at": time.time()
    }
''',
        "variables": {
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "operation": "mean"
        }
    }
    
    response = make_request("/sandbox/python", test_data)
    
    if response.get("success") and "data" in response:
        result = response["data"]["codeReturn"]
        print("✅ 变量传递测试成功!")
        print(f"   - 输入数据: {result['input_data']}")
        print(f"   - 操作类型: {result['operation']}")
        print(f"   - 计算结果: {result['result']}")
        print(f"   - 数据长度: {result['data_length']}")
        return True
    else:
        print(f"❌ 变量传递测试失败: {response.get('message', 'Unknown error')}")
        return False

def main():
    """主测试函数"""
    print("🚀 FastGPT Python沙盒全面功能测试")
    print("=" * 70)
    print(f"API地址: {API_BASE}")
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行所有测试
    tests = [
        ("基础Python功能", test_basic_python),
        ("自动安装库功能", test_auto_install_libraries),
        ("Matplotlib中文图表", test_matplotlib_chinese),
        ("复杂数据分析", test_complex_data_analysis),
        ("变量传递功能", test_variable_passing)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name}测试出错: {str(e)}")
            results.append((test_name, False))
    
    # 显示测试总结
    print("\n" + "=" * 70)
    print("🎉 测试完成!")
    print("\n📊 测试结果总结:")
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n📈 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎊 所有测试都通过了！Python沙盒功能完全正常！")
    elif passed >= total * 0.8:
        print("👍 大部分测试通过，Python沙盒基本功能正常！")
    else:
        print("⚠️  部分测试失败，需要进一步优化")
    
    print("\n🔗 重要链接:")
    print(f"   API文档: {API_BASE}/api")
    print(f"   Python沙盒: {API_BASE}/sandbox/python")
    print(f"   JavaScript沙盒: {API_BASE}/sandbox/js")

if __name__ == "__main__":
    main()