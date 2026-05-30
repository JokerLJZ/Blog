# -*- coding: utf-8 -*-
"""
一次性迁移脚本：把 NotionNext 博客 + SMA 交易日志从 Notion 迁移到 Astro。

- 普通文章 -> src/content/posts/<slug>.md
- 交易日志月度页 -> src/content/posts/trading-log-2026-XX/index.md
- 正文/图表图片下载到 public/posts/<slug>/ 或 public/trading-log/2026-XX/

仅用标准库（urllib），避免依赖问题。在 Blog 仓库根目录运行：
    python scripts/migrate_notion.py
"""
import json
import os
import re
import ssl
import sys
import time
import urllib.request
import urllib.error

_SSL_UNVERIFIED = ssl._create_unverified_context()

# 一次性迁移脚本：运行前请先设置环境变量 NOTION_API_KEY
NOTION_KEY = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "src", "content", "posts")
PUBLIC_DIR = os.path.join(ROOT, "public")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
}

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(str(msg))


# ----------------------------------------------------------------------
# Notion API
# ----------------------------------------------------------------------
def _request(method, url, data=None):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    for attempt in range(4):
        try:
            ctx = None if attempt == 0 else _SSL_UNVERIFIED
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "ignore")[:300]
            log(f"  [HTTP {e.code}] {url}\n    {txt}")
            if e.code == 429 and attempt < 3:
                time.sleep(3 * (attempt + 1))
                continue
            return None
        except Exception as e:
            log(f"  [ERR] {url} {e}")
            if attempt < 3:
                time.sleep(2)
                continue
            return None
    return None


def get_children(block_id):
    """获取一个 block/page 的全部子块（自动翻页）。"""
    results = []
    cursor = None
    while True:
        url = f"{API}/blocks/{block_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        data = _request("GET", url)
        if not data:
            break
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return results


def query_database(db_id):
    results = []
    cursor = None
    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        data = _request("POST", f"{API}/databases/{db_id}/query", payload)
        if not data:
            break
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return results


# ----------------------------------------------------------------------
# 图片下载
# ----------------------------------------------------------------------
_img_counter = {}
def download_image(url, dest_subdir, public_prefix):
    """下载图片到 public/<dest_subdir>/，返回站点绝对路径 /<public_prefix>/<name>。失败返回 None。"""
    abs_dir = os.path.join(PUBLIC_DIR, *dest_subdir.split("/"))
    os.makedirs(abs_dir, exist_ok=True)
    # 推断扩展名
    clean = url.split("?")[0]
    ext = os.path.splitext(clean)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        ext = ".png"
    key = dest_subdir
    _img_counter[key] = _img_counter.get(key, 0) + 1
    name = f"img-{_img_counter[key]:03d}{ext}"
    abs_path = os.path.join(abs_dir, name)
    site_path = f"/{public_prefix}/{name}"
    # 幂等：已下载过则跳过（保持编号一致）
    if os.path.exists(abs_path) and os.path.getsize(abs_path) >= 100:
        return site_path
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for ctx in (None, _SSL_UNVERIFIED):
        try:
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                content = resp.read()
            if len(content) < 100:
                log(f"    [img too small, skip] {url}")
                return None
            with open(abs_path, "wb") as f:
                f.write(content)
            log(f"    [img saved] {name} <- {url[:70]}")
            return site_path
        except urllib.error.HTTPError as e:
            log(f"    [img FAIL] {url[:70]} : HTTP {e.code}")
            return None
        except Exception as e:
            if ctx is None:
                continue  # 重试用无验证 SSL 上下文
            log(f"    [img FAIL] {url[:70]} : {e}")
            return None
    return None


# ----------------------------------------------------------------------
# rich_text -> markdown
# ----------------------------------------------------------------------
def rich_to_md(rich):
    out = []
    for r in rich or []:
        t = r.get("plain_text", "")
        if not t and r.get("type") == "equation":
            t = r.get("equation", {}).get("expression", "")
            out.append(f"${t}$")
            continue
        ann = r.get("annotations", {})
        href = r.get("href")
        if ann.get("code"):
            t = f"`{t}`"
        else:
            if ann.get("bold"):
                t = f"**{t}**"
            if ann.get("italic"):
                t = f"*{t}*"
            if ann.get("strikethrough"):
                t = f"~~{t}~~"
        if href:
            t = f"[{t}]({href})"
        out.append(t)
    return "".join(out)


# ----------------------------------------------------------------------
# blocks -> markdown
# ----------------------------------------------------------------------
def blocks_to_md(blocks, img_subdir, img_prefix, depth=0):
    lines = []
    indent = "  " * depth
    i = 0
    while i < len(blocks):
        b = blocks[i]
        bt = b.get("type")
        data = b.get(bt, {})

        if bt == "paragraph":
            txt = rich_to_md(data.get("rich_text"))
            lines.append(indent + txt if txt else "")
        elif bt in ("heading_1", "heading_2", "heading_3"):
            level = {"heading_1": "#", "heading_2": "##", "heading_3": "###"}[bt]
            lines.append(f"{level} {rich_to_md(data.get('rich_text'))}")
            lines.append("")
        elif bt == "bulleted_list_item":
            lines.append(f"{indent}- {rich_to_md(data.get('rich_text'))}")
            if b.get("has_children"):
                child = get_children(b["id"])
                lines.append(blocks_to_md(child, img_subdir, img_prefix, depth + 1))
        elif bt == "numbered_list_item":
            lines.append(f"{indent}1. {rich_to_md(data.get('rich_text'))}")
            if b.get("has_children"):
                child = get_children(b["id"])
                lines.append(blocks_to_md(child, img_subdir, img_prefix, depth + 1))
        elif bt == "to_do":
            checked = "x" if data.get("checked") else " "
            lines.append(f"{indent}- [{checked}] {rich_to_md(data.get('rich_text'))}")
        elif bt == "quote":
            lines.append(f"> {rich_to_md(data.get('rich_text'))}")
            lines.append("")
        elif bt == "callout":
            icon = (data.get("icon") or {}).get("emoji", "")
            lines.append(f"> {icon} {rich_to_md(data.get('rich_text'))}")
            lines.append("")
        elif bt == "code":
            lang = data.get("language", "")
            if lang == "plain text":
                lang = ""
            code = "".join(x.get("plain_text", "") for x in data.get("rich_text", []))
            lines.append(f"```{lang}")
            lines.append(code)
            lines.append("```")
            lines.append("")
        elif bt == "divider":
            lines.append("")
            lines.append("---")
            lines.append("")
        elif bt == "equation":
            lines.append(f"$$\n{data.get('expression','')}\n$$")
            lines.append("")
        elif bt == "image":
            src = ""
            if data.get("type") == "external":
                src = data.get("external", {}).get("url", "")
            else:
                src = data.get("file", {}).get("url", "")
            cap = rich_to_md(data.get("caption"))
            local = download_image(src, img_subdir, img_prefix) if src else None
            if local:
                lines.append(f"![{cap}]({local})")
            elif src:
                lines.append(f"![{cap}]({src})")
            if cap:
                lines.append(f"*{cap}*")
            lines.append("")
        elif bt == "table":
            child = get_children(b["id"])
            rows = []
            for row in child:
                if row.get("type") != "table_row":
                    continue
                cells = row["table_row"]["cells"]
                rows.append([rich_to_md(c) for c in cells])
            if rows:
                ncol = len(rows[0])
                lines.append("| " + " | ".join(rows[0]) + " |")
                lines.append("|" + "|".join(["------"] * ncol) + "|")
                for r in rows[1:]:
                    while len(r) < ncol:
                        r.append("")
                    lines.append("| " + " | ".join(r) + " |")
                lines.append("")
        elif bt == "toggle":
            lines.append(f"{indent}- {rich_to_md(data.get('rich_text'))}")
            if b.get("has_children"):
                child = get_children(b["id"])
                lines.append(blocks_to_md(child, img_subdir, img_prefix, depth + 1))
        elif bt == "child_page":
            # 交易日志父页时单独处理，文章里一般不出现
            pass
        elif bt in ("column_list", "column"):
            if b.get("has_children"):
                child = get_children(b["id"])
                lines.append(blocks_to_md(child, img_subdir, img_prefix, depth))
        elif bt == "synced_block":
            # 同步块：副本指向原始块，需取原始块的子块
            ref = (data.get("synced_from") or {})
            src_id = ref.get("block_id") if ref else None
            child = get_children(src_id or b["id"])
            lines.append(blocks_to_md(child, img_subdir, img_prefix, depth))
        else:
            # 兜底：有 rich_text 就输出文本
            rt = data.get("rich_text")
            if rt:
                lines.append(rich_to_md(rt))
        i += 1
    return "\n".join(lines)


# ----------------------------------------------------------------------
# frontmatter
# ----------------------------------------------------------------------
def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def write_post(path, frontmatter, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fm = ["---"]
    for k, v in frontmatter.items():
        if k in ("published", "updated"):
            # 日期字段必须是未加引号的 YAML 日期，才能被 z.date() 解析
            fm.append(f"{k}: {v}")
        elif isinstance(v, list):
            fm.append(f"{k}: [{', '.join(yaml_str(x) for x in v)}]")
        elif isinstance(v, bool):
            fm.append(f"{k}: {str(v).lower()}")
        else:
            fm.append(f"{k}: {yaml_str(v)}")
    fm.append("---")
    content = "\n".join(fm) + "\n\n" + body.strip() + "\n"
    # 清理多余空行
    content = re.sub(r"\n{3,}", "\n\n", content)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    log(f"  -> wrote {os.path.relpath(path, ROOT)} ({len(content)} chars)")


# ----------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------
def prop_val(p, name):
    v = p.get("properties", {}).get(name, {})
    t = v.get("type")
    if t == "title":
        return "".join(x.get("plain_text", "") for x in v["title"])
    if t == "rich_text":
        return "".join(x.get("plain_text", "") for x in v["rich_text"])
    if t == "select":
        return (v["select"] or {}).get("name", "")
    if t == "multi_select":
        return [x["name"] for x in v["multi_select"]]
    if t == "date":
        return ((v["date"] or {}).get("start", "") or "")
    if t == "status":
        return (v["status"] or {}).get("name", "")
    return ""


DB_ID = "2c0ce72004d0812da5d0cc9003aedade"
TRADING_LOG_PARENT = "325ce72004d081d79becd7c8279ea85c"

# 要迁移的普通文章（排除交易日志父页，它单独处理）
ARTICLE_SLUGS = {
    "32bce72004d08168a3bddbf39a4c15ad": "sma-strategy-optimization-report-2026_0322",
    "318ce72004d080689129f2af51a87b5c": "debian-NFS",
    "2c0ce72004d0807da8dcd0da592a8c61": "Router-VPN",
    "2c0ce72004d081bd954ae3e75e176d2a": "DSM-Flexget",
}


def migrate_articles():
    log("\n=== 迁移普通文章 ===")
    pages = query_database(DB_ID)
    by_id = {p["id"].replace("-", ""): p for p in pages}
    for pid, slug in ARTICLE_SLUGS.items():
        p = by_id.get(pid)
        if not p:
            log(f"  [missing] {pid} {slug}")
            continue
        title = prop_val(p, "title")
        log(f"\n[文章] {title} ({slug})")
        date = prop_val(p, "date") or p.get("created_time", "")[:10]
        date = date[:10] if date else "2025-01-01"
        cat = prop_val(p, "category") or ""
        tags = prop_val(p, "tags") or []
        if isinstance(tags, str):
            tags = [tags] if tags else []
        summary = prop_val(p, "summary") or ""

        blocks = get_children(p["id"])
        img_subdir = f"posts/{slug}"
        body = blocks_to_md(blocks, img_subdir, img_subdir)

        fm = {
            "title": title,
            "published": date,
            "description": summary,
            "tags": tags,
            "category": cat,
            "draft": False,
        }
        write_post(os.path.join(POSTS_DIR, f"{slug}.md"), fm, body)


MONTHS = {
    "344ce72004d08180b315fd6dbed2aba1": ("2026", "03"),
    "344ce72004d08169acd3ecc5e3a8b2f4": ("2026", "04"),
    "358ce72004d081a7ac29f724d9e997d1": ("2026", "05"),
}


def migrate_trading_logs():
    log("\n=== 迁移交易日志（月度页）===")
    for pid, (year, month) in MONTHS.items():
        log(f"\n[交易日志] {year}年{month}月")
        slug = f"trading-log-{year}-{month}"
        blocks = get_children(pid)
        img_subdir = f"trading-log/{year}-{month}"
        body = blocks_to_md(blocks, img_subdir, img_subdir)
        fm = {
            "title": f"SMA实盘交易日志 — {year}年{month}月",
            "published": f"{year}-{month}-01",
            "description": f"{year}年{month}月 SMA 策略实盘交易日志（按日记录，最新优先）",
            "tags": ["SMA", "实盘交易", "交易日志"],
            "category": "量化交易",
            "draft": False,
        }
        # 月度日志放到独立文件夹的 index.md
        out = os.path.join(POSTS_DIR, slug, "index.md")
        write_post(out, fm, body)


if __name__ == "__main__":
    log(f"ROOT = {ROOT}")
    migrate_articles()
    migrate_trading_logs()
    with open(os.path.join(ROOT, "scripts", "migrate_log.txt"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("\n".join(log_lines))
    log("\n=== DONE ===")
