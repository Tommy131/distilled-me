# 测试规范

> software-engineering 子文档（保留原编号 §10）。适用场景：测试设计、测试执行、测试门禁。
> 对齐 ISO/IEC/IEEE 29119 思想：测试与需求可追溯、分层、可自动化进门禁。

## 10. 测试规范

### 10.1 分层与目录

| 层级 | 目标 | 依赖 | 速度 |
|------|------|------|------|
| **单元** | 领域/纯函数/状态机/算法 | 被测模块 + 标准库；边界 mock 第三方 | 秒级 |
| **集成** | 模块协作、真实夹具 | 内存 DB / 本地 server / 测试容器 | 十秒～分钟 |
| **E2E / 冒烟** | 关键用户路径、对外契约 | 接近生产的栈 | 分钟级 |
| **契约/快照** | API/CLI 输出不漂移 | 录制基线 + 比对脚本 | 随 CI |

- 测试目录**镜像源码结构**；命名 `<module>_test` / `<module>.spec` / `test_<module>`。
- 每个数据结构 / 算法 / 状态机 SHOULD 有对应单测；**修 bug 先补能复现的失败测试**，再改代码。

### 10.2 单元测试铁律

- **零外部依赖**：框架/领域层测试 MUST NOT 真连网络、磁盘上的生产路径、真实第三方服务。
- **在边界 mock**：HTTP、DB、文件系统、平台 API 在适配层替换；被测逻辑保持纯。
- **可并行**：测试之间无共享可变全局状态；需要隔离用 fixture / temp dir。
- **断言意图**：断言业务结果与不变量，避免只断言"没抛异常"。

### 10.3 集成与 E2E

- **集成**：用真实依赖夹具（内存 DB、嵌入式 server、testcontainers）验证模块协作。
- **E2E**：覆盖登录/核心写路径/失败恢复等冒烟集；B 档对外发布 MUST 有冒烟集进 CI。
- **基线快照**：对外接口录"期望响应快照"（如 `baseline/endpoints.json` 或 CLI golden files），脚本比对实际 vs 期望，回归立刻可见。
- **不稳定测试**：flaky 测试 MUST 修根因或隔离标注；禁止用重试掩盖确定性失败。

### 10.4 与需求追溯

- 测试用例 ID / 名称 SHOULD 能回溯到 FR/NFR 或 DESIGN 章节（如 `FR-12_submit_order`）。
- 新功能合并前：对应 FR 至少有一条自动化或明确记录的手工验收步骤（A 档可手工；B 档优先自动化）。

### 10.5 预提交与 CI 门禁

```
编译零告警 → 单元测试全过 →（B 档）冒烟/E2E 或契约快照通过
```

任一不过不得合并（A 档可按 SKILL.md 规模分级降为「编译 + 核心单测」）。

### 10.6 最小检查清单（写测/审测时用）

- [ ] 新逻辑有单测；边界条件（空、极大、非法输入）有覆盖
- [ ] 修 bug 附带回归测试
- [ ] 第三方仅在边界 mock；无隐藏网络依赖
- [ ] 集成/E2E 使用夹具，可在 CI 复现
- [ ] 快照/基线有意更新时随 PR 说明原因
- [ ] 测试命名可读，失败信息能定位问题

### 10.7 按栈提示（取一即可）

| 栈 | 常用工具 |
|----|----------|
| C# | xUnit/NUnit + Moq/NSubstitute；集成用 WebApplicationFactory / Testcontainers |
| Dart/Flutter | `test` / `flutter_test`；golden 测 UI |
| C++ | GoogleTest / Catch2；集成用本地 fixture |
| TS/JS | Vitest/Jest + Testing Library；E2E 用 Playwright |
| Python | pytest + fixtures；E2E 按项目选 |
| Go | `testing` + httptest / sqlmock 等 |

项目选定后写入 `CLAUDE.md`，不在同一仓库混用两套主测试框架。
