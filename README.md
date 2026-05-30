# 火柴人的Blog

> 想的多，动得少，拥有超强的质疑精神。动漫、游戏、技术，什么玩意儿都略懂但只懂点皮毛。

个人博客，记录技术、动漫、游戏以及各种乱七八糟的想法。

- 🌐 站点地址：<https://blog.stickman.life>
- 🎨 主题：[Firefly](https://github.com/CuteLeaf/Firefly)（基于 [Fuwari](https://github.com/saicaca/fuwari) 二次开发）
- ⚙️ 技术栈：Astro 6 + Svelte 5 + Tailwind CSS 4 + pnpm
- ☁️ 部署：Cloudflare Pages

---

## 🚀 快速开始

### 环境要求

- **Node.js ≥ 22**
- **pnpm ≥ 9**（项目通过 `preinstall` 强制使用 pnpm，请勿用 npm / yarn 安装）

### 本地开发

```bash
pnpm install      # 安装依赖
pnpm dev          # 启动开发服务器，访问 http://localhost:4321
pnpm build        # 构建到 ./dist/
pnpm preview      # 本地预览构建结果
```

### 常用命令

| 命令                       | 作用                                   |
|:---------------------------|:---------------------------------------|
| `pnpm install`             | 安装依赖                               |
| `pnpm dev`                 | 在 `localhost:4321` 启动开发服务器     |
| `pnpm build`               | 构建网站到 `./dist/`                   |
| `pnpm preview`             | 本地预览已构建的网站                   |
| `pnpm check`               | 检查代码错误                           |
| `pnpm format`              | 使用 Biome 格式化代码                  |
| `pnpm new-post <filename>` | 创建新文章                             |

## 📝 写文章

文章放在 `src/content/posts/` 下（`.md` 或 `.mdx`）。Frontmatter 格式如下：

```yaml
---
title: 文章标题
published: 2025-05-28      # 发布日期
description: 文章摘要
image: ./cover.jpg         # 可选，封面图；或填 "api" 启用随机封面
tags: [标签1, 标签2]        # 数组
category: 分类              # 字符串（注意：单个分类，不是数组）
draft: false               # 草稿
pinned: false              # 置顶
comment: true              # 是否允许评论
---
```

> ⚠️ Frontmatter 字段与旧主题不同，详见下方[注意事项](#-注意事项)。

## ⚙️ 配置

所有配置集中在 `src/config/` 目录，按功能拆分：

| 文件                  | 作用                       |
|:----------------------|:---------------------------|
| `siteConfig.ts`       | 站点基础信息、布局、页面开关 |
| `profileConfig.ts`    | 个人资料、社交链接          |
| `commentConfig.ts`    | 评论系统（giscus 等）       |
| `navBarConfig.ts`     | 导航栏                      |
| `announcementConfig.ts` | 公告                      |
| `sidebarConfig.ts`    | 侧边栏小组件                |
| `musicConfig.ts`      | 音乐播放器                  |
| `pioConfig.ts`        | Live2D 看板娘               |
| `effectsConfig.ts`    | 樱花等动画特效              |
| `footerConfig.ts`     | 页脚                        |
| `friendsConfig.ts` / `galleryConfig.ts` / `sponsorConfig.ts` | 友链 / 相册 / 赞助 |

> 完整配置说明可参考 Firefly 官方文档：<https://docs-firefly.cuteleaf.cn/>

## ☁️ 部署

### Cloudflare Pages（当前使用，直接构建 `main`）

| 项目       | 值              |
|:-----------|:----------------|
| 生产分支   | `main`          |
| 构建命令   | `pnpm run build` |
| 输出目录   | `dist`          |
| 安装命令   | `pnpm install`  |
| Node 版本  | `22`（已由 `.node-version` 固定，亦可设环境变量 `NODE_VERSION=22`） |

> 必须使用 `pnpm run build`（包含 generate-icons、generate-lqips、pagefind 等步骤），不要直接用 `astro build`。
> Cloudflare 会依据 `package.json` 的 `packageManager: pnpm@9.14.4` 自动启用 pnpm（corepack）。

> ⚠️ 单一构建源：已移除原 `.github/workflows/deploy.yml`（它会把产物推到 `pages` 分支，与 Cloudflare 直接构建 `main` 冲突，导致 Cloudflare 对静态产物误跑 `npm run build` 而失败）。现仅保留 `build.yml`（CI 检查，不部署）。每次 push 到 `main`（含量化程序自动推送的交易日志）由 Cloudflare 直接构建部署。

---

## 🆕 更新记录

### 2026-05-30 · 从 Notion 迁移 + 接入量化交易日志

- **弃用 Notion**：原先经 NotionNext 发布的博客与 SMA 交易日志全部迁移到本 Astro 站点。
- **历史文章迁移**：NotionNext 数据库中的 4 篇文章 + 3 个月（2026-03/04/05）交易日志已转成 markdown 放入 `src/content/posts/`，图片下载到 `public/`。
  - `小米路由器局域网科学上网` 因正文在 Notion「同步块」中且来源页未授权 API，未能自动迁移，已标记为 `draft: true` 待手动补全。
  - 2026-04 部分交易日志图表原存于 catbox.moe，已失效的少量图片为坏链（源已丢失）。
- **交易日志自动发布**：量化程序（`quant_claude`）每日收盘后直接写 markdown 到
  `src/content/posts/trading-log-YYYY-MM/index.md`（按月一篇，当日段落置顶 upsert），
  图表存 `public/trading-log/YYYY-MM/`，并自动 `git push` 触发 Cloudflare 部署。
- **研究报告**同理写入 `src/content/posts/sma-strategy-optimization-report-YYYY_MMDD.md`。
- 一次性迁移脚本：`scripts/migrate_notion.py`（已完成迁移，可留作存档或删除）。

> ⚠️ 本仓库现由量化程序自动提交交易日志，请勿与自动 push 冲突；本地有改动时先 `git pull`。

### 2026-05-30 · 执行迁移待办

- **评论（giscus）**：已开启仓库 `JokerLJZ/Blog` 的 Discussions，填入真实 `repoId`（`R_kgDOSpjRaw`）与 `General` 分类的 `categoryId`，`type` 改为 `giscus`。**仅剩手动安装 [giscus App](https://github.com/apps/giscus) 并授权本仓库这一步。**
- **头像 / Favicon**：头像改用站点 `logo.svg`；`favicon.ico` 换成旧主题保留的图标，并据此重新生成了 8 个 PNG 变体（light/dark × 32/128/180/192）。
- **音乐播放器**：已关闭（导航栏 + 双侧边栏），并清空主题自带的网易云歌单、移除演示音频文件。
- **留言板**：已启用（复用上面配好的 giscus 评论）。
- **相册**：已启用，清空了主题自带的演示相册，目前为空白页，待填入自己的图片。
- 友链 / 赞助 / 番组计划仍保持关闭（需要各自的内容 / 账号后再开启）。

### 2026-05-29 · 切换至 Firefly 主题

将博客主题由「Modern Personal Blog」（Astro 4 + React + Tailwind 3 + npm）整体更换为 [Firefly](https://github.com/CuteLeaf/Firefly)（基于 Fuwari，Astro 6 + Svelte 5 + Tailwind 4 + pnpm）。

主要变更：

- **技术栈升级**：Node 要求提升至 ≥ 22，包管理器由 npm 改为 pnpm ≥ 9。
- **套用本站身份**：站点标题/副标题/描述/URL/关键词、作者资料、社交链接（GitHub `JokerLJZ`、Email）、导航栏、关于页、公告均已替换为本站信息。
- **评论系统**：预置 giscus，仓库设为 `JokerLJZ/Blog`；待填入 `repoId` / `categoryId` 后启用。
- **暂时关闭演示页面**：随主题附带演示内容的「友链 / 赞助 / 留言板 / 番组计划 / 相册」页面已关闭（访问会跳转 404），配置好自己的内容后可在 `siteConfig.ts` 的 `pages` 中逐个开启。
- **文章迁移**：首篇 `Hello World` 已转换为 Firefly 的 frontmatter 格式保留，其余主题自带的演示文章已移除。
- **CI / 部署**：GitHub Actions 工作流触发分支由 `master` 调整为 `main`。
- **清理上游文件**：移除了 CuteLeaf 专属的 `FUNDING.yml`、Issue / PR 模板、多语言项目 README 与宣传图。

> 详细的迁移清单与待办见 [docs/CHANGELOG.md](docs/CHANGELOG.md)。

## ⚠️ 注意事项

1. **运行环境**：必须 Node.js ≥ 22、pnpm ≥ 9。项目已用 `preinstall` 强制 pnpm，使用 npm / yarn 会被拦截。
2. **Frontmatter 格式已变化**（从旧主题迁移文章时务必注意）：
   - 发布日期：`pubDate` → **`published`**
   - 分类：`categories: [...]`（数组）→ **`category: "..."`**（字符串）
   - 置顶：`featured` → **`pinned`**
3. **构建命令**：本地与平台都用 `pnpm run build`；它会先生成图标、LQIP 占位图，构建后再跑 Pagefind 索引，单独 `astro build` 会缺少这些步骤。
4. **评论仅剩最后一步**：giscus 已配好（仓库 `JokerLJZ/Blog`、`repoId`、`categoryId` 均已填入，Discussions 已开启，`type` 已为 `giscus`）。**还需手动在 <https://github.com/apps/giscus> 安装 giscus App 并授权 `JokerLJZ/Blog` 仓库**，评论才会加载。
5. **相册需要你的图片**：相册页已启用但内容为空，请在 `galleryConfig.ts` 添加相册并把图片放进 `public/gallery/<id>/`。
6. **仍关闭的页面**：`friends`（友链）/ `sponsor`（赞助）/ `bangumi`（番组计划）仍为关闭状态，配置好对应内容后在 `siteConfig.ts` 的 `pages` 开启。
7. **本地构建报 `EACCES`**：若 `npx` 因 npm 缓存权限报错（`~/.npm` 含 root 文件），执行 `sudo chown -R $(id -u):$(id -g) ~/.npm` 修复，或临时设置 `npm_config_cache=/tmp/npm-cache` 后再构建。
8. **版权与署名**：Firefly 与 Fuwari 均为 MIT 协议，已保留 `LICENSE` 中的版权声明；若复用了 Firefly 的特色组件设计或代码，请按其要求注明来源。

## 🙏 致谢与许可

- 主题：[Firefly](https://github.com/CuteLeaf/Firefly) © 2025 [CuteLeaf](https://github.com/CuteLeaf)
- 原始模板：[Fuwari](https://github.com/saicaca/fuwari) © 2024 [saicaca](https://github.com/saicaca)

本项目遵循 [MIT License](./LICENSE)，详见 `LICENSE` 文件。
