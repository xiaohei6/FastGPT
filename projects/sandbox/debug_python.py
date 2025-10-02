import os
import subprocess
import json
import ast
import base64
import tempfile
import shutil
import urllib.parse
import sys
import importlib.util

# 全局变量存储已安装的包
_installed_packages = set()

def extract_imports(code):
    """提取代码中所有的导入语句"""
    try:
        tree = ast.parse(code)
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                if module:
                    imports.append(module)
        return list(set(imports))  # 去重
    except Exception as e:
        return []

def run_pythonCode(data):
    if not data or "code" not in data:
        return {"error": "Invalid request format: missing code"}
    
    code = data.get("code")
    if not code or not code.strip():
        return {"error": "Code cannot be empty"}
    
    # 处理变量
    variables = data.get("variables", {})
    if variables is None:
        variables = {}
    
    var_def = ""
    for k, v in variables.items():
        if not isinstance(k, str) or not k.strip():
            return {"error": "Invalid variable name: " + repr(k)}
        
        try:
            one_var = k + " = " + repr(v) + "\n"
            var_def = var_def + one_var
        except Exception as e:
            return {"error": "Error processing variable " + k + ": " + str(e)}
    
    # 创建执行代码
    execution_code = """
# 变量定义
""" + var_def + """

# 用户代码
""" + code + """

# 执行main函数
if __name__ == '__main__':
    import inspect
    try:
        # 获取main函数签名
        sig = inspect.signature(main)
        params = list(sig.parameters.keys())
        
        # 调用main函数
        if 'variables' in params:
            result = main(variables)
        elif params:
            # 如果有其他参数，尝试传递
            args = []
            for param_name in params:
                if param_name in locals():
                    args.append(locals()[param_name])
            if args:
                result = main(*args)
            else:
                result = main()
        else:
            result = main()
        
        print(result)
    except Exception as e:
        print({"error": "Error calling main function: " + str(e)})
"""
    
    # 写入临时文件并执行
    tmp_file = os.path.join(data["tempDir"], "subProcess.py")
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(execution_code)
    
    try:
        result = subprocess.run(["python3", tmp_file], capture_output=True, text=True, timeout=60)
        if result.stderr != "":
            return {"error": result.stderr}

        out = ast.literal_eval(result.stdout.strip())
        return out
    except subprocess.TimeoutExpired:
        return {"error": "Timeout error or blocked by system security policy"}
    except Exception as e:
        return {"error": str(e)}

# 测试代码
if __name__ == "__main__":
    test_data = {
        "code": "def main():\n    return 'Hello World'",
        "variables": {},
        "tempDir": "/tmp"
    }
    
    result = run_pythonCode(test_data)
    print("Test result:", result)