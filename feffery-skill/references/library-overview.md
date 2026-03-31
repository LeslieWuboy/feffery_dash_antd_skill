# Feffery Dash 组件库概览

> 5 个 Feffery Dash 组件库的快速参考。

---

## 库列表

| 库名 | 前缀 | import 语句 | 组件数 | 定位 |
|------|------|------------|--------|------|
| feffery-antd-components | `fac` | `import feffery_antd_components as fac` | 112 | Ant Design 风格 UI 组件 |
| feffery-antd-charts | `fact` | `import feffery_antd_charts as fact` | 29 | AntV 数据可视化图表 |
| feffery-utils-components | `fuc` | `import feffery_utils_components as fuc` | 122 | 工具/增强组件 |
| feffery-markdown-components | `fmc` | `import feffery_markdown_components as fmc` | 2 | Markdown 渲染 |
| feffery-leaflet-components | `flc` | `import feffery_leaflet_components as flc` | 16 | Leaflet 地图组件 |

---

## fac — feffery-antd-components (112 组件)

Ant Design 组件的 Dash 封装，覆盖完整 UI 需求。

| 分类 | 组件数 | 代表组件 |
|------|--------|---------|
| 通用 | 4 | AntdButton, AntdIcon, AntdFloatButton |
| 排版 | 3 | AntdTitle, AntdText, AntdParagraph |
| 布局 | 15 | AntdLayout, AntdRow, AntdCol, AntdSpace, AntdFlex |
| 导航 | 7 | AntdMenu, AntdBreadcrumb, AntdSteps, AntdPagination |
| 数据录入 | 30 | AntdForm, AntdInput, AntdSelect, AntdDatePicker, AntdUpload |
| 数据展示 | 32 | AntdTable, AntdCard, AntdTree, AntdDescriptions, AntdStatistic |
| 反馈 | 9 | AntdModal, AntdMessage, AntdNotification, AntdDrawer |
| 骨架屏 | 7 | AntdSkeleton (含多个变体) |
| 其他 | 5 | AntdConfigProvider, AntdWatermark, AntdTour |

---

## fact — feffery-antd-charts (29 组件)

基于 AntV/G2 的数据可视化图表组件。

| 分类 | 组件 |
|------|------|
| 趋势类 | AntdLine, AntdArea, AntdStock |
| 对比类 | AntdColumn, AntdBar, AntdBidirectionalBar, AntdDualAxes, AntdHistogram |
| 占比类 | AntdPie, AntdRose, AntdRingProgress, AntdTreemap |
| 分布类 | AntdScatter, AntdBox, AntdViolin, AntdHeatmap |
| 流程类 | AntdFunnel, AntdSankey, AntdChord |
| 指标类 | AntdGauge, AntdLiquid, AntdBullet, AntdProgress, AntdRadar |
| 迷你图 | AntdTinyLine, AntdTinyArea, AntdTinyColumn |
| 其他 | AntdWaterfall, AntdWordCloud |

**数据格式**: 所有图表组件接受 `data` 参数（字典列表），`xField`/`yField` 指定字段映射。

---

## fuc — feffery-utils-components (122 组件)

功能增强工具集，覆盖事件、通信、存储、动效等非 UI 能力。

| 分类 | 组件数 | 代表组件 |
|------|--------|---------|
| 事件监听 | 23 | FefferyEventListener, FefferyKeyPress, FefferyListenScroll |
| 通信 | 6 | FefferyHttpRequests, FefferyWebSocket, FefferyEventSource |
| 存储 | 4 | FefferyLocalStorage, FefferySessionStorage, FefferyCookie |
| 动效 | 15 | FefferyAutoAnimate, FefferyMotion + 各种背景特效 |
| 拖拽交互 | 5 | FefferyDraggable, FefferySortable, FefferyGrid |
| 颜色选择 | 8 | FefferyBlockColorPicker, FefferyHexColorPicker, FefferyEyeDropper |
| 数据展示 | 9 | FefferyJsonViewer, FefferyCountUp, FefferyBarcode |
| 容器 | 7 | FefferyDiv, FefferyPortal, FefferyScrollbars, FefferyShadowDom |
| 编辑器 | 3 | FefferyMarkdownEditor, FefferyRichTextEditor, FefferyVditor |
| 性能优化 | 4 | FefferyLazyLoad, FefferyVirtualList, FefferyDebounceProp |
| 页面控制 | 5 | FefferyFullscreen, FefferyReload, FefferyScroll |
| 文件 | 3 | FefferyDownload, FefferyExcelPreview, FefferyWordPreview |
| 图片 | 5 | FefferyImageCropper, FefferyImageGallery, FefferyPhotoSphereViewer |
| 验证码 | 2 | FefferyCaptcha, FefferySliderCaptcha |
| 其他 | 28 | FefferyExecuteJs, FefferyGuide, FefferyFancyButton 等 |

---

## fmc — feffery-markdown-components (2 组件)

| 组件 | 用途 |
|------|------|
| FefferyMarkdown | Markdown 内容渲染 |
| FefferySyntaxHighlighter | 代码语法高亮 |

---

## flc — feffery-leaflet-components (16 组件)

| 分类 | 组件 |
|------|------|
| 地图容器 | LeafletMap, LeafletFeatureGroup |
| 底图 | LeafletTileLayer |
| 矢量要素 | LeafletMarker, LeafletCircle, LeafletCircleMarker, LeafletPolygon, LeafletPolyline, LeafletRectangle, LeafletGeoJSON |
| 附加内容 | LeafletPopup, LeafletTooltip |
| 特殊图层 | LeafletHeatMap, LeafletStaticHeatMap, LeafletFlowLayer |

---

## 通用代码模板

```python
from dash import Dash, html, callback, Input, Output, State
import feffery_antd_components as fac
import feffery_antd_charts as fact
import feffery_utils_components as fuc
import feffery_markdown_components as fmc
import feffery_leaflet_components as flc

app = Dash(__name__)

app.layout = fac.AntdConfigProvider(
    html.Div([
        # 你的组件组合
    ])
)

if __name__ == '__main__':
    app.run(debug=True)
```
