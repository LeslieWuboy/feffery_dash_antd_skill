# Feffery 开发场景推荐

> 根据 281 个组件的功能特性，映射常见 Dash 开发场景到跨库组件组合。
> 每个场景列出核心组件、增强组件和关键实现思路。

---

## 1. 登录/注册页面

- **核心**: fac.AntdForm, fac.AntdFormItem, fac.AntdInput, fac.AntdButton
- **增强**: fac.AntdCheckbox (记住密码), fac.AntdInput(mode='password') (密码输入)
- **安全**: fuc.FefferyCaptcha, fuc.FefferySliderCaptcha (验证码)
- **反馈**: fac.AntdMessage (登录结果提示)
- **回调**: 表单值收集 → 验证 → 登录请求(fuc.FefferyHttpRequests) → 成功跳转(fuc.FefferyReload)

## 2. 数据管理后台（CRUD 表格）

- **核心**: fac.AntdTable (数据展示), fac.AntdSpace, fac.AntdButton
- **筛选**: fac.AntdInput, fac.AntdSelect, fac.AntdDatePicker, fac.AntdDateRangePicker
- **操作**: fac.AntdModal (编辑弹窗), fac.AntdPopconfirm (删除确认)
- **反馈**: fac.AntdMessage (操作提示), fac.AntdNotification (重要通知)
- **分页**: fac.AntdPagination 或 AntdTable 内置分页
- **表格模式**: AntdTableBasic(客户端), AntdTableServerSideMode(服务端)

## 3. 数据可视化仪表盘

- **布局**: fac.AntdLayout, fac.AntdRow, fac.AntdCol, fac.AntdCard
- **图表**: fact.AntdLine(趋势), fact.AntdColumn(对比), fact.AntdPie(占比), fact.AntdGauge(指标)
- **筛选**: fac.AntdSelect(下拉筛选), fac.AntdDateRangePicker(时间范围)
- **增强**: fuc.FefferyCountUp(数字动画), fuc.FefferyAutoAnimate(过渡动效)
- **通信**: fuc.FefferyHttpRequests (异步数据加载)

## 4. 文件上传与管理

- **核心**: fac.AntdUpload, fac.AntdDraggerUpload (拖拽上传)
- **图片**: fac.AntdPictureUpload (图片上传)
- **进度**: fac.AntdProgress (上传进度)
- **预览**: fuc.FefferyExcelPreview (Excel预览), fuc.FefferyWordPreview (Word预览)
- **反馈**: fac.AntdMessage (上传结果)

## 5. 交互式地图应用

- **核心**: flc.LeafletMap (地图容器), flc.LeafletTileLayer (底图)
- **标注**: flc.LeafletMarker (标记点), flc.LeafletPopup (弹窗), flc.LeafletTooltip (提示)
- **区域**: flc.LeafletPolygon, flc.LeafletPolyline, flc.LeafletCircle
- **高级**: flc.LeafletGeoJSON (GeoJSON数据), flc.LeafletHeatMap (热力图), flc.LeafletFlowLayer (流向图)
- **组合**: flc.LeafletFeatureGroup (要素分组)

## 6. 内容编辑器

- **Markdown**: fuc.FefferyMarkdownEditor, fuc.FefferyVditor
- **富文本**: fuc.FefferyRichTextEditor
- **预览**: fmc.FefferyMarkdown (Markdown 渲染), fmc.FefferySyntaxHighlighter (代码高亮)
- **增强**: fuc.FefferyImagePaste (粘贴图片)

## 7. 响应式布局页面

- **布局**: fac.AntdLayout, fac.AntdHeader, fac.AntdContent, fac.AntdSider
- **网格**: fac.AntdRow, fac.AntdCol (栅格系统)
- **自适应**: fuc.FefferyAutoFit (等比缩放), fuc.FefferyResponsive (响应式监听)
- **间距**: fac.AntdSpace, fac.AntdFlex

## 8. 表单与数据录入

- **基础表单**: fac.AntdForm, fac.AntdFormItem
- **输入控件**: fac.AntdInput, fac.AntdInputNumber, fac.AntdTextarea
- **选择控件**: fac.AntdSelect, fac.AntdCascader, fac.AntdTreeSelect
- **日期时间**: fac.AntdDatePicker, fac.AntdDateRangePicker, fac.AntdTimePicker
- **颜色**: fuc.FefferyBlockColorPicker, fuc.FefferyHexColorPicker
- **验证**: fac.AntdForm 内置验证规则

## 9. 实时通信应用

- **WebSocket**: fuc.FefferyWebSocket (双向通信)
- **SSE**: fuc.FefferyEventSource, fuc.FefferyPostEventSource (服务端推送)
- **跨页面**: fuc.FefferyTabMessenger (标签页通信), fuc.FefferyIframeMessenger (iframe通信)
- **HTTP**: fuc.FefferyHttpRequests (HTTP 请求)

## 10. 拖拽排序与自由布局

- **拖拽**: fuc.FefferyDraggable (自由拖拽), fuc.FefferySortable (拖拽排序)
- **网格**: fuc.FefferyGrid, fuc.FefferyGridItem (网格布局)
- **缩放移动**: fuc.FefferyRND (可拖拽+可缩放)

## 11. 导航菜单系统

- **菜单**: fac.AntdMenu (侧边/顶部菜单)
- **面包屑**: fac.AntdBreadcrumb (路径导航)
- **锚点**: fac.AntdAnchor (页内锚点)
- **下拉**: fac.AntdDropdown (下拉菜单)
- **步骤**: fac.AntdSteps (步骤条)

## 12. 数据趋势分析

- **折线**: fact.AntdLine (基础折线), fact.AntdArea (面积图)
- **迷你图**: fact.AntdTinyLine, fact.AntdTinyArea, fact.AntdTinyColumn (内嵌趋势)
- **高级**: fact.AntdDualAxes (双轴对比), fact.AntdStock (K线图)
- **筛选**: fac.AntdSegmented (时间粒度切换)

## 13. 对比分析可视化

- **柱状**: fact.AntdColumn (柱状), fact.AntdBar (条形), fact.AntdBidirectionalBar (双向)
- **瀑布**: fact.AntdWaterfall (瀑布图)
- **分布**: fact.AntdBox (箱线), fact.AntdViolin (小提琴), fact.AntdHistogram (直方)
- **散点**: fact.AntdScatter (散点)

## 14. 占比与层级分析

- **饼图**: fact.AntdPie (饼图), fact.AntdRose (玫瑰图)
- **树图**: fact.AntdTreemap (矩形树图)
- **进度**: fact.AntdProgress (进度), fact.AntdRingProgress (环形), fact.AntdLiquid (水波)
- **漏斗**: fact.AntdFunnel (转化漏斗)

## 15. 用户事件监听

- **按键**: fuc.FefferyKeyPress (快捷键), fuc.FefferyLongPress (长按)
- **鼠标**: fuc.FefferyMousePosition (位置追踪), fuc.FefferyListenHover (悬停)
- **滚动**: fuc.FefferyListenScroll (滚动监听)
- **视口**: fuc.FefferyInViewport (进入视口), fuc.FefferyWindowSize (窗口尺寸)
- **通用**: fuc.FefferyEventListener (自定义 DOM 事件)

## 16. 数据存储与持久化

- **本地**: fuc.FefferyLocalStorage, fuc.FefferyLocalLargeStorage
- **会话**: fuc.FefferySessionStorage
- **Cookie**: fuc.FefferyCookie

## 17. 性能优化方案

- **懒加载**: fuc.FefferyLazyLoad (组件懒加载)
- **虚拟列表**: fuc.FefferyVirtualList (大数据量渲染)
- **防抖节流**: fuc.FefferyDebounceProp, fuc.FefferyThrottleProp
- **骨架屏**: fac.AntdSkeleton (加载占位)

## 18. 主题与样式定制

- **全局**: fac.AntdConfigProvider (主题配置)
- **水印**: fac.AntdWatermark
- **CSS 变量**: fuc.FefferyCssVar, fuc.FefferyStyle
- **外部资源**: fuc.FefferyExternalCss, fuc.FefferyExternalJs

## 19. 图片处理与展示

- **展示**: fac.AntdImage, fac.AntdImageGroup (图片预览)
- **动图**: fuc.FefferyAnimatedImage (动图控制)
- **裁剪**: fuc.FefferyImageCropper (图片裁剪)
- **画廊**: fuc.FefferyImageGallery (图片画廊)
- **全景**: fuc.FefferyPhotoSphereViewer (全景图)

## 20. 全局反馈与通知系统

- **轻提示**: fac.AntdMessage (全局消息)
- **通知**: fac.AntdNotification (右上角通知)
- **弹窗**: fac.AntdModal (对话框), fac.AntdPopupCard (弹出卡片)
- **抽屉**: fac.AntdDrawer (侧边抽屉)
- **结果页**: fac.AntdResult (操作结果)
