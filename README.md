# Feffery Skill - Dash 组件专家

Claude Code skill for Feffery Dash 组件库开发支持。

## 功能

- **组件查询**: 快速查找 Feffery 生态中 281 个组件的 API 和用法
- **代码示例**: 提供可直接使用的组件代码示例
- **场景推荐**: 根据开发场景推荐合适的组件组合

## 支持的组件库

| 库 | 前缀 | 组件数 | 用途 |
|----|------|--------|------|
| feffery-antd-components | fac | 112 | Ant Design UI 组件 |
| feffery-antd-charts | fact | 29 | 数据可视化图表 |
| feffery-utils-components | fuc | 122 | 工具/增强组件 |
| feffery-markdown-components | fmc | 2 | Markdown 渲染 |
| feffery-leaflet-components | flc | 16 | Leaflet 地图 |

## 安装

将 `skill/feffery-skill` 目录复制到你的项目 `.claude/skills/` 目录下：

```bash
cp -r skill/feffery-skill /your-project/.claude/skills/
```

## 使用

在 Claude Code 中提及 feffery、fac、fact、fuc、fmc、flc 或 Dash 组件相关关键词时，此 skill 会自动激活。

## 数据目录配置

Skill 需要从 `parsed_output/` 目录读取组件文档数据。

**方式 1：默认路径（推荐）**

在项目根目录下创建 `parsed_output/` 目录：

```
your-project/
├── .claude/
│   └── skills/
│       └── feffery-skill/
└── parsed_output/          # 数据目录
    ├── feffery-antd-components/
    ├── feffery-antd-charts/
    └── ...
```

**方式 2：自定义路径**

如果数据在其他位置，在项目根目录创建 `.claude/settings.local.json`：

```json
{
  "feffery-skill": {
    "data-path": "/your/custom/path/parsed_output/"
  }
}
```

## 生成数据

使用 [parse_docs.py](parse_docs.py) 脚本从 Feffery 官方文档生成数据：

```bash
# 克隆 feffery 文档仓库
git clone https://github.com/feffery/feffery-docs.git

# 运行解析脚本
python parse_docs.py --docs-dir feffery-docs --output-dir parsed_output
```

## 文件结构

```
skill/
├── feffery-skill/
│   ├── SKILL.md              # Skill 主逻辑和工作流
│   └── references/
│       ├── category-map.md   # 组件分类映射
│       ├── library-overview.md # 组件库概览
│       └── scenario-map.md   # 开发场景映射
```

## License

MIT
