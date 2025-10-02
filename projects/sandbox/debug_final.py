#!/usr/bin/env python3
import ast
import tempfile
import os

# 模拟constants.ts中的Python脚本生成逻辑
def generate_python_script():
    # 模拟execution_code_parts
    execution_code_parts = [
        "# 设置matplotlib中文字体",
        "try:",
        "    setup_matplotlib_chinese_font()",
        "except:",
        "    pass",
        "",
        "# 变量定义",
        "",  # var_def为空
        "# 用户代码",
        "def main():\n    return \"Hello World\"",
        "",
        "# 执行main函数",
        "if __name__ == '__main__':",
        "    import inspect",
        "    try:",
        "        # 获取main函数签名",
        "        sig = inspect.signature(main)",
        "        params = list(sig.parameters.keys())",
        "        ",
        "        # 调用main函数",
        "        if 'variables' in params:",
        "            result = main(variables)",
        "        elif params:",
        "            # 如果有其他参数，尝试传递",
        "            args = []",
        "            for param_name in params:",
        "                if param_name in locals():",
        "                    args.append(locals()[param_name])",
        "            if args:",
        "                result = main(*args)",
        "            else:",
        "                result = main()",
        "        else:",
        "            result = main()",
        "        ",
        "        # 处理matplotlib图片并转换为base64",
        "        try:",
        "            result = process_matplotlib_images(result)",
        "        except Exception:",
        "            pass",
        "        ",
        "        print(result)",
        "    except Exception as e:",
        "        print({\"error\": \"Error calling main function: \" + str(e)})"
    ]
    
    execution_code = "\\n".join(execution_code_parts)
    return execution_code

# 生成代码
code = generate_python_script()
print("Generated code:")
print(repr(code))
print("\n" + "="*50 + "\n")

# 检查语法
try:
    ast.parse(code)
    print("✓ Syntax check passed!")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
    print(f"Line {e.lineno}: {e.text}")
    print(" " * (e.offset - 1) + "^")

# 写入文件测试
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
    f.write(code)
    temp_file = f.name

print(f"\nCode written to: {temp_file}")

# 尝试执行
import subprocess
try:
    result = subprocess.run(['python3', temp_file], capture_output=True, text=True, timeout=10)
    print(f"Exit code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")
except Exception as e:
    print(f"Execution error: {e}")

# 清理
os.unlink(temp_file)