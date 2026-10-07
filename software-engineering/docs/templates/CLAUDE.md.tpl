# CLAUDE.md — <项目名> 贡献者约定

> 本文件只写**项目专属差异**与**规模分级声明**；通用规则指向 software-engineering skill（本仓库路径或外链）。
> 权威设计：`docs/DESIGN.md`。

## 规模分级声明
- 档位：A（个人/小工具）/ B（团队/对外发布）
- 豁免的门禁（A 档，逐项声明）：…

## 栈与命名（按栈取一、项目内统一）
- 语言/框架：…
- 命名风格：（选 software-engineering `docs/coding.md` §5.2 对照表中该栈一列）
- 换行/编码：LF / UTF-8 无 BOM

## 目录 = 命名空间映射
- `src/core/` → …
- `src/modules/<feature>/` → …
- `docs/` → 一切生成文档唯一归属

## 避坑清单（真实教训）
- 命名不遮蔽根类型：用 `Sys`（非 `System`）、`Infra`（非 `App`）…
- …

## 变更影响矩阵（改 A 必须连带检查 B）
| 改动 | 必须连带检查 |
|---|---|
| … | … |
