# OwO source distillation

> This skill’s **default visual language** is distilled from real OwO products. WCAG / process docs remain general; tokens, layout shells, and component recipes prefer OwO conventions.

## Source map

| Project | Stack | Role in distillation |
|---------|-------|----------------------|
| `owo_dashboard` | Flutter | Canonical `AppThemeData`, responsive shell, sidebar / bottom nav |
| `owo_flight_assistant` | Flutter | Same theme core as dashboard; domain severity colors |
| `owo-bahnklar` | Flutter | Same theme + `chipTheme`; formal delay/status palette |
| `OwO-FlightAssistant-Middleware/web` | React + CSS vars | Web port of Flutter tokens (`generateThemeTokens`), type scale, reduced-motion |
| `owo-ai-studio` | React | Dark-ops variant (teal accent, denser chrome) |
| `exam-trainer` | React | Dark study/tool variant (blue accent, topbar shell) |
| `owo-win-deploy` | WPF | Light-first desktop cousin (blue accent, 200px nav, DynamicResource theme) |

## What is canonical vs product-local

| Layer | Canonical (default) | Product-local (override) |
|-------|---------------------|--------------------------|
| Surfaces / text / border | Flight/Dashboard light+dark | Studio/Exam dark-only skins |
| Spacing / radius / motion | 8/16/24/32 · 8/12/16 · 300ms | Studio radius 10; Exam radius 12 |
| Brand triad | 默认紫 `#6C5CE7` / `#A29BFE` / `#00B894` | `[data-product]` accents |
| Shell | Desktop sidebar 200/60; mobile bottom nav; desktop min ~1000 | Topbar shells (Exam/Studio) |
| Status colors | BahnKlar-inspired ok/caution/critical/neutral | Flight NOTAM / log severities may still use ad hoc colors — prefer promoting to status tokens |

## Preset brand triads (Flutter / Web Flight)

| Name | Primary | Secondary | Accent |
|------|---------|-----------|--------|
| 默认紫 | `#6C5CE7` | `#A29BFE` | `#00B894` |
| 圣诞红 | `#D32F2F` | `#EF5350` | `#FF9800` |
| 海洋蓝 | `#0277BD` | `#4FC3F7` | `#00BCD4` |
| 自然绿 | `#388E3C` | `#66BB6A` | `#8BC34A` |
| 温暖橙 | `#E64A19` | `#FF7043` | `#FFB74D` |
| 优雅紫 | `#7B1FA2` | `#AB47BC` | `#BA68C8` |

Apps SHOULD allow system / light / dark mode, optional contrast adjustment (lerp backgrounds), and custom primary via color picker when matching the Flutter shell.

## Implementation pointers

- Flutter: `lib/core/theme/app_theme_data.dart` + `theme_provider.dart`
- Web Flight: `src/core/theme/app-theme-data.ts` → inject CSS vars on `:root`
- WPF: `ThemeManager` brush swap + DWM title bar
- Skill copy-paste: `assets/tokens.css`
