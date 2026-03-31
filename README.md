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
