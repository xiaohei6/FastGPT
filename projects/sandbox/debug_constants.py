#!/usr/bin/env python3
import re
import ast
import tempfile
import os

# 读取constants.ts文件
with open('src/sandbox/constants.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取pythonScript的内容
match = re.search(r'export const pythonScript = `\n(.*?)\n`;', content, re.DOTALL)
if match:
    python_script = match.group(1)
    print("Extracted Python script:")
    print("="*50)
    print(python_script[:500] + "..." if len(python_script) > 500 else python_script)
    print("="*50)
    
    # 检查语法
    try:
        ast.parse(python_script)
        print("✓ Python script syntax check passed!")
    except SyntaxError as e:
        print(f"✗ Python script syntax error: {e}")
        print(f"Line {e.lineno}: {e.text}")
        if e.offset:
            print(" " * (e.offset - 1) + "^")
else:
    print("Could not extract Python script from constants.ts")