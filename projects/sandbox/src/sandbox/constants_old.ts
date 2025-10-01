export const pythonScript = `
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

def get_package_mapping():
    """获取包名映射"""
    return {
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
        'bs4': 'beautifulsoup4',
        'plotly.graph_objects': 'plotly',
        'plotly.express': 'plotly',
        'matplotlib.pyplot': 'matplotlib',
        'seaborn': 'seaborn',
        'requests': 'requests',
        'beautifulsoup4': 'beautifulsoup4',
        'scipy': 'scipy',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'tqdm': 'tqdm',
        'jupyter': 'jupyter',
        'IPython': 'ipython'
    }

def is_package_installed(package_name):
    """检查包是否已安装"""
    try:
        # 处理子模块导入
        if '.' in package_name:
            main_module = package_name.split('.')[0]
            importlib.import_module(main_module)
        else:
            importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package_safely(package_name, timeout=60):
    """安全安装包，支持依赖关系"""
    try:
        # 检查是否已经安装
        if package_name in _installed_packages:
            return True
            
        # 检查是否已安装
        if is_package_installed(package_name):
            _installed_packages.add(package_name)
            return True
        
        print(f"Installing package: {package_name}", file=sys.stderr)
        
        # 安装包
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', package_name,
            '--quiet', '--disable-pip-version-check', '--no-warn-script-location'
        ], capture_output=True, text=True, timeout=timeout)
        
        if result.returncode == 0:
            _installed_packages.add(package_name)
            return True
        else:
            print(f"Failed to install {package_name}: {result.stderr}", file=sys.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"Timeout installing {package_name}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error installing {package_name}: {str(e)}", file=sys.stderr)
        return False

def install_missing_packages(imports):
    """智能安装缺失的包，支持依赖关系"""
    package_mapping = get_package_mapping()
    
    # 预安装的包，不需要安装
    preinstalled = {
        'os', 'sys', 'json', 'ast', 'base64', 'tempfile', 'shutil', 'urllib',
        'datetime', 'math', 'random', 'collections', 'itertools', 'functools',
        'operator', 're', 'string', 'time', 'calendar', 'hashlib', 'uuid',
        'importlib', 'subprocess', 'platform', 'errno', 'inspect'
    }
    
    packages_to_install = []
    
    for imp in imports:
        if imp in preinstalled:
            continue
            
        # 获取实际包名
        package_name = package_mapping.get(imp, imp)
        
        # 检查是否需要安装
        if not is_package_installed(imp):
            if package_name not in packages_to_install:
                packages_to_install.append(package_name)
    
    # 安装包
    failed_packages = []
    for package in packages_to_install:
        if not install_package_safely(package):
            failed_packages.append(package)
    
    if failed_packages:
        return f"Failed to install packages: {', '.join(failed_packages)}"
    
    return None

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
        return f"Font setup error: {str(e)}"

def process_matplotlib_images(result):
    """处理matplotlib图片"""
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
                figures_data.append(f"data:image/png;base64,{image_base64}")
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
        
    except ImportError:
        # matplotlib未安装，跳过图片处理
        pass
    except Exception as e:
        # 图片处理失败，继续返回原结果
        pass

def run_pythonCode(data:dict):
    if not data or "code" not in data:
        return {"error": "Invalid request format: missing code"}
    
    code = data.get("code")
    if not code or not code.strip():
        return {"error": "Code cannot be empty"}
    
    # 提取导入的包
    imports = extract_imports(code)
    
    # 自动安装缺失的包
    install_error = install_missing_packages(imports)
    if install_error:
        return {"error": install_error}
    
    # 移除print语句
    code = remove_print_statements(code)
    
    # 检查危险导入
    dangerous_import = detect_dangerous_imports(code)
    if dangerous_import:
        return {"error": f"Importing {dangerous_import} is not allowed."}
    
    # 检查文件写入操作
    write_operation = detect_file_write_operations(code)
    if write_operation:
        return {"error": f"File write operations are not allowed: {write_operation}"}
    
    # 处理变量
    variables = data.get("variables", {})
    if variables is None:
        variables = {}
    
    var_def = ""
    for k, v in variables.items():
        if not isinstance(k, str) or not k.strip():
            return {"error": f"Invalid variable name: {repr(k)}"}
        
        try:
            one_var = f"{k} = {repr(v)}\\n"
            var_def = var_def + one_var
        except Exception as e:
            return {"error": f"Error processing variable {k}: {str(e)}"}
    
    # 创建执行代码
    execution_code = f'''
# 设置matplotlib中文字体
try:
    setup_matplotlib_chinese_font()
except:
    pass

# 变量定义
{var_def}

# 用户代码
{code}

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
        
        # 处理matplotlib图片
        process_matplotlib_images(result)
        
        print(result)
    except Exception as e:
        print({{"error": f"Error calling main function: {{str(e)}}"}})
'''
    
    # 写入临时文件并执行
    tmp_file = os.path.join(data["tempDir"], "subProcess.py")
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(seccomp_prefix + "\\n" + execution_code)
    
    try:
        result = subprocess.run(["python3", tmp_file], capture_output=True, text=True, timeout=60)
        if result.returncode == -31:
            return {"error": "Dangerous behavior detected (likely file write attempt)."}
        if result.stderr != "":
            return {"error": result.stderr}

        out = ast.literal_eval(result.stdout.strip())
        return out
    except subprocess.TimeoutExpired:
        return {"error": "Timeout error or blocked by system security policy"}
    except Exception as e:
        return {"error": str(e)}

seccomp_prefix = """
import platform
import sys

# Skip seccomp on macOS since it's Linux-specific
if platform.system() == 'Linux':
    try:
        from seccomp import *
        import errno
        allowed_syscalls = [
            # File operations - READ ONLY (removed SYS_WRITE)
            "syscall.SYS_READ",
            # Removed "syscall.SYS_WRITE" - no general write access
            "syscall.SYS_OPEN",      # Still needed for reading files
            "syscall.SYS_OPENAT",   # Still needed for reading files
            "syscall.SYS_CLOSE",
            "syscall.SYS_FSTAT",
            "syscall.SYS_LSTAT",
            "syscall.SYS_STAT",
            "syscall.SYS_NEWFSTATAT",
            "syscall.SYS_LSEEK",
            "syscall.SYS_GETDENTS64",
            "syscall.SYS_FCNTL",
            "syscall.SYS_ACCESS",
            "syscall.SYS_FACCESSAT",
            
            # Memory management - essential for Python
            "syscall.SYS_MMAP",
            "syscall.SYS_BRK",
            "syscall.SYS_MPROTECT",
            "syscall.SYS_MUNMAP",
            "syscall.SYS_MREMAP",
            
            # Process/thread operations
            "syscall.SYS_GETUID",
            "syscall.SYS_GETGID",
            "syscall.SYS_GETEUID",
            "syscall.SYS_GETEGID",
            "syscall.SYS_GETPID",
            "syscall.SYS_GETPPID",
            "syscall.SYS_GETTID",
            "syscall.SYS_EXIT",
            "syscall.SYS_EXIT_GROUP",
            
            # Signal handling
            "syscall.SYS_RT_SIGACTION",
            "syscall.SYS_RT_SIGPROCMASK",
            "syscall.SYS_RT_SIGRETURN",
            "syscall.SYS_SIGALTSTACK",
            
            # Time operations
            "syscall.SYS_CLOCK_GETTIME",
            "syscall.SYS_GETTIMEOFDAY",
            "syscall.SYS_TIME",
            
            # Threading/synchronization
            "syscall.SYS_FUTEX",
            "syscall.SYS_SET_ROBUST_LIST",
            "syscall.SYS_GET_ROBUST_LIST",
            "syscall.SYS_CLONE",
            
            # System info
            "syscall.SYS_UNAME",
            "syscall.SYS_ARCH_PRCTL",
            "syscall.SYS_RSEQ",
            
            # I/O operations
            "syscall.SYS_IOCTL",
            "syscall.SYS_POLL",
            "syscall.SYS_SELECT",
            "syscall.SYS_PSELECT6",
            
            # Process scheduling
            "syscall.SYS_SCHED_YIELD",
            "syscall.SYS_SCHED_GETAFFINITY",
            
            # Additional Python runtime essentials
            "syscall.SYS_GETRANDOM",
            "syscall.SYS_GETCWD",
            "syscall.SYS_READLINK",
            "syscall.SYS_READLINKAT",
        ]
        allowed_syscalls_tmp = allowed_syscalls
        L = []
        for item in allowed_syscalls_tmp:
            item = item.strip()
            parts = item.split(".")[1][4:].lower()
            L.append(parts)
        f = SyscallFilter(defaction=KILL)
        for item in L:
            f.add_rule(ALLOW, item)
        # Only allow writing to stdout and stderr for output
        f.add_rule(ALLOW, "write", Arg(0, EQ, sys.stdout.fileno()))
        f.add_rule(ALLOW, "write", Arg(0, EQ, sys.stderr.fileno()))
        # Remove other write-related syscalls
        # f.add_rule(ALLOW, 307)  # Removed - might be file creation
        # f.add_rule(ALLOW, 318)  # Removed - might be file creation
        # f.add_rule(ALLOW, 334)  # Removed - might be file creation
        f.load()
    except ImportError:
        # seccomp module not available, skip security restrictions
        pass
"""

def remove_print_statements(code):
    class PrintRemover(ast.NodeTransformer):
        def visit_Expr(self, node):
            if (
                isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "print"
            ):
                return None
            return node

    tree = ast.parse(code)
    modified_tree = PrintRemover().visit(tree)
    ast.fix_missing_locations(modified_tree)
    return ast.unparse(modified_tree)

def detect_dangerous_imports(code):
    # Add file writing modules to the blacklist
    dangerous_modules = [
        "os", "sys", "subprocess", "shutil", "socket", "ctypes", 
        "multiprocessing", "threading", "pickle",
        # Additional modules that can write files
        "tempfile", "pathlib", "io", "fileinput"
    ]
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in dangerous_modules:
                    return alias.name
        elif isinstance(node, ast.ImportFrom):
            if node.module in dangerous_modules:
                return node.module
    return None

def detect_file_write_operations(code):
    """Detect potential file writing operations in code"""
    dangerous_patterns = [
        'open(', 'file(', 'write(', 'writelines(',
        'with open', 'f.write', '.write(', 
        'create', 'mkdir', 'makedirs'
    ]
    
    for pattern in dangerous_patterns:
        if pattern in code:
            return f"File write operation detected: {pattern}"
    return None

def run_pythonCode(data:dict):
    if not data or "code" not in data:
        return {"error": "Invalid request format: missing code"}
    
    code = data.get("code")
    if not code or not code.strip():
        return {"error": "Code cannot be empty"}
    
    # 提取导入的包
    imports = extract_imports(code)
    
    # 自动安装缺失的包
    install_error = install_missing_packages(imports)
    if install_error:
        return {"error": install_error}
    
    code = remove_print_statements(code)
    dangerous_import = detect_dangerous_imports(code)
    if dangerous_import:
        return {"error": f"Importing {dangerous_import} is not allowed."}
    
    # Check for file write operations
    write_operation = detect_file_write_operations(code)
    if write_operation:
        return {"error": f"File write operations are not allowed: {write_operation}"}
    
    # Handle variables - default to empty dict if not provided or None
    variables = data.get("variables", {})
    if variables is None:
        variables = {}
    
    var_def = ""
    
    # Process variables with proper validation
    for k, v in variables.items():
        if not isinstance(k, str) or not k.strip():
            return {"error": f"Invalid variable name: {repr(k)}"}
        
        # Use repr() to properly handle Python True/False/None values
        try:
            one_var = f"{k} = {repr(v)}\\n"
            var_def = var_def + one_var
        except Exception as e:
            return {"error": f"Error processing variable {k}: {str(e)}"}
    
    # 使用增强的输出代码，支持matplotlib图片
    output_code = create_enhanced_output_code()
    
    code = seccomp_prefix + "\\n" + var_def + "\\n" + code + "\\n" + output_code
    
    # Note: We still need to create the subprocess file for execution,
    # but user code cannot write additional files
    tmp_file = os.path.join(data["tempDir"], "subProcess.py")
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(code)
    try:
        result = subprocess.run(["python3", tmp_file], capture_output=True, text=True, timeout=30)
        if result.returncode == -31:
            return {"error": "Dangerous behavior detected (likely file write attempt)."}
        if result.stderr != "":
            return {"error": result.stderr}

        out = ast.literal_eval(result.stdout.strip())
        return out
    except subprocess.TimeoutExpired:
        return {"error": "Timeout error or blocked by system security policy"}
    except Exception as e:
        return {"error": str(e)}

`;
