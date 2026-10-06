# 标准映射与文档规范

> Engineering Playbook 子文档（保留原编号 §2、§12）。适用场景：写需求/设计文档（FR/NFR、架构视图、SDD、ADR）、决定文档落盘位置。

## 2. 国际标准映射（Standards Alignment）

文档与流程对标下列标准，便于评审、招标、合规引用。

| 维度 | 标准 | 落点 |
|---|---|---|
| 软件质量模型 | **ISO/IEC 25010**（可维护/可移植/安全/可靠/性能/兼容/易用/功能适合性） | DESIGN.md 的 **NFR** 逐条对应质量子特性 |
| 需求工程 | **ISO/IEC/IEEE 29148**（承接 IEEE 830） | **FR-n（功能性）/ NFR-n（非功能性）** 编号、可追溯 |
| 架构描述 | **ISO/IEC/IEEE 42010**（相关者/视图/关注点） | 分层图 + 数据流视图 + 依赖方向 |
| 详细设计 | **IEEE 1016**（SDD） | 数据模型 / 引擎设计 / 接口设计 / UI 设计 |
| 设计原则 | **SOLID** + Clean/Hexagonal Architecture | `docs/coding.md` §5.1 代码组织 + `docs/architecture.md` §3.1 依赖方向 |
| 测试 | **ISO/IEC/IEEE 29119** | `docs/testing.md` 测试规范（单元/集成/E2E/基线快照） |
| 生命周期过程 | **ISO/IEC/IEEE 12207** | 路线图 M1→Mn 里程碑切分 |
| 维护过程 | **ISO/IEC 14764** | CHANGELOG「新增/调整/删除」、兼容策略、变更影响矩阵 |
| 版本编号 | **SemVer 2.0.0** | `Major.Minor.Patch[+Build]` |
| 提交规范 | **Conventional Commits 1.0** | `type(scope): subject` |
| 架构决策 | **ADR**（Architecture Decision Record） | `docs/adr/NNNN-*.md` 记录关键取舍 |
| 信息安全 | **ISO/IEC 27001 / 27002** 控制思想 | 凭据不入库、脱敏清单、最小权限、输入校验 |
| 文档化 | **ISO/IEC/IEEE 26515 / 15289** | DESIGN 权威、README 用户向、CHANGELOG 变更向 |

**铁律：需求可编号、可追溯**。FR/NFR → 设计章节 → 代码模块 → 测试用例，全链路可回溯（29148 核心）。

---

## 12. 文档规范

**文档落盘铁律（强制）**：**除以下例外，一切生成的文档（`.md`/设计/规格/指南/调研/汇报/ADR/变更日志…）MUST 写在 `<repo>/docs/` 下**，按需分子目录（`docs/adr/`、`docs/reports/`、`docs/specs/`…）。仓库根目录与源码目录**不得堆放散装 `.md`**。

**唯三例外，置于仓库根**：
1. `README.md` 及其语言变体 `README_<lang>.md`（用户首屏，平台约定置根）；
2. 工具/平台强制置根的文件（`CLAUDE.md`、`LICENSE`、`CONTRIBUTING.md` 等）—— 但其正文应**精简并指向 `docs/`**；
3. 其它"语言相关的说明文档"（如各语言版 README）。

推论：`CHANGELOG.md` 归 `docs/CHANGELOG.md`（CI 从此处取版本段落生成 Release notes）；临时调研/汇报/计划也写进 `docs/`（可分 `docs/reports/`、`docs/adr/` 等子目录），不要丢在根目录。

### 12.1 文档矩阵

| 文档 | 位置 | 内容要点 |
|---|---|---|
| **DESIGN.md（权威）** | `docs/DESIGN.md` | 定位/痛点/核心理念 → FR/NFR 编号 → 架构视图（mermaid + 依赖方向）→ 数据模型 → 引擎/接口/UI 设计 → 路线图 → 开放问题。唯一事实来源。 |
| **CHANGELOG** | `docs/CHANGELOG.md` | 见 `docs/workflow.md` §11.4；CI 从此处取版本段落生成 Release notes。 |
| **ADR** | `docs/adr/NNNN-title.md` | 每个关键架构取舍一条（背景/决策/后果）。 |
| **指南/规格/调研/汇报** | `docs/<guides\|specs\|reports>/` | 一切临时或长期文档都进 `docs/`，不丢根目录。 |
| **README（用户向）** | 仓库根（例外） | 顶部版本行、一行上机、截图、快速开始；多语言用 `README_<lang>.md`。 |
| **CLAUDE.md（贡献者向）** | 仓库根（工具要求，例外） | 专属约定 + 关键决定 + 目录=命名空间映射 + 避坑清单 + 变更影响矩阵；正文精简，**指向 `docs/DESIGN.md`**。 |
| **模板（脚手架）** | `docs/templates/`（本 skill 内） | `DESIGN.md.tpl` / `ADR.md.tpl` / `CLAUDE.md.tpl` / `CHANGELOG.md.tpl` / `.editorconfig` / `.gitattributes` 范例 —— 新建项目直接复制改填。 |

### 12.2 交接与上手（Onboarding）

- **README 质量基线**（用户向，仓库根）：顶部版本行 + **一行上机命令**（不预装任何环境也能跑，呼应"零依赖落地"）+ 快速开始 + 截图；读者假设"完全不知道这是什么"。
- **新人/新 AI 会话上手路径**（M1 即可走通）：`README` → `CLAUDE.md`（项目差异 + 变更影响矩阵）→ `docs/DESIGN.md`（架构与依赖方向）→ 跑通构建 + 核心测试 → 读一条最近的 ADR 了解决策风格。
- **可复现环境**：构建/测试/CI 用同一份配置（版本钉死，呼应 §3.4），"在我机器上能跑"不成立 = 环境不可复现，须修环境而非绕过。
- **交接检查**（换人/换 AI 会话前）：文档与代码同步（DESIGN/CHANGELOG/README）、门禁全绿、无未记录的重大决定（补 ADR）。
