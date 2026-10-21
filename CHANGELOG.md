# Changelog / 更新日志

All notable changes to this project will be documented in this file.

本项目的所有重要变更都会记录在此文件中。

---

## [1.6.0] - 2026-10-21

### 🆕 New Channels / 新增渠道

#### 🎯 Boss直聘 channel
- 新增 `boss` channel：经 boss-agent-cli + CDP 真 Chrome 搜岗位、取 JD 全文。
- `check()` 四层只读探测（boss-agent-cli 装没装 → 9222 端口通不通 → 有无 zhipin 页签
  → 浏览器内有无 `wt2` 登录 cookie）。
- 抓取走公开 API（`search_jobs` + `job_card_browser` + `browser_source="existing-browser"`）。
- `agent-reach install --system --channels=boss` 可安装锁定上游 boss-agent-cli
  （#403–#407 已合并入 master）固定提交的后端；上游发布正式版后切回版本约束。
- Skill 与安装指南支持"帮我配 Boss直聘"：Agent 启动仅监听回环地址的专用 Chrome，
  用户只负责手动登录，最后由 Agent 验证登录态与 CDP 链路。
- 固定依赖从 fork 快照 `8ff6bd3` 切换到上游 commit `4c991b7`（#403–#407 已合并入
  master）：已登录 CDP 会话可直接复用，搜索可通过 `--browser-source existing-browser`
  禁止 headless 降级。
- code 37 按原始文案分类：环境异常为 `ENVIRONMENT_RISK` 并立即停止；只有明确
  token/stoken 过期才允许一次刷新。专用 Chrome profile 应长期复用并降低频率。

#### 📘 Facebook & 📷 Instagram (opencli)
- New `facebook` and `instagram` channels via OpenCLI, reusing the user's existing Chrome
  login session (no separate credential flow): search, home feed, groups (Facebook);
  user search, profile, recent posts, Explore (Instagram).
- 新增 `facebook`、`instagram` channel，通过 OpenCLI 复用用户已有的 Chrome 登录态：
  Facebook 支持搜索、主页、Feed、群组列表；Instagram 支持用户搜索、Profile、
  最近帖子、Explore。
- Channel count: 14 → 16.

### 🔐 Security Hardening / 安全加固
- Closed remaining trust-boundary gaps and hardened local credential handling and storage
  paths (honors `HOME`, hides setup credentials from logs/output, enforces least-privilege
  credential boundaries, fails closed on credential setup errors).
- Made `doctor` and other diagnostics provably read-only — isolated pytest from the real
  user home so tests can't touch live credentials, and added read-only assertions for the
  diagnostic paths.
- Bounded media processing for transcription (rejects oversized media before processing,
  decodes subprocess output as UTF-8, blocks shorthand IPv4 spellings of internal hosts).
- Hardened the `web` channel's reader against malicious input/response boundaries.
- 收紧剩余的信任边界，加固本地凭据的存储与读取路径（遵循 `HOME`、日志/输出不回显凭据、
  最小权限边界、凭据配置失败时安全失败）。
- 让 `doctor` 及其他诊断确定性只读——测试环境与真实用户 home 隔离，诊断路径新增只读断言。
- 收紧转写流程的媒体处理边界（处理前拒绝超大媒体、子进程输出按 UTF-8 解码、
  拦截指向内部主机的简写 IPv4 地址）。
- 加固 `web` channel 的 reader 输入/响应边界。

### 🐛 Bug Fixes / 修复

#### 🔐 Boss直聘 — 登录态误判（双凭据存储）
- **根因：** Boss 有两个互不代表的登录态存储——本地 `~/.boss-agent/auth/session.enc`
  和专用 Chrome profile 内的浏览器 cookie。`boss status` / `status --live` **只校验前者**
  （Bridge/httpx 时代的遗留凭据库），而 `existing-browser` 严格 CDP 模式下搜索走的是浏览器 cookie。
  「本地有旧凭据 + 浏览器未登录」时 `boss status` 会报 `logged_in: true`，误导 Agent
  跳过登录直接搜索，最终撞上 `AUTH_EXPIRED`；旧 runbook 又禁止把 `_security_check`
  当成未登录，两条规则叠加把 Agent 推向「反爬滑块」的错误分支。
- **修复：** `check()` 新增第 4 层只读探测 `_cdp_zhipin_login_cookie()`，用纯标准库
  实现的最小 WebSocket 客户端直接问 CDP 浏览器本体（`Storage.getCookies`）有无 zhipin
  的 `wt2` cookie，**以浏览器为准**，不引入新依赖、不拉起浏览器、不执行搜索。
  无 wt2 → 明确报「浏览器未登录，搜索会报 AUTH_EXPIRED」并指向「用户登录 +
  `login --cdp`」；探测失败 → 报「登录态未知」；安全校验页提示也附带浏览器 cookie 状态。
- **Runbook 修正：** 删除误导规则「判断登录态只信 `boss status`」，改为以 doctor 的
  浏览器 cookie 探测为准；拉起专用 Chrome 后**强制暂停让用户肉眼确认**登录状态；
  `AUTH_EXPIRED` 定为 ground truth（直接走登录流程，禁止往安全校验方向解释），
  `_security_check` 仅在无 `AUTH_EXPIRED` 时按滑块处理。

#### Channel reliability
- `v2ex`: encode caller-supplied values in URLs, constrain the TLS fallback boundary, recover
  from Python TLS EOF errors.
- `xueqiu`: honor and clamp hot-post limits, return detail quote fields safely.
- `xiaohongshu`: fail (not silently continue) when container restart fails; resolve OpenCLI
  status at check time instead of install time.
- `linkedin`: refresh the uvx stdio contract.
- `youtube`: install required default dependencies, align `yt-dlp` runtime support.
- `transcribe`: decode subprocess output as UTF-8, support Windows Git Bash.
- `skill`: use shell-safe `mcporter` arguments, propagate install failures instead of
  swallowing them, use registered Exa search tools, support OpenCode discovery, document
  verified backend fallbacks.
- `cli`: make P0 configuration paths explicit.
- 渠道可靠性修复：`v2ex`（URL 编码调用方输入、收紧 TLS fallback 边界、从 TLS EOF 错误恢复）、
  `xueqiu`（限制并校验热帖数量、安全返回详情行情字段）、`小红书`（容器重启失败时报错而非静默
  继续、OpenCLI 状态改为 check 时解析而非安装时）、`linkedin`（修复 uvx stdio 契约）、
  `youtube`（补齐默认依赖、对齐 yt-dlp 运行时支持）、转写（子进程输出按 UTF-8 解码、支持
  Windows Git Bash）、skill（shell 安全的 mcporter 参数、安装失败不吞错、使用已注册的 Exa
  搜索工具、支持 OpenCode 发现、补充已验证的 backend fallback 文档）、cli（P0 配置路径显式化）。

### 🧪 Testing & CI / 测试与持续集成
- Added a Windows CI suite (Git Bash discovery, UTF-8 decoding of Git Bash output, portable
  shell command doubles).
- Added unit tests for the `youtube`, `v2ex`, `xueqiu`, `reddit`, `web`, and `rss` channels.
- 新增 Windows CI 测试套件（Git Bash 探测、Git Bash 输出 UTF-8 解码、可移植的 shell 命令替身）。
- 为 `youtube`、`v2ex`、`xueqiu`、`reddit`、`web`、`rss` channel 新增单元测试。

### 📈 Improvements / 改进
- Channel count: 14 → 16.
- 渠道数量：14 → 16。

## [1.3.1] - 2026-03-27

### 🐛 Bug Fixes / 修复

#### 📈 Xueqiu (雪球) — 全面修复

- **修复 400 错误根本原因：** `_ensure_cookies()` 仅访问首页只能获取 `acw_tc`（防 DDoS token），`xq_a_token` 由雪球前端 JS 动态生成，无法通过纯 HTTP 请求获取。新增三级 cookie 加载策略：① 读取 config 文件（`--from-browser` 保存的）→ ② 自动从本地 Chrome 浏览器提取（需安装 browser-cookie3）→ ③ homepage fallback
- **修复 User-Agent：** `"agent-reach/1.0"` 被雪球反爬系统识别拒绝，改为真实 Chrome UA
- **修复缺失 `Referer` 头：** 所有 API 请求加上 `Referer: https://xueqiu.com/`
- **修复 `get_hot_posts()` 端点：** 原端点 `/statuses/hot/listV3.json` 已废弃（返回空 body），改为 `/v4/statuses/public_timeline_by_category.json`，正确解析 `item.data` JSON 字符串获取 author/likes/text
- **修复 `urllib.request.quote` → `urllib.parse.quote`：** 明确使用正确模块
- **修复 `configure --from-browser` 不提取雪球 Cookie：** `PLATFORM_SPECS` 加入 Xueqiu，检测 `xq_a_token` 存在才保存
- **修正文档误导：** README/SKILL.md 中"无需配置"/"public API, no login required" → 准确描述需要 browser cookie
- **改善错误信息：** `check()` 失败时提示 `configure --from-browser chrome` 而非"可能需要代理"

---

## [1.3.0] - 2026-03-12

### 🆕 New Channels / 新增渠道

#### 💻 V2EX
- Hot topics, node topics, topic detail + replies, user profile via public JSON API
- Zero config — no auth, no proxy, no API key required
- `get_hot_topics(limit)`, `get_node_topics(node_name, limit)`, `get_topic(id)`, `get_user(username)`
- 通过公开 JSON API 获取热门帖子、节点帖子、帖子详情+回复、用户信息
- 零配置，无需认证、无需代理、无需 API Key

### 📈 Improvements / 改进

- Channel count: 14 → 15
- 渠道数量：14 → 15

---

## [1.1.0] - 2025-02-25

### 🆕 New Channels / 新增渠道

#### ~~📷 Instagram~~ (removed — upstream blocked)
- ~~Read public posts and profiles via [instaloader](https://github.com/instaloader/instaloader)~~
- **Removed:** Instagram's aggressive anti-scraping measures broke all available open-source tools (instaloader, etc.). See [instaloader#2585](https://github.com/instaloader/instaloader/issues/2585). Will re-add when upstream recovers.
- **已移除：** Instagram 反爬封杀导致所有开源工具（instaloader 等）失效。上游恢复后会重新加回。

#### 💼 LinkedIn
- Read person profiles, company pages, and job details via [linkedin-scraper-mcp](https://github.com/stickerdaniel/linkedin-mcp-server)
- Search people and jobs via MCP, with Exa fallback
- Fallback to Jina Reader when MCP is not configured
- 通过 linkedin-scraper-mcp 读取个人 Profile、公司页面、职位详情
- 通过 MCP 搜索人才和职位，Exa 兜底
- 未配置 MCP 时自动 fallback 到 Jina Reader

#### 🏢 Boss直聘
- QR code login via [mcp-bosszp](https://github.com/mucsbr/mcp-bosszp)
- Job search and recruiter greeting via MCP
- Fallback to Jina Reader for reading job pages
- 通过 mcp-bosszp 扫码登录
- MCP 搜索职位、向 HR 打招呼
- Jina Reader 兜底读取职位页面

### 📈 Improvements / 改进

- Channel count: 9 → 12
- `agent-reach doctor` now detects all 12 channels
- CLI: added `search-linkedin`, `search-bosszhipin` subcommands
- Updated install guide with setup instructions for new channels
- 渠道数量：9 → 11
- `agent-reach doctor` 现在检测全部 11 个渠道
- CLI：新增 `search-linkedin`、`search-bosszhipin` 子命令
- 安装指南新增渠道配置说明

---

## [1.0.0] - 2025-02-24

### 🎉 Initial Release / 首次发布

- 9 channels: Web, Twitter/X, YouTube, Bilibili, GitHub, Reddit, XiaoHongShu, RSS, Exa Search
- CLI with `read`, `search`, `doctor`, `install` commands
- Unified channel interface — each platform is a single pluggable Python file
- Auto-detection of local vs server environments
- Built-in diagnostics via `agent-reach doctor`
- Skill registration for Claude Code / OpenClaw / Cursor
- 9 个渠道：网页、Twitter/X、YouTube、B站、GitHub、Reddit、小红书、RSS、Exa 搜索
- CLI 支持 `read`、`search`、`doctor`、`install` 命令
- 统一渠道接口 — 每个平台一个独立可插拔的 Python 文件
- 自动检测本地/服务器环境
- 内置诊断 `agent-reach doctor`
- Skill 注册支持 Claude Code / OpenClaw / Cursor
