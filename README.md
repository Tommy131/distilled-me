# destilled-me

个人 skill 集合，布局与 [anthropics/skills](https://github.com/anthropics/skills) 相同：整个仓库放在某个工具的 skills 根目录下，工具递归找到 `skills/<name>/SKILL.md`。不需要给每个 skill 单独做链接。

## Skills

| Skill | 用途 |
|---|---|
| `skills/software-engineering/` | 语言无关的工程基线：脚手架、架构、编码、测试、安全、发布、AI 协作边界 |
| `skills/ui-ux-design/` | OwO 设计系统：token、布局壳、组件、WCAG 2.2 AA、动效 |

## 新增一个 skill

1. 建 `skills/<skill-name>/SKILL.md`，带 `name` 与 `description` frontmatter。
2. 参考文档放 `skills/<skill-name>/docs/`，脚本放 `scripts/`，模板和静态资源放 `assets/`。
3. 提交即可。仓库已经在 `~/.claude/skills/destilled-me`，Grok、Codex 也从这里读，不用再加 junction。

## 目录约定

```
destilled-me/
├── README.md
└── skills/
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

## 为什么不用每个 skill 一条链接

工具扫描的是 skills 根目录下面任意深度的 `SKILL.md`（Codex 深度上限 6，`skills/<name>/SKILL.md` 在范围内）。集合仓库本身就是根目录的一个子目录，里面的 skill 会被一并发现。`anthropic-skills` 在 `~/.codex/skills` 和 `~/.grok/skills` 各有一份完整检出，所以那边连集合这一层也不用链接。本仓库只保留一份，另外两个工具的 skills 目录用一条指向整仓的 junction，避免三份历史分叉。
