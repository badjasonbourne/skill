---
name: linear-style
description: ONLY use the skill when actively triggered by the user.
---

# Linear Style

本指南将指导如何设计使得界面的UI和交互对齐 Linear 的设计语言。

## 启发式经验

- 避免使用全大写的单词（包括 label、tag、按钮文案、section 标题）。
- 避免使用太多卡片。一屏里 card 数量应该是"克制的"，能用分隔线、留白、分组标题表达层级时优先用它们
- 尽量避免使用阴影。
- 不使用状态圆点。圆点仅在确实表示"实时在线/运行中"等场景出现
- 优先使用较小的按钮来提升精致感
- 减少视觉上卡片套卡片的设计。
- 避免过多的边框引发视觉疲劳。

## 视觉准则

1. **按钮**: 按钮尺寸不宜过大，通常其高度约为内部文字字体大小的两倍。例如，文字使用14px时，按钮的上下内边距可设为7px左右。无需严格遵循两倍比例，找最接近且**偏小**的 token，不要四舍五入到偏大。
2. **卡片/Modal**: 卡片/modal分为Header、Body、Footer 三个部分，其中Header和Body是必选，Footer是可选的。Header右侧需含关闭按钮，使用remixicon close-line圆形图标按钮，圆心与卡片/modal圆角重合；左侧默认需要有标题。