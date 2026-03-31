# Feffery 组件分类索引

> 跨 5 库按功能维度组织，帮助快速定位所需组件。
> 数据路径: `/Users/leslie/coding/items/feffery_docs_analysis/parsed_output/`

---

## UI 基础组件 (fac)

### 通用
AntdButton, AntdFloatButton, AntdFloatButtonGroup, AntdIcon

### 排版
AntdTitle, AntdText, AntdParagraph

### 布局
AntdLayout, AntdHeader, AntdContent, AntdSider, AntdFooter, AntdSplitter
AntdRow, AntdCol, AntdSpace, AntdFlex, AntdCenter, AntdDivider, AntdCompact

### 卡片与容器
AntdCard, AntdCardGrid, AntdCardMeta, AntdCollapse, AntdCarousel

---

## 导航组件 (fac)

AntdMenu, AntdBreadcrumb, AntdAnchor, AntdDropdown, AntdSteps, AntdPageHeader, AntdPagination, AntdSegmented

---

## 数据录入 (fac)

### 表单
AntdForm, AntdFormItem, AntdInput, AntdInputNumber, AntdMentions, AntdOTP
AntdRadioGroup, AntdRate, AntdSelect, AntdSlider, AntdSwitch, AntdTransfer, AntdTreeSelect

### 日期时间
AntdCalendar, AntdDatePicker, AntdDateRangePicker, AntdTimePicker, AntdTimeRangePicker

### 选择与勾选
AntdCheckbox, AntdCheckboxGroup, AntdCheckCard, AntdCheckCardGroup, AntdColorPicker, AntdSegmentedColoring

### 文件上传
AntdUpload, AntdDraggerUpload, AntdPictureUpload

---

## 数据展示 (fac)

### 表格
AntdTable (含 Basic/Advanced/ServerSide/Rerender 四种模式)

### 列表与描述
AntdAccordion, AntdDescriptions, AntdDescriptionItem, AntdList
AntdCountdown, AntdCountup, AntdStatistic

### 标签与标记
AntdTag, AntdCheckableTag, AntdBadge, AntdRibbon

### 树形
AntdTree, AntdTreeSelect

### 其他展示
AntdAvatar, AntdAvatarGroup, AntdImage, AntdImageGroup, AntdPopover
AntdQRCode, AntdSpoiler, AntdTimeline, AntdTooltip, AntdEmpty

---

## 反馈组件 (fac)

AntdModal, AntdDrawer, AntdPopupCard, AntdMessage, AntdNotification
AntdAlert, AntdResult, AntdPopconfirm, AntdProgress
AntdSpin, AntdSkeleton (含 Avatar/Button/Image/Input/Custom 变体)

---

## 其他 UI (fac)

AntdConfigProvider, AntdWatermark, AntdBackTop, AntdAffix, AntdTour, AntdCopyText, Fragment

---

## 数据可视化图表 (fact)

### 趋势类图表
AntdLine (折线图), AntdArea (面积图), AntdStock (K线图)
AntdTinyLine, AntdTinyArea, AntdTinyColumn (迷你趋势)

### 对比类图表
AntdColumn (柱状图), AntdBar (条形图), AntdBidirectionalBar (双向柱状图)
AntdDualAxes (双轴图), AntdHistogram (直方图)

### 占比类图表
AntdPie (饼图), AntdRose (玫瑰图), AntdRingProgress (环形进度), AntdTreemap (矩形树图)

### 分布类图表
AntdScatter (散点图), AntdBox (箱线图), AntdViolin (小提琴图), AntdHeatmap (热力图)

### 流程与关系
AntdFunnel (漏斗图), AntdSankey (桑基图), AntdChord (和弦图)

### 进度与指标
AntdGauge (仪表盘), AntdLiquid (水波图), AntdBullet (子弹图), AntdProgress (进度条), AntdRadar (雷达图)

### 其他
AntdWaterfall (瀑布图), AntdWordCloud (词云图)

---

## 工具组件 (fuc)

### 事件监听
FefferyEventListener, FefferyKeyPress, FefferyListenScroll, FefferyListenHover
FefferyListenDrag, FefferyListenDrop, FefferyListenPaste, FefferyListenElementSize
FefferyListenUnload, FefferyLongPress, FefferyMousePosition, FefferyTextSelection
FefferyInViewport, FefferyIdle, FefferyMediaQuery, FefferyResponsive
FefferyDeviceDetect, FefferyDocumentVisibility, FefferyNetwork
FefferyGeolocation, FefferyLocation, FefferyPageLeave, FefferyWindowSize

### 通信
FefferyHttpRequests, FefferyWebSocket, FefferyEventSource, FefferyPostEventSource
FefferyIframeMessenger, FefferyTabMessenger

### 存储
FefferyLocalStorage, FefferyLocalLargeStorage, FefferySessionStorage, FefferyCookie

### 动效
FefferyAutoAnimate, FefferyMotion, FefferyTiltHover
FefferyBirdsBackground, FefferyCellsBackground, FefferyCloudsBackground
FefferyCloudsTwoBackground, FefferyFogBackground, FefferyGlobeBackground
FefferyHaloBackground, FefferyNetBackground, FefferyRingsBackground
FefferyTopologyBackground, FefferyTrunkBackground, FefferyWavesBackground

### 拖拽交互
FefferyDraggable, FefferySortable, FefferyRND, FefferyGrid, FefferyGridItem

### 颜色选择
FefferyBlockColorPicker, FefferyCircleColorPicker, FefferyGithubColorPicker
FefferyHexColorPicker, FefferyRgbColorPicker, FefferyTwitterColorPicker
FefferyWheelColorPicker, FefferyEyeDropper

### 数据展示
FefferyJsonViewer, FefferyCountUp, FefferyFormatBytes, FefferyFormatNumber
FefferyBarcode, FefferyQRCode, FefferyRawHTML, FefferyCompareSlider, FefferySeamlessScroll

### 容器与布局
FefferyDiv, FefferyFixed, FefferyPortal, FefferyShadowDom, FefferySticky
FefferyScrollbars, FefferyHighlightWords, FefferyAutoFit, FefferyResizable

### 文件与下载
FefferyDownload, FefferyExcelPreview, FefferyWordPreview, FefferyDom2Image

### 编辑器
FefferyMarkdownEditor, FefferyRichTextEditor, FefferyVditor

### 图片处理
FefferyAnimatedImage, FefferyImageCropper, FefferyImageGallery, FefferyPhotoSphereViewer, FefferyImagePaste

### 性能优化
FefferyLazyLoad, FefferyVirtualList, FefferyDebounceProp, FefferyThrottleProp

### 页面控制
FefferyFullscreen, FefferyReload, FefferyScroll, FefferySetTitle, FefferySetFavicon

### 验证码
FefferyCaptcha, FefferySliderCaptcha

### 播放器
FefferyAPlayer, FefferyDPlayer, FefferyMusicPlayer

### 其他工具
FefferyExecuteJs, FefferyExternalCss, FefferyExternalJs
FefferyCssVar, FefferyStyle, FefferyDebugGuardian, FefferyGuide
FefferyCountDown, FefferyTimeout, FefferyShortcutPanel
FefferyBurger, FefferyFancyButton, FefferyFancyMessage, FefferyFancyNotification
FefferyExtraSpinner, FefferyTopProgress, FefferyEmojiPicker

---

## Markdown 组件 (fmc)

FefferyMarkdown, FefferySyntaxHighlighter

---

## 地图组件 (flc)

### 地图容器
LeafletMap, LeafletFeatureGroup

### 底图
LeafletTileLayer

### 矢量要素
LeafletMarker, LeafletCircle, LeafletCircleMarker, LeafletPolygon, LeafletPolyline, LeafletRectangle, LeafletGeoJSON

### 附加内容
LeafletPopup, LeafletTooltip

### 特殊图层
LeafletHeatMap, LeafletStaticHeatMap, LeafletFlowLayer
