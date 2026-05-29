# 更新与注意事项

本文件记录博客的重要更新与运维注意事项，最新的更新在最上方。

---

## 2026-05-30 · 执行迁移待办

承接上一条迁移，集中处理了遗留待办：

### 评论系统（giscus）

- 通过 GitHub API 开启了仓库 `JokerLJZ/Blog` 的 Discussions。
- 查询并填入真实 ID：`repoId = R_kgDOSpjRaw`，`General` 分类 `categoryId = DIC_kwDOSpjRa84C-F_H`。
- `commentConfig.ts` 的 `type` 已改为 `giscus`，`mapping` 为 `pathname`。
- **仍需手动完成**：到 <https://github.com/apps/giscus> 安装 giscus App 并授权 `JokerLJZ/Blog` 仓库，否则评论区不会加载。

### 头像与 Favicon

- `profileConfig.ts` 的 `avatar` 改为 `/logo.svg`。
- `public/favicon/favicon.ico` 替换为旧主题保留下来的图标。
- 用 `sharp` 从 `logo.svg` 重新生成了 8 个 PNG 变体：`favicon-{light,dark}-{32,128,180,192}.png`。

### 音乐播放器（关闭）

- `musicConfig.ts` 的 `showInNavbar` 设为 `false`。
- `sidebarConfig.ts` 中两个 `music` 组件的 `enable` 设为 `false`。
- 清空主题自带的网易云歌单（`meting.id`）与本地歌单（`local.playlist`），并删除演示音频 `public/assets/music/`。
- 说明：播放器引擎 `MusicManager` 仍随主题全局挂载，但只有在播放器 UI 触发时才会加载歌单；UI 全部关闭后它不会发起任何网络请求，页面也无音乐内容。

### 页面开关

- 启用 **留言板**（`pages.guestbook = true`，复用 giscus）。
- 启用 **相册**（`pages.gallery = true`）：清空 `galleryConfig.ts` 的演示相册（`firefly-2026`、`encrypted-test`），删除 `public/gallery/` 下的演示图，目前为空白相册页，待填入自己的图片。
- 友链 / 赞助 / 番组计划维持关闭（需各自内容 / Bangumi ID）。

### 看板娘 / 特效

- 经确认，`pioConfig.ts`（Live2D 流萤看板娘）与 `effectsConfig.ts`（樱花特效）默认即为关闭（`enable: false`），无需改动。

---

## 2026-05-29 · 切换至 Firefly 主题

### 概述

博客主题由初始的「Modern Personal Blog」整体更换为 [Firefly](https://github.com/CuteLeaf/Firefly)（基于 [Fuwari](https://github.com/saicaca/fuwari) 二次开发）。这是一次完整的技术栈替换，并已套用本站的身份信息。

### 技术栈对比

| 项目       | 旧主题（Modern Personal Blog） | 新主题（Firefly）            |
|:-----------|:-------------------------------|:-----------------------------|
| 框架       | Astro 4                        | Astro 6                      |
| UI 框架    | React 18                       | Svelte 5                     |
| 样式       | Tailwind CSS 3                 | Tailwind CSS 4               |
| 包管理器   | npm                            | pnpm ≥ 9（强制）             |
| Node 要求  | —                              | ≥ 22                         |
| 搜索       | Fuse.js                        | Pagefind                     |
| 内容目录   | `src/content/blog/`            | `src/content/posts/`         |

### 已完成的定制

- **站点信息**（`src/config/siteConfig.ts`）
  - 标题 `火柴人的Blog`、副标题、描述、`site_url = https://blog.stickman.life`、关键词
  - 导航栏 Logo 改为 `public/logo.svg`、标题改为本站名
  - `siteStartDate` 设为 `2025-05-28`
  - `bangumi.userId` 置空
  - `pages` 中 `friends / sponsor / guestbook / bangumi / gallery` 全部关闭
- **个人资料**（`src/config/profileConfig.ts`）
  - 名字、个性签名
  - 社交链接：GitHub（`JokerLJZ`）、Email（`Stickman.life@outlook.com`），移除了 QQ
- **评论**（`src/config/commentConfig.ts`）
  - giscus 仓库设为 `JokerLJZ/Blog`、`mapping = pathname`
  - `repoId` / `categoryId` 暂为占位符，`type` 仍为 `none`
- **导航栏**（`src/config/navBarConfig.ts`）：自定义「链接」菜单改为本站 GitHub，移除 Gitee / QQ 群
- **公告**（`src/config/announcementConfig.ts`）：改为本站欢迎语
- **关于页**（`src/content/spec/about.md`）：改为本站介绍，保留对 Firefly / Fuwari 的署名
- **文章**：保留并转换首篇 `Hello World`（`src/content/posts/hello-world.md`），移除全部主题自带演示文章及配图
- **CI / 部署**：`.github/workflows/*.yml` 触发分支由 `master` → `main`
- **清理**：移除 `FUNDING.yml`、`.github/ISSUE_TEMPLATE/`、`pull_request_template.md`、`CONTRIBUTING.md`、多语言项目 README（`README.en.md` 等）与 `docs/images/` 宣传图

### 待办清单（多数已于 2026-05-30 完成，详见本文件顶部）

- [x] **评论**：已填入真实 `repoId` / `categoryId` 并启用 giscus（仅剩手动安装 giscus App）
- [x] **头像**：已改为 `/logo.svg`
- [x] **Favicon**：已替换并重新生成 PNG 变体
- [x] **音乐播放器**：已关闭并清空演示歌单
- [x] **看板娘 / 特效**：确认默认即关闭，无需改动
- [x] **留言板**：已启用
- [x] **相册**：已启用并清空演示数据（待填入自己的图片）
- [ ] **友链**：`src/config/friendsConfig.ts` 配好后在 `pages.friends` 开启
- [ ] **赞助**：`src/config/sponsorConfig.ts` 换成自己的收款码后在 `pages.sponsor` 开启
- [ ] **番组计划**：填 `siteConfig.ts` 的 `bangumi.userId` 后在 `pages.bangumi` 开启

### 注意事项

1. **运行环境**：必须 Node.js ≥ 22、pnpm ≥ 9。项目用 `preinstall: only-allow pnpm` 强制 pnpm，npm / yarn 会被拦截。
2. **Frontmatter 字段变化**（迁移旧文章时注意）：
   - `pubDate` → `published`
   - `categories: [...]`（数组）→ `category: "..."`（字符串）
   - `featured` → `pinned`
3. **构建命令**：务必用 `pnpm run build`。它依次执行 `generate-icons.js`、`generate-lqips.ts`、`astro build`、`pagefind --site dist`；单独 `astro build` 会缺图标与搜索索引。
4. **本地构建 `EACCES` 报错**：`pnpm run build` 中的 `npx tsx` 会用到 npm 缓存（`~/.npm`）。若该目录含 root 拥有的文件会报 `EACCES`，可：
   - 永久修复：`sudo chown -R $(id -u):$(id -g) ~/.npm`，或
   - 临时绕过：`npm_config_cache=/tmp/npm-cache pnpm run build`
5. **关闭的页面行为**：被关闭的页面（如 `/friends/`、`/gallery/`）会构建为 `noindex` 并跳转 `/404/` 的占位页，不会泄露主题自带的演示内容。
6. **版权与署名**：Firefly 与 Fuwari 均为 MIT，已在 `LICENSE` 保留版权声明；复用 Firefly 特色组件请注明来源。

### 回滚

本次为整仓替换，如需回到旧主题：

```bash
git log --oneline          # 找到切换前的提交
git revert <commit>        # 或 git checkout <commit> -- .
```
