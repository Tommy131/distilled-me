# 编码规范

> Engineering Playbook 子文档（保留原编号 §5）。适用场景：写代码、代码评审（SOLID/命名/错误/并发/平台）。

## 5. 编码规范（Coding Conventions）

### 5.1 SOLID 与代码组织（语言无关）

- **SRP（单一职责）**：**1 文件 = 1 职责**。路由 ≠ 业务逻辑 ≠ 引擎内部。文件**启发式上限约 400 行**：超过且职责单一时 SHOULD 拆（提取协作类/模块）；若超长但职责确实单一，SHOULD 在 CLAUDE.md 记录豁免理由而非机械拆分。
- **OCP（开闭）**：扩展靠**新增文件/模块**，而非修改稳定核心。
- **LSP/ISP（里氏/接口隔离）**：面向**抽象接口**编程（`TorrentBackend`/`AssetProvider`/`SourceProvider` 这类抽象基类），公开头/接口只暴露必要面。
- **DIP（依赖倒置）**：**依赖注入**优先（构造注入 / 服务定位器 / Provider），减少全局可变单例；上层注入下层实现。
  > 张力提示：小型 UI 项目用单例服务（Flutter `Service()` 单例）可接受；核心引擎/后端 SHOULD 用构造注入避免隐藏耦合。按项目规模选择，但**在 DESIGN 里声明哪种**。
- **按业务域而非类型组织**：头文件/目录按领域分（`download/`、`search/`），不要 `controllers/`、`models/`、`utils/` 大杂烩。

### 5.2 命名（按栈对照 + 通则）

通则：**标识符一律英文**；命名一致、可检索；**不得遮蔽语言/框架根类型或 BCL**。

下表每列是来源项目该栈的惯例，**采纳时按栈取一、项目内统一**（取舍写入 CLAUDE.md）：

| 元素 | C# | Dart | C++ | TS/JS | Python | Go |
|---|---|---|---|---|---|---|
| 类型/类 | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` | `PascalCase` |
| 方法/函数 | `PascalCase` | `camelCase` | `snake_case` | `camelCase` | `snake_case` | `camelCase` |
| 变量/参数 | `camelCase` | `camelCase` | `snake_case` | `camelCase` | `snake_case` | `camelCase` |
| 私有字段 | `_camelCase` | `_camelCase` | `m_snake_case` | `#private`/`_x` | `_snake` | `unexported` |
| 常量/枚举 | `PascalCase`¹ | `camelCase`/`SCREAMING` | `UPPER_SNAKE` | `UPPER_SNAKE` | `UPPER_SNAKE` | `PascalCase` |
| 文件 | `PascalCase.cs` | `snake_case.dart` | `snake_case.cpp` | `kebab`/`PascalCase` | `snake_case.py` | `snake_case.go` |
| 命名空间/包 | `PascalCase` | `snake_case` | `snake_case` | — | `snake_case` | `lowercase` |

> ¹ 来源项目 C# 常量/枚举用 `PascalCase`（枚举成员）；若项目更贴近 C# 社区惯例，可用 `UPPER_SNAKE`（常量）+ `PascalCase`（枚举成员）。两种都合规，**项目内取一、统一执行**。

- **命名避坑（强制）**：子命名空间/类型不得遮蔽根类型。
  > 真实教训：用 `Sys`（非 `System`，否则遮蔽 `global::System`）、`Infra`（非 `App`）、`Common`（非 `Dialogs`）。命名前先想"它会撞上语言/框架的根类型吗"。
- 模块内命名成套：`<Feature>Module` / `<Feature>Provider` / `<Feature>Page` / `<feature>.<key>`（i18n）。

### 5.3 注释

- 公共 API 用文档注释（`///` / docstring / Doxygen）写**意图与契约**：*为什么*、边界条件、线程约束、失败行为 —— 而非复述代码。
- 行内注释解释**非显然决策**（性能、兼容、误报规避），对"刻意为之"的反直觉代码加显式标记。
  > 真实标记：`// MATCHED:` 标注"匹配外部工具的本地化输出、绝不翻译"；`// 单文件发布下 Read 可能短读，故用 ReadExactly`。
- 注释密度、命名风格、惯用法**向周围代码看齐**。

### 5.4 错误处理与健壮性（ISO/IEC 25010 可靠性）

**分边界处理**：
- **公共边界**（API/库导出/HTTP 响应）：返回**显式结果类型**（`Result<T,E>` / `std::error_code` / `Outcome` 枚举 / `{error: ...}` JSON），**不把原始异常抛过边界**。HTTP 用语义状态码：200 成功、4xx 客户端错、5xx 服务端错 + 日志。
- **内部/热路径/后台线程**：**记录 + 优雅降级，绝不崩溃**。告警线程、回调、轮询循环里捕获并续跑。
- **永不让解析/格式化抛到调用方**：JSON/模板解析包 try/catch，坏输入返回空对象/原文而非抛。
- **启动路径绝不因单个坏资源崩溃**：加载循环里 `catch { /* skip */ }` 跳过坏项。
- **缺失即可见**：缺翻译显示 key、缺图标用占位、缺数据给默认 —— 让缺口暴露在界面而非静默空白。
- **负缓存**：对"已知会失败的远程拉取"加 TTL 负缓存（标记文件 + 过期时间），避免每次启动重复联网/刷屏日志。
- **失败隔离**：批处理 continue-on-fail，结束统一列失败明细。

### 5.5 并发与资源

- **跨线程回调 MUST marshal 到 UI/正确线程**再触碰 UI（`Dispatcher.Invoke` / `setState`-equivalent）。
- **锁的纪律**：共享可变状态加锁，临界区尽量小；**绝不持锁调用可能回调自身或第三方库的方法**（死锁风险）。
  > 真实模式：`加锁 → 拷贝句柄 → 解锁 → 再调用第三方库`。
- **订阅即生命周期**：长生命周期对象可依赖静态/全局订阅；**瞬态对象（弹窗、明细、列表行）MUST 显式退订/Dispose**，否则静态事件会让它泄漏。高频列表用父级统一刷新，避免每行订阅全局事件。
- **请求按通道隔离**：前端多类异步请求（搜索/元数据/下载/流）各用独立可取消通道，取消一类不波及关键路径。

### 5.6 平台与编码策略（项目首日就定）

在 DESIGN + `.editorconfig` + `.gitattributes` 显式声明：

- **目标平台/运行时**：明确支持矩阵（如"仅 Linux 生产"/"Windows 10 1809+"/"iOS+Android+Desktop"），不支持的平台不假装支持。
- **字符编码**：源文件统一 **UTF-8（无 BOM）**。
- **换行**：统一（跨平台后端常用 **LF**），由 `.gitattributes` 强制。
- **路径**：跨平台代码用正斜杠/路径 API，**不假设盘符或绝对路径**；机器相关路径一律变量化（`${Var}`）。

### 5.7 性能预算与剖析

- **预算写进 NFR**（DESIGN）：启动时间、内存峰值、帧率/延迟分位（p95/p99），发布前可度量、可对比。
- **先剖析，再优化**（猜测式优化是反模式）：热点定位（profiler/trace）→ 改热点 → 复测对比；优化改动附带 before/after 数据。
- **三禁**：热路径上的 IO（磁盘/网络）；N+1（循环内查库/请求）；无上限的大对象/集合（缓存、事件队列、日志缓冲都要有上限或淘汰策略）。
- **异步默认**：IO 操作不阻塞主线程/UI 线程；耗时工作放后台 + 可取消（§5.5 通道隔离）。

### 5.8 UI 三态基线

每个数据视图 MUST 显式设计三态，缺一视为未完成：
- **Loading**：骨架/进度 + 可取消（长任务）。
- **Empty**：空态文案 + 下一步动作（"去创建/去同步"），不显示裸空列表。
- **Error**：错误信息 + 可重试入口（§5.4 缺失即可见、§8 用户可见反馈）。
- 三态与 i18n 联动：三态文案走 Localizer，多语言齐全。
