# 文章管理指南（POST_GUIDANCE）

本指南说明本博客（Firefly 主题 / Astro 6）中文章的创建、编辑、图片、特殊状态与发布流程。
文章内容集中在 `src/content/posts/`，校验规则定义在 [`src/content.config.ts`](src/content.config.ts)。

---

## 1. 快速开始：创建一篇新文章

```bash
# 推荐：用脚手架生成带 frontmatter 的空文章
pnpm new-post my-first-post          # 生成 src/content/posts/my-first-post.md
pnpm new-post guide/setup-nas        # 支持子目录，会自动创建 guide/ 目录
```

脚本（[`scripts/new-post.js`](scripts/new-post.js)）会自动填好 `published` 为当天日期。
也可以直接手动在 `src/content/posts/` 下新建 `.md` / `.mdx` 文件。

写完后本地预览：

```bash
pnpm dev        # 启动开发服务器，默认 http://localhost:4321
```

---

## 2. 文件存放与 URL 规则

| 文件路径 | 生成的访问地址 |
|----------|----------------|
| `src/content/posts/hello-world.md` | `/posts/hello-world/` |
| `src/content/posts/guide/setup-nas.md` | `/posts/setup-nas/`（slug 取文件名，不含目录） |
| `src/content/posts/trading-log-2026-05/index.md` | `/posts/trading-log-2026-05/` |

- 支持 `.md` 和 `.mdx`（`.mdx` 可在正文中使用组件）。
- 文件名即 slug，建议用**英文小写 + 连字符**，避免空格和中文（中文标题写在 frontmatter 的 `title` 里）。

---

## 3. Frontmatter 字段完整说明

文件顶部用 `---` 包裹的 YAML。字段与校验规则以 [`src/content.config.ts`](src/content.config.ts) 为准：

```yaml
---
title: 文章标题              # 【必填】字符串
published: 2026-05-30        # 【必填】发布日期 (YYYY-MM-DD)
updated: 2026-05-31          # 可选，更新日期
description: 文章摘要         # 可选，用于列表/SEO/分享卡片
image: ./cover.jpg           # 可选，封面图（见第 4 节）；填 "api" 用随机封面
tags: [标签1, 标签2]          # 可选，数组
category: 技术分享            # 可选，单个分类字符串（注意：不是数组！）
draft: false                 # 草稿，true = 不发布（见第 5 节）
pinned: false                # 置顶到列表顶部
unlisted: false              # 详情页正常，但不出现在列表/归档/RSS/分类/标签（见第 6 节）
comment: true                # 是否显示评论区（giscus）
lang: ''                     # 文章语言，留空跟随站点默认
author: ''                   # 可选，作者署名
sourceLink: ''               # 可选，原文/来源链接
licenseName: ''              # 可选，版权协议名
licenseUrl: ''               # 可选，版权协议链接
password: ''                 # 可选，给文章加访问密码（见第 7 节）
passwordHint: ''             # 可选，密码提示
---
```

> ⚠️ `prevTitle` / `prevSlug` / `nextTitle` / `nextSlug` 是内部字段，由系统生成，**不要手动填写**。

**最小可用 frontmatter**（只有 `title` 和 `published` 是必填）：

```yaml
---
title: 群晖配置 Flexget 套件
published: 2025-12-04
description: 群晖的 Flexget 套件安装配置教程
tags: ["工具", "推荐"]
category: "技术分享"
draft: false
---
```

---

## 4. 图片管理

正文图片放在 `public/posts/<slug>/` 下，在 Markdown 中用**绝对路径**引用：

```
public/posts/DSM-Flexget/img-001.jpg
```

```markdown
![群晖套件中心](/posts/DSM-Flexget/img-001.jpg)
```

- 路径以 `/` 开头，对应 `public/` 根目录（不要写成 `./` 或带 `public/`）。
- 封面图 `image`：
  - 站内相对图：`image: ./cover.jpg`（放在文章同级）；
  - 随机封面：`image: "api"`；
  - 不要封面：留空 `image: ''`。
- 习惯命名 `img-001.jpg`、`img-002.png`，按文章分目录，便于管理。

---

## 5. 草稿、置顶与更新

- **草稿**：`draft: true` → 不会被发布（不进列表、不生成页面）。完稿后改 `false`。
- **置顶**：`pinned: true` → 在文章列表中排到最前。
- **更新时间**：内容有较大修订时填 `updated: YYYY-MM-DD`，详情页会显示更新日期。

---

## 6. 特殊文章类型

### 6.1 隐藏文章（unlisted）—— 用于交易日志按月归集

`unlisted: true` 的文章：详情页**正常生成可访问**，但**不出现**在首页、归档、RSS、分类、标签等任何列表中。
用于「父索引页统一归集」的子页面。本站交易日志即采用此模式：

```
src/content/posts/trading-log/index.md            ← 父索引（pinned，列出各月链接）
src/content/posts/trading-log-2026-05/index.md    ← 月度日志（unlisted: true）
src/content/posts/trading-log-2026-04/index.md    ← 月度日志（unlisted: true）
```

父索引 frontmatter 示例：

```yaml
---
title: "SMA 实盘交易日志"
published: 2026-03-01
updated: 2026-05-29
tags: ["SMA", "实盘交易", "交易日志"]
category: "量化交易"
pinned: true
draft: false
---
```

月度日志 frontmatter 示例（多了 `unlisted: true`）：

```yaml
---
title: "SMA实盘交易日志 — 2026年05月"
published: 2026-05-01
tags: ["SMA", "实盘交易", "交易日志"]
category: "量化交易"
draft: false
unlisted: true
---
```

> 新增一个月：在 `trading-log-YYYY-MM/index.md` 建月度日志（`unlisted: true`），
> 并在父索引 `trading-log/index.md` 的「月度日志」列表里加一行链接。

### 6.2 研究报告

按 `src/content/posts/sma-strategy-optimization-report-YYYY_MMDD.md` 命名，普通文章模式即可。

---

## 7. 文章加密（可选）

给单篇文章设访问密码：

```yaml
password: "your-secret"
passwordHint: "提示：项目内部约定的口令"
```

访问者需输入密码才能看正文。`passwordHint` 会显示在密码框旁。

---

## 8. 发布流程

本站由 **Cloudflare Pages 直接构建 `main` 分支**（见 README）。发布即「提交并推送到 main」：

```bash
git add src/content/posts/ public/posts/
git commit -m "post: 新增《文章标题》"
git push
```

推送后 Cloudflare 自动构建部署，无需手动跑 build。
发布前可本地自检：

```bash
pnpm check      # 类型 / 内容 schema 校验，能提前发现 frontmatter 错误
pnpm dev        # 本地预览效果
```

---

## 9. 常用命令速查

| 命令 | 作用 |
|------|------|
| `pnpm new-post <name>` | 创建新文章（自动填发布日期） |
| `pnpm dev` | 本地开发预览（http://localhost:4321） |
| `pnpm check` | 校验内容 schema / 类型错误 |
| `pnpm build` | 构建到 `./dist/` |
| `pnpm preview` | 预览已构建产物 |
| `pnpm format` | Biome 格式化 |

---

## 10. 注意事项

- `category` 是**单个字符串**，不是数组（`tags` 才是数组）。
- 文件名（slug）用英文小写连字符；中文标题放 `title`。
- 图片引用用 `/posts/<slug>/xxx.jpg` 绝对路径，文件放 `public/posts/<slug>/`。
- `draft: true` 不发布；`unlisted: true` 可访问但不进列表。
- 必填字段只有 `title` 和 `published`，缺失会导致 `pnpm check` / 构建失败。
- 评论默认开启（giscus），单篇关闭用 `comment: false`。
