# KouriChat v2.0 后端 
## [此储存库处于开发中，非开发人员请勿使用，用户请转至https://github.com/KouriChat/KouriChat]

## 简介
TODO: 简介待完善

## 项目结构

## TODO
- [ ] 日志修改：全局所有 print 更换为 logger 统一打印
- [x] 模块动态载入： modules 完善
- [ ] 配置文件支持
- [ ] 图形化界面（web）接口 
- [ ] 图片识别
- [ ] 文档识别
    - [ ] docx,doc
    - [ ] xlsx,xls
    - [ ] txt
    - [ ] csv
- [ ] 语音识别
- [ ] 反向通信「MQTT,反向websocket,http轮循支持」
- [ ] 人设管理
- [ ] flask 更换 fastapi
- [ ] socket 支持(http已实现，需要完善socket)
- [ ] 开发文档
- [ ] docker 部署支持
- [ ] 全平台适配
- [ ] ApiFox 

## PR 规范
KouriChatv2.0-Server 贡献规范 
 
提交PR前的准备工作 
 
1. 创建讨论议题
   - 重大功能修改必须先创建issue进行讨论
 
2. 开发环境配置
   ```bash 
   git clone https://github.com/你的用户名/KouriChatv2.0-Server.git 
   cd KouriChatv2.0-Server
   ```
 
分支管理规范 
 
分支命名规则 
- 功能开发：`feature/功能描述` (例如：`feature/用户认证`)
- 问题修复：`fix/问题描述` (例如：`fix/登录异常`)
- 文档更新：`docs/修改内容` (例如：`docs/API文档补充`)
- 代码重构：`refactor/重构内容` (例如：`refactor/数据库模块`)
 
分支同步要求 
- 开发过程中需定期执行以下命令同步主分支：
  ```bash 
  git fetch upstream 
  git rebase upstream/main 
  ```
- 严格禁止使用`git push -f`强制覆盖远程分支
- 单一 pr 只能（修改，删除，增加） 单一功能，请勿叠加 pr ，否则将驳回你的 pr
 
代码提交规范 
 
Commit Message格式 
```
类型(范围): 简要描述 
 
详细说明（可选）
 
相关issue: #123 
```
 
类型说明：
- 新增功能：`feat`
- 修复问题：`fix` 
- 文档更新：`docs`
- 代码重构：`refactor`
- 测试相关：`test`
- 持续集成：`ci`
 
示例：
```
feat(用户模块): 添加手机号注册功能 
 
1. 实现短信验证码发送 
2. 完成手机号注册接口 
3. 添加相关单元测试 
 
相关issue: #45 
```
 
PR提交要求 
 
1. 标题格式  
   `[类型] 功能描述`  
   示例：`[功能] 实现消息已读状态功能`
 
2. 内容模板  
   ```markdown 
   ## 修改目的 
   （说明为什么要做这个修改）
 
   ## 变更内容 
   （详细描述具体修改了哪些内容）
 
   ## 测试验证 
   （说明如何测试这些修改，包括测试用例）
 
   ## 影响范围 
   （说明会影响哪些现有功能）
 
   ## 相关Issue 
   关闭 #{issue编号}
   ```
 
3. 质量要求 
   - 通过所有单元测试：`npm test`
   - 代码风格检查：`npm run lint`
   - 新功能必须包含测试用例 
   - 重大修改需要更新文档 
 
代码审查标准 
 
1. 审查流程
   - 至少需要1位其他核心成员批准 
   - 所有CI检查必须通过 
   - 可能需要根据反馈进行修改 
 
2. 审查重点
   - 代码是否符合项目规范 
   - 是否引入安全隐患 
   - 性能影响评估 
   - 文档是否同步更新 
   - 测试覆盖率是否达标 

**不符合标准的pr将会被驳回，如果不幸并入主分支请回滚**
合并规范 
 
1. 合并方式
   - 使用`Create a merge commit`方式合并 
   - 禁止使用`Rebase and merge`或`Squash and merge`
 
2. 后续处理
   - 合并后相关分支会被自动删除 
   - 重大更新需要在CHANGELOG.md中添加记录 
 
特别注意事项 
 
1. 数据库变更
   - 必须提供迁移脚本 
   - 需要兼容旧版本数据 
 
2. API修改
   - 必须同步更新API文档 
   - 需要考虑版本兼容性 
 
3. 依赖更新
   - 新增依赖需要说明必要性 
   - 版本更新需要测试兼容性 
 
4. 其他要求
   - 不要提交与PR无关的修改 
   - 不要包含敏感信息 
   - 代码注释使用中文 
 
---