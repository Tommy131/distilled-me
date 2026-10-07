# 版本、提交、分支与发布

> software-engineering 子文档（保留原编号 §11）。适用场景：提交、分支、版本号、CHANGELOG、发布。

## 11. 版本、提交、分支与变更管理（ISO/IEC 14764）

### 11.1 版本（SemVer + 跨产物同步）

- **单一版本源（SSOT）**：在一个权威处定义版本（`csproj <Version>` / `pubspec version` / `version.h`）。
- **跨产物同步校验**：当版本散落多个文件（后端 `version.h` ↔ 前端 `version.ts` ↔ README）时，**CI 必须有同步校验脚本**（`check_version_sync`），不一致即失败。
- 语义：破坏性 → Major；向后兼容新功能 → Minor；修复 → Patch；可选 `+Build`（如日期戳 `+2026021401`）。
- API 版本化：对外接口带版本前缀（`/api/v2`），破坏性变更升大版本。

### 11.2 提交（Conventional Commits）

- 格式 `type(scope): subject`，英文祈使句。type：`feat / fix / refactor / docs / chore / ci / test / perf`。
- **提交信息不加 AI 署名**。小步提交、可回滚；多分支并行 rebase 时更要尽早提交。

### 11.3 分支纪律与合并门禁

- **不直接提交主干**（`main`/`master`/`wip`）；一律走特性分支，命名空间化：`feat/<topic>`、`fix/<topic>`、`refactor/phase<N>-<topic>`、`chore/<topic>`。（A 档个人项目可豁免，见 SKILL.md 规模分级）
- **合并门禁**：编译通过 + 测试全过 + 功能验证 + 无回归，才能并入主干。
- **历史策略**：默认 **rebase → fast-forward** 保持线性；**共享分支/已发布 tag 的提交不做改写**，必要时用 merge 提交并写清摘要。团队若偏好 merge 流，SHOULD 在 CLAUDE.md 声明并统一执行。未通过测试的分支**禁止**入主干。

### 11.4 变更日志（发布硬约束）

- **每次发布前 MUST 在 `CHANGELOG.md` 顶部新增 `## v<版本> — <YYYY-MM-DD>`**，按 `### 新增 / ### 调整 / ### 删除 / ### 修复` 写清本次"新增/删除/调整"了什么，无对应项写"无"。
- CI 从对应段落**自动生成 Release notes** → 段落写清楚 = 发行说明清楚。

### 11.5 变更影响矩阵（Change Impact Matrix）

在 CLAUDE.md/DESIGN 维护"**改 A 必须连带检查 B**"的耦合清单，例如：
- 改领域模型序列化字段 → 检查 快照存储、引擎、路由、前端合并逻辑；
- 改路由上下文签名 → 检查 server 装配与所有 `register_*`；
- 改数据 schema → 检查 加载器、迁移、i18n 侧车。

让隐式耦合显式化，是降低回归的关键实践。

### 11.6 发布流程

打 `v<版本>` tag → CI 构建产物 + 建 Release；notes = CHANGELOG 段落 + 静态下载表 + 自动提交列表。

### 11.7 CI / CD 流水线规范

- **必选 job 矩阵**（PR 即触发）：编译零告警 → 单测 → 门禁脚本（`check-*`：版本同步 / i18n / 文档落盘）→ 安全扫描（secret + 依赖漏洞，呼应 §3.4）。
- **PR 门禁 vs 合并门禁分工**：PR 跑"编译+单测+门禁脚本"（快反馈）；合并/发布追加"集成+E2E+冒烟"（§10）。
- **secrets 纪律**：CI 只经平台密钥系统注入（环境变量/secret store），**禁止把 token 写进 workflow 文件或日志**；workflow 文件本身可入库。
- **产物保留**：构建产物/日志保留有限期（建议 ≤ 90 天）；发布产物不可变（按 tag 归档，不覆盖）。
- **发布 job**：仅由 `v*` tag 触发，与 PR/合并解耦（§11.6）。

### 11.8 回滚与灰度

- **发布前写回滚路径**：每个发布（尤其含数据迁移的）在发布说明/ADR 里写清"回滚怎么做"；数据迁移回滚优先走 §6.5 的 down/备份路径。
- **降级开关**：关键新功能带 feature flag（默认关），出问题关 flag 即降级，不依赖回滚二进制。
- **分阶段发布**（B 档对外发布 SHOULD）：小流量/灰度 → 全量；指标（错误率/延迟）退化即自动停止推进并告警。
