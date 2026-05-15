---
name: design-in-paper
description: The best practice of prototyping in paper and converting prototypes to code. ONLY use the skill when actively triggered by the user.
---

# 在Paper中进行原型设计

## 一、Overview
在Paper中进行设计时，请严格遵守本规范，确保设计交付物能与前端团队进行无缝对接。本规范采用如下流程: "设计 → 审查"的循环。

## 二、设计阶段
- 布局优先采用 Flexbox + fill/fit 实现流式自适应：
    - 外层容器负责填充可用空间，内层模块默认由内容、padding 和 gap 自然撑开。
    - 尺寸策略默认遵循“内容决定大小”，只有在需要统一视觉节奏、批量对齐或明确建立秩序感时，才使用统一的固定宽高或固定间距。
    - 固定尺寸仅用于具有明确固有尺寸或强约束的元素，例如 icon、头像、缩略图，以及需要统一高度的输入控件、列表项或卡片。
    - 避免为对齐而随意写死容器高度，优先通过 padding、gap、对齐方式来解决布局问题。
- **非必要不嵌套**：非必要请勿使用过多Flexbox嵌套，确保布局层次的扁平。
- **基础属性优先**：优先使用基础的样式属性达到效果，因为paper的CSS兼容性较差。**禁止**使用如下属性:
    - 最大最小尺寸: max-width, max-height, min-width, min-height
    - grid, flex的wrap属性。
- **局部重构优于补丁**: 当遇到明显布局问题时，优先考虑将局部删除，然后通过write_html重写，而非在原有基础上用update_styles进行修补
- get_tree_summary工具仅能返回计算后的尺寸，无法体现fill/fit。

## 三、审查阶段
设计完成后，进入审查阶段。请综合使用get_jsx、get_computed_styles、get_screenshot 对上述原则的遵守情况进行二次核查：
- 使用get_jsx检查布局是否符合Flexbox+fill/fit的规范。对于具体节点的样式，使用get_computed_styles检查。
- 在保持视觉效果不变的情况下，是否存在冗余的节点嵌套。
- get_jsx和get_computed_styles仅能反映代码逻辑层面的正确性。具体还需通过get_screenshot获取视觉截图，通过视觉维度做二次核对。
- 避免直接依赖get_tree_summary的结果，此工具仅返回计算后的尺寸，无法体现fill/fit。

## 四、注意事项
1. 若初始设计稿目标区域不满足Flexbox+fill/fit的规范，或冗余嵌套过多，请勿直接再其上进行修补，而是直接删除内容并重构。仅优化结构，不得修改设计意图。
2. 进行截图时，为从大局判断布局是否符合规范，请截取所需节点的父节点。

# 将Paper中的原型转换为代码
**核心原则**：准确参考，而非盲目照搬。设计表达意图，代码必须是对其忠实的、生产级的诠释。

## Workflow
1. 从 Paper 读取设计稿（Frame）（使用 get_screenshot、get_jsx、get_computed_styles），识别目标前端组件。
2. **必须**在编写任何代码前，向用户简要说明转换方案。列出：(a) 关键转换决策（如"按钮高度 48px → py-3"），(b) 任何不确定之处（如"这个 360px 宽度是刻意为之还是应该用 w-full？"）。等待用户确认后再动手。**即使你认为一切清晰，也绝不跳过此步**。
3. 用户确认后，将设计转为代码，并与设计截图进行核对验证。

## Translation Rules
1. **样式 → Tailwind CSS 变量**：将设计稿中的硬编码值转换为最接近的 Tailwind CSS 变量。例如：`font-size: 14px` → `text-sm`；`border-radius: 8px` → `rounded-lg`；`padding: 16px` → `p-4`；`gap: 12px` → `gap-3`。保留设计稿中的硬编码 hex/rgb 颜色值以确保还原度。仅当设计色值与 Tailwind 预设颜色**完全一致**时，才使用 Tailwind 颜色工具类。
2. 容器元素（按钮、卡片、区块等）用于包裹内容进行布局。默认规则：**宽度撑满父级，高度自适应内容。** 不要在容器上硬编码像素尺寸：
    - 若设计稿中容器已使用 flexbox → 代码中直接采用 flex 布局，尺寸自然由内容驱动。
    - 若设计稿使用硬编码尺寸 → 反推其意图，转换为 padding + 内容自适应高度。EXAMPLE: 一个包含 16px 文字的 `h-12` 按钮 → `py-3`。
    - 非容器的、有固有尺寸的元素（图标、头像、分隔线）保留其固定尺寸。
3. **例外情况** - 容器确需保留固定或受限尺寸的场景：
    - 侧边栏有明确的固定宽度 → `w-[260px]` 或 `w-64`
    - 内容区有最大宽度约束 → `max-w-[720px]`
    - 网格单元有明确宽高比 → 保留固定尺寸或使用 `aspect-square`

### 绝对禁止添加的内容
1. 设计稿（Paper）是视觉决策的**唯一事实来源**。**不得**添加：
    - 设计稿中不存在的阴影
    - 设计稿中不存在的边框
    - 设计稿中没有的背景色
    - 设计师未包含的任何装饰元素
2. <reminder>设计稿省略的内容即为有意省略，请尊重这一决定。即使你认为这一设计是错误的，也请尊重这一决定。</reminder>