# 架构规范与标准脚手架

> software-engineering 子文档（保留原编号 §3、§4）。适用场景：开新项目搭脚手架、定分层/包划分/生命周期、评审架构。

## 3. 架构规范（Architecture）

### 3.1 分层与依赖方向（强制 · 语言无关）

不同项目层数不同，但都收敛到**同一拓扑：依赖只能向内/向下，内层对外层一无所知**。

```
┌─ 交互层 Interface  ── UI / HTTP 路由 / CLI：仅做协议翻译与展示
│        ↓ 依赖
├─ 应用层 Application ── 用例编排：组合领域与基础设施，不含协议细节
│        ↓ 依赖
├─ 基础设施层 Infrastructure ── 有状态引擎/适配器：DB、第三方库、外部进程的封装
│        ↓ 依赖
├─ 框架层 Framework ── 可复用基建：日志池、线程池、配置、生命周期、DI 容器
│        ↓ 依赖
└─ 领域层 Domain ── 纯业务不变量：实体、状态机、值对象（零框架/零 IO 依赖）
```

**铁律（评审一票否决）**：
- 依赖**单向向内**；领域层 MUST NOT 依赖任何上层、框架或 IO。
- 引擎/核心库 MUST NOT 依赖任何 UI 框架（保证可单测、可换前端、可 CLI 先行）。
- 反向依赖、跨层穿透、把协议细节（HTTP/JSON、SQL、控件类型）泄漏进领域层 —— 一律拒绝。

> 真实映射：
> - 桌面（.NET）：`Core`(纯库) → `App`(WPF) / `Cli`，Core 取最小框架，**平台 API 只在上层**。
> - 跨平台（Flutter）：`lib/core/`(框架+服务) ←被← `lib/modules/`(功能模块) ←被← UI；服务从不调 UI，UI 经状态层观察。
> - 后端（C++）：Interface→Application→Infrastructure→Framework→Domain 五层，CLAUDE.md 显式列"禁止的反向依赖"。

### 3.2 模块化 / 插件注册表（强制）

**按功能（feature）而非按类型（type）分目录**；每个功能是一个自描述模块，通过**注册表**接入框架，彼此零硬耦合。

- 每个模块实现统一的**注册接口**（`ModuleRegistrar` / `RouteRegistry::register_*` / 插件 manifest），声明它要挂载的：导航项、路由、设置页、状态容器、清理回调、向导步骤。
- 框架有一个**中央注册入口**（`registerAll()` / `RouteRegistry`），`main`/启动期统一拉起。
- 模块可**独立测试、独立裁剪**：删一个模块目录 + 去掉一行注册，应用仍能编译运行。
- 新增功能 = 加一个模块目录 + 注册一行，**不改框架核心**（OCP：对扩展开放、对修改关闭）。

> 这是"声明式 + 模块化"是否达标的验收点：加功能不应外科手术式修改稳定核心。

### 3.3 工程 / 包划分

```
核心/引擎包  —— 纯逻辑，依赖最小集（不引 UI/平台 API）→ 优先保证可移植、可测试
前端/交互包  —— 平台框架；平台相关重活（注册表、托盘、传感器、文件系统）只在这里，且 try/catch 降级兜底
薄命令行/工具包 —— 复用核心包，用于无人值守 / 引导 / 脚本
```

- **核心先行**：先用 CLI/测试跑通核心引擎，验证可行后再投 UI（降低早期验证成本）。
- 核心包教训：目标平台/运行时取**能力最小集**；平台专属能力（注册表、WMI、窗口系统）放上层，核心保持中立。

### 3.4 依赖治理（引入第三方依赖的规则）

引入新第三方依赖 MUST 满足（AI 改动同样适用，见 §18.2）：

1. **先问标准库/自实现**：语言标准库、项目已有依赖、≤50 行可自实现的，不引新包。
2. **许可证兼容**：与项目许可证兼容（MIT/Apache-2.0 优先；GPL 系须显式评估并记录）。
3. **维护与漏洞**：近 12 个月有维护；漏洞扫描（`audit`/`npm audit`/`vulncheck` 等）进 CI；已知漏洞 MUST 修复或升级后才能合并。
4. **版本钉死**：锁定确切版本（lockfile / 精确版本号）；**升级走变更流程**（PR + CHANGELOG + 回归测试），不随手 bump。
5. **核心包依赖预算**：核心/引擎包依赖数设上限（建议 ≤ 5，含标准库外全部），新增核心依赖 MUST ADR 记录理由。
6. **平台专属依赖只进上层**（呼应 §3.3 包划分）：注册表/托盘/传感器等平台能力不进核心。

### 3.5 生命周期管理（启动/关闭有序化）

复杂应用 SHOULD 有显式的**生命周期管理器**，分阶段启停：

- **启动**：按依赖顺序分阶段拉起（框架 → 持久化 → 数据 → 应用 → 网络/UI），每阶段失败可中止并清理。
- **关闭**：捕获信号（SIGINT/SIGTERM/窗口关闭）→ **逆序**优雅停机，释放资源、flush 日志、断连。
- 避免"构造即副作用"和散落各处的全局初始化；初始化集中、有序、可观测。

### 3.6 横切关注点 / 中间件链

鉴权、CORS、限流、输入校验、请求日志等**横切关注点**用**中间件链**统一处理，而非散落在每个处理函数里：

```
请求 → [鉴权] → [CORS] → [限流] → [输入校验] → [请求日志] → 业务处理 → 响应
```

- 每个关注点是一个可插拔中间件，顺序可配置；业务代码只管业务。
- 等价物：Web 后端的 middleware、UI 的 behavior/拦截器、桌面的 elevate-once 提权闸。

### 3.7 三条数据流（声明式系统通用范式）

- **Apply（执行/部署）**：加载声明 → 选择 → 依赖拓扑排序 → 逐项 `detect → execute → postConfig` → 汇总。
- **Export（采集/回写）**：扫描现状 → 抓取 → 回写数据层 → 提示提交。
- **Sync（多端）**：pull → apply 差异；export → push。

---

## 4. 标准脚手架（Project Skeleton）

按技术栈裁剪文件名，但**结构骨架一致**：

```
<repo>/
├─ src/ 或 lib/               源码（按"功能/层"组织，不按"类型"堆）
│  ├─ core/ | framework/      框架层：日志/配置/DI/生命周期/i18n（零业务、零 UI）
│  ├─ domain/ | models/       领域层：实体/状态机/值对象（纯）
│  ├─ modules/ | features/    功能模块（每个一目录，自带 pages/state/services/models/i18n）
│  └─ app|cli|server          交互层入口
├─ <data>/                    声明式数据层（catalog/routes/config，带 schemaVersion）
├─ configs/                   配置仓库（与"是否启用"解耦）
├─ assets/                    图标/资源（按 <id> 命名，离线可用）
├─ bootstrap/                 裸机/首次引导（一行上机脚本）
├─ scripts/                   build / publish / 质量校验（check-*）
├─ tests/                     单元/集成/E2E（镜像 src 结构）
├─ docs/                      ★ 所有文档的唯一归属地（见 docs/standards.md §12 文档落盘铁律）
│  ├─ DESIGN.md               权威设计（IEEE 1016 + 42010 + 29148）
│  ├─ CHANGELOG.md            变更记录（发布前必更）
│  ├─ adr/                    架构决策记录
│  └─ <guides|specs|reports>/ 其它一切生成文档（指南/规格/调研/汇报…）
├─ .github/workflows/         CI（tag 触发发布；版本同步校验）
├─ CLAUDE.md                  项目专属约定（指向 docs/DESIGN.md）— 工具要求置根，例外
├─ README.md / README_<lang>  用户向文档（含版本行）— 例外，置根
├─ .editorconfig / .gitattributes   编码/换行/缩进统一（docs/coding.md §5.6）
├─ LICENSE
└─ .gitignore
```

> **文档落盘铁律**：完整定义见 `docs/standards.md` §12 —— 除 `README*` 与工具强制置根文件外，一切生成文档 MUST 落在 `<repo>/docs/`。

**目录即命名空间**：子目录名 = 子命名空间/子模块；引用时语言各按其法（C# global using、Dart import、C++ namespace、TS path alias），但**XAML/标记语言等不读全局导入的，MUST 显式声明命名空间**。

### 4.1 工程基线开关（按栈对照）

| 关注点 | C#/.NET | Dart/Flutter | C++ | TS/React |
|---|---|---|---|---|
| 空安全 | `<Nullable>enable` | 默认 sound null safety | `std::optional`/不裸指针 | `strict: true` |
| 警告即错误 | 视警告为错误 | `flutter analyze` 零告警 | `-Wall -Wextra` 零告警 | `noUnusedLocals` 等 |
| 发布形态 | 自包含单文件 | 各平台打包 | 静态/最小依赖二进制 | 打包 + 版本注入 |
