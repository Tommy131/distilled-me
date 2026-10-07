# destilled-me

个人 skill 集合。每个子目录是一个独立 skill（自带 `SKILL.md`），以后新增的 skill 都放在这个仓库里，用一条 git 历史统一管理。

## Skills

| Skill | 用途 |
|---|---|
| `software-engineering/` | 语言无关的工程基线：脚手架、架构、编码、测试、安全、发布、AI 协作边界 |
| `ui-ux-design/` | OwO 设计系统：token、布局壳、组件、WCAG 2.2 AA、动效 |

## 新增一个 skill

1. 在仓库根建 `<skill-name>/SKILL.md`，带 `name` 与 `description` frontmatter。
2. 参考文档放 `<skill-name>/docs/`，可执行脚本放 `<skill-name>/scripts/`，模板与静态资源放 `<skill-name>/assets/`。
3. 提交后三个工具都会看到它：`~/.claude/skills`、`~/.grok/skills`、`~/.agents/skills` 里的同名目录都是指向本仓库对应子目录的 junction。

## 目录约定

```
destilled-me/
├── software-engineering/
│   ├── SKILL.md
│   ├── docs/
│   ├── scripts/
│   └── evals/
└── ui-ux-design/
    ├── SKILL.md
    ├── docs/
    └── assets/
```

`SKILL.md` 只做路由入口，按任务加载对应子文档，不要把全部文档一次性塞进上下文。
