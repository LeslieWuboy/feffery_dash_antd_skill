#!/usr/bin/env python3
"""
feffery-docs 统一文档解析脚本
解析5个文档仓库，提取组件分类、组件名、使用案例、API参数说明
生成适合知识库检索的JSON文件
"""

import os
import re
import json
from pathlib import Path

# ============================================================
# 配置：5个文档仓库的基础信息
# ============================================================
BASE_DIR = Path(__file__).parent / 'feffery-docs'

LIBRARIES = {
    'feffery-antd-components': {
        'dir': 'feffery-antd-docs',
        'prefix': 'fac',
        'import_name': 'feffery_antd_components',
        'pattern': 'A',  # 结构化demos
    },
    'feffery-antd-charts': {
        'dir': 'feffery-antd-charts-docs',
        'prefix': 'fact',
        'import_name': 'feffery_antd_charts',
        'pattern': 'A',
    },
    'feffery-utils-components': {
        'dir': 'feffery-utils-docs',
        'prefix': 'fuc',
        'import_name': 'feffery_utils_components',
        'pattern': 'A',
    },
    'feffery-markdown-components': {
        'dir': 'feffery-markdown-docs',
        'prefix': 'fmc',
        'import_name': 'feffery_markdown_components',
        'pattern': 'A',
    },
    'feffery-leaflet-components': {
        'dir': 'feffery-leaflet-docs',
        'prefix': 'flc',
        'import_name': 'feffery_leaflet_components',
        'pattern': 'B',  # 内联demos
    },
}



def _flatten_category(category_path: str) -> str:
    """将分类路径扁平化，去掉'组件介绍 / '前缀，只保留最后一级"""
    parts = category_path.replace('组件介绍 / ', '').replace('组件介绍', '').strip()
    if not parts:
        return '未分类'
    # 只取最后一级
    last = parts.split(' / ')[-1].strip()
    return last if last else '未分类'


def parse_config_categories_v2(config_path: str) -> dict:
    """
    v3: 基于return块正则的健壮分类解析
    提取side_menu_items()返回的完整菜单数据块，按层级解析分类
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 查找 side_menu_items 方法中的 return [ 块
    in_return = False
    brace_depth = 0
    menu_lines = []
    for line in lines:
        if 'return [' in line or ('menuItems' in line and '= [' in line and 'side_menu' not in line):
            in_return = True
        if in_return:
            menu_lines.append(line)
            brace_depth += line.count('[') - line.count(']')
            if brace_depth <= 0 and len(menu_lines) > 2:
                break

    if not menu_lines:
        return {}

    menu_content = ''.join(menu_lines)

    components = {}
    current_group = None
    current_sub = None
    current_sub_sub = None

    comp_pattern = re.compile(r"'component':\s*'(ItemGroup|SubMenu|Item|Divider)'")
    comp_positions = [(m.start(), m.group(1)) for m in comp_pattern.finditer(menu_content)]

    for idx, (pos, comp_type) in enumerate(comp_positions):
        if comp_type == 'Divider':
            continue

        end_pos = comp_positions[idx+1][0] if idx+1 < len(comp_positions) else len(menu_content)
        block = menu_content[pos:end_pos]

        key_m = re.search(r"'key':\s*'([^']*)'", block)
        title_m = re.search(r"'title':\s*(?:translator\.t\(\s*)?['\"]([^'\"]*?)['\"]", block)

        key_val = key_m.group(1) if key_m else None
        title_val = title_m.group(1) if title_m else None

        if not key_val:
            continue

        # 通过缩进判断层级
        line_start = menu_content.rfind('\n', 0, pos) + 1
        indent = pos - line_start

        if comp_type == 'ItemGroup':
            current_group = title_val or key_val
            current_sub = None
            current_sub_sub = None
        elif comp_type == 'SubMenu':
            if indent >= 28:
                current_sub_sub = title_val or key_val
            else:
                current_sub = title_val or key_val
                current_sub_sub = None
        elif comp_type == 'Item':
            if not key_val.startswith('/'):
                continue
            comp_name = key_val.lstrip('/')
            cat_parts = []
            if current_group:
                cat_parts.append(current_group)
            if current_sub:
                cat_parts.append(current_sub)
            if current_sub_sub:
                cat_parts.append(current_sub_sub)

            components[comp_name] = {
                'category_path': ' / '.join(cat_parts),
                'title': title_val or comp_name,
                'route': key_val,
            }

    return components


def parse_leaflet_config(config_path: str) -> dict:
    """
    leaflet 的 config.py 结构不同，需要特殊处理
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    components = {}
    current_sub = None

    lines = content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()

        if "'component': 'SubMenu'" in stripped:
            for j in range(max(0, i-3), min(len(lines), i+8)):
                m = re.search(r"'title':\s*['\"]([^'\"]*?)['\"]", lines[j])
                if m:
                    title = m.group(1)
                    # 检查是否是三级菜单（LeafletMap的子菜单）
                    indent = len(lines[j]) - len(lines[j].lstrip())
                    if 'key' in lines[max(0,j-2):j+1]:
                        km = re.search(r"'key':\s*'([^']*)'", lines[max(0,j-3)])
                        if km:
                            key_val = km.group(1)
                            if '/' in key_val:  # 三级菜单
                                current_sub = title
                            else:
                                current_sub = title
                    else:
                        current_sub = title
                    break

        elif "'component': 'Item'" in stripped:
            key_match = None
            title_match = None
            for j in range(max(0, i-1), min(len(lines), i+15)):
                km = re.search(r"'key':\s*'(/[^']*)'", lines[j])
                if km:
                    key_match = km.group(1)
                tm = re.search(r"'title':\s*['\"]([^'\"]*?)['\"]", lines[j])
                if tm:
                    title_match = tm.group(1)
                if key_match and title_match:
                    break

            if key_match and title_match:
                comp_name = key_match.lstrip('/')
                components[comp_name] = {
                    'category_path': f'组件介绍 / {current_sub}' if current_sub else '组件介绍',
                    'title': title_match,
                    'route': key_match,
                }

    return components


def extract_intro_from_file(intro_path: str) -> str:
    """从 intro.py 提取组件简介"""
    if not os.path.exists(intro_path):
        return ''

    with open(intro_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 查找 AntdParagraph 中的文字
    descriptions = []
    # 匹配 translator.t('...') 和直接文字
    desc_matches = re.findall(
        r"translator\.t\(\s*'([^']*)'\s*\)|"
        r"translator\.t\(\s*\"([^\"]*)\"\s*\)|"
        r"fac\.AntdParagraph\(\s*\[?\s*(?:translator\.t\(|'|\")",
        content
    )

    # 更简单的方法：找 AntdParagraph 内的文字
    paragraphs = re.findall(
        r"AntdParagraph\(\s*\[?\s*(?:translator\.t\(\s*)?['\"]([^'\"]*?)['\"]",
        content
    )
    if paragraphs:
        return paragraphs[0]

    # 备选：找任何中文描述
    chinese = re.findall(r"'([^']*[\u4e00-\u9fff][^']*)'", content)
    for text in chinese:
        if '组件介绍' not in text and '通用' not in text and len(text) > 3:
            return text

    return ''


def extract_demos_config(demos_init_path: str) -> list:
    """
    从 demos/__init__.py 提取 demos_config() 返回的demo列表
    """
    if not os.path.exists(demos_init_path):
        return []

    with open(demos_init_path, 'r', encoding='utf-8') as f:
        content = f.read()

    demos = []

    # 提取 demos_config 函数中的 return [ ... ] 部分
    # 匹配每个 demo 的 path, title, description
    demo_pattern = re.compile(
        r"\{\s*"
        r"'path':\s*'([^']*)',\s*"
        r"'title':\s*(?:t\(\s*)?['\"]([^'\"]*?)['\"]",
        re.DOTALL
    )

    for m in demo_pattern.finditer(content):
        path = m.group(1)
        title = m.group(2)

        # 提取 description - 在 title 之后
        remaining = content[m.end():]
        desc_match = re.search(
            r"'description':\s*(?:t\(\s*)?['\"]([^'\"]*?)['\"]",
            remaining[:500]
        )
        description = desc_match.group(1) if desc_match else ''

        demos.append({
            'path': path,
            'title': title,
            'description': description,
        })

    return demos


def extract_demo_code(demo_file_path: str) -> str:
    """从单个demo文件提取 code_string() 返回的代码"""
    if not os.path.exists(demo_file_path):
        return ''

    with open(demo_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 code_string 中的代码
    # 模式1：code_string 返回列表，里面有 'code': """..."""
    code_matches = re.findall(
        r"'code':\s*\"{3}(.*?)\"{3}",
        content,
        re.DOTALL
    )

    if code_matches:
        # 优先取 zh-cn 的代码
        return code_matches[0].strip()

    # 模式2：code_string 直接返回字符串
    code_matches2 = re.findall(
        r"'code':\s*['\"](.*?)['\"]",
        content,
        re.DOTALL
    )
    if code_matches2:
        return code_matches2[0].strip()

    return ''


def extract_leaflet_demos(view_path: str) -> list:
    """
    从leaflet的单文件视图中提取demos
    代码嵌入在 FefferySyntaxHighlighter 的 codeString 属性中
    """
    if not os.path.exists(view_path):
        return []

    with open(view_path, 'r', encoding='utf-8') as f:
        content = f.read()

    demos = []

    # 提取 demo 标题（从 AntdDivider 的第一个参数或 innerText）
    titles = re.findall(
        r"AntdDivider\(\s*['\"]([^'\"]*?)['\"]",
        content
    )

    # 提取代码（从 codeString 属性）
    codes = re.findall(
        r"codeString\s*=\s*['\"]{3}(.*?)['\"]{3}",
        content,
        re.DOTALL
    )

    # 提取描述（从 AntdParagraph 中的文字）
    descriptions = re.findall(
        r"AntdParagraph\(\s*\[([^\]]+)\]",
        content,
        re.DOTALL
    )

    # 提取简介
    intro_text = ''
    intro_matches = re.findall(
        r"AntdParagraph\(\s*\[?\s*(?:fac\.AntdText\(\s*)?['\"]([^'\"]*[\u4e00-\u9fff][^'\"]*)['\"]",
        content
    )
    if intro_matches:
        intro_text = intro_matches[0]

    # 组装 demos
    for i in range(min(len(titles), len(codes))):
        demos.append({
            'title': titles[i],
            'code': codes[i].strip(),
        })

    return demos, intro_text


def parse_api_doc(md_path: str) -> str:
    """读取API文档markdown文件"""
    if not os.path.exists(md_path):
        return ''
    with open(md_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def _extract_default_from_type(type_str: str) -> str:
    """从类型字符串中提取默认值，如 'string; default hello' → 'hello'"""
    m = re.search(r';\s*default\s+(.+)$', type_str)
    if m:
        return m.group(1).strip()
    return ''


def parse_api_params(api_content: str) -> list:
    """
    解析API参数文档，提取结构化参数列表。
    支持两种格式：
    1. 英文格式: - param_name (type; optional): description
    2. 中文格式: **paramName：** *type*型\n\n　　description
    """
    params = []
    if not api_content:
        return params

    # 格式1: 英文标准格式  - param_name (type; optional): description
    param_pattern_en = re.compile(
        r"^-\s+([\w\-\*]+)\s*\(([^)]+)\)\s*:?\s*(.*?)(?=\n-\s|\n\n|\Z)",
        re.MULTILINE | re.DOTALL
    )

    for m in param_pattern_en.finditer(api_content):
        param_name = m.group(1)
        param_type_raw = m.group(2).strip()
        param_desc = m.group(3).strip()
        param_desc = re.sub(r'\n\s{4,}', '\n', param_desc).strip()
        if param_name == 'loading_state':
            continue
        default_val = _extract_default_from_type(param_type_raw)
        # 清理 type 中的 default 部分
        param_type = re.sub(r';\s*default\s+.+$', '', param_type_raw).strip()
        params.append({
            'name': param_name,
            'type': param_type,
            'default': default_val,
            'description': param_desc,
        })

    # 如果英文格式未匹配到，尝试中文格式
    if not params:
        # 格式2: 中文格式 **paramName：** *type*型\n\n　　description
        param_pattern_cn = re.compile(
            r"\*\*([\w]+)[：:]\*\*\s*\*([^*]+)\*(?:型)?[^\n]*\n+(?:[　\s]*([^\n]+))?",
            re.MULTILINE
        )

        for m in param_pattern_cn.finditer(api_content):
            param_name = m.group(1)
            param_type = m.group(2).strip()
            param_desc = m.group(3).strip() if m.group(3) else ''

            if param_name in ('children',):
                param_type = '组件型'

            params.append({
                'name': param_name,
                'type': param_type,
                'default': '',
                'description': param_desc,
            })

    return params


def extract_extra_api(extra_path: str) -> str:
    """提取额外API说明"""
    if not os.path.exists(extra_path):
        return ''
    with open(extra_path, 'r', encoding='utf-8') as f:
        return f.read().strip()


def extract_leaflet_api(doc_path: str) -> str:
    """提取leaflet组件的API文档"""
    if not os.path.exists(doc_path):
        return ''
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 去除前面的非参数部分
    content = re.sub(r'^.*?参数说明\:', '', content, flags=re.S)
    return content.strip()


# ============================================================
# 从已安装的 Python 库 __doc__ 提取中文 API 参数
# ============================================================

# 缓存已导入的库模块
_LIB_MODULES = {}

def _get_lib_module(import_name: str):
    """延迟导入组件库"""
    if import_name not in _LIB_MODULES:
        try:
            _LIB_MODULES[import_name] = __import__(import_name)
        except ImportError:
            _LIB_MODULES[import_name] = None
    return _LIB_MODULES[import_name]


def parse_api_params_from_docstring(import_name: str, comp_name: str) -> tuple:
    """
    从已安装的 Python 组件库的 __doc__ 属性提取中文 API 参数。
    返回 (api_params_list, api_params_raw)
    """
    module = _get_lib_module(import_name)
    if module is None:
        return [], ''

    comp_class = getattr(module, comp_name, None)
    if comp_class is None or not comp_class.__doc__:
        return [], ''

    doc = comp_class.__doc__

    # 找到 "Keyword arguments:" 之后的内容
    kw_marker = 'Keyword arguments:'
    idx = doc.find(kw_marker)
    if idx == -1:
        # 没有 Keyword arguments 段落
        return [], ''

    raw = doc[idx + len(kw_marker):].strip()
    params = []

    # 解析格式: - name (type; default val): description
    param_pattern = re.compile(
        r"^-\s+([\w\-\*]+)\s*\(([^)]+)\)\s*:?\s*(.*?)(?=\n-\s|\Z)",
        re.MULTILINE | re.DOTALL
    )

    for m in param_pattern.finditer(raw):
        param_name = m.group(1)
        param_type_raw = m.group(2).strip()
        param_desc = m.group(3).strip()
        # 清理多行缩进
        param_desc = re.sub(r'\n\s{4,}', '\n', param_desc).strip()
        if param_name == 'loading_state':
            continue
        default_val = _extract_default_from_type(param_type_raw)
        param_type = re.sub(r';\s*default\s+.+$', '', param_type_raw).strip()
        params.append({
            'name': param_name,
            'type': param_type,
            'default': default_val,
            'description': param_desc,
        })

    return params, raw


# ============================================================
# 主解析逻辑
# ============================================================

def find_api_doc(api_dir: Path, comp_name: str) -> str:
    """
    在api_documents目录中查找组件的API文档。
    支持多种目录结构：
    - 直接在根目录: api_documents/AntdButton.md (fac zh-cn)
    - en_us子目录: api_documents/en_us/AntdButton.md (fac/fact en)
    - 根目录直接: api_documents/action.md (fuc)
    """
    if not api_dir.exists():
        return ''

    # 按优先级搜索各种路径
    search_paths = [
        api_dir / f'{comp_name}.md',           # 直接在根目录
        api_dir / 'en_us' / f'{comp_name}.md',  # en_us子目录
        api_dir / 'zh-cn' / f'{comp_name}.md',  # zh-cn子目录
    ]

    for path in search_paths:
        if path.exists():
            return parse_api_doc(str(path))

    return ''


def find_extra_api(extra_dir: Path, comp_name: str) -> str:
    """在extra_api_descriptions目录中查找额外API说明"""
    if not extra_dir.exists():
        return ''

    search_paths = [
        extra_dir / f'{comp_name}.md',
        extra_dir / 'en_us' / f'{comp_name}.md',
        extra_dir / 'zh-cn' / f'{comp_name}.md',
    ]

    for path in search_paths:
        if path.exists():
            return extract_extra_api(str(path))

    return ''


def parse_pattern_a_library(lib_key: str, lib_config: dict) -> dict:
    """
    解析模式A的库（fac, fact, fuc, fmc）
    """
    lib_dir = BASE_DIR / lib_config['dir']
    config_path = lib_dir / 'config.py'
    views_dir = lib_dir / 'views'
    api_dir = lib_dir / 'public' / 'api_documents'
    extra_dir = lib_dir / 'public' / 'extra_api_descriptions'

    result = {
        'library': lib_key,
        'prefix': lib_config['prefix'],
        'import_name': lib_config['import_name'],
        'components': [],
    }

    # 1. 解析分类体系
    categories = parse_config_categories_v2(str(config_path))

    # 2. 获取所有组件目录
    if not views_dir.exists():
        return result

    comp_dirs = sorted([
        d for d in views_dir.iterdir()
        if d.is_dir() and not d.name.startswith('_')
    ])

    for comp_dir in comp_dirs:
        comp_name = comp_dir.name

        # 跳过非组件目录
        intro_path = comp_dir / 'intro.py'
        demos_dir = comp_dir / 'demos'
        if not demos_dir.exists() and not intro_path.exists():
            continue

        comp_info = categories.get(comp_name, {
            'category_path': '',
            'title': comp_name,
            'route': f'/{comp_name}',
        })

        # 3. 提取组件简介
        description = extract_intro_from_file(str(intro_path))

        # 4. 提取demos
        demos = extract_demos_config(str(demos_dir / '__init__.py'))

        # 5. 提取每个demo的代码
        demo_list = []
        for demo in demos:
            demo_file = demos_dir / f"{demo['path']}.py"
            code = extract_demo_code(str(demo_file))
            demo_list.append({
                'title': demo['title'],
                'description': demo['description'],
                'code': code,
            })

        # 6. 提取API参数 (优先从已安装库的 __doc__ 获取中文说明)
        # 对 AntdTable 子页面，映射到 AntdTable 组件
        actual_comp_name = comp_name
        if comp_name in ('AntdTableBasic', 'AntdTableAdvanced',
                         'AntdTableRerender', 'AntdTableServerSideMode'):
            actual_comp_name = 'AntdTable'

        api_params, api_content = parse_api_params_from_docstring(
            lib_config['import_name'], actual_comp_name
        )
        if not api_params:
            # 回退到 markdown 文件
            api_content = find_api_doc(api_dir, comp_name)
            api_params = parse_api_params(api_content)

        # 7. 额外API说明
        extra_api = find_extra_api(extra_dir, comp_name)

        comp_record = {
            'name': comp_name,
            'category': comp_info.get('category_path', ''),
            'title': comp_info.get('title', comp_name),
            'description': description,
            'demos': demo_list,
            'api_params': api_params,
            'extra_api': extra_api,
        }

        result['components'].append(comp_record)

    return result


def parse_pattern_b_library(lib_key: str, lib_config: dict) -> dict:
    """
    解析模式B的库（leaflet）
    """
    lib_dir = BASE_DIR / lib_config['dir']
    config_path = lib_dir / 'config.py'
    views_dir = lib_dir / 'views'
    docs_dir = lib_dir / 'documents'

    result = {
        'library': lib_key,
        'prefix': lib_config['prefix'],
        'import_name': lib_config['import_name'],
        'components': [],
    }

    # 1. 解析分类体系
    categories = parse_leaflet_config(str(config_path))

    # 2. 获取所有组件视图文件
    if not views_dir.exists():
        return result

    comp_files = sorted([
        f for f in views_dir.iterdir()
        if f.is_file() and f.suffix == '.py'
        and not f.name.startswith('_')
        and f.name not in ('side_props.py', 'template.py', 'what_is_flc.py',
                           'map_basic.py', 'map_advanced.py')
    ])

    # 加上 map_basic 和 map_advanced 作为 LeafletMap 的两个页面
    map_files = {
        'LeafletMap-basic': views_dir / 'map_basic.py',
        'LeafletMap-advanced': views_dir / 'map_advanced.py',
    }

    # 处理普通组件文件
    for comp_file in comp_files:
        comp_name = comp_file.stem

        comp_info = categories.get(comp_name, {
            'category_path': '',
            'title': comp_name,
            'route': f'/{comp_name}',
        })

        # 提取demos和简介
        demos_and_intro = extract_leaflet_demos(str(comp_file))
        if isinstance(demos_and_intro, tuple):
            demos, description = demos_and_intro
        else:
            demos = demos_and_intro
            description = ''

        # 提取API文档
        api_content = ''
        if docs_dir.exists():
            md_path = docs_dir / f'{comp_name}.md'
            if md_path.exists():
                api_content = parse_api_doc(str(md_path))

        # 提取API参数 (优先从 __doc__)
        api_params, _ = parse_api_params_from_docstring(
            lib_config['import_name'], comp_name
        )
        if not api_params:
            api_params = parse_api_params(api_content)

        comp_record = {
            'name': comp_name,
            'category': comp_info.get('category_path', ''),
            'title': comp_info.get('title', comp_name),
            'description': description,
            'demos': demos,
            'api_params': api_params,
            'extra_api': '',
        }

        result['components'].append(comp_record)

    # 处理 LeafletMap (map_basic 和 map_advanced)
    for map_key, map_file in map_files.items():
        if not map_file.exists():
            continue

        comp_info = categories.get(map_key, {
            'category_path': '组件介绍 / 基础组件',
            'title': f'LeafletMap {"基础功能" if "basic" in map_key else "进阶功能"}',
            'route': f'/{map_key}',
        })

        demos_and_intro = extract_leaflet_demos(str(map_file))
        if isinstance(demos_and_intro, tuple):
            demos, description = demos_and_intro
        else:
            demos = demos_and_intro
            description = ''

        # API文档用 LeafletMap.md
        api_content = ''
        if docs_dir.exists():
            md_path = docs_dir / 'LeafletMap.md'
            if md_path.exists():
                api_content = parse_api_doc(str(md_path))

        api_params, _ = parse_api_params_from_docstring(
            lib_config['import_name'], 'LeafletMap'
        )
        if not api_params:
            api_params = parse_api_params(api_content)

        comp_record = {
            'name': 'LeafletMap',
            'category': comp_info.get('category_path', ''),
            'title': comp_info.get('title', map_key),
            'description': description,
            'demos': demos,
            'api_params': api_params,
            'extra_api': '',
        }

        result['components'].append(comp_record)

    return result


def extract_keywords(comp: dict) -> list:
    """从组件信息中提取搜索关键词"""
    keywords = set()
    name = comp.get('name', '')

    # 组件名本身
    keywords.add(name)

    # title 中的中文词
    title = comp.get('title', '')
    for part in re.findall(r'[\u4e00-\u9fff]+', title):
        if len(part) > 1:
            keywords.add(part)

    # 英文名去前缀
    for prefix in ('Antd', 'Leaflet', 'Feffery'):
        if name.startswith(prefix):
            keywords.add(name[len(prefix):].lower())
            break

    # description 关键词
    desc = comp.get('description', '')
    for word in re.findall(r'[\u4e00-\u9fff]{2,6}', desc):
        keywords.add(word)

    # 分类关键词
    cat = comp.get('category', '')
    for part in re.findall(r'[\u4e00-\u9fff]{2,}', cat):
        keywords.add(part)

    return sorted(keywords)


def generate_docs_md(comp: dict, prefix: str, import_name: str, lib_name: str) -> str:
    """生成组件文档文件(简介 + 何时使用 + API参数)，不含代码示例"""
    lines = []
    lines.append(f"# {comp['name']}\n")
    lines.append(f"- **所属库**: {lib_name}")
    lines.append(f"- **导入**: `import {import_name} as {prefix}`")
    lines.append(f"- **分类**: {comp['category'] or '未分类'}")
    if comp.get('description'):
        lines.append(f"- **简介**: {comp['description']}")
    lines.append('')

    # 何时使用
    if comp.get('description'):
        lines.append("## 何时使用\n")
        lines.append(comp['description'])
        lines.append('')

    # API参数
    if comp['api_params']:
        lines.append("## API参数\n")
        has_default = any(p.get('default') for p in comp['api_params'])
        if has_default:
            lines.append("| 参数名 | 类型 | 默认值 | 说明 |")
            lines.append("|--------|------|--------|------|")
            for param in comp['api_params']:
                desc = param['description'].replace('\n', ' ').strip()
                if len(desc) > 200:
                    desc = desc[:200] + '...'
                default_val = param.get('default', '')
                lines.append(f"| `{param['name']}` | {param['type']} | {default_val} | {desc} |")
        else:
            lines.append("| 参数名 | 类型 | 说明 |")
            lines.append("|--------|------|------|")
            for param in comp['api_params']:
                desc = param['description'].replace('\n', ' ').strip()
                if len(desc) > 200:
                    desc = desc[:200] + '...'
                lines.append(f"| `{param['name']}` | {param['type']} | {desc} |")
        lines.append('')

    if comp.get('extra_api'):
        lines.append("## 特殊参数说明\n")
        lines.append(comp['extra_api'])
        lines.append('')

    return '\n'.join(lines)


def generate_examples_md(comp: dict, prefix: str, import_name: str, lib_name: str) -> str:
    """生成组件示例文件(纯代码示例)"""
    lines = []
    lines.append(f"## {comp['name']} 使用示例\n")
    lines.append(f"`import {import_name} as {prefix}`\n")

    if not comp.get('demos'):
        lines.append("暂无示例。")
        return '\n'.join(lines)

    for demo in comp['demos']:
        lines.append(f"### {demo['title']}")
        if demo.get('description'):
            lines.append(f"> {demo['description']}")
        if demo.get('code'):
            lines.append("```python")
            lines.append(demo['code'])
            lines.append("```")
        lines.append('')

    return '\n'.join(lines)


def main():
    from datetime import datetime, timezone

    output_dir = Path(__file__).parent / 'parsed_output'
    output_dir.mkdir(exist_ok=True)

    all_results = {}

    # ===== Phase 1: 解析所有库 =====
    for lib_key, lib_config in LIBRARIES.items():
        print(f"\n{'='*60}")
        print(f"正在解析: {lib_key} ({lib_config['dir']})")
        print(f"模式: {'结构化demos' if lib_config['pattern'] == 'A' else '内联demos'}")
        print(f"{'='*60}")

        if lib_config['pattern'] == 'A':
            lib_data = parse_pattern_a_library(lib_key, lib_config)
        else:
            lib_data = parse_pattern_b_library(lib_key, lib_config)

        comp_count = len(lib_data['components'])
        demo_count = sum(len(c['demos']) for c in lib_data['components'])
        api_count = sum(1 for c in lib_data['components'] if c['api_params'])

        print(f"  组件数: {comp_count}")
        print(f"  示例数: {demo_count}")
        print(f"  有API文档: {api_count}")

        all_results[lib_key] = lib_data

    # ===== Phase 2: 生成组件文件 + 索引 =====
    print(f"\n{'='*60}")
    print("生成组件文件...")
    print(f"{'='*60}")

    index_components = []

    for lib_key, lib_data in all_results.items():
        prefix = lib_data['prefix']
        import_name = lib_data['import_name']
        lib_name = lib_data['library']

        # 使用库原名作为目录名
        lib_dir = output_dir / lib_name
        lib_dir.mkdir(exist_ok=True)

        for comp in lib_data['components']:
            comp_name = comp['name']
            comp_dir = lib_dir / comp_name
            comp_dir.mkdir(exist_ok=True)

            # docs.md: 简介 + 何时使用 + API参数
            docs_content = generate_docs_md(comp, prefix, import_name, lib_name)
            with open(comp_dir / 'docs.md', 'w', encoding='utf-8') as f:
                f.write(docs_content)

            # examples.md: 纯代码示例
            examples_content = generate_examples_md(comp, prefix, import_name, lib_name)
            with open(comp_dir / 'examples.md', 'w', encoding='utf-8') as f:
                f.write(examples_content)

            # 扁平化分类
            flat_category = _flatten_category(comp.get('category', ''))

            kws = extract_keywords(comp)
            index_components.append({
                'name': comp_name,
                'library': lib_name,
                'prefix': prefix,
                'import_name': import_name,
                'description': comp.get('description', ''),
                'category': flat_category,
                'keywords': kws,
                'dir': f'{lib_name}/{comp_name}',
            })

        print(f"  {lib_name}: {len(lib_data['components'])} 组件")

    # ===== Phase 3: 生成 INDEX.json =====
    print(f"\n{'='*60}")
    print("生成索引文件...")

    index_libraries = {}
    for lib_key, lib_data in all_results.items():
        index_libraries[lib_data['library']] = {
            'import_name': lib_data['import_name'],
            'prefix': lib_data['prefix'],
            'component_count': len(lib_data['components']),
        }

    index_json = {
        'version': '3.0',
        'generatedAt': datetime.now(timezone.utc).isoformat(),
        'total_components': sum(len(r['components']) for r in all_results.values()),
        'libraries': index_libraries,
        'components': index_components,
    }

    index_json_path = output_dir / 'INDEX.json'
    with open(index_json_path, 'w', encoding='utf-8') as f:
        json.dump(index_json, f, ensure_ascii=False, indent=2)
    print(f"  INDEX.json: {len(index_components)} 组件")

    # 汇总
    total_comps = sum(len(r['components']) for r in all_results.values())
    total_demos = sum(
        sum(len(c['demos']) for c in r['components'])
        for r in all_results.values()
    )
    print(f"\n完成: {len(all_results)} 个库, {total_comps} 个组件, {total_demos} 个示例")


if __name__ == '__main__':
    main()
