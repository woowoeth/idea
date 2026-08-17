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
SECLABEL = {"build": "值得两周", "watch": "挂着看", "archive": "留档"}
CONTRACT = ("hook","does","voices","gap","counter","differentiator","workload","consumer_angle")
# 75/75 覆盖的四条骨架，永远先渲染；其余字段有才渲染
SPINE = (("pain","痛点"), ("gap","缺口"))
RISKK = (("kill","风险"), ("risk","风险"))
VERDICT_ZH = {"build":"值得两周","watch":"挂着看","archive":"留档"}
WORKLOAD_ZH = {"2w":"两周","2m":"两个月","1w":"一周","no":"不做","2d":"两天"}
TITLES = {}
VOICES_ZH = {}

CSS = """
:root{
  color-scheme:light only;
  --white:#fafaf7;--paper:#f0f0ec;--paper2:#eae9e3;
  --ink:#2a2e2c;--ink-70:#4c524e;--ink-50:#767c76;--ink-30:#a3a8a1;
  --up:#66794a;--sulfur:#b8c49a;--up-bg:rgba(184,196,154,.28);
  --down:#b4574b;--down-bg:rgba(180,87,75,.10);
  --line:rgba(42,46,44,.08);--line-strong:rgba(42,46,44,.12);--line-2:rgba(42,46,44,.045);
  --tint:rgba(42,46,44,.03);--tint-hover:rgba(42,46,44,.055);
  --ease-out-expo:cubic-bezier(0.16,1,0.3,1);
  --ease-out-quart:cubic-bezier(0.25,1,0.5,1);
  --dur-tap:100ms;--dur-fast:150ms;--dur-base:200ms;--dur-slow:260ms;
  --shadow-card:0 0 0 1px var(--line),0 1px 2px rgba(42,46,44,.04),0 4px 12px rgba(42,46,44,.02);
  --shadow-card-hover:0 0 0 1px var(--line-strong),0 2px 4px rgba(42,46,44,.05),0 8px 24px rgba(42,46,44,.05);
  --shadow-focus:0 0 0 3px rgba(42,46,44,.16);
  --glass-chrome:rgba(240,240,236,.72);--glass-light:rgba(250,250,247,.85);
  --r1:8px;--r2:12px;
}
@font-face{font-family:"Huiwen-mincho";src:url("../hw-mincho-subset.woff2") format("woff2");font-display:swap}
*{box-sizing:border-box}
html,body{background:var(--paper)}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Noto Sans SC","Hiragino Sans GB",sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased;font-optical-sizing:auto;line-height:1.55;min-height:100vh}
.skip-link{position:absolute;left:12px;top:-52px;z-index:100;padding:8px 16px;background:var(--ink);color:var(--white);border-radius:6px;font-size:13px;font-weight:600;text-decoration:none;transition:top var(--dur-base) var(--ease-out-quart)}
.skip-link:focus{top:12px}
.wrap{max-width:860px;margin:0 auto;padding:0 24px 96px}
.hd{position:sticky;top:0;z-index:50;margin:0 -24px 26px;padding:26px 24px 15px;background:var(--glass-chrome);-webkit-backdrop-filter:blur(16px) saturate(160%);backdrop-filter:blur(16px) saturate(160%)}
.hd::after{content:'';position:absolute;left:24px;right:24px;bottom:0;height:1px;background:linear-gradient(90deg,transparent,rgba(42,46,44,.10),transparent)}
.brand{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-50);margin-bottom:11px}
.hd-row{display:flex;align-items:baseline;gap:12px;margin-bottom:13px;flex-wrap:wrap}
.hd-title{font-family:"Huiwen-mincho",serif;font-size:26px;font-weight:700;letter-spacing:-.03em;line-height:1.05;margin:0}
.hd-en{font-size:13px;color:var(--ink-50);letter-spacing:-.005em;font-weight:400}
.hd-stats{display:flex;gap:20px;flex-wrap:wrap}
.stat{font-size:12px;color:var(--ink-50);font-variant-numeric:tabular-nums}
.stat b{color:var(--ink);font-weight:600}
.bar{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin-top:13px}
.bar button{font:inherit;font-size:11px;font-weight:600;letter-spacing:.04em;color:var(--ink-50);padding:3px 11px;border:0;border-radius:20px;background:var(--tint);cursor:pointer;transition:background var(--dur-fast) var(--ease-out-quart),color var(--dur-fast) var(--ease-out-quart)}
.bar button:hover{background:var(--tint-hover)}
.bar button[aria-pressed=true]{background:var(--ink);color:var(--white)}
.bar button:focus-visible{outline:0;box-shadow:var(--shadow-focus)}
.bar .spacer{flex:1}
.sec{font-size:10px;font-weight:600;color:var(--ink-50);text-transform:uppercase;letter-spacing:.14em;margin:30px 0 10px}
.sec:first-of-type{margin-top:0}
.card{padding:16px 18px;border-radius:var(--r2);background:var(--white);box-shadow:var(--shadow-card);margin-bottom:10px;transition:box-shadow var(--dur-base) var(--ease-out-quart)}
.card:hover{box-shadow:var(--shadow-card-hover)}
.card-head{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.era-label{font-size:10px;font-weight:600;letter-spacing:.04em;color:var(--ink-50);white-space:nowrap;padding:3px 10px;border-radius:20px;background:var(--tint);font-variant-numeric:tabular-nums}
.era-label.v-build{color:var(--up);background:var(--up-bg)}
.era-line{flex:1;height:1px;background:var(--line)}
.card h2{font-family:"Huiwen-mincho",serif;font-size:16.5px;font-weight:700;line-height:1.5;letter-spacing:-.01em;margin:0 0 2px}
.f{margin:11px 0;display:grid;grid-template-columns:44px 1fr;gap:14px;align-items:start}
.k{font-size:10px;font-weight:600;color:var(--ink-30);text-transform:uppercase;letter-spacing:.1em;padding-top:4px;white-space:nowrap}
.v{font-size:14px;color:var(--ink-70);line-height:1.75}
ul.q{margin:0;padding:0;list-style:none}
ul.q li{padding:12px 14px;border-left:2px solid var(--sulfur);background:var(--tint);border-radius:0 var(--r1) var(--r1) 0;font-size:13.5px;color:var(--ink-70);line-height:1.75;margin-bottom:6px}
.card footer{display:flex;align-items:center;gap:10px;margin-top:13px;padding-top:11px;border-top:1px solid var(--line-2)}
.meta{flex:1;display:flex;gap:14px;flex-wrap:wrap}
.tag{font-size:11.5px;color:var(--ink-50);font-variant-numeric:tabular-nums;text-decoration:none}
.tag.link{color:var(--ink-70);border-bottom:1px solid var(--line-strong)}
.tag.warn{color:var(--down)}
.marks{display:flex;gap:3px}
.marks .m{font-size:14px;line-height:1;padding:5px 9px;border:0;background:transparent;border-radius:20px;cursor:pointer;opacity:.28;transition:opacity var(--dur-fast) var(--ease-out-quart),background var(--dur-fast) var(--ease-out-quart)}
.marks .m:hover{opacity:.6;background:var(--tint)}
.marks .m[aria-pressed=true]{opacity:1;background:var(--tint-hover)}
.marks .m:focus-visible{outline:0;box-shadow:var(--shadow-focus)}
p.lead{margin:0 0 14px;font-size:14.5px;color:var(--ink);line-height:1.8}
.v .orig{display:block;margin-top:5px;font-size:12px;color:var(--ink-30);font-style:normal;line-height:1.6}
.v.verify .scale{display:inline-block;font-size:11.5px;color:var(--ink);background:var(--tint);border-radius:20px;padding:2px 10px;margin-bottom:6px;font-variant-numeric:tabular-nums}
.v.verify .how{display:block;font-size:12.5px;color:var(--ink-50);line-height:1.7}
.era-label.miss{color:var(--down);background:var(--down-bg);cursor:help}
.cnt{font-size:10.5px;color:var(--ink-30);font-variant-numeric:tabular-nums;white-space:nowrap}
ul.q li cite{display:block;margin-top:6px;font-style:normal;font-size:11.5px;color:var(--ink-30)}
ul.q li cite a{color:var(--ink-30);text-decoration:none;border-bottom:1px solid var(--line-strong)}
.srcs{display:flex;flex-direction:column;gap:4px}
a.src{display:inline-flex;align-items:baseline;gap:7px;font-size:12.5px;color:var(--ink-50);text-decoration:none;font-variant-numeric:tabular-nums}
a.src:hover{color:var(--ink)}
a.src .n{display:inline-block;min-width:15px;font-size:10px;color:var(--ink-30)}
details.method{margin-top:11px}
details.method summary{font-size:10px;font-weight:600;color:var(--ink-30);text-transform:uppercase;letter-spacing:.1em;cursor:pointer;list-style:none}
details.method summary::-webkit-details-marker{display:none}
details.method summary::before{content:"\uff0b ";}
details.method[open] summary::before{content:"\uff0d ";}
details.method p{margin:8px 0 0;font-size:12.5px;color:var(--ink-50);line-height:1.7}
html[data-lang=zh] .en,html[data-lang=en] .zh{display:none}
.hide{display:none}
@media(max-width:640px){
  .wrap{padding:0 16px 80px}
  .hd{margin:0 -16px 24px;padding:22px 16px 13px}
  .hd::after{left:16px;right:16px}
  .hd-title{font-size:22px}
  .f{grid-template-columns:1fr;gap:3px}
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
    cards.sort(key=lambda c: (ORDER.get(c.get("verdict"), 9), str(c.get("id"))))
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
        v = c.get("verdict") or "watch"
        if v != cur:
            body.append('<h2 class="sec">%s</h2>' % e(SECLABEL.get(v, v)))
            cur = v
        body.append(render_card(c, i))

    doc = """<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>痛点雷达 · Idea</title>
<meta name="description" content="每天读普通人用自己的话说自己问题的地方，把反复出现的缺口写成卡片。当前 %d 条：build %d / watch %d / archive %d。">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
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
    <span class="hd-en">指得出具体的人，说得出他拿到什么成品</span>
  </div>
  <div class="hd-stats">
    <div class="stat"><b>%d</b> 张卡</div>
    <div class="stat">值得两周 <b>%d</b></div>
    <div class="stat">挂着看 <b>%d</b></div>
    <div class="stat">留档 <b>%d</b></div>
    <div class="stat">更新于 %s</div>
  </div>
  <nav class="bar" aria-label="筛选">
    <button data-filter="all" aria-pressed="true">全部</button>
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
