# Idea

普通人的痛点雷达。每天读普通人用自己的话说自己问题的地方（小红书、Reddit、HN、Product Hunt），
把反复出现的缺口写成卡片，只留**指得出具体普通人**的那些。

## 这个仓库是什么

| 路径 | 作用 |
|---|---|
| `docs/STANDARD.md` | 板面契约。**标准是这份文件，不是任何人的观点。** `build` / `watch` / `archive` 三档，顶层为空是合法结果 |
| `docs/RADAR.md` | 雷达规则与数据源 |
| `docs/RADAR-INDEX.md` | 条目索引与去重基线，当前到 **#591**。「标记」列是操作者手写的，任何自动流程都不得覆盖 |
| `docs/RADAR-LOG.md` | 更新日志，每轮一行 |
| `findings/feed.json` | 全部卡片（当前 75 条：build 56 / watch 7 / archive 12） |
| `findings/<id>.json` | 每张卡单独落盘 |
| `marks.json` | 操作者标记，key 为 finding id 或 owner/repo，值为 `star` / `no` / `maybe` |

## 最高优先：终端用户闸门

写任何条目前先回答两个问题：**谁在用（必须是非开发者身份）？他因此拿到什么成品？**
答不出、或答案只能是「开发者」或「某个 AI agent」，直接不要，星数多高都不要。

依据是一次全板通标：✅27 / ❌102。❌ 几乎全是终端／CLI 工具、coding agent 周边、
给 agent 用的基础设施、开发基础设施、「某 SaaS 的开源替代」克隆。✅ 全都指得出具体普通人。
**唯一例外**：AI 直接产出人能用的成品（设计稿／幻灯片／成片／书稿）。

## 卡片的字段标准

`hook`（谁在痛、痛到愿付钱）· `does` · `voices`（逐字原话，**绝不编造**，没有就留空并标 `pain_verified: false`）·
`gap` · `counter`（要扎人）· `differentiator`（含中英冷启动入口）· `workload` · `consumer_angle`，全字段镜像 `i18n.zh`。

`verdict` 判 `build` 需同时满足：有验证过的痛 **且** 缺口具体 **且** `workload` ≠ `no`。

## 完整性红线

一万星照杀：薅别人服务（养号、绕验证码风控、接码、转卖代理付费 API、号池、破解、刷量、
爬个人数据售卖、换脸冒充）；换皮 fork 与薄壳；内容伪装成产品。**看主打卖点，不看边缘用法。**

## 沿革

本仓库于 2026-08-17 从 2026-08-14 的本地快照重建——原仓库 `ourword-ai/idea` 所属账号被 GitHub 停用，
仓库与 GitHub Pages 一并不可访问。docs 四件、feed 全部 74 条卡片、marks.json 与
RADAR-INDEX 中操作者手写的 ⭐69／❌3 全部逐字还原，编号自 **#591** 续接。
原站点的 `index.html` 不在快照内，需要时另行重建。
