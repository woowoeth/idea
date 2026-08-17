#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 findings/feed.json 生成板面页 index.html。
视觉沿用 ourword.ai 根站的设计系统（纸墨色板 / Huiwen-mincho / shadow-card / light only）。
契约：
  - 只渲染 verdict in (build, watch, archive)；以 _ 开头的 id 与 _watch 永不渲染
  - 卡片字段维持现状：不渲染兴奋分 / 命中规则 / ⭐❌计数 / 内部推理
  - 标记写 localStorage["idea_marks"]，形状与 marks.json 的 marks 一致：
      {"<finding id>": {"mark": "star"|"no"|"maybe", "at": "YYYY-MM-DD"}}
    逐键合并写入，绝不整体覆盖，页面不清空用户已有键
用法：python3 tools/build_index.py     # 仓库根目录执行
"""
import json, html, os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEED = os.environ.get("FEED", os.path.join(ROOT, "findings", "feed.json"))
OUT  = os.environ.get("OUT",  os.path.join(ROOT, "index.html"))
SITE = "https://ourword.ai/idea/"

ORDER = {"build": 0, "watch": 1, "archive": 2}
DATEFMT = "%s 年 %s 月 %s 日"
SECLABEL = {"build": "值得两周", "watch": "挂着看", "archive": "留档"}
def date_label(d):
    y, m, dd = d[:4], d[5:7], d[8:10]
    return DATEFMT % (y, m.lstrip("0"), dd.lstrip("0"))
CONTRACT = ("hook","does","voices","gap","counter","differentiator","workload","consumer_angle")
# 75/75 覆盖的四条骨架，永远先渲染；其余字段有才渲染
SPINE = (("pain","痛点"), ("gap","缺口"))
RISKK = (("kill","风险"), ("risk","风险"))
VERDICT_ZH = {"build":"值得两周","watch":"挂着看","archive":"留档"}
WORKLOAD_ZH = {"2w":"两周","2m":"两个月","1w":"一周","no":"不做","2d":"两天"}
TITLES = {}
VOICES_ZH = {}

CSS = """
/* 北欧黑白风 v1.0 —— token 与 ourword-site 基准一致；只换视觉层，DOM 与字段不变 */
:root{
  color-scheme:light only;
  --ink:#0a0a0a; --ink-70:#404040; --ink-50:#666666; --ink-30:#b3b3b3;
  --hairline:#e5e5e5; --surface:#ffffff; --bg:#fafafa; --tint:#f0f0f0;
  --cta-fill:#0a0a0a; --cta-text:#ffffff;
  --down:#a13a2e;
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:24px; --sp-6:32px;
  --fs-micro:10px; --fs-caption:11px; --fs-body:13px; --fs-strong:14px; --fs-heading:16px; --fs-display:20px;
  --h-sm:28px; --h-md:36px; --h-lg:46px;
  --r-block:8px; --r-card:16px;              /* 胶囊圆角一律 = 高度/2，见下方注释 */
  --shadow-card:0 1px 2px rgba(10,10,10,.03),0 6px 20px rgba(10,10,10,.06);
  --shadow-pop:0 2px 6px rgba(10,10,10,.05),0 12px 32px rgba(10,10,10,.08);
  --focus:0 0 0 2px var(--ink);
  --font:'Inter','Noto Sans CJK SC','PingFang SC','Hiragino Sans GB','Microsoft YaHei',system-ui,sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg)}
body{color:var(--ink);font-family:var(--font);font-size:var(--fs-strong);line-height:1.65;-webkit-font-smoothing:antialiased}
.caps{letter-spacing:.07em}
.skip-link{position:absolute;left:var(--sp-3);top:-52px;z-index:100;padding:var(--sp-2) var(--sp-4);
  background:var(--ink);color:var(--cta-text);border-radius:var(--r-block);font-size:var(--fs-body);font-weight:700;
  text-decoration:none;transition:top .2s ease-out}
.skip-link:focus{top:var(--sp-3)}
.wrap{max-width:720px;margin:0 auto;padding:0 var(--sp-5) var(--sp-6)}

/* 页眉：细描边分隔，无阴影（描边与阴影二选一） */
.hd{position:sticky;top:0;z-index:50;margin:0 calc(-1 * var(--sp-5)) var(--sp-5);
  padding:var(--sp-5) var(--sp-5) var(--sp-3);background:var(--bg);border-bottom:1px solid var(--hairline)}
.brand{font-size:var(--fs-micro);letter-spacing:.22em;text-transform:uppercase;color:var(--ink-50);margin-bottom:var(--sp-2)}
.hd-row{display:flex;align-items:baseline;gap:var(--sp-3);margin-bottom:var(--sp-3);flex-wrap:wrap}
.hd-title{font-size:var(--fs-display);font-weight:700;letter-spacing:-.01em;line-height:1.2;margin:0}
.hd-en{font-size:var(--fs-body);color:var(--ink-50);font-weight:400}
.hd-stats{display:flex;gap:var(--sp-5);flex-wrap:wrap}
.stat{font-size:var(--fs-caption);color:var(--ink-50);font-variant-numeric:tabular-nums;white-space:nowrap}
.stat b{color:var(--ink);font-weight:700}

/* 筛选：中档胶囊，圆角 = 36/2 = 18px；选中态跳变为黑色实心 */
.bar{display:flex;gap:var(--sp-2);flex-wrap:wrap;align-items:center;margin-top:var(--sp-3)}
.bar button{font:inherit;font-size:var(--fs-body);font-weight:700;color:var(--ink-70);height:var(--h-md);
  padding:0 var(--sp-4);border:0;border-radius:18px;background:var(--tint);cursor:pointer;
  transition:background .18s ease-out,color .18s ease-out,transform .12s ease-out}
.bar button:hover{background:var(--hairline)}
.bar button:active{transform:scale(.96)}
.bar button[aria-pressed=true]{background:var(--cta-fill);color:var(--cta-text)}
.bar button:focus-visible{outline:0;box-shadow:var(--focus)}
.bar .spacer{flex:1}

.sec{font-size:var(--fs-caption);font-weight:700;color:var(--ink-50);text-transform:uppercase;
  letter-spacing:.07em;margin:var(--sp-6) 0 var(--sp-3)}
.sec:first-of-type{margin-top:0}

/* 卡片：无外描边，纯白底 + 双层低透明阴影 */
.card{padding:var(--sp-5);border-radius:var(--r-card);background:var(--surface);box-shadow:var(--shadow-card);
  margin-bottom:var(--sp-3);transition:box-shadow .2s ease-out}
.card:hover{box-shadow:var(--shadow-pop)}
.card-head{display:flex;align-items:center;gap:var(--sp-2);margin-bottom:var(--sp-3)}
/* 小档胶囊：圆角 = 28/2 = 14px，浅灰底填充而非描边 */
.era-label{font-size:var(--fs-caption);font-weight:700;color:var(--ink-70);white-space:nowrap;
  height:var(--h-sm);display:inline-flex;align-items:center;padding:0 var(--sp-3);border-radius:14px;
  background:var(--tint);font-variant-numeric:tabular-nums}
.era-label.v-build{color:var(--ink)}
.era-label.miss{color:var(--down)}
.era-label.date{color:var(--ink-50);background:transparent;padding:0 var(--sp-1)}
.era-line{flex:1;height:1px;background:var(--hairline)}
.card h2{font-size:var(--fs-heading);font-weight:700;line-height:1.5;letter-spacing:-.01em;margin:0 0 var(--sp-2)}
p.lead{margin:0 0 var(--sp-4);font-size:var(--fs-body);color:var(--ink-70);line-height:1.8}

.f{margin:var(--sp-3) 0;display:grid;grid-template-columns:44px 1fr;gap:var(--sp-4);align-items:start}
/* grid 子项默认 min-width:auto，长链接会把轨道撑破视口——必须显式归零 */
.f>*{min-width:0}
.k{font-size:var(--fs-caption);font-weight:700;color:var(--ink-50);letter-spacing:.07em;padding-top:var(--sp-1);white-space:nowrap}
.v{font-size:var(--fs-strong);color:var(--ink-70);line-height:1.8;overflow-wrap:anywhere}

/* 原声：浅灰底块承载，不用描边 */
ul.q{margin:0;padding:0;list-style:none}
ul.q li{padding:var(--sp-3) var(--sp-4);background:var(--tint);border-radius:var(--r-block);
  font-size:var(--fs-body);color:var(--ink-70);line-height:1.8;margin-bottom:var(--sp-2)}
.v .orig{display:block;margin-top:var(--sp-1);font-size:var(--fs-caption);color:var(--ink-50);line-height:1.6}
ul.q li cite{display:block;margin-top:var(--sp-2);font-style:normal;font-size:var(--fs-caption);color:var(--ink-50)}
ul.q li cite a{display:inline-block;min-height:24px;min-width:24px;line-height:24px;text-align:left;color:var(--ink-50);
  text-decoration:none;border-bottom:1px solid var(--ink-30);overflow-wrap:anywhere}
ul.q li cite a:hover{color:var(--ink)}

.v.verify .scale{display:inline-block;font-size:var(--fs-caption);font-weight:700;color:var(--ink);
  background:var(--tint);border-radius:14px;padding:var(--sp-1) var(--sp-3);margin-bottom:var(--sp-2);
  font-variant-numeric:tabular-nums}
.v.verify .how{display:block;font-size:var(--fs-body);color:var(--ink-50);line-height:1.7}

.srcs{display:flex;flex-direction:column;gap:var(--sp-1)}
a.src{display:inline-flex;align-items:center;gap:var(--sp-2);min-height:24px;font-size:var(--fs-body);
  color:var(--ink-50);text-decoration:none;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}
a.src:hover{color:var(--ink)}
a.src .n{display:inline-block;min-width:16px;font-size:var(--fs-caption);color:var(--ink-50)}

.card footer{display:flex;align-items:center;gap:var(--sp-3);margin-top:var(--sp-4);
  padding-top:var(--sp-3);border-top:1px solid var(--hairline)}
.meta{flex:1}
/* 标记：未选=浅灰块，选中=黑色实心（跳变式选中态） */
.marks{display:flex;gap:var(--sp-1)}
.marks .m{font-size:var(--fs-body);line-height:1;height:var(--h-sm);min-width:var(--h-sm);border:0;
  background:var(--tint);border-radius:14px;padding:0 var(--sp-3);cursor:pointer;
  transition:background .18s ease-out,transform .12s ease-out}
.marks .m:hover{background:var(--hairline)}
.marks .m:active{transform:scale(.96)}
.marks .m[aria-pressed=true]{background:var(--cta-fill)}
.marks .m:focus-visible{outline:0;box-shadow:var(--focus)}
.hide{display:none}

@media(max-width:640px){
  .wrap{padding:0 var(--sp-4) var(--sp-6)}
  .hd{margin:0 calc(-1 * var(--sp-4)) var(--sp-5);padding:var(--sp-5) var(--sp-4) var(--sp-3)}
  .card{padding:var(--sp-4)}
  .f{grid-template-columns:1fr;gap:var(--sp-1)}
  .k{padding-top:0}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = """
(function(){
  var KEY="idea_marks";
  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)||"{}")||{}; }catch(e){ return {}; } }
  function save(id,mark){
    var m=load();
    if(mark===null){ delete m[id]; }
    else{ m[id]={mark:mark,at:new Date().toISOString().slice(0,10)}; }
    localStorage.setItem(KEY,JSON.stringify(m));
  }
  function paint(){
    var m=load();
    document.querySelectorAll(".card").forEach(function(c){
      var cur=(m[c.dataset.id]||{}).mark||null;
      c.dataset.mark=cur||"";
      c.querySelectorAll(".m").forEach(function(b){
        b.setAttribute("aria-pressed", b.dataset.m===cur ? "true" : "false");
      });
    });
  }
  document.addEventListener("click",function(ev){
    var b=ev.target.closest(".m"); if(!b) return;
    var card=b.closest(".card"), cur=(load()[card.dataset.id]||{}).mark||null;
    save(card.dataset.id, cur===b.dataset.m ? null : b.dataset.m);
    paint(); applyFilter();
  });
  var filter="all";
  function applyFilter(){
    document.querySelectorAll(".card").forEach(function(c){
      var ok = filter==="all" ? true
        : filter==="marked"   ? !!c.dataset.mark
        : filter==="unmarked" ? !c.dataset.mark
        : filter==="todo"     ? (+c.dataset.miss)>=4
        : c.dataset.verdict===filter;
      c.classList.toggle("hide",!ok);
    });
    document.querySelectorAll(".sec").forEach(function(h){
      var n=0,x=h.nextElementSibling;
      while(x&&x.classList.contains("card")){ if(!x.classList.contains("hide")) n++; x=x.nextElementSibling; }
      h.classList.toggle("hide",n===0);
    });
  }
  document.querySelectorAll("[data-filter]").forEach(function(b){
    b.addEventListener("click",function(){
      filter=b.dataset.filter;
      document.querySelectorAll("[data-filter]").forEach(function(x){
        x.setAttribute("aria-pressed", x===b ? "true" : "false");
      });
      applyFilter();
    });
  });
  document.getElementById("export").addEventListener("click",function(){
    var m=load(), t=JSON.stringify(m,null,2), b=this;
    if(navigator.clipboard) navigator.clipboard.writeText(t);
    b.textContent="已复制 "+Object.keys(m).length+" 条";
    setTimeout(function(){ b.textContent="导出标记"; },2200);
  });
  paint(); applyFilter();
})();
"""

def e(s):
    return html.escape(s if isinstance(s, str) else ("" if s is None else str(s)))

def field(c, key, zh=False):
    if zh:
        v = (c.get("i18n") or {}).get("zh", {}).get(key)
        if v: return v
    return c.get(key)

def voices(c, zh=False):
    """原声在数据里是对象：{quote|text, source|user|src, url}；也兼容纯字符串。"""
    v = field(c, "voices", zh) or c.get("voices") or []
    if isinstance(v, (str, dict)): v = [v]
    out = []
    for x in v:
        if isinstance(x, str):
            if x.strip(): out.append({"quote": x.strip(), "src": "", "url": ""})
        elif isinstance(x, dict):
            q = (x.get("quote") or x.get("text") or "").strip()
            if not q: continue
            out.append({"quote": q,
                        "src": (x.get("source") or x.get("user") or x.get("src") or "").strip(),
                        "url": (x.get("url") or "").strip()})
    return out

def host(u):
    m = re.match(r"https?://([^/]+)", u or "")
    h = m.group(1).lower() if m else (u or "")
    return h[4:] if h.startswith("www.") else h

def sources(c):
    ev = c.get("evidence") or []
    if isinstance(ev, str): ev = [ev]
    urls, seen = [], set()
    for item in ([c.get("url")] if c.get("url") else []) + list(ev):
        if not isinstance(item, str): continue
        # evidence 里存在 "Label: https://..." 这种带前缀的写法，一律抽取其中的 URL
        for u in re.findall(r"https?://[^\s,;）)\]】]+", item) or []:
            u = u.rstrip(".,;")
            if u not in seen:
                seen.add(u); urls.append(u)
    return urls

def missing(c):
    return [k for k in CONTRACT if c.get(k) in (None, "", [], {})]


def render_card(c, i):
    cid = c.get("id") or ("card-%d" % i)
    verdict = c.get("verdict") or "watch"
    zh = (c.get("i18n") or {}).get("zh", {})

    # 标题：一句中文说清这是什么（覆盖文件 → zh.title → zh.claim → 英文兜底）
    title = TITLES.get(cid) or zh.get("title") or zh.get("claim") or c.get("title") or c.get("claim") or cid

    parts = []
    lead = zh.get("move") or c.get("move")
    if lead:
        parts.append('<p class="lead">%s</p>' % e(lead))

    for key, lab in SPINE:
        t = zh.get(key) or c.get(key)
        if t: parts.append('<div class="f"><span class="k">%s</span><div class="v">%s</div></div>' % (e(lab), e(t)))

    # 验证：怎么查到的 + 证据规模
    ev = sources(c)
    vs = voices(c)
    m = zh.get("method") or c.get("method")
    if m or ev or vs:
        bits = []
        if vs or ev:
            bits.append('<span class="scale">%d 条原声 · %d 个来源</span>' % (len(vs), len(ev)))
        if m: bits.append('<span class="how">%s</span>' % e(m))
        parts.append('<div class="f"><span class="k">验证</span><div class="v verify">%s</div></div>' % "".join(bits))

    # 风险
    risk = zh.get("kill") or c.get("kill")
    extra_risk = zh.get("risk") or c.get("risk")
    if extra_risk and extra_risk != risk:
        risk = (risk + " ") if risk else ""
        risk += extra_risk
    if risk:
        parts.append('<div class="f"><span class="k">风险</span><div class="v">%s</div></div>' % e(risk))

    # 原声：中译在上，原文在下
    if vs:
        lis = []
        for n, q in enumerate(vs):
            zhq = VOICES_ZH.get("@%s#%d" % (cid, n))
            zv = voices(c, True)
            if not zhq and n < len(zv) and re.search(r"[\u4e00-\u9fff]", zv[n]["quote"]):
                zhq = zv[n]["quote"]
            body = e(zhq) if zhq else e(q["quote"])
            orig = ('<span class="orig">%s</span>' % e(q["quote"])) if zhq else ""
            cite = ""
            if q["src"]:
                cite = ('<cite><a href="%s" target="_blank" rel="noopener">%s</a></cite>' % (e(q["url"]), e(q["src"]))
                        if q["url"] else "<cite>%s</cite>" % e(q["src"]))
            lis.append("<li>%s%s%s</li>" % (body, orig, cite))
        parts.append('<div class="f"><span class="k">原声</span><ul class="v q">%s</ul></div>' % "".join(lis))

    # 来源
    if ev:
        links = "".join('<a class="src" href="%s" target="_blank" rel="noopener"><span class="n">%d</span>%s</a>'
                        % (e(u), n + 1, e(host(u))) for n, u in enumerate(ev))
        parts.append('<div class="f"><span class="k">来源</span><div class="v srcs">%s</div></div>' % links)

    miss = missing(c)
    head = ['<span class="era-label v-%s">%s</span>' % (e(verdict), e(VERDICT_ZH.get(verdict, verdict)))]
    w = c.get("workload")
    if w: head.append('<span class="era-label">工作量 %s</span>' % e(WORKLOAD_ZH.get(w, w)))
    d = str(c.get("posted_at") or "")[:10]
    if d: head.append('<span class="era-label date">%s</span>' % e(d[5:].replace("-", "/")))
    if miss: head.append('<span class="era-label miss" title="%s">缺 %d 项</span>' % (e("、".join(miss)), len(miss)))
    head.append('<span class="era-line"></span>')

    return ('<article class="card" id="%s" data-id="%s" data-verdict="%s" data-miss="%d">\n'
            '  <div class="card-head">%s</div>\n'
            '  <h2>%s</h2>\n'
            '  <div class="fields">%s</div>\n'
            '  <footer><div class="meta"></div>\n'
            '    <div class="marks" role="group" aria-label="标记">\n'
            '      <button class="m" data-m="star" title="值得做" aria-label="值得做">\u2b50</button>\n'
            '      <button class="m" data-m="maybe" title="待定" aria-label="待定">\U0001f914</button>\n'
            '      <button class="m" data-m="no" title="不要" aria-label="不要">\u274c</button>\n'
            '    </div>\n  </footer>\n</article>'
            % (e(cid), e(cid), e(verdict), len(miss), "".join(head), e(title), "".join(parts)))

def load_overrides():
    global TITLES, VOICES_ZH
    here = os.path.dirname(os.path.abspath(__file__))
    for name, target in (("titles.zh.json", "T"), ("voices.zh.json", "V")):
        for p in (os.path.join(here, name), os.path.join(ROOT, "docs", name)):
            if os.path.exists(p):
                d = json.load(open(p, encoding="utf-8"))
                if target == "T": TITLES.update(d)
                else: VOICES_ZH.update(d)
                break

def main():
    load_overrides()
    feed = json.load(open(FEED, encoding="utf-8"))
    cards = [c for c in feed.get("findings", []) if not str(c.get("id", "")).startswith("_")]
    # 首页按时间倒序（最新在最前）；档位从分组维度降为筛选维度
    cards.sort(key=lambda c: (str(c.get("posted_at") or ""), str(c.get("id"))), reverse=True)
    counts = {k: sum(1 for c in cards if c.get("verdict") == k) for k in ORDER}
    gen = str(feed.get("generated_at") or datetime.date.today().isoformat())[:10]

    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "name": "普通人的痛点雷达", "numberOfItems": len(cards),
          "itemListElement": [{"@type": "ListItem", "position": i + 1,
                               "url": SITE + "#" + str(c.get("id")),
                               "name": (c.get("title") or c.get("claim") or str(c.get("id")))[:180]}
                              for i, c in enumerate(cards)]}

    body, cur = [], None
    for i, c in enumerate(cards):
        d = str(c.get("posted_at") or "")[:10]
        if d != cur:
            body.append('<h2 class="sec" data-date="%s">%s</h2>' % (e(d), e(date_label(d) if d else "未标注日期")))
            cur = d
        body.append(render_card(c, i))

    doc = """<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>痛点雷达 · Idea</title>
<meta name="description" content="每天读普通人用自己的话说自己问题的地方，把反复出现的缺口写成卡片。当前 %d 条：build %d / watch %d / archive %d。">
<link rel="canonical" href="%s">
<script type="application/ld+json">%s</script>
<style>%s</style>
</head>
<body>
<a href="#main" class="skip-link">跳至主内容</a>
<div class="wrap">
<header class="hd" role="banner">
  <div class="brand">PAINPOINT RADAR</div>
  <div class="hd-row">
    <h1 class="hd-title">普通人的痛点雷达</h1>
    <span class="hd-en">痛点足够痛，付费意愿足够强</span>
  </div>
  <div class="hd-stats">
    <div class="stat"><b>%d</b> 张卡</div>
    <div class="stat">值得两周 <b>%d</b></div>
    <div class="stat">挂着看 <b>%d</b></div>
    <div class="stat">留档 <b>%d</b></div>
    <div class="stat">更新于 %s</div>
  </div>
  <nav class="bar" aria-label="筛选">
    <button data-filter="all" aria-pressed="true">最新</button>
    <button data-filter="build" aria-pressed="false">值得两周</button>
    <button data-filter="watch" aria-pressed="false">挂着看</button>
    <button data-filter="archive" aria-pressed="false">留档</button>
    <button data-filter="marked" aria-pressed="false">已标记</button>
    <button data-filter="unmarked" aria-pressed="false">未标记</button>
    <button data-filter="todo" aria-pressed="false">待回填</button>
    <span class="spacer"></span>
    <button id="export">导出标记</button>
  </nav>
</header>
<main id="main">
%s
</main>
</div>
<script>%s</script>
</body>
</html>
""" % (len(cards), counts["build"], counts["watch"], counts["archive"],
       SITE, json.dumps(ld, ensure_ascii=False), CSS,
       len(cards), counts["build"], counts["watch"], counts["archive"], e(gen),
       "\n".join(body), JS)

    open(OUT, "w", encoding="utf-8").write(doc)
    print("wrote", OUT, len(doc), "bytes,", len(cards), "cards", counts)

if __name__ == "__main__":
    main()
