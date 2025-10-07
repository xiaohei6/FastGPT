# FastGPT Python沙盒增强版功能说明

## 🎯 增强功能概览

本次增强主要解决了Python沙盒的以下问题并添加了新功能：

### ✅ 已修复的问题
1. **API响应格式错误** - 修复了返回数据格式不正确的问题
2. **中文字体支持** - 解决了matplotlib中文字符显示问题
3. **图片生成优化** - 改进了matplotlib图片生成和base64转换

### 🚀 新增功能
1. **增强的包管理** - 自动安装缺失的Python包
2. **安全机制强化** - 更严格的代码执行安全控制
3. **图片生成支持** - 完整的matplotlib图片生成和base64返回
4. **复杂函数支持** - 支持嵌套函数和复杂的数据处理

## 📋 功能详情

### 1. 基本代码执行
```json
{
  "code": "def main(data1, data2):\n    return {\n        \"result\": data1,\n        \"data2\": data2\n    }",
  "variables": {"data1": 1, "data2": 2}
}
```

**预期返回:**
```json
{
  "success": true,
  "data": {
    "codeReturn": {
      "result": 1,
      "data2": 2
    },
    "log": ""
  }
}
```

### 2. Matplotlib图片生成
```json
{
  "code": "import matplotlib.pyplot as plt\n\n# 示例数据\nx = [1, 2, 3, 4, 5]\ny = [10, 12, 15, 14, 16]\n\n# 绘制折线图\nplt.plot(x, y)\n\n# 添加标题和标签\nplt.title('折线图示例')\nplt.xlabel('X轴标签')\nplt.ylabel('Y轴标签')\n\n# 显示图形\nplt.show()",
  "variables": {}
}
```

**预期返回:**
```json
{
  "success": true,
  "data": {
    "codeReturn": {
      "matplotlib_images": [
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
      ]
    },
    "log": ""
  }
}
```

### 3. 复杂数据处理
```json
{
  "code": "import pandas as pd\nimport numpy as np\n\ndef main(data):\n    df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})\n    return {\n        'mean_x': float(df['x'].mean()),\n        'correlation': float(df['x'].corr(df['y'])),\n        'shape': list(df.shape)\n    }",
  "variables": {"data": "test"}
}
```

## 🔒 安全机制

### 1. 危险模块检测
以下模块被禁止导入：
- `os`, `subprocess`, `shutil`, `socket`
- `ctypes`, `multiprocessing`, `threading`
- `pickle`, `tempfile`, `pathlib`
- `fileinput`, `glob`, `fnmatch`
- `zipfile`, `tarfile`, `gzip`, `bz2`, `lzma`
- `mmap`, `signal`, `resource`, `pwd`, `grp`

### 2. 文件操作限制
禁止的文件操作：
- `open()`, `file()`, `write()`, `writelines()`
- `mkdir`, `makedirs`, `rmdir`, `removedirs`
- `unlink`, `remove`, `rename`, `replace`

### 3. 系统调用限制
使用seccomp限制系统调用，只允许必要的系统调用。

## 🎨 中文字体支持

### 字体优先级
1. Noto Sans CJK SC (简体中文)
2. Noto Sans CJK TC (繁体中文)
3. SimHei, Microsoft YaHei
4. DejaVu Sans (备用)

### 字体配置
- 自动检测可用字体
- 设置unicode负号显示
- 优化字体大小和DPI设置

## 📦 支持的包

### 预装包
- `numpy`, `pandas`, `matplotlib`, `seaborn`
- `plotly`, `requests`, `beautifulsoup4`
- `scipy`, `scikit-learn`, `pillow`
- `opencv-python`, `jupyter`, `ipython`
- `tqdm`, `sympy`, `openpyxl`, `bokeh`

### 自动安装
- 智能包名映射
- 依赖关系处理
- 多种安装方式尝试

## 🚀 使用方法

### 1. 构建镜像
```bash
./build_and_test.sh
```

### 2. 启动服务
```bash
docker run -d -p 3005:3005 fastgpt-sandbox-enhanced
```

### 3. 测试API
```bash
python3 test_complete_api.py
```

### 4. 健康检查
```bash
curl http://localhost:3005/sandbox
```

## 🔧 技术细节

### 1. 代码执行流程
1. 接收前端请求 (`code` + `variables`)
2. 创建临时目录和文件
3. 自动安装缺失的包
4. 安全检查（危险模块、文件操作）
5. 执行Python代码
6. 处理matplotlib图片
7. 返回JSON格式结果

### 2. 图片处理
- 自动检测matplotlib图形
- 转换为base64格式
- 支持多个图形
- 内存优化和清理

### 3. 错误处理
- 超时控制（60秒）
- 异常捕获和报告
- 资源清理
- 安全错误提示

## 📊 性能优化

1. **包缓存** - 避免重复安装已存在的包
2. **内存管理** - 及时清理matplotlib图形
3. **并发控制** - 限制同时执行的代码数量
4. **资源清理** - 自动清理临时文件

## 🐛 故障排除

### 常见问题

1. **中文字体显示问题**
   - 检查Docker镜像是否包含Noto字体
   - 验证字体缓存是否正确

2. **包安装失败**
   - 检查网络连接
   - 验证包名是否正确

3. **图片生成失败**
   - 检查matplotlib是否正确安装
   - 验证代码语法是否正确

4. **安全限制触发**
   - 检查代码是否包含危险操作
   - 验证导入的模块是否被允许

## 📝 更新日志

### v1.0.0 (当前版本)
- ✅ 修复API响应格式问题
- ✅ 添加中文字体支持
- ✅ 增强matplotlib图片生成
- ✅ 强化安全机制
- ✅ 优化包管理
- ✅ 添加完整测试套件

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 运行测试
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。