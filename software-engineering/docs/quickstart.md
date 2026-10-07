# 新项目快速起步（Quick Start，语言无关）

> software-engineering 子文档（保留原编号 §14）。适用场景：开新项目、搭脚手架（配合 `docs/architecture.md` 使用）。

1. **定栈与平台**：选语言/框架，DESIGN 里写明目标平台矩阵、编码(UTF-8)、换行策略；建 `.editorconfig`/`.gitattributes`。
2. **建分层骨架**：核心/框架包（最小依赖、零 UI）+ 交互包 + 可选 CLI；开空安全、警告即错误（按栈对照见 `docs/architecture.md` §4.1）。
3. **搭模块注册表**：定义模块注册接口 + 中央注册入口；按功能分目录（`docs/architecture.md` §3.2）。
4. **定基础抽象**：日志器、配置、DI 方式、生命周期管理器、状态/可观察基类、命令封装、抽象后端接口。
5. **设计数据层 schema**：带 `schemaVersion` + `type` 分派 + `detect`/`apply` 两面 + `${Var}` 路径变量（`docs/data-i18n.md` §6）。
6. **落 i18n**：`Localizer` + `Resources/{en,zh,...}` 扁平映射 + 回退链 + `check-i18n` 校验脚本（`docs/data-i18n.md` §7）。
7. **写文档（一律落 `docs/`，README 与 CLAUDE.md 除外，见 `docs/standards.md` §12；骨架直接取 `docs/templates/`）**：`docs/DESIGN.md`（FR/NFR + 架构视图 + 依赖方向，模板 `templates/DESIGN.md.tpl`）、`docs/CHANGELOG.md`（`templates/CHANGELOG.md.tpl`）、`docs/adr/0001-*.md` 首条 ADR（`templates/ADR.md.tpl`）；根目录仅 `README`（用户向）、`CLAUDE.md`（专属约定 + 变更影响矩阵，指向 `docs/DESIGN.md`，模板 `templates/CLAUDE.md.tpl`）。
8. **配工程化**：`scripts/`（build/publish/check-version-sync；从本 skill 拷贝 `check_docs_layout.py` / `check_i18n.py`）、`tests/`（镜像结构）、`.github/workflows/`（tag 触发发布 + 版本同步/文档落盘/i18n 门禁）、`bootstrap/`。
9. **核心先行**：先用 CLI/测试跑通核心引擎，验证可行后再投 UI（M1=核心，后续里程碑叠加）。
10. **立分支纪律**：保护主干，特性分支 + 合并门禁（编译/测试/无回归）从第一天起执行（B 档；A 档见 SKILL.md 规模分级）。
11. **跑一次基线校验**：`python scripts/check_docs_layout.py .`；若已建 locales，再跑 `python scripts/check_i18n.py <locales> --baseline en`。
