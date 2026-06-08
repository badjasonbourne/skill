---
name: create-linear-issue
description: When users want to create a linear issue, please use this skill.
---

创建一个标准且无歧义的linear issue，便于相关同事看到后能迅速接手开发。大致流程为: 检查环境中是否有linear MCP -> 与用户讨论需求中的模糊点，并达成共识 -> 创建issue，写入linear:

## 一、需求确认

首先请先检查当前环境中是否存在 Linear MCP。若不存在，立即停止任务并向用户汇报。
然后，请你阅读相关的上下文，并指出几个最核心的不确定或模糊点，并同时给出可选的解决策略与你的推荐，便于用户在不同取舍之间做决策。


## 二、Issue创建

在与用户进行了充分的沟通后，开始创建linear issue，准确记录整体任务规划。必须包含 Context、Expected Result、Strategy、Verification 模块。

可根据任务实际灵活添加其他自定义模块，可自行命名，如Phases(如果任务比较难，或步骤较多)、Interface Changes、Data flow、User flow。其中表达流程时，如果合适，请使用文字+Mermaid图表的方式。

### 确保验收要求的可靠性

Verification 模块应能通过命令、接口请求、浏览器操作等来完成。验收方式必须贴近真实使用路径，避免“确认功能正常”“检查逻辑正确”“看起来没问题”这类不可执行描述。Examples:
- `npm test -- user.service.test.ts`
- `curl -X POST ...`
- 通过ChromeMCP操作页面并检查网络请求、DOM 状态或样式计算结果

对前端功能: 整体原则是以ChromeMCP进行真实操作为主要验收方法，可以辅以Vitest和Testing Library测试来减少验证成本（ChromeMCP消耗token较多），但ChromeMCP应该仍为主要验收方式。
- 对于纯函数的测试，可以使用Vitest来测试，不必上ChromeMCP。
- 对于受控组件，可以选择Testing Library来测试。React项目使用@testing-library/react，Svelte项目使用@testing-library/svelte。
- 对于e2e测试，优先设计基于 ChromeMCP 的浏览器验收：启动项目后，通过页面操作、样式计算、脚本执行、网络请求检查等方式验证结果。请在issue中明确，**需根据README.md中的说明自行启动前端，并根据输出信息拿到前端地址，不要假设前端地址已存在。**

对后端 API:
- 先判断接口是否受认证保护。若不受认证保护，可使用 curl 或测试用例直接验证；若受认证保护，应优先通过 ChromeMCP 在已登录浏览器会话中从前端触发请求并验证结果；若浏览器中用户未登录，暂停该任务并通知用户登录后继续。

## 三、注意事项

- 请记住，issue的核心目标是确保交接到该任务的同事能准确无误地进行开发。不要有直接的代码实现，你要相信你的同事水平也很高。
- 在 issue 中，可通过引用文件路径增加准确性，路径格式为 @src/example.ts , 路径前后保留一个空格，不使用反引号。
- 如果用户没有指定project，就不应该保存，应先询问用户想保存在哪个project。