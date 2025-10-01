# FastGPT 沙盒增强功能

## 🚀 新增功能概述

本次更新为 FastGPT 沙盒环境增加了以下强大功能：

### 1. 自动安装缺失库 📦
- **功能描述**: 自动检测代码中导入的库，并安装缺失的依赖包
- **支持范围**: 除危险库外的所有合法Python包
- **安装方式**: 使用pip自动安装，无需手动配置

### 2. Matplotlib 图片生成与返回 🎨
- **功能描述**: 自动检测matplotlib生成的图片，转换为base64格式返回
- **返回格式**: `data:image/png;base64,{base64编码}`
- **支持特性**: 多图表、高分辨率、内存优化

### 3. 中文字体支持 🈶
- **功能描述**: 自动配置matplotlib中文字体，支持中文图表显示
- **支持字体**: SimHei, Microsoft YaHei, WenQuanYi Micro Hei等
- **降级策略**: 自动选择可用字体，确保最佳显示效果

## 📋 预安装的常用库

以下库已预安装，无需额外安装：

```python
# 数据处理
numpy, pandas, scipy, scikit-learn

# 可视化
matplotlib, seaborn, plotly

# 图像处理
PIL (pillow), opencv-python

# 网络请求
requests, beautifulsoup4

# 开发工具
jupyter, ipython, tqdm
```

## 🔧 使用示例

### 基础数据可视化示例

```python
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
    
    return {
        "message": "图表生成成功",
        "data_points": len(x),
        "functions": ["sin", "cos"]
    }
```

**返回结果**:
```json
{
  "codeReturn": {
    "message": "图表生成成功",
    "data_points": 100,
    "functions": ["sin", "cos"],
    "matplotlib_images": [
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
    ]
  },
  "log": ""
}
```

### 自动安装库示例

```python
def main(variables):
    # 这些库会自动安装（如果未安装）
    import wordcloud
    import jieba
    import plotly.graph_objects as go
    
    # 创建词云数据
    text = "Python 机器学习 人工智能 数据分析"
    words = jieba.lcut(text)
    
    # 创建Plotly图表
    fig = go.Figure(data=go.Scatter(x=[1,2,3], y=[4,5,6]))
    
    return {
        "message": "自动安装库测试成功",
        "libraries": ["wordcloud", "jieba", "plotly"],
        "words": words
    }
```

## 🛡️ 安全特性

### 1. 危险库检测
以下库被禁止导入：
- `os`, `sys`, `subprocess`, `shutil`
- `socket`, `ctypes`, `multiprocessing`
- `threading`, `pickle`, `tempfile`

### 2. 文件写入限制
- 禁止所有文件写入操作
- 禁止创建目录
- 只允许matplotlib图片生成

### 3. 系统调用限制
- 使用seccomp限制系统调用
- 只允许必要的系统操作
- 防止恶意代码执行

## 🔄 返回数据格式

### 标准返回格式
```json
{
  "codeReturn": {
    // 你的代码返回的数据
    "data": "your data",
    
    // matplotlib图片（如果存在）
    "matplotlib_images": [
      "data:image/png;base64,{base64编码}"
    ]
  },
  "log": "执行日志"
}
```

### 错误返回格式
```json
{
  "error": "错误描述信息"
}
```

## 🚀 部署说明

### Docker 构建
```bash
# 构建新的沙盒镜像
docker build -t fastgpt-sandbox-enhanced .

# 运行沙盒服务
docker run -p 3000:3000 fastgpt-sandbox-enhanced
```

### 环境变量
```bash
# matplotlib配置
export MPLCONFIGDIR=/tmp/matplotlib

# Python路径
export PYTHONPATH=/usr/local/lib/python3.11/site-packages
```

## 🧪 测试

运行测试脚本验证功能：

```bash
# 安装测试依赖
pip install requests

# 运行测试
python test_enhanced_sandbox.py
```

## 📝 注意事项

1. **性能考虑**: 自动安装库会增加首次执行时间
2. **内存管理**: matplotlib图片会自动清理内存
3. **字体支持**: 优先使用系统中文字体，降级到DejaVu Sans
4. **超时设置**: 代码执行超时时间延长至30秒

## 🔮 未来计划

- [ ] 支持更多图表库（bokeh, altair等）
- [ ] 添加图片缓存机制
- [ ] 支持自定义字体上传
- [ ] 增加更多预安装库
- [ ] 优化包安装速度

## 📞 技术支持

如有问题或建议，请提交Issue或联系开发团队。
