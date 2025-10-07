export const pythonScriptEnhanced = `
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
import platform
import io
import warnings

# 忽略matplotlib警告
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

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
        'IPython': 'ipython',
        'sympy': 'sympy',
        'openpyxl': 'openpyxl',
        'bokeh': 'bokeh',
        'urllib3': 'urllib3',
        'fonttools': 'fonttools'
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
        
        print("Installing package: " + package_name, file=sys.stderr)
        
        # 安装包 - 尝试多种安装方式
        install_commands = [
            [sys.executable, '-m', 'pip', 'install', package_name, '--break-system-packages', '--quiet', '--disable-pip-version-check'],
            [sys.executable, '-m', 'pip', 'install', package_name, '--user', '--quiet', '--disable-pip-version-check'],
            ['pip3', 'install', package_name, '--break-system-packages', '--quiet'],
        ]
        
        result = None
        for cmd in install_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                if result.returncode == 0:
                    break
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        if result and result.returncode == 0:
            _installed_packages.add(package_name)
            return True
        else:
            print("Failed to install " + package_name, file=sys.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("Timeout installing " + package_name, file=sys.stderr)
        return False
    except Exception as e:
        print("Error installing " + package_name + ": " + str(e), file=sys.stderr)
        return False

def install_missing_packages(imports):
    """智能安装缺失的包，支持依赖关系"""
    package_mapping = get_package_mapping()
    
    # 预安装的包，不需要安装
    preinstalled = {
        'os', 'sys', 'json', 'ast', 'base64', 'tempfile', 'shutil', 'urllib',
        'datetime', 'math', 'random', 'collections', 'itertools', 'functools',
        'operator', 're', 'string', 'time', 'calendar', 'hashlib', 'uuid',
        'importlib', 'subprocess', 'platform', 'errno', 'inspect', 'io', 'warnings'
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
        return "Failed to install packages: " + ', '.join(failed_packages)
    
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
            'DejaVu Sans', 'Arial Unicode MS', 'Noto Sans CJK SC',
            'Liberation Sans', 'Droid Sans Fallback', 'FreeSans'
        ]
        
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        selected_font = None
        
        for font in chinese_fonts:
            if font in available_fonts:
                selected_font = font
                break
        
        if selected_font:
            plt.rcParams['font.sans-serif'] = [selected_font, 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        else:
            # 如果没有找到中文字体，使用默认字体但配置unicode支持
            plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        
        # 设置字体大小和样式
        plt.rcParams['font.size'] = 12
        plt.rcParams['figure.dpi'] = 100
        plt.rcParams['savefig.dpi'] = 150
        plt.rcParams['savefig.bbox'] = 'tight'
        
        return selected_font
    except Exception as e:
        return "Font setup error: " + str(e)

def process_matplotlib_images(result):
    """处理matplotlib图片并转换为base64格式"""
    try:
        import matplotlib.pyplot as plt
        
        # 检查是否有matplotlib图形需要保存
        if hasattr(plt, 'get_fignums') and plt.get_fignums():
            figures_data = []
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                buffer = io.BytesIO()
                fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
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

def detect_dangerous_imports(code):
    """检测危险的导入模块"""
    dangerous_modules = [
        "os", "subprocess", "shutil", "socket", "ctypes", 
        "multiprocessing", "threading", "pickle",
        "tempfile", "pathlib", "fileinput", "glob", "fnmatch",
        "zipfile", "tarfile", "gzip", "bz2", "lzma",
        "mmap", "signal", "resource", "pwd", "grp"
    ]
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in dangerous_modules:
                        return alias.name
            elif isinstance(node, ast.ImportFrom):
                if node.module in dangerous_modules:
                    return node.module
    except Exception:
        pass
    
    return None

def detect_file_write_operations(code):
    """检测潜在的文件写入操作"""
    dangerous_patterns = [
        'open(', 'file(', 'write(', 'writelines(',
        'with open', 'f.write', '.write(', 
        'mkdir', 'makedirs', 'rmdir', 'removedirs',
        'unlink', 'remove', 'rename', 'replace'
    ]
    
    # 允许matplotlib相关的操作
    matplotlib_patterns = [
        'plt.figure', 'plt.plot', 'plt.show', 'plt.savefig',
        'matplotlib.pyplot', 'fig.savefig', 'plt.savefig'
    ]
    
    # 检查是否包含matplotlib操作
    has_matplotlib = any(pattern in code for pattern in matplotlib_patterns)
    
    for pattern in dangerous_patterns:
        if pattern in code:
            # 如果是matplotlib相关代码，允许特定操作
            if has_matplotlib and ('savefig' in pattern or 'figure' in pattern):
                continue
            return "File write operation detected: " + pattern
    return None

def setup_seccomp():
    """设置seccomp安全限制"""
    # Skip seccomp on macOS since it's Linux-specific
    if platform.system() == 'Linux':
        try:
            import seccomp
            import errno
            allowed_syscalls = [
                # File operations - READ ONLY
                "syscall.SYS_READ",
                "syscall.SYS_OPEN",
                "syscall.SYS_OPENAT",
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
            f = seccomp.SyscallFilter(defaction=seccomp.KILL)
            for item in L:
                f.add_rule(seccomp.ALLOW, item)
            # Only allow writing to stdout and stderr for output
            f.add_rule(seccomp.ALLOW, "write", seccomp.Arg(0, seccomp.EQ, sys.stdout.fileno()))
            f.add_rule(seccomp.ALLOW, "write", seccomp.Arg(0, seccomp.EQ, sys.stderr.fileno()))
            f.load()
        except ImportError:
            # seccomp module not available, skip security restrictions
            pass

def run_pythonCode(data):
    """执行Python代码的主函数"""
    if not data or "code" not in data:
        return {"error": "Invalid request format: missing code"}
    
    code = data.get("code")
    if not code or not code.strip():
        return {"error": "Code cannot be empty"}
    
    # 设置安全限制
    setup_seccomp()
    
    # 提取导入的包
    imports = extract_imports(code)
    
    # 自动安装缺失的包
    install_error = install_missing_packages(imports)
    if install_error:
        return {"error": install_error}
    
    # 检查危险导入
    dangerous_import = detect_dangerous_imports(code)
    if dangerous_import:
        return {"error": "Importing " + dangerous_import + " is not allowed."}
    
    # 检查文件写入操作
    write_operation = detect_file_write_operations(code)
    if write_operation:
        return {"error": "File write operations are not allowed: " + write_operation}
    
    # 处理变量
    variables = data.get("variables", {})
    if variables is None:
        variables = {}
    
    var_def = ""
    for k, v in variables.items():
        if not isinstance(k, str) or not k.strip():
            return {"error": "Invalid variable name: " + repr(k)}
        
        try:
            # 使用json.dumps来安全地序列化变量值
            import json
            one_var = k + " = " + json.dumps(v) + "\n"
            var_def = var_def + one_var
        except Exception as e:
            return {"error": "Error processing variable " + k + ": " + str(e)}
    
    # 创建执行代码，添加结果收集与图片处理逻辑
    execution_code = var_def + "\n" + """
# 设置matplotlib中文字体支持
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    
    # 尝试设置中文字体
    chinese_fonts = [
        'Noto Sans CJK SC', 'Noto Sans CJK TC', 'Noto Sans CJK JP', 'Noto Sans CJK KR',
        'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 
        'DejaVu Sans', 'Arial Unicode MS',
        'Liberation Sans', 'Droid Sans Fallback', 'FreeSans'
    ]
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    selected_font = None
    
    for font in chinese_fonts:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams['font.sans-serif'] = [selected_font, 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    else:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
    
    # 设置字体大小和样式
    plt.rcParams['font.size'] = 12
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 150
    plt.rcParams['savefig.bbox'] = 'tight'
    
except Exception:
    pass

""" + code + """

# 若用户提供了 main 函数，则尝试按参数名自动调用
try:
    if 'main' in locals() and callable(main):
        import inspect
        sig = inspect.signature(main)
        kwargs = {}
        for name in sig.parameters.keys():
            if name in locals():
                kwargs[name] = locals()[name]
        r = main(**kwargs)
        # 若用户未显式设置 result，则用 main 的返回值作为 result
        if 'result' not in locals():
            result = r
except Exception:
    pass

# 收集所有局部变量作为结果
import json
import io
import base64
locals_dict = dict(locals())
# 移除内置变量和模块
filtered_locals = {}
for k, v in locals_dict.items():
    if not k.startswith('__') and k not in ['json', 'locals_dict', 'io', 'base64', 'matplotlib', 'plt', 'fm', 'selected_font', 'chinese_fonts', 'available_fonts']:
        try:
            # 尝试序列化以确保变量可以被JSON化
            json.dumps(v)
            filtered_locals[k] = v
        except (TypeError, ValueError):
            # 如果不能序列化，转换为字符串
            filtered_locals[k] = str(v)

# 处理 matplotlib 生成的图片为 base64
try:
    if 'plt' in locals() and hasattr(plt, 'get_fignums') and plt.get_fignums():
        figures_data = []
        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            figures_data.append("data:image/png;base64," + image_base64)
            buffer.close()
            plt.close(fig)
        if figures_data:
            filtered_locals['matplotlib_images'] = figures_data
    # 关闭所有图形
    if 'plt' in locals():
        plt.close('all')
except Exception:
    pass

# 构造最终输出结构，契合前端契约：
# - 若存在 main(**kwargs) 返回的字典，则直接展开到顶层（例如 result、data2）
# - 若没有 main，优先使用局部变量中的 result
# - 始终附加 matplotlib_images（如有）
final_output = {}

try:
    # 将 main(**kwargs) 的返回值展开到顶层
    if 'r' in locals():
        if isinstance(r, dict):
            for _k, _v in r.items():
                try:
                    json.dumps(_v)
                    final_output[_k] = _v
                except (TypeError, ValueError):
                    final_output[_k] = str(_v)
        else:
            try:
                json.dumps(r)
                final_output['result'] = r
            except (TypeError, ValueError):
                final_output['result'] = str(r)
except Exception:
    pass

# 若调用 main 时使用了 kwargs（例如 data1/data2），则把这些入参一并回传，便于前端直接取值
try:
    if 'kwargs' in locals() and isinstance(kwargs, dict):
        for _k, _v in kwargs.items():
            try:
                json.dumps(_v)
                final_output[_k] = _v
            except (TypeError, ValueError):
                final_output[_k] = str(_v)
except Exception:
    pass

# 若仍未设置 result，但局部存在 result，则附加
try:
    if 'result' in locals() and 'result' not in final_output:
        try:
            json.dumps(result)
            final_output['result'] = result
        except (TypeError, ValueError):
            final_output['result'] = str(result)
except Exception:
    pass

# 附加图像结果
if 'matplotlib_images' in filtered_locals and filtered_locals['matplotlib_images']:
    final_output['matplotlib_images'] = filtered_locals['matplotlib_images']

# 如果最终仍无任何键，则返回 success:true 以提示执行成功但无可回传变量
if not final_output:
    final_output = {"success": True}

# 使用 JSON 输出，保持前端解析一致
print(json.dumps(final_output, ensure_ascii=False))
"""
    
    # 写入临时文件并执行
    tmp_file = os.path.join(data["tempDir"], "subProcess.py")
    
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(execution_code)
    
    try:
        result = subprocess.run(["python3", tmp_file], capture_output=True, text=True, timeout=60)
        if result.returncode == -31:
            return {"error": "Dangerous behavior detected (likely file write attempt)."}
        if result.stderr != "":
            return {"error": result.stderr}

        if not result.stdout.strip():
            return {"error": "No output from code execution"}
            
        # 优先按 JSON 解析子进程输出
        out = json.loads(result.stdout.strip())
        return out
    except subprocess.TimeoutExpired:
        return {"error": "Timeout error or blocked by system security policy"}
    except Exception as e:
        return {"error": str(e)}
`;
