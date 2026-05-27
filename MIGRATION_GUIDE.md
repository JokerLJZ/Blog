# Notion Blog 迁移至 Cloudflare Pages + Astro 完整指南

> 本指南将帮助你将 Notion 博客迁移为基于 Astro 框架的静态博客，使用 [Modern Personal Blog](https://github.com/copyboy/product_whoami) 主题，并部署到 Cloudflare Pages。

---

## 目录

1. [环境准备](#1-环境准备)
2. [初始化项目](#2-初始化项目)
3. [个性化配置](#3-个性化配置)
4. [从 Notion 迁移内容](#4-从-notion-迁移内容)
5. [本地开发与测试](#5-本地开发与测试)
6. [推送至 GitHub](#6-推送至-github)
7. [部署到 Cloudflare Pages](#7-部署到-cloudflare-pages)
8. [绑定自定义域名](#8-绑定自定义域名)
9. [部署后验证](#9-部署后验证)
10. [日常写作流程](#10-日常写作流程)
11. [常见问题排查](#11-常见问题排查)

---

## 1. 环境准备

### 1.1 必需软件

| 工具 | 最低版本 | 检查命令 | 安装地址 |
|------|---------|---------|---------|
| Node.js | 18.x（推荐 20.x LTS） | `node --version` | https://nodejs.org/ |
| npm | 随 Node.js 安装 | `npm --version` | — |
| Git | 任意现代版本 | `git --version` | https://git-scm.com/ |

### 1.2 必需账号

- [x] **GitHub 账号** — 用于托管代码仓库
- [x] **Cloudflare 账号** — 用于部署和域名管理（你已有且 DNS 已托管在 Cloudflare）

### 1.3 推荐工具

- **VS Code** — 推荐安装 [Astro 扩展](https://marketplace.visualstudio.com/items?itemName=astro-build.astro-vscode)，提供语法高亮和智能提示
- **浏览器** — Chrome/Edge DevTools 用于调试

---

## 2. 初始化项目

### 2.1 使用模板创建项目

打开终端，进入你的项目**父级目录**（如 `D:\GitHub`），运行：

```bash
npm create astro@latest -- --template copyboy/product_whoami#demo Blog
```

交互式提示中选择：
- **Install dependencies?** → Yes
- **Initialize a git repository?** → Yes
- **TypeScript?** → Yes（主题默认使用 TypeScript）

> **注意**：如果 `D:\GitHub\Blog` 目录已存在且非空，请先清空或删除它。

### 2.2 验证安装

```bash
cd D:\GitHub\Blog
npm run dev
```

浏览器访问 `http://localhost:4321`，应该能看到主题的演示页面。确认无误后 `Ctrl+C` 停止开发服务器。

### 2.3 了解项目结构

```
Blog/
├── astro.config.mjs          # Astro 框架配置
├── tailwind.config.js         # Tailwind CSS 配置
├── tsconfig.json              # TypeScript 配置
├── package.json               # 依赖与脚本
├── public/                    # 静态资源（favicon、图片等）
│   ├── favicon.ico
│   └── ...
└── src/
    ├── config/
    │   └── site.json          # ★ 网站核心配置（标题、作者、社交链接等）
    ├── content/
    │   ├── config.ts           # 内容集合 Schema 定义
    │   ├── blog/               # ★ 博客文章存放目录（MDX 格式）
    │   └── projects/           # 项目展示目录
    ├── components/             # UI 组件
    ├── layouts/                # 页面布局模板
    ├── pages/                  # 页面路由
    │   └── about.astro         # ★ 关于页面（需要自定义）
    ├── styles/                 # 全局样式
    └── utils/                  # 工具函数
```

标注 ★ 的文件是你需要重点修改的。

---

## 3. 个性化配置

### 3.1 修改网站配置 `src/config/site.json`

这是整个博客最核心的配置文件。打开后将所有字段替换为你自己的信息：

```json
{
  "site": {
    "title": "你的博客名称",
    "description": "你的博客描述，用于 SEO 和社交分享",
    "url": "https://你的域名.com",
    "author": {
      "name": "你的名字",
      "email": "your@email.com",
      "bio": "一句话简介"
    },
    "social": {
      "github": "https://github.com/你的用户名",
      "twitter": "",
      "linkedin": ""
    }
  }
}
```

> **提示**：保留 JSON 文件中的字段结构，只替换值。如果原文件有更多字段（如 Giscus 评论配置、feature toggles），根据需要修改或保持默认值。

### 3.2 修改关于页面 `src/pages/about.astro`

打开此文件，保留页面布局结构（`ThreeColumnLayout` 等 import 和组件包裹），替换所有个人信息内容：

- 个人简介
- 技能列表
- 工作经历
- 联系方式

### 3.3 替换静态资源

替换 `public/` 目录下的以下文件：

| 文件 | 用途 | 建议尺寸 |
|------|------|---------|
| `favicon.ico` | 浏览器标签页图标 | 32x32 或 16x16 |
| `logo.svg`（如果有） | 网站 Logo | 根据主题设计调整 |

可以使用 [favicon.io](https://favicon.io/) 在线生成 favicon。

### 3.4 清除示例内容

删除主题自带的所有示例文章和项目：

```bash
# 删除示例博客文章
rm -rf src/content/blog/*

# 删除示例项目（如果不需要项目展示功能）
rm -rf src/content/projects/*
```

---

## 4. 从 Notion 迁移内容

### 4.1 从 Notion 导出文章

#### 方法 A：逐篇导出（推荐，内容少于 20 篇时）

1. 在 Notion 中打开一篇文章
2. 点击右上角 `···` 菜单
3. 选择 **Export** → 格式选 **Markdown & CSV**
4. 下载 zip 文件并解压

#### 方法 B：批量导出

1. Notion 左侧边栏 → **Settings & members**
2. **Settings** → 滚动到底部 → **Export all workspace content**
3. 格式选 **Markdown & CSV**
4. 下载并解压

### 4.2 处理导出文件

Notion 导出的文件结构通常是：

```
Export/
├── 文章标题 abc123def.md
├── 文章标题 abc123def/
│   ├── image1.png
│   └── image2.jpg
└── 另一篇文章 xyz789.md
```

你需要对每篇文章进行以下处理：

### 4.3 文件转换步骤（每篇文章重复此流程）

#### 步骤 1：重命名文件

将文件名改为英文 kebab-case 格式，扩展名改为 `.mdx`：

```
# 原始文件名
我的第一篇博客 abc123def.md

# 改为
my-first-blog-post.mdx
```

> 文件名将直接成为 URL 路径。例如 `my-first-blog-post.mdx` 的访问地址为 `https://你的域名.com/blog/my-first-blog-post`

#### 步骤 2：添加 Frontmatter

在文件**最顶部**添加 YAML frontmatter 元数据块：

```yaml
---
title: "我的第一篇博客"
description: "这篇文章介绍了……（150 字以内的摘要，用于 SEO 和文章列表展示）"
pubDate: 2024-01-15
tags: ["标签1", "标签2"]
categories: ["分类名"]
draft: false
featured: false
---

正文内容从这里开始...
```

**字段说明：**

| 字段 | 必填 | 类型 | 说明 |
|------|------|------|------|
| `title` | 是 | 字符串 | 文章标题 |
| `description` | 是 | 字符串 | 文章摘要（建议 150 字以内） |
| `pubDate` | 是 | 日期 | 发布日期，格式 `YYYY-MM-DD` |
| `tags` | 否 | 字符串数组 | 标签列表 |
| `categories` | 否 | 字符串数组 | 分类列表 |
| `draft` | 否 | 布尔值 | `true` 表示草稿（不会在生产环境显示） |
| `featured` | 否 | 布尔值 | `true` 表示置顶/精选文章 |
| `heroImage` | 否 | 字符串 | 封面图片路径 |
| `updatedDate` | 否 | 日期 | 最后更新日期 |

#### 步骤 3：处理图片

1. 在 `public/` 目录下创建图片文件夹：

```bash
mkdir -p public/images/blog
```

2. 将 Notion 导出的图片复制到 `public/images/blog/`
3. 更新文章中的图片路径：

```markdown
# Notion 导出的原始路径
![图片描述](文章标题%20abc123def/image1.png)

# 改为
![图片描述](/images/blog/image1.png)
```

> **建议**：为避免图片文件名冲突，可以按文章添加前缀，如 `my-first-post-image1.png`

#### 步骤 4：处理 MDX 特殊字符

MDX 比普通 Markdown 更严格。以下字符在非代码块区域需要特殊处理：

| 字符 | 问题 | 解决方案 |
|------|------|---------|
| `{` 和 `}` | MDX 会将其解析为 JSX 表达式 | 改为 `\{` 和 `\}` 或包裹在行内代码中 `` `{}` `` |
| `<` | MDX 会将其解析为 HTML/JSX 标签 | 改为 `&lt;` 或包裹在行内代码中 `` `<` `` |

**示例**：

```markdown
# 错误 ❌（MDX 会报错）
如果 a < b 且 {value} 不为空

# 正确 ✅
如果 a &lt; b 且 \{value\} 不为空
```

#### 步骤 5：修复内部链接

如果文章之间有互相引用的链接：

```markdown
# Notion 导出的链接
[参考文章](另一篇文章%20xyz789.md)

# 改为（使用目标文章的 MDX 文件名，去掉扩展名）
[参考文章](/blog/another-article-slug)
```

### 4.4 放置文件

将所有处理好的 `.mdx` 文件放入 `src/content/blog/` 目录：

```
src/content/blog/
├── my-first-blog-post.mdx
├── learning-javascript.mdx
├── cloudflare-deployment-guide.mdx
└── ...
```

### 4.5 迁移检查清单

对每篇文章确认：

- [ ] 文件名：英文 kebab-case，`.mdx` 扩展名
- [ ] Frontmatter：包含 `title`、`description`、`pubDate` 三个必填字段
- [ ] 日期格式：`YYYY-MM-DD`（如 `2024-01-15`）
- [ ] 图片：已复制到 `public/images/blog/`，路径已更新
- [ ] 特殊字符：`{}`、`<` 已正确转义
- [ ] 内部链接：已更新为新的 URL 格式

---

## 5. 本地开发与测试

### 5.1 启动开发服务器

```bash
npm run dev
```

访问 `http://localhost:4321`，开始测试。

### 5.2 测试检查清单

逐项验证以下功能：

**核心功能：**
- [ ] 首页正确显示文章列表
- [ ] 文章页面正常渲染（标题、正文、代码高亮、目录）
- [ ] 分类页面正常工作
- [ ] 标签页面正常工作
- [ ] 搜索功能可用
- [ ] 关于页面显示正确的个人信息

**视觉与交互：**
- [ ] 深色/浅色模式切换正常
- [ ] 移动端响应式布局正常（使用浏览器开发者工具模拟）
- [ ] 图片正常显示

**SEO 与元数据：**
- [ ] RSS Feed 可访问：`http://localhost:4321/rss.xml`
- [ ] Sitemap 可访问：`http://localhost:4321/sitemap-index.xml`

### 5.3 生产构建测试

```bash
# 构建生产版本
npm run build

# 本地预览生产版本
npm run preview
```

访问 `http://localhost:4321` 验证生产版本是否正常。

### 5.4 常见构建错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `frontmatter validation failed` | Frontmatter 字段类型不对 | 检查日期是否为 `YYYY-MM-DD` 格式，数组是否用 `[]` 包裹 |
| `Unexpected token` in MDX | MDX 解析错误 | 检查 `{}`、`<` 等特殊字符是否已转义 |
| `Image not found` / 404 | 图片路径错误 | 确认图片在 `public/` 目录下，路径以 `/` 开头 |

---

## 6. 推送至 GitHub

### 6.1 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`Blog`（或你喜欢的名字）
3. 可见性：Public 或 Private 均可（Cloudflare Pages 支持私有仓库）
4. **不要**勾选 "Add a README file"（项目已有内容）
5. 点击 **Create repository**

### 6.2 推送代码

```bash
cd D:\GitHub\Blog

# 添加所有文件到暂存区
git add .

# 创建初始提交
git commit -m "feat: initial blog setup with Modern Personal Blog theme and migrated content"

# 关联远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/Blog.git

# 推送到 main 分支
git branch -M main
git push -u origin main
```

---

## 7. 部署到 Cloudflare Pages

### 7.1 创建 Pages 项目

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. 左侧导航栏选择 **Workers & Pages**
3. 点击 **Create application**
4. 选择 **Pages** 标签页
5. 点击 **Connect to Git**

### 7.2 授权并选择仓库

1. 选择 **GitHub**，授权 Cloudflare 访问你的 GitHub 账号
2. 在仓库列表中选择刚才创建的 `Blog` 仓库
3. 点击 **Begin setup**

### 7.3 配置构建设置

| 设置项 | 值 |
|-------|-----|
| Project name | `blog`（或你喜欢的名字，这也是 `*.pages.dev` 的子域名） |
| Production branch | `main` |
| Framework preset | `Astro` |
| Build command | `npm run build` |
| Build output directory | `dist` |

### 7.4 添加环境变量

在构建设置页面下方找到 **Environment variables** 区域，添加：

| 变量名 | 值 | 说明 |
|-------|-----|------|
| `NODE_VERSION` | `20` | 指定 Node.js 版本，确保兼容性 |

### 7.5 开始部署

1. 点击 **Save and Deploy**
2. 等待构建完成（首次约 1-3 分钟）
3. 部署成功后，你会获得一个 `https://blog-xxx.pages.dev` 的临时地址
4. 点击该地址验证博客是否正常显示

> **如果构建失败**：查看构建日志中的错误信息，通常是 Node.js 版本问题或构建命令错误。确认环境变量 `NODE_VERSION=20` 已正确设置。

---

## 8. 绑定自定义域名

由于你的域名 DNS 已经托管在 Cloudflare，绑定过程非常简单。

### 8.1 添加自定义域名

1. 在 Cloudflare Dashboard 中，进入你的 Pages 项目
2. 点击 **Custom domains** 标签页
3. 点击 **Set up a custom domain**
4. 输入你的域名（如 `blog.yourdomain.com` 或 `yourdomain.com`）
5. 点击 **Continue**

### 8.2 自动 DNS 配置

因为 DNS 已在 Cloudflare 上，系统会**自动创建**所需的 CNAME 记录，你不需要手动配置 DNS。

1. 确认显示的 DNS 记录信息
2. 点击 **Activate domain**
3. SSL 证书会自动申请和配置（通常几分钟内完成）

### 8.3 更新网站配置

将 `src/config/site.json` 中的 `url` 字段更新为你的自定义域名：

```json
{
  "site": {
    "url": "https://你的域名.com"
  }
}
```

提交并推送更改（Cloudflare Pages 会自动重新部署）：

```bash
git add src/config/site.json
git commit -m "chore: update site URL to custom domain"
git push
```

### 8.4 验证域名

- 访问 `https://你的域名.com`，确认博客正常显示
- 确认浏览器地址栏显示 🔒 锁图标（HTTPS 已生效）
- 如果需要 www 跳转，在 Cloudflare DNS 中添加 www 的 CNAME 记录指向你的 Pages 项目

---

## 9. 部署后验证

### 9.1 功能验证

- [ ] 首页加载正常，文章列表完整
- [ ] 每篇文章都能正常打开和阅读
- [ ] 图片正常显示
- [ ] 搜索功能可用
- [ ] 深色/浅色模式正常
- [ ] 移动端显示正常
- [ ] RSS Feed 可访问：`https://你的域名.com/rss.xml`

### 9.2 SEO 验证

1. 使用 [opengraph.xyz](https://www.opengraph.xyz/) 测试社交分享卡片
2. 将 Sitemap 提交至搜索引擎：
   - [Google Search Console](https://search.google.com/search-console/) — 添加站点 → 提交 `https://你的域名.com/sitemap-index.xml`
   - [Bing Webmaster Tools](https://www.bing.com/webmasters/) — 同样操作

### 9.3 性能测试

使用 [PageSpeed Insights](https://pagespeed.web.dev/) 测试性能分数，该主题目标 90+ 分。

---

## 10. 日常写作流程

部署完成后，发布新文章只需以下步骤：

### 10.1 创建新文章

在 `src/content/blog/` 目录下创建新的 `.mdx` 文件：

```bash
# 示例：创建一篇新文章
touch src/content/blog/my-new-article.mdx
```

### 10.2 编写内容

```yaml
---
title: "文章标题"
description: "文章摘要"
pubDate: 2025-05-28
tags: ["标签"]
categories: ["分类"]
draft: false
---

正文内容...

## 二级标题

正文内容...

### 三级标题

正文内容...

```javascript
// 代码会自动高亮
console.log('Hello World');
```　

![图片描述](/images/blog/my-image.png)
```

### 10.3 本地预览

```bash
npm run dev
```

在浏览器中检查文章渲染效果。

### 10.4 发布

```bash
git add .
git commit -m "post: 文章标题"
git push
```

推送后 Cloudflare Pages 会在 1-2 分钟内自动重新部署。

### 10.5 草稿功能

如果文章还未完成，设置 `draft: true`：

```yaml
---
title: "未完成的文章"
draft: true
---
```

草稿在开发环境（`npm run dev`）中可见，但**不会出现在生产版本**中。

---

## 11. 常见问题排查

### Q: 构建时报 "frontmatter validation failed"

**原因**：Frontmatter 字段不符合 `src/content/config.ts` 中定义的 Schema。

**排查**：
- `pubDate` 格式必须是 `YYYY-MM-DD`（如 `2024-01-15`），不能加引号包裹
- `tags` 和 `categories` 必须是数组格式 `["tag1", "tag2"]`
- `draft` 和 `featured` 必须是布尔值 `true` 或 `false`

### Q: MDX 文件解析报错

**原因**：MDX 比 Markdown 更严格，某些字符需要转义。

**排查**：
- 检查文中是否有未转义的 `{}`，需改为 `\{\}`
- 检查文中是否有非代码块中的 `<`，需改为 `&lt;`
- 检查是否有不完整的 HTML 标签

### Q: 图片 404

**排查**：
- 确认图片文件在 `public/images/blog/` 目录下
- 确认 MDX 中的路径以 `/` 开头（如 `/images/blog/photo.png`）
- 注意文件名大小写敏感

### Q: Cloudflare Pages 构建失败

**排查**：
- 检查是否设置了环境变量 `NODE_VERSION=20`
- 查看 Cloudflare 构建日志中的具体错误信息
- 在本地先运行 `npm run build` 确认无错误

### Q: 自定义域名无法访问

**排查**：
- 在 Cloudflare Pages 项目的 Custom domains 页面查看状态
- 确认 DNS 记录已正确创建（通常是自动的）
- SSL 证书可能需要几分钟才能生效，稍等再试
- 清除浏览器缓存后重试

### Q: 想要使用不同的代码高亮主题

修改 `astro.config.mjs` 中 Shiki 的主题配置：

```javascript
// astro.config.mjs
export default defineConfig({
  markdown: {
    shikiConfig: {
      theme: 'github-dark' // 可选: dracula, nord, one-dark-pro 等
    }
  }
});
```

### Q: 如何添加评论功能

该主题支持 [Giscus](https://giscus.app/)（基于 GitHub Discussions 的评论系统）。在 `src/config/site.json` 中配置 Giscus 相关字段。具体步骤：

1. 访问 https://giscus.app/ 配置你的仓库
2. 获取 `repo`、`repoId`、`category`、`categoryId` 等参数
3. 填入 `site.json` 对应字段

---

## 附录 A：Frontmatter 快速模板

复制以下模板到每篇新文章的顶部：

```yaml
---
title: ""
description: ""
pubDate: 2025-01-01
tags: []
categories: []
draft: false
featured: false
---
```

## 附录 B：完整时间估算

| 步骤 | 预计耗时 |
|------|---------|
| 环境准备 + 项目初始化 | 15 分钟 |
| 个性化配置 | 30-60 分钟 |
| 内容迁移（~20 篇） | 2-3 小时 |
| 本地测试 | 30 分钟 |
| GitHub + Cloudflare 部署 | 20 分钟 |
| 域名配置 + 验证 | 10 分钟 |
| **总计** | **约 4-5 小时** |

## 附录 C：有用链接

- [Astro 官方文档](https://docs.astro.build/)
- [主题 GitHub 仓库](https://github.com/copyboy/product_whoami)
- [Cloudflare Pages 文档](https://developers.cloudflare.com/pages/)
- [MDX 语法参考](https://mdxjs.com/docs/what-is-mdx/)
- [Tailwind CSS 文档](https://tailwindcss.com/docs)
