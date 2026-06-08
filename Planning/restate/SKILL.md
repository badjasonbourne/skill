---
name: restate
description: Based on conversation, restate the requirement or problem in a structured format. ONLY use the skill when actively triggered by the user.
---

# 需求重述Convention

将开发讨论整理为结构化的需求文档，便于后续执行。请遵守如下模板：
<template>
请[添加xxx功能/重构xxx/修复xxx...]（范围聚焦，描述详细）：

## 需求简述
[3-5句话描述需求背景和目标]

## 当前状况/问题
1. [...，@文件路径 以提升准确性]。
2. ...

## 预期效果
1. [预期效果]
2. ...

---

请首先熟悉上下文:
1. @文件路径: (该文件的作用)
2. …

然后进行如下工作:
[概括性描述解决方案步骤]
1. …
2. …

验收:
[此处请给出开发的验收标准。该标准必须是效果上可验证的，而非单纯逻辑上可验证（如“确保功能正常”或“确保界面美观”）。常见验证方案：静态检查；用curl命令调用API；用ChromeMCP打开页面，观察页面行为和网络请求等。]
</template>

撰写要点:
1. **标题**：用动词开头（添加/重构/修复/优化），范围不要过大，聚焦具体问题
2. **文件引用**：使用 @文件路径 格式（不是 `@文件路径`）
3. **问题描述**：具体指出代码位置，引用相关文件
4. **预期效果**：可验证、可衡量
5. **上下文**：列出需要理解的关键文件及其作用
6. **工作步骤**：按执行顺序列出，每步独立可完成

<example>
请添加用户登出功能，支持清除本地缓存和服务端会话：

## 需求简述
当前应用没有登出功能，用户无法主动退出登录状态。需要在用户设置页添加登出按钮，点击后清除本地存储的 token 并通知服务端销毁会话。

## 当前状况/问题
1. @src/pages/Settings.tsx 没有登出入口。
2. @src/services/auth.ts 只有登录逻辑，缺少登出 API 调用。
3. 服务端 @app/api/auth.py 没有登出接口。

## 预期效果是
1. 设置页显示"退出登录"按钮
2. 点击后清除本地 token、跳转到登录页
3. 服务端会话同步失效

---

请首先熟悉上下文:
1. @src/pages/Settings.tsx: 用户设置页面组件
2. @src/services/auth.ts: 认证相关 API 封装
3. @app/api/auth.py: 后端认证接口

然后进行如下工作:
1. 在 @app/api/auth.py 添加 POST /auth/logout 接口
2. 在 @src/services/auth.ts 添加 logout() 函数
3. 在 @src/pages/Settings.tsx 添加登出按钮和处理逻辑

验收:
xxxx
</example>

请在项目根目录下新建Markdown文件，保存重述内容。