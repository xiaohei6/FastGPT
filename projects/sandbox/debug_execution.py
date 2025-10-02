#!/usr/bin/env python3
"""
调试execution_code生成逻辑
"""

def debug_execution_code():
    # 模拟数据
    code = "def main():\n    return 'Hello World'"
    variables = {}
    
    # 处理变量
    var_def = ""
    for k, v in variables.items():
        if not isinstance(k, str) or not k.strip():
            print(f"Invalid variable name: {repr(k)}")
            return
        
        try:
            one_var = k + " = " + repr(v) + "\n"
            var_def = var_def + one_var
        except Exception as e:
            print(f"Error processing variable {k}: {str(e)}")
            return
    
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
    
    print("Generated execution code:")
    print("=" * 50)
    print(execution_code)
    print("=" * 50)
    
    # 写入文件测试
    with open("/tmp/test_execution.py", "w", encoding="utf-8") as f:
        f.write(execution_code)
    
    print("Code written to /tmp/test_execution.py")
    
    # 测试语法
    try:
        import ast
        ast.parse(execution_code)
        print("✅ Syntax check passed!")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        print(f"Line {e.lineno}: {e.text}")
    
    # 执行测试
    import subprocess
    try:
        result = subprocess.run(["python3", "/tmp/test_execution.py"], 
                              capture_output=True, text=True, timeout=10)
        print(f"Exit code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
    except Exception as e:
        print(f"Execution error: {e}")

if __name__ == "__main__":
    debug_execution_code()