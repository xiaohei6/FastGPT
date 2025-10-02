#!/usr/bin/env python3
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

def setup_matplotlib_chinese_font():
    """配置matplotlib中文字体支持"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        
        # 尝试设置中文字体
        chinese_fonts = [
            'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 
            'DejaVu Sans', 'Arial Unicode MS', 'Noto Sans CJK SC'
        ]
        
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        selected_font = None
        
        for font in chinese_fonts:
            if font in available_fonts:
                selected_font = font
                break
        
        if selected_font:
            plt.rcParams['font.sans-serif'] = [selected_font]
            plt.rcParams['axes.unicode_minus'] = False
        else:
            # 如果没有找到中文字体，使用默认字体但配置unicode支持
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        
        return selected_font
    except Exception as e:
        return "Font setup error: " + str(e)

def process_matplotlib_images(result):
    """处理matplotlib图片并转换为base64格式"""
    try:
        import matplotlib.pyplot as plt
        import io
        import base64
        
        # 检查是否有matplotlib图形需要保存
        if hasattr(plt, 'get_fignums') and plt.get_fignums():
            figures_data = []
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                buffer = io.BytesIO()
                fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                figures_data.append("data:image/png;base64," + image_base64)
                buffer.close()  # 关闭buffer释放内存
                plt.close(fig)
            
            # 如果有图片，添加到结果中
            if figures_data:
                if isinstance(result, dict):
                    result['matplotlib_images'] = figures_data
                else:
                    result = {
                        'data': result,
                        'matplotlib_images': figures_data
                    }
        
        # 清理所有图形
        plt.close('all')
        return result
        
    except ImportError:
        # matplotlib未安装，跳过图片处理
        return result
    except Exception as e:
        # 图片处理失败，继续返回原结果
        return result

# 设置matplotlib中文字体
try:
    setup_matplotlib_chinese_font()
except:
    pass

# 变量定义

# 用户代码
def main():
    return "Hello World"

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
        
        # 处理matplotlib图片并转换为base64
        try:
            result = process_matplotlib_images(result)
        except Exception:
            pass
        
        print(result)
    except Exception as e:
        print({'error': 'Error calling main function: ' + str(e)})