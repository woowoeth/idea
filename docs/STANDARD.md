# The Standard — what earns a place on the Idea board

> 中文在下方。This is the editorial contract for the board. Scouts, the autopilot and any
> agent writing to this repo must satisfy it. Set 2026-07-29, after a 24-question interview
> with the operator. It replaces "new + trending + could be a business" as the bar.

## 0. What the board is for

One job: **surface product opportunities the operator could actually copy and build, earlier
than everyone else.** Two success tests, one year out: *(a)* at least one real project started
from a board entry, *(b)* a window known here weeks before it was obvious elsewhere.

The board is not a news feed, not a trending mirror, and not a daily-habit product. Missing an
item is cheap; a front page full of plausible-but-empty entries is expensive.

## 1. A useful entry = verified pain × a nameable gap × a wedge open to you

All three must hold. Two out of three is "interesting", not useful.

**(1) The pain is verified by real people — not inferred by us.**
At least one checkable piece of first-hand evidence: someone saying they would pay, someone
complaining in earnest, someone forking it to run their own. Stars measure attention, not
demand, and never satisfy this condition on their own. Repo age is *not* part of the standard:
a six-month-old project with real users beats a two-day-old repo with a spike.

*Calibration, 2026-07-29:* a verbatim quote is the strongest evidence but cannot be a hard gate —
fresh repos often have no comments at all, and a bot-filled issue tracker hides the real ones. So
**behaviour counts as weaker first-hand evidence**: forks outnumbering a third of stars (people
standing up their own copies rather than bookmarking), or several contributors on an actively
maintained tracker. Quotes still outrank behaviour, and a card shows them whenever they exist.
What must never happen is the reverse of this rule: an entry with no evidence yet is **archived,
never dropped** — collection is wide, promotion is strict. Only the integrity red line drops.

*Calibration, 2026-08-09 (operator):* what condition (1) verifies is **the pain, not the product**.
Pain evidence may predate the product by years — the duct-tape workaround, the recurring forum thread —
and a launched-yesterday tool with zero users loses nothing for having none of its own. Evidence is
therefore a **ranking bonus, not a gate**: entries carrying it sort above entries that don't, and nothing
is refused purely for lacking it. What a genuinely new, evidence-free entry must pass instead is 1c.

**(2) There is a gap you can say out loud.** One of:
- *only geeks can use it* — CLI, self-hosting, config files, no product around the capability;
- *the Chinese / local-market case is empty* — it exists in English, nobody built it here;
- *it hits a real pain but solves it imperfectly* — the wedge is doing that one job properly.

If you cannot write the gap in one sentence, the entry does not qualify.

**(3) The wedge is open to the operator.** Excluded regardless of how real the demand is:
hardware manufacturing / supply chain, races that require burning money for speed, anything
that needs BD or enterprise sales to start, and pure B2B internal tooling. Buildability is not
a hard gate, but every entry carries an honest **workload tag**: `2w` (two weeks to a usable
version) · `2m` (about two months) · `no` (out of reach alone).

### Corollaries that reverse the old bar

- **"Someone already built it" is good news** — it is demand evidence. The window only closes
  when they have also served the non-technical side well.
- **Developer tools are no longer opportunities in themselves — they are capability signals.**
  A dev/agent-infra project earns the front page only when the card states the opportunity on
  the ordinary-person side. Otherwise it lives in the archive as evidence that something just
  became possible.
- **Taste is shared with the operator's private pain-point radar** (life-stream → asset,
  life-transition packs, creator output pipeline, anchor-document translation; hard-excluded:
  adversarial/complaint tooling, proxying for elders, group coordination, government-subsidy
  errands, creator business-ops).

## 1a. The end-user gate (added 2026-08-03, from a 129-entry operator pass)

**Before anything else, name the person.** An entry only qualifies if you can write, in one
sentence: *who uses this — as a non-developer identity — and what finished thing they walk away
with.* If the only honest answer is "a developer" or "an AI agent", it does not go on the board,
no matter the star count.

The operator marked the whole board on 2026-08-03: **27 ✅ / 102 ❌**. The ❌ pile is almost
entirely one shape — tools whose user is a programmer or a coding agent:

- terminal / CLI / TUI utilities (multiplexers, note apps, spreadsheets, markdown previewers)
- coding-agent surroundings: harnesses, agent memory, statuslines, token counters, IDE plugins,
  model switchers, "agent factories"
- infrastructure *for agents to consume* ("built for agents", "a slide framework for agents")
- developer infrastructure: databases, compilers, languages, object stores, K8s tooling
- "the open-source alternative to <SaaS>" clones with no rework of the ordinary-person side

The ✅ pile is the opposite shape — every one of them has a nameable civilian:
a dental clinic front desk, someone learning guitar, a small-business owner whose phone rings
after hours, a Chinese retail stock investor, a person who wants to know what is in their closet,
someone making an audiobook, someone writing a novel.

**The one allowed exception**: developer-facing tools where the AI produces *a finished artefact a
human uses* — a design, a deck, a whole requirement→delivery chain. A deliverable, not a part.

**Corollary for sourcing.** Star rate by source in that same pass:

| source | ✅ | ❌ | hit rate |
|---|---|---|---|
| operator's own radar findings | 4 | 1 | **80%** |
| Product Hunt | 8 | 7 | **53%** |
| Hacker News | 2 | 7 | 22% |
| GitHub trending / new repos | 13 | 87 | **13%** |

GitHub supplied 100 of 129 entries at a 13% hit rate: it is structurally a developer-tool
firehose and must not be the default intake. Weight Product Hunt and consumer-pain sources up,
GitHub down, and go looking where ordinary people describe their own problems in their own words.

## 1b. One card shape, no exceptions (added 2026-08-03)

Every entry ships the same fields regardless of which source it came from — Reddit, Xiaohongshu,
X, Product Hunt, Hacker News, GitHub or the operator's own radar. A scout that cannot fill them
does not get to post a thinner card; the writer fills them or the entry waits.

**Required, or the entry is not front-page eligible:**

| field | what it must answer |
|---|---|
| `hook` | who is in pain, and in pain enough to pay — concrete people, concrete pain |
| `does` | what it concretely is + its standout capability, 1-2 sentences |
| `gap` | why it is not solved well yet, in one sentence |
| `counter` | the case against building it, and it must sting |
| `differentiator` | your wedge — **and one cold-start entry point in Chinese and one in English** |
| `value` | who exactly pays, for what outcome |
| `risk` | the single concrete reason it fails |
| `workload` | `2w` / `2m` / `no` |
| `voices` | verbatim first-hand quotes with links, or `[]` — **never invented, never paraphrased** |
| `i18n.zh` | faithful 中文 for claim / does / gap / counter / differentiator |

`consumer_angle` is additionally required for anything developer-facing, per 1a.

An entry missing any of these is **held, not published thin**. The daily run backfills 8 per
pass, **starred entries first** — the operator's own picks are the ones that must be complete.

## 1c. The new-window channel (added 2026-08-09)

The mission says *weeks before it was obvious* — a hard evidence gate on brand-new things guarantees
being late, because the newest things have no one watching them yet. So an evidence-free entry may
enter **watch**, on one condition: before writing it, the reviewer can answer three questions —

1. **the hypothesized pain** — a nameable non-developer person, and what hurts;
2. **why now** — which capability or cost just moved to open this window;
3. **the promote-or-kill trigger** — the observable signal that upgrades it to `build`, plus a review
   date 2–4 weeks out on which no-signal drops it to archive.

These three are **the reviewer's ruler, not card content**. The reader gets a clean opportunity card;
the ruler lives in this file and in an internal `_watch` object on the finding
(`{"hypothesis": …, "why_now": …, "trigger": …, "review_by": "YYYY-MM-DD", "on_miss": "archive"}`)
that the site never renders. The daily run / weekly retro sweeps `_watch.review_by` and demotes what
expired.

`build` is unchanged: verified pain or an operator ⭐. A story on its own is never worth two weeks of
the operator's life.

## 1d. The wallet signal, and the cheapest falsification (added 2026-08-11)

Imported from an outside playbook (a Chinese indie dev who builds English SEO tool sites),
keeping only what survives our own use case:

**(a) The wallet signal — is anyone already paying for a crude version near this pain?**
An ugly Excel template, a small subscription, a $4-5k narrow-key piano, an 800-yuan
callout fee: if money has changed hands, the habit of paying is already proven. This is a
**ranking bonus, not a gate** (same logic as evidence in 1b) — a genuinely new window has
nobody charging yet, which is exactly the dementia-call entry. Inverted: if nothing within
a mile of this pain has ever been paid for, that is usually not an immature market, it is a
pain that cannot carry a price. Say so in the `wallet` field and let the card sort itself
down.

**(b) A build-tier `move` must name the cheapest falsification.** Not how to build it — how
to kill it for the least money and time: a landing page, one community post, ten people
asked for money. The board's job ends at "worth two weeks"; day one of those two weeks
should be spent trying to kill it, not writing code.

**Not imported: CPC.** That playbook is tuned for English search traffic and tool
subscriptions, where high CPC means real commercial demand — but it also means traffic you
cannot afford. He wins it organically; this board cold-starts on 小红书 and vertical
communities. CPC stays a manual sanity check on build-tier entries, out of the pipeline.

## 2. Integrity red line (checked before anything else)

Popularity is never a defence — a 10k-star repo is still cut. Out: mass/automated account
creation, CAPTCHA / rate-limit / ban evasion, temp-mail or SMS identity farms, reselling or
proxying a paid API (`*2api`, free-quota pools), credential or cookie pools, piracy and licence
cracking, engagement farming, scraping personal data for resale, impersonation. Also out:
renamed forks and thin wrappers with no substantive delta, and content dressed as product
(awesome lists, guides, courses, prompt galleries, cosmetic skins).

Judge the core pitch, not the edge case: a browser-automation library or a debugging proxy
stays. Enforced in code by `integrity_veto()` in `scouts/scout_lib.py`.

## 3. Two tiers, and the score means one thing

`score` answers exactly one question: **is this worth building?**

| tier | `verdict` | requirement |
|---|---|---|
| 值得动手 · Worth starting | `build` | all three conditions hold, gap is concrete, workload `2w` or `2m` |
| 先盯着 · Watch | `watch` | pain is verified, but the gap or the wedge is not yet clear, or workload is heavy |
| 档案 · Archive | `archive` | capability signals, crowded families, everything else worth keeping as evidence |

**An empty top tier is a valid outcome.** If nothing qualifies today the front page says so;
we never pad it, and we never lower the bar to fill a page.

Collection is wide, promotion is strict: everything vetted is kept as archive; only `build`
and `watch` reach the front page. Same-family pile-ups are all kept and tagged with a family
label — five conversational video editors in one week *is* the signal, and the crowding is
information.

## 4. Card shape (the operator reads for ~10 minutes)

Fields in this order:

1. **hook** — who is in pain, and in pain enough to pay. One sentence, first thing on the card.
2. **does** — what it is: overview and standout capability merged into one tight paragraph.
3. **voices** — verbatim quotes from real users (issue, HN, Reddit) with links. The hardest
   evidence there is; only mined for candidates that already passed the gates above.
4. **gap** — why it is not solved well yet. This is the entry point, and it is more useful than
   a generic risk line.
5. **counter** — the honest case against, and it should sting: who already owns this, whether a
   platform kills it with one feature, why it may be a feature and not a company.
6. **differentiator** — what you would do differently (package for ordinary people, local /
   private version, Chinese-market version), plus the workload tag.
7. **value** — who pays and for what, when it is not already obvious from the hook.

Language follows the audience: entries about Chinese-market scenarios lead in 中文, everything
else leads in English. Both languages are always present.

## 5. How the standard gets sharper

- **Operator marks entries ✅ / ❌ on the board itself.** Every card carries the two buttons; a
  mark is stored in the browser immediately and the bar above the feed offers *copy marks.json*,
  which yields the exact `{"marks": {...}}` block to paste into `marks.json` at the repo root
  (`{"<finding id or repo>": {"mark": "star|no", "at": "YYYY-MM-DD"}}`). Scouts and the autopilot
  read that file.
- **A mark outranks the model.** ✅ is a human confirmation that something is worth doing, so it
  enters the top tier regardless of which fields are filled in; ❌ leaves the top tier for good and
  the card renders dimmed. Marks are the primary training signal for what "worth building" means —
  the weekly retro reads them before it touches any rule.
- **Weekly retro** — what happened to last week's `build` entries (still alive? absorbed by a
  platform? dead?) and the ⭐/❌ distribution. The ⭐ rate on `build` entries is the one number
  that says whether the board works. Retro findings adjust the scoring rules, in this file.
- The operator's historical pain-point marks (⭐36 / ❌176) are **a reference, not a rule**:
  surface "you marked something similar (#xxx)" as a hint, never auto-adjust the score.

## 6. Known trade-off

Unifying taste with the private radar pushes the developer-tool stream — currently the source
of most search traffic — down into the archive. Public reach will likely fall. This was chosen
deliberately: the operator's judgement comes first.

## Retro log

### 2026-08-10 (Monday retro — marks, cohort, misfires)
- **The one number is undefined for a fourth week.** `marks.json` holds 134 marks, every one dated
  2026-07-30 → 2026-08-04, so the ⭐ rate on `build` cannot be computed: nothing promoted since 08-04
  has been marked either way. The other channel is dead on arrival — 50 finding issues, **0 reactions,
  ever**. Marks come from the board or they do not come at all.
- **1–4 weeks out, the ⭐ cohort is intact.** petdex (#147/#314) still live with an open submission
  queue, ClinicFrame (#296), SoundGate (#297), the WeChat-history exporters (#306), the handwriting-font
  pipeline (#309), the solo-business receptionist (#312). Nothing absorbed by a platform yet; the
  absorption rule stays untested for another week.
- **Backfill is the binding constraint, and today it got worse before it got better.** 66 findings.
  25 of the 33 `build` entries carry no `hook` — no first line on the card — and 30 of 66 have no
  `voices`. Eight of the worst (#317-324, all `build`, all hook-less) were written this pass. Note the
  contradiction to settle: 1b still lists `hook`/`does`/`value`/`risk` as required, while today's
  redesign stopped storing them. One of the two has to move, and the file is the standard.
- **Misfire review, 3.** (1) Solo-business invoice↔bank reconciliation (r/smallbusiness 69/85,
  *"Spent my Saturday manually matching 47 invoices to bank payments"*) — declined, correctly: the
  thread's own top answers are QuickBooks/Xero/Zoho, so the gap is "he has not set up accounting
  software", not a product gap. (2) The r/ADHD *"call me instead of pushing a notification"* post —
  independently re-hit today by a different query, and found a second time in r/Mommit in almost the
  same words; already carried as #570, so the earlier decision to rescue it from the archive family
  holds. (3) Craft *preview-before-you-cut* (r/quilting, r/crochet, one asker naming aphantasia) —
  parked under #579 rather than opened, because EQ8 occupies the quilting side; revisit if a second
  independent voice names the no-modelling wedge.
- **Read the scout yield correctly.** 38 candidates (HN 33 + PH 5) → **0 cards**, second time this
  week: terminals, compilers, runtimes, agent infrastructure. Under 1a that is the expected yield of
  those streams, not a board failure — intake volume from them says nothing about board health.
- **Calibration question** (the rule fires: ⭐ rate on `build` undefined two weeks running). Entries
  reach `build` on verified pain plus a concrete gap, but nothing promoted since 08-04 has been marked
  — would you rather the daily run hold the top tier to a handful you will actually mark, or keep
  promoting everything that clears the bar and let the archive absorb the rest?

### 2026-08-10 (second pass — the source, not just the card)
- **Diagnosis that matters more than any cut:** every card the operator liked (the kindergarten
  craft, the r/AskVet lab report, seven r/singing threads) came from **reddit-scout — which has
  never once run.** It is `workflow_dispatch` only and the repo holds no Reddit credentials.
  Meanwhile github / HN / Product Hunt scouts run 48x a day. The board was structurally unable to
  find pain: the pain-first source was off, and the repo-first sources never stopped.
- **appstore-scout added** as a pain-first source that needs no credentials: App Store reviews are
  ordinary people, verbatim, about products they already use. Calibrated against live samples —
  <=3 stars (a 3-star 'great, but I wish it could X' is the purest signal), pricing and paywall
  rants excluded (a price complaint is not a missing capability), and aggregated per SHELF, not per
  app: >=3 voices across >=2 different apps, so the gap is 'the shelf fails at X' rather than one
  unhappy user.
- **reddit-scout armed** with an hourly cron. Without secrets it exits 0; the day
  `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET` land, the best source restarts with no further wiring.
- **The gate moved to the door.** A finding with no voice and no `_watch` is now WRITTEN as
  `archive`, and score/pick/hook/does/value/risk are no longer stored at all — the standard is
  structural, not a render-time argument.
- **Second cut to the card:** the metadata line (category name, agent, operator) and the tag pile
  left the face for the drawer; one meaningful tag remains; the score-chip rack collapsed to a
  single switch. What is left is the five fields and the proof.

### 2026-08-10 (redesign)
- **The card lost half its body.** Operator's verdict on the product: not meeting expectations. Ten rendered rows (hook/claim/does/edge/why_use/gap/counter/differentiator/value/risk) collapse to five fields: **pain / voices / gap / kill / move**. Everything a reader needs to spend or save two weeks of their life; nothing else. Score, stats badges, images and the metadata rows leave the card (provenance stays in the file and the collapsed evidence drawer).
- **The front page is now evidence-gated.** Nothing shows above the archive without first-hand voices, an operator ⭐, or a live 1c `_watch` ruler. Sort inside tiers = voices first, then recency — never score, never stars.
- **Scouts re-aimed.** The carding prompt now demands the five fields and rules: no nameable civilian pain → archive at best. Launched products are demand evidence that attach to a pain, not headlines.

### 2026-08-09
- **Evidence demoted from gate to bonus (operator correction).** His words: evidence can score, it
  cannot gate — the newest things have no one watching yet. Condition (1) now verifies the pain, not
  the product; product traction is never required. Brand-new, evidence-free items go through 1c
  (hypothesized pain / why-now / promote-or-kill trigger), held as the reviewer's internal ruler and an
  unrendered `_watch` field — never on the card.
- First pass under the new bar: the 7-item X daily batch of 2026-08-09. **0 `build`** — the batch's
  shared defect was capability-first, person-nowhere. **1 → `watch` on appeal**: Soloop (solo-founder
  bandwidth is a long-verified pain; a one-day-old product having no evidence of its own is exactly what
  1c exists for; trigger = first-hand "it actually finished my work" voices or retention numbers, review
  2026-09-06). **4 → archive**: Higgsfield/Seedance 2.5 (capability marker — 30s scenes + 50 refs make
  consistent-character long-form possible), SLATE (feature-not-company), LocalAGI + Paygent (agent-infra
  capability signals, consumer_angle stated per 1a). **2 routed off-board** to the competitive-intel line
  (ShadowsClaw, Bit Agents — Future/GMGN turf, per the 08-05 zerosupercycle precedent). **2 declined**
  (HermesWorldAI, CountryMouse — no nameable pain).

### 2026-08-03 (week 2)
- **The board was frozen and the dashboard said green.** GitHub Models was retired 2026-07-30; every
  `llm_copy` / `editor_pick` call returned 410, so each scout held every candidate and exited "success"
  with `posted: 0` — four days, zero ingestion. Fixed: pluggable OpenAI-compatible provider
  (`LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`), a 410/401 circuit breaker, and a 0-posted run under a
  dead model now **fails the workflow**. Ingestion resumes only once the operator sets `LLM_API_KEY`.
- Last week's `build` entries are all alive and independent after 6 days: penecho/penecho 1.8k★,
  darrylmorley/whatcable 8.1k★, antirez/ds4 20k★. Too early to test the absorption rule.
- Marks: **0 ✅ / 0 ❌**. The ⭐ rate on `build` entries — the one number that says whether this works —
  is undefined for a second week. Nothing here is calibrated yet.
- **New rule (promotional hook = defect).** A hook opening with "Revolutionize / Transform your /
  Unlock / Meet / Empower / 颠覆 / 赋能" is vendor copy, not "who is in pain enough to pay". Such entries
  jump the backfill queue ahead of score. 8 entries currently qualify.
- **New rule (a voice must come from a user, not a maintainer).** Mining shipped contributor debugging
  chatter ("I can't check that from here", "I can't reproduce") as first-hand pain. Bare "I can't" no
  longer counts; only "I can't get/use/find/install/run …" does.

---

# 中文版 · 什么条目才配上板

## 0. 板子为什么存在

只有一个任务：**把你真能抄、真能动手做的产品机会，比别人更早摆到你面前。** 一年后的两个成功标准：
①至少一个真实项目起点来自这块板；②某个窗口你比别人早几周知道。

它不是新闻流、不是趋势镜像，也不追求"每天愿意打开"。漏掉一条很便宜；首屏塞满"看着像但没内容"的条目很贵。

## 1. 一条真有用 = 验证过的痛 × 说得出口的缺口 × 你能补的那一刀

三条必须同时成立，缺一条只是"有意思"。

**（1）痛被真人验证过**——不是我们推断的。至少一条可核查的一手证据：有人说愿意付钱、有人在认真抱怨、
有人 fork 回去自己搭。星数只衡量注意力，单独永远不满足这一条。项目新旧**不进标准**：一个跑了半年有真
用户的项目，胜过一个两天涨一波星的新仓。

*校准（2026-07-29）*：真句子是最硬的证据，但**不能当硬门槛**——新仓常常一条评论都没有，机器人刷满的
issue 区也会把真话埋掉。所以**行为算较弱的一手证据**：fork 数超过 star 的三分之一（说明人们在自己搭而
不是收藏）、或活跃维护且有多位贡献者。原声仍然优先于行为，有原声就在卡片上显示。绝不能反向操作的是：
暂时没有证据的条目**进档案，不是丢弃**——收录宽、推送严，只有完整性红线才丢弃。

*校准（2026-08-09，用户）*：条件（1）验证的是**痛，不是产品**。痛的证据往往早于产品多年——土办法、隔几个月就复现的求助帖；
昨天才上线、一个用户都没有的产品，不因「自己没证据」被扣一分。证据由此从门槛降为**排序加分项**：有证据的排前面，
没有证据的不因此被拒。全新的零证据条目要过的，是 1c。

**（2）缺口能一句话说清**，三种之一：只有极客用得了（命令行、自己部署、能力外面没有产品）／中文本土场景
空白（英文世界有了，这边没人做）／痛点击中了但解得不完美（把这一件事做对就是切入口）。写不出缺口，不算数。

**（3）切入口对你开放**。以下即便需求真也排除：硬件量产与供应链、必须烧钱抢速度的赛道、要靠 BD 或企业
销售才能开局的、纯 B 端内部工具。可做性不设硬门槛，但每条都要标**工量**：`2w`（两周出可用版）·`2m`
（约两个月）·`no`（一个人做不了）。

### 三条推论（与旧标准相反）

- **"已经有人做出来了"是好消息**，那是需求证据。只有当他把普通人那侧也做好了，窗口才算关。
- **开发者工具不再算机会本身，只算能力信号**。dev / agent 基建类要上首屏，卡片必须写出"普通人那侧的
  机会是什么"；否则留在档案层，作为"某件事现在能做了"的证据。
- **口味与私人痛点雷达统一**（生活流资产化、人生转型包、创作者产出流水线、锚点级文档翻译；硬排除：对抗维权、
  代际代劳、群体协调、政务补贴、创作者经营侧）。

## 1a. 终端用户闸门（2026-08-03 新增，来自 129 条全量标记）

**先说得出人，再谈别的。** 一条候选要成立，你必须能用一句话写清：*谁在用它——一个非开发者的身份——
以及他因此拿到什么成品。* 如果诚实的答案只能是"开发者"或"某个 AI agent"，那它不上板，星数再高也不上。

用户在 2026-08-03 对全板做了一次通标：**✅27 / ❌102**。❌ 那一堆几乎是同一个形状——
使用者是程序员或 coding agent 的工具：

- 终端 / CLI / TUI 工具（多路复用器、便签、表格、Markdown 预览）
- coding agent 周边：harness、agent 记忆、状态栏、token 计数、IDE 插件、模型切换器、"agent 工厂"
- **给 agent 用**的基础设施（"built for agents"、"给 agent 的幻灯片框架"）
- 开发基础设施：数据库、编译器、语言、对象存储、K8s
- "某某 SaaS 的开源替代"这类克隆，且没有对普通人那一侧做实质改造

✅ 那一堆恰好相反，每一条都指得出一个具体的普通人：
牙科诊所的前台、在学吉他的人、下班后电话没人接的小生意主、炒 A 股的散户、
想知道自己衣柜里到底有什么的人、在做有声书的人、在写小说的人。

**唯一允许的例外**：面向开发者但 AI 直接产出*人能拿去用的成品*——设计稿、幻灯片、
一整条从需求到交付的链。是成品，不是零件。

**由此推出的采集原则。** 同一次通标里按来源统计的命中率：

| 来源 | ✅ | ❌ | 命中率 |
|---|---|---|---|
| 雷达自己挖的方向 | 4 | 1 | **80%** |
| Product Hunt | 8 | 7 | **53%** |
| Hacker News | 2 | 7 | 22% |
| GitHub 趋势/新仓 | 13 | 87 | **13%** |

GitHub 一家贡献了 129 条里的 100 条，命中率只有 13%：它在结构上就是一根开发者工具的消防水管，
**不能再当默认进料口**。Product Hunt 与"普通人吐槽"类源加权，GitHub 降权，
并且要主动去普通人用自己的话描述自己问题的地方找。

## 1b. 一种卡片格式，没有例外（2026-08-03 新增）

不管来自哪个源——Reddit、小红书、X、Product Hunt、Hacker News、GitHub，还是雷达自己挖的——
每条上板内容都交同一套字段。scout 填不满就不许发一张更薄的卡；要么写满，要么让它等着。

**缺任何一项就不具备上前台的资格：**

| 字段 | 必须回答什么 |
|---|---|
| `hook` | 谁在痛，且痛到愿意付钱——具体的人、具体的痛 |
| `does` | 它具体是什么 + 最突出的能力，1-2 句 |
| `gap` | 为什么至今没被解好，一句话 |
| `counter` | 反对做它的理由，而且要扎人 |
| `differentiator` | 你的切入打法——**并且内含中英各一个冷启动入口** |
| `value` | 谁确切地付钱，为什么结果付钱 |
| `risk` | 它失败的那一个具体原因 |
| `workload` | `2w` / `2m` / `no` |
| `voices` | 带链接的逐字一手原话，或 `[]`——**绝不编造、绝不改写** |
| `i18n.zh` | claim / does / gap / counter / differentiator 的忠实中文 |

按 1a，任何面向开发者的条目还必须额外有 `consumer_angle`。

缺字段的条目**扣住不发，而不是发一张薄卡**。每日一轮回填 8 条，**⭐ 的优先**——
用户自己挑出来的那些，才是最该完整的。

## 1c. 新窗口通道（2026-08-09 新增）

使命写的是「比别人早几周」——对全新事物设证据硬门槛，等于保证永远晚，因为最新的东西恰恰还没人注意。
所以零证据条目允许进 **watch**，唯一条件：下笔前，评审自己能答出三问——

1. **假设的痛**——一个说得出名字的非开发者身份，痛在哪；
2. **为什么是现在**——哪个能力或成本刚变，窗口才开；
3. **升级/击杀触发器**——出现什么可观察信号→升 `build`；并定一个 2–4 周后的复核日，到期没信号→落档案。

这三问是**评审的尺子，不是卡片内容**。读者拿到的是一张干净的机会卡；尺子只存在本文件与 finding 的内部字段
`_watch`（`{"hypothesis":…,"why_now":…,"trigger":…,"review_by":"YYYY-MM-DD","on_miss":"archive"}`），站点永不渲染。
每日跑／每周复盘扫 `_watch.review_by`，到期降级。

`build` 档不动：要么痛有证据，要么用户打 ⭐——光靠故事，永远换不走你两周的命。

## 1d. 钱包信号与最便宜的证伪（2026-08-11 新增）

外部输入（一位做英文 SEO 工具站的独立开发者的选品方法论）里有两件我们缺的，取其可取：

**（a）钱包信号——这条痛的附近，已经有人在为粗糙的方案掏钱吗？**
哪怕在卖的是一个丑陋的 Excel 模板、一个订阅制小工具、一台四五千美元的窄键钢琴、
一次 800 块的上门维修——只要有人真的付过钱，付费习惯就已经被验证。这是**排序加分项，
不是门槛**（与 1b 证据同理）：全新窗口本来就还没有人收过钱，失智老人来电那条正是如此。
反过来，若一条痛的方圆之内从来没有任何付费行为，那大概率不是市场不成熟，是它撑不起付费——
这种卡要在 `wallet` 字段里明写「弱」，让它自己排到后面去。

**（b）build 档的「切入」必须包含最便宜的证伪。**
不是「怎么做出来」，是「花最少的钱和时间，怎么证明这条是错的」——一个落地页、
一次社群发帖、十个人的付费意愿。板子的职责止于「值不值两周」，而两周的第一天就该用来
杀掉它，不是用来写代码。

**不照搬的部分：CPC。** 那套方法围绕英文搜索流量与工具订阅配置，CPC 高说明商业需求真，
但同时说明这条流量买不起；他靠自然排名吃下来，本板的冷启动是小红书与垂直社群，
CPC 因此只作 build 档的人工旁证，不进管线。同理，「竞品多＝市场已验证」在他那里是死法之一，
在这里等价于同族拥挤（见 Pocket Fit）。

## 1e. 我们该筛什么维度（2026-08-11）

外部流行的机械筛法是「筛月收入 >$25k、评分 <4.5 的应用，做得更好」。**当天实测证伪**：
榜上评分最低收入最高的那个（Phone Tracker，4.3★），最近 50 条评论里 34 条差评——
12 条骂收费、1 条骂坏、**0 条说缺功能**。低分标记的是收费问题，不是机会；它评分低恰恰
因为那台让它赚钱的机器（激进付费墙、夸大宣传、取消后继续扣款）。「做得更好」＝做一个
诚实版本去打一个靠不诚实赚钱的产品，而诚实版本赚不到那笔钱。

**筛子的形式是对的（可反复跑、不靠人一条条读），要换的是维度。** 我们该筛这三个：

**（1）痛龄 × 能力龄。** 老痛 × 新能力＝窗口；老痛 × 老能力＝早有人做了或根本做不成；
新痛 × 新能力＝一时风潮。工具：`scouts/pain_age.py`，按年抽样量「这句痛占当年帖子的
百分比」（绝对条数不可比，密度可比），连续多年复发＝耐久痛。这是 1c「为什么是现在」
的机械化版本。

**（2）被善意填补的缺口。** 当一个社区被迫把某个答案**建制化**——每周固定的新手求助大帖、
置顶 FAQ、志愿者轮值——那是「高频未满足需求」的结构性证据，比赞数难伪造得多。
手工活那条卡就是这么来的：r/knitting 常年挂着每周新手大帖。附带一个必须写进 kill 的推论：
**在位者不是产品，是善意**——它既难打败，又极容易得罪。

**（3）缺功能密度，而不是评分。** 把差评按「骂钱／骂坏／缺功能」分类，只看第三类的占比。
一个 4.7 星但 15% 的评论在说「要是能 X 就好了」的应用，远胜过一个 3.9 星、八成在骂
扣款的应用。分类器已在 `appstore_scout` 里（WISH／NOISE 词网＋按货架聚合）。

**反维度（永远不筛）**：排名、下载量、评分、赞数、收入。全是流行度的代理，
而 08-11 的实测证明评分不只是无用，是**主动误导**。

## 2. 完整性红线（先于一切判断）

星数永远不是豁免理由，一万星也拦。出局：批量注册养号、验证码/风控/封号绕过、接码与临时邮箱身份农场、
转卖或代理付费 API（`*2api`、免费额度池）、号池与 cookie 池、破解盗版、刷量涨粉、爬个人数据售卖、
换脸冒充。同样出局：换皮改名的 fork 与无实质增量的薄壳，以及伪装成产品的内容（awesome 清单、指南、
课程、prompt 画廊、皮肤主题）。看主打卖点，不看边缘用法——正经的浏览器自动化库、调试代理照常留。

## 3. 两档展示，分数只回答一件事

`score` 只回答：**到底值不值得做。**

| 档位 | `verdict` | 条件 |
|---|---|---|
| 值得动手 | `build` | 三条件齐全、缺口具体、工量 `2w` 或 `2m` |
| 先盯着 | `watch` | 痛够硬，但缺口或切入口还没想清，或工量偏重 |
| 档案 | `archive` | 能力信号、拥挤同族、其余值得留档的证据 |

**首屏空着是合法结果。** 今天没有达标的就明写没有；不凑数，也不为填页降标准。

收录宽、推送严：过筛的全部留档，只有 `build` 与 `watch` 上首屏。同族撞车全留并打同族标签——
一周冒出五个对话式剪辑本身就是信号，拥挤度是信息。

## 4. 卡片结构（按 10 分钟认真读来排）

字段顺序：**谁在痛、痛到愿付钱**（第一眼那句）→ **是什么**（简介与亮点合并成一段）→ **用户原声**
（issue / HN / Reddit 的真句子＋链接，只给已过门的候选去挖）→ **它为何还没被做好**（这就是你的入口）→
**反面，要狠**（谁已占住、大厂一个功能会不会碾平、为何是功能不是公司）→ **我会怎么做不一样**＋工量标 →
**商业**（谁付钱，若首句没交代清楚）。

语言按人群分流：中文场景条目中文为主，其余英文为主，两种语言始终都在。

## 5. 标准怎么变准

- **直接在板上标 ✅/❌**：每张卡片都有这两个按钮，点了立刻存在浏览器里，信息流上方的小条提供
  「复制 marks.json」，把 `{"marks": {...}}` 整块粘到仓库根目录的 `marks.json` 即可
  （格式 `{"<条目 id 或 owner/repo>": {"mark":"star|no","at":"YYYY-MM-DD"}}`），scout 与 autopilot 都读它。
- **人的标记压过模型**：✅ 是"我确认这值得做"，无论字段齐不齐都直接进顶档；❌ 永久离开顶档、卡片变灰。
  标记是"什么叫值得做"最主要的训练信号——每周复盘先读标记，再动任何规则。
- **每周复盘**：上周 `build` 条目后来怎么了（活着？被平台吸收？凉了？）＋⭐/❌ 分布。`build` 条目的
  ⭐率是判断这块板有没有用的唯一数字。复盘结论直接改这份文件里的规则。
- 你在痛点雷达的历史标记（⭐36 / ❌176）**只作参考不作准**：卡片上提示"你标过类似的 #xxx"，不自动改分。

## 6. 已知代价

口味与私人雷达统一后，目前撑着搜索流量的开发者工具流会被压到档案层，公开流量大概率下滑。这是明知代价后
的选择：以你的判断为先。
