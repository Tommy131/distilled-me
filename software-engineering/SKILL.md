---
name: software-engineering
description: >
  Language-agnostic engineering playbook for scaffolding, architecture, coding standards,
  testing, security, observability, API design, workflow/release, and AI collaboration.
  Distilled from real multi-stack projects (.NET/WPF, Flutter, C++20 + React/TS). Aligns with
  ISO/IEC 25010, IEEE 1016/42010/29148, ISO/IEC/IEEE 29119, SOLID, SemVer, Conventional Commits.
  Use when starting a new project, scaffolding a repo, writing DESIGN/ADR docs, reviewing code
  or PRs, designing APIs/data/i18n, setting CI/quality gates, planning releases/rollbacks, or
  constraining AI-generated code. Also use for 工程规范、脚手架、架构评审、质量门禁、提交发布.
metadata:
  type: reference
  scope: cross-project, cross-language
  distilled-from: owo-win-deployer(.NET/WPF) · owo_dashboard/owo_flight_assistant/owo_tool_box/owo-bahnklar(Flutter) · btplayer(C++20 + React/TS)
---

# 工程规范手册（Engineering Playbook · 语言无关）

> 一份**不绑定任何语言或框架**的工程基线。无论项目用 C# / Dart / C++ / TypeScript / Python / Go / Rust，都照这套基线搭骨架、统一理念、对齐质量门禁。
>
> **本文件是路由入口，不是全文**：先按下表识别任务场景，再加载对应子文档（`docs/`），**不要一次性加载全部子文档**。子文档保留原章节编号（§N），交叉引用按编号解析。
> 标注约定：**MUST / SHOULD / MAY** 取 RFC 2119 语义；括注国际标准号（ISO / IEC / IEEE）。

## 通用原则 vs 项目默认

| 类别 | 含义 | 如何覆盖 |
|------|------|----------|
| **通用门禁** | 铁律 1–7、依赖单向、凭据不入库、边界错误模型、需求可追溯 | 不可静默跳过；B 档项目必须遵守 |
| **手册默认** | 文档一律进 `docs/`、核心包依赖预算 ≤5、零依赖落地、模块注册表形态 | 可裁剪；**必须在项目 `CLAUDE.md` / `docs/DESIGN.md` 声明差异** |
| **按栈惯例** | 命名表、工程基线开关等多列对照 | **按栈取一、项目内统一**，取舍写入 `CLAUDE.md`，禁止混用两套 |

裁剪可以，一经声明必须贯穿；未声明则按本手册默认执行。

## 路由表：任务场景 → 子文档

| 任务场景 | 加载 |
|---|---|
| 开新项目、搭脚手架 | `docs/quickstart.md` + `docs/architecture.md` + 模板 `docs/templates/` |
| 写需求/设计文档（FR/NFR、架构视图、SDD、ADR）、文档落盘、交接/上手 | `docs/standards.md`（模板 `docs/templates/DESIGN.md.tpl`、`ADR.md.tpl`；含 §12.2 交接与上手） |
| 写代码、代码评审（SOLID/命名/错误/并发/平台） | `docs/coding.md` |
| 数据层 / 配置 / schema 设计 / 存量数据迁移 | `docs/data-i18n.md`（§6，含 §6.5 迁移策略） |
| 国际化多语言 | `docs/data-i18n.md`（§7） |
| 设计 API / IPC / 接口契约 / 错误模型 | `docs/api.md`（§15） |
| 日志 / 排障 / 可观测性 | `docs/observability.md` |
| 安全加固 / 凭据管理 / 权限 | `docs/security.md` |
| 测试设计 / 测试执行 / 门禁 | `docs/testing.md` |
| 提交 / 分支 / 版本 / CHANGELOG / 发布 / CI / 回滚 | `docs/workflow.md`（§11，含 §11.7 CI/CD、§11.8 回滚灰度） |
| 提交/发布前收尾评审（Definition of Done） | `docs/quality-gate.md` |
| 代码评审扫红旗（反模式） | `docs/antipatterns.md`（§17） |
| AI 生成/修改代码的协作边界 | `docs/ai-collab.md`（§18） |
| 校验文档落盘 / i18n 键集 | 运行 `scripts/check_docs_layout.py`、`scripts/check_i18n.py`（见下） |

## 捆绑脚本（拷贝到目标仓库 `scripts/` 或直接指向本 skill 路径）

| 脚本 | 作用 | 示例 |
|------|------|------|
| `scripts/check_docs_layout.py` | 文档落盘铁律：根目录/源码树不得散落生成文档 | `python scripts/check_docs_layout.py .` |
| `scripts/check_i18n.py` | 多语言键集一致、占位符对齐、无空译文 | `python scripts/check_i18n.py path/to/locales --baseline en` |

Agent 在做脚手架、收尾门禁或修 i18n/文档结构时 SHOULD 运行相关脚本；失败则先修再继续。触发评测样本见 `evals/trigger-eval.json`（优化 description 时用）。

## 十二核心原则

新项目应在 DESIGN.md 显式声明采纳了其中哪些；**裁剪可以，一经声明必须贯穿**。

| 理念 | 含义 |
|---|---|
| **声明式优先** | "做什么"写进数据/配置，"怎么做"留给引擎；加功能 = 加数据或加模块 |
| **关注点分离** | 数据 ↔ 引擎 ↔ 交互分层；UI 不写 IO，引擎不依赖 UI |
| **依赖单向** | 依赖只能外层 → 内层；领域核心零依赖 |
| **模块化可插拔** | 功能以模块注册，彼此零硬耦合；加功能不改稳定核心 |
| **幂等可重入** | 重复执行结果一致，可中断重跑；写操作前先检测 |
| **可复现** | 钉版本 + 校验和 + 路径变量化；不假设隐式环境 |
| **零依赖落地** | 目标环境无需预装即可启动（手册默认；嵌入式/受管运行时可声明豁免） |
| **失败隔离** | 单点失败不连坐，最后统一汇报 |
| **可观测** | 每次运行产出结构化日志 + 人读汇总 |
| **安全优先** | 凭据永不入库；敏感项默认排除 |
| **最小权限** | 仅在确需时提权，集中、可审计 |
| **单一事实来源（SSOT）** | 同一信息只有一个权威定义点 |

## 铁律（评审一票否决，任何阶段必查）

1. **依赖单向向内**：领域层 MUST NOT 依赖上层/框架/IO；引擎/核心库 MUST NOT 依赖任何 UI 框架；反向依赖、跨层穿透、协议细节（HTTP/JSON、SQL、控件类型）泄漏进领域层 —— 一律拒绝。
2. **加功能不做外科手术**：新增功能 = 加一个模块目录 + 注册一行 + 数据文件，**不修改稳定核心**（OCP）。
3. **文档落盘铁律**（手册默认）：除 `README*`（含语言变体）与工具强制置根文件（`CLAUDE.md`/`LICENSE`/`CONTRIBUTING.md`）外，一切生成的文档 MUST 落在 `<repo>/docs/`，禁止散落在仓库根或源码目录。项目若另有文档布局，MUST 在 `CLAUDE.md` 声明。
4. **需求可编号、可追溯**：FR/NFR → 设计章节 → 代码模块 → 测试用例，全链路可回溯。
5. **凭据永不入库**：私钥/token/密码 MUST NOT 进版本库；机密经环境变量/密钥库注入。
6. **公共边界不抛原始异常**：边界返回显式结果类型（`Result<T,E>` / `error_code` / `{error: ...}`）；内部/热路径/后台线程记录 + 优雅降级，绝不崩溃。
7. **写操作前先检测**：任何写/apply 操作有检测分支，可重跑无副作用（幂等）。

## 规模分级：哪些门禁必做、哪些可豁免

本手册门禁按"团队/生产"档设计。小项目可按下表降档，**但降档决定必须在项目 CLAUDE.md/DESIGN.md 中声明**；声明后不得混用两套标准。

| 维度 | A 档：个人/小工具（≤2 人） | B 档：团队/对外发布（≥3 人或对外交付） |
|---|---|---|
| 依赖方向、错误处理边界、凭据不入库、幂等检测 | 必做 | 必做 |
| `schemaVersion`、i18n 结构（单语言也按可扩展结构搭） | 必做 | 必做 |
| 单元测试 | 核心逻辑必做 | 单元 + 集成 + E2E/快照全做 |
| 预提交门禁 | 编译零告警 + 核心单测 | `编译零告警 → 单测 → 冒烟/E2E` 全过 |
| 分支纪律（不直接提交主干 + 合并门禁） | 可豁免（允许直接提交 main） | 必做 |
| ADR | 只记重大决策 | 每个关键取舍一条 |
| CHANGELOG 版本段落 + 跨产物版本同步 CI | 对外发布必做；多产物必做 | 必做 |
| NFR 逐条对应 25010 质量子特性 | 可选 | 必做 |

## 使用说明

- **两类条款**：核心原则与铁律是**门禁**（强制）；子文档中带 SHOULD / MAY 的规范是**参考**，按项目声明后统一执行。
- **两份必备文件**：每个项目根目录都应有 `CLAUDE.md`（或 `CONTRIBUTING.md`）—— 项目**专属**约定 + 指向权威设计；`docs/DESIGN.md` —— 权威设计（唯一事实来源）。本手册是它们的**上游母本**：项目文件只写"本项目的差异点"，通则引用本手册。
- **冲突处理**：子文档中多栈对照表（如命名表、工程基线开关）每列是来源项目该栈的惯例；采纳时**按栈取一、项目内统一**，并把取舍写进 CLAUDE.md，不在一个项目里混用两套。
- **加载纪律**：每次任务只加载路由表指向的子文档；完成后再按需追加，避免上下文膨胀。
