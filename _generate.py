#!/usr/bin/env python3
"""Generate United Citizen Law practice-area pages + team page.
All pages share one shell (header, contact band, footer, a11y toggles) and each
carries unique SEO meta + schema. Copy is original, grounded in the firm's real
services — not copied from uclaw.net (avoids duplicate-content self-competition)."""
import base64, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
def av(name):
    with open(os.path.join(BASE,'team',f'{name}.jpg'),'rb') as f:
        return 'data:image/jpeg;base64,'+base64.b64encode(f.read()).decode()
def av96(name):
    with open(os.path.join(BASE,'team','av',f'{name}.jpg'),'rb') as f:
        return 'data:image/jpeg;base64,'+base64.b64encode(f.read()).decode()

PHONE='(916) 800-8457'; TEL='+19168008457'

CSS = r"""
:root{
  --black:#070708;--coal:#0d0d10;--coal-2:#131318;--white:#fff;--paper:#fbfaf7;
  --ink:#101216;--body-d:#c9c4b4;--body-l:#41444c;--mute-d:#8d8878;--mute-l:#6b6e77;
  --gold:#d4a72c;--gold-hi:#f0cf6a;--gold-deep:#7a5e0b;
  --hair-d:rgba(255,255,255,.09);--hair-g:rgba(212,167,44,.28);--hair-l:rgba(16,18,22,.12);
  --ease:cubic-bezier(.32,.72,0,1);
  --serif:"Didot","Bodoni MT","Playfair Display","Palatino","Palatino Linotype",Georgia,serif;
  --sans:"Avenir Next","Avenir","Segoe UI","Helvetica Neue",Helvetica,Arial,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:6.5rem}
html.bigtext{font-size:118%}
body{background:var(--black);color:var(--body-d);font-family:var(--sans);line-height:1.75;font-size:1.075rem;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.1;letter-spacing:.004em;text-wrap:balance;color:var(--white)}
a{color:var(--gold-hi)}
img{max-width:100%;height:auto}
:focus-visible{outline:3px solid var(--gold-hi);outline-offset:3px;border-radius:3px}
.skip{position:absolute;left:-9999px;top:0;background:var(--gold);color:var(--black);padding:.8rem 1.4rem;z-index:120;font-weight:700}
.skip:focus{left:0}
.wrap{max-width:86rem;margin-inline:auto;padding-inline:clamp(1.25rem,4.5vw,2.5rem)}
.wide{max-width:86rem}
/* top + nav */
.topstrip{position:fixed;top:0;left:0;right:0;z-index:92;display:flex;justify-content:center;gap:.4rem;padding:.45rem 1rem 0}
.langsw{display:inline-flex;gap:.1rem;background:rgba(13,13,16,.7);backdrop-filter:blur(14px);border:1px solid var(--hair-d);border-radius:999px;padding:.18rem;max-width:calc(100vw - 1.2rem)}
.langsw button{background:none;border:0;color:var(--mute-d);font-family:var(--sans);font-size:.72rem;font-weight:700;letter-spacing:.04em;padding:.28rem .6rem;border-radius:999px;cursor:pointer;transition:all .35s var(--ease);min-height:2.1rem}
.langsw button:hover{color:var(--white)}
.langsw button.on{background:rgba(212,167,44,.16);color:var(--gold-hi)}
@view-transition{ navigation: auto; }
@media(prefers-reduced-motion:reduce){ @view-transition{ navigation: none; } }
::view-transition-old(root),::view-transition-new(root){ animation-duration:.28s; }
.navwrap{position:fixed;top:2.5rem;left:0;right:0;z-index:90;display:flex;justify-content:center;padding-inline:1rem}
.pillnav{display:flex;align-items:center;gap:1.3rem;background:rgba(13,13,16,.74);backdrop-filter:blur(22px);border:1px solid var(--hair-d);border-radius:999px;padding:.5rem .55rem .5rem 1.35rem;box-shadow:0 18px 50px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);max-width:100%}
.brand{font-family:var(--serif);font-size:1.05rem;color:var(--white);text-decoration:none;letter-spacing:.05em;white-space:nowrap;display:flex;align-items:center;gap:.55rem}
.brand b{color:var(--gold-hi);font-weight:500}
.brandlogo{height:1.9rem;width:auto;display:block}
.pillnav ul{display:flex;gap:1.3rem;list-style:none;align-items:center}
.pillnav ul a{color:#e7e3d6;text-decoration:none;font-size:.88rem;font-weight:600;transition:color .4s var(--ease)}
.pillnav ul a:hover{color:var(--gold-hi)}
@media(max-width:60rem){.pillnav ul{display:none}}
.btn{display:inline-flex;align-items:center;gap:.7rem;border-radius:999px;text-decoration:none;font-weight:700;font-size:1rem;padding:.55rem .6rem .55rem 1.4rem;min-height:52px;border:1px solid transparent;transition:transform .5s var(--ease),box-shadow .5s var(--ease);cursor:pointer;font-family:var(--sans)}
.btn:hover{transform:translateY(-2px)}
.btn .orb{width:2.1rem;height:2.1rem;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;flex:none}
.btn-gold{background:linear-gradient(155deg,var(--gold-hi),var(--gold) 70%);color:#151004;box-shadow:0 14px 40px rgba(212,167,44,.28),inset 0 1px 0 rgba(255,255,255,.35)}
.btn-gold .orb{background:rgba(12,9,2,.18)}
.btn-ghost{border-color:var(--hair-g);color:var(--gold-hi);background:rgba(212,167,44,.05)}
.btn-ghost .orb{background:rgba(212,167,44,.12)}
.btn-white{background:var(--white);color:var(--ink)}
.btn-white .orb{background:rgba(16,18,22,.08)}
.navcall{padding:.4rem .45rem .4rem 1.05rem;min-height:44px;font-size:.9rem}
.navcall .orb{width:1.85rem;height:1.85rem}
/* breadcrumb */
.crumb{padding-top:8.5rem;padding-bottom:.5rem;font-size:.85rem;color:var(--mute-d)}
.crumb a{color:var(--mute-d);text-decoration:none}.crumb a:hover{color:var(--gold-hi)}
.crumb span{color:var(--gold-hi)}
/* hero */
.phero{position:relative;overflow:hidden;padding-block:1.5rem clamp(3rem,6vw,4.5rem)}
.phero::before{content:"";position:absolute;width:40rem;height:40rem;top:-16rem;right:-12rem;border-radius:50%;background:radial-gradient(circle,rgba(212,167,44,.14),transparent 65%);filter:blur(80px);pointer-events:none}
.eyebrow{display:inline-flex;align-items:center;gap:.5rem;border-radius:999px;padding:.32rem .95rem;font-size:.68rem;font-weight:700;letter-spacing:.22em;text-transform:uppercase;margin-bottom:1.3rem;background:rgba(212,167,44,.08);border:1px solid var(--hair-g);color:var(--gold-hi)}
.eyebrow::before{content:"";width:.4rem;height:.4rem;border-radius:99px;background:currentColor}
.phero h1{font-size:clamp(2.3rem,5vw,3.8rem);margin-bottom:1.1rem;position:relative}
.phero h1 em{font-style:italic;background:linear-gradient(120deg,var(--gold-hi),var(--gold));-webkit-background-clip:text;background-clip:text;color:transparent}
.phero .lede{font-size:1.2rem;max-width:44rem;color:var(--body-d);margin-bottom:1.7rem;position:relative}
.phero .cta-row{display:flex;flex-wrap:wrap;gap:1rem;position:relative}
.phero .risk{margin-top:1rem;font-size:.92rem;color:var(--mute-d);position:relative}
/* content */
.prose{padding-block:clamp(2.5rem,5vw,4rem)}
.prose.light{background:var(--paper);color:var(--body-l)}
.prose.light h2,.prose.light h3{color:var(--ink)}
.prose h2{font-size:clamp(1.7rem,3.4vw,2.4rem);margin-bottom:1rem;max-width:44rem}
.prose h3{font-size:1.3rem;margin:1.8rem 0 .6rem}
.prose p{font-size:1.08rem;margin-bottom:1.1rem;max-width:48rem}
.prose.light p{color:var(--body-l)}
.lead-answer{font-size:1.2rem;border-inline-start:3px solid var(--gold);padding-inline-start:1.3rem;margin-bottom:1.6rem;color:var(--white)}
.prose.light .lead-answer{color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.4rem 0}
.chip{background:rgba(212,167,44,.08);border:1px solid var(--hair-g);color:var(--gold-hi);border-radius:999px;padding:.4rem .95rem;font-size:.92rem;font-weight:600}
.prose.light .chip{background:rgba(122,94,11,.08);border-color:rgba(122,94,11,.25);color:var(--gold-deep)}
/* steps */
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:1.1rem;margin-top:1.8rem;counter-reset:s}
@media(max-width:56rem){.steps{grid-template-columns:1fr}}
.stepc{border-radius:1.3rem;padding:.4rem;background:rgba(16,18,22,.04);border:1px solid var(--hair-l)}
.stepc-in{border-radius:calc(1.3rem - .4rem);background:var(--white);border:1px solid rgba(16,18,22,.05);padding:1.6rem;height:100%;counter-increment:s;box-shadow:inset 0 1px 1px rgba(255,255,255,.9)}
.stepc-in::before{content:"0" counter(s);font-family:var(--serif);font-size:2.4rem;color:var(--gold-deep);opacity:.55;display:block;margin-bottom:.7rem;line-height:1}
.stepc-in h3{color:var(--ink);font-size:1.2rem;margin:0 0 .4rem}
.stepc-in p{font-size:.96rem;color:var(--body-l);margin:0}
/* faq */
details{border:1px solid var(--hair-l);border-radius:1.1rem;background:var(--white);margin-bottom:.85rem;overflow:hidden}
details[open]{box-shadow:0 22px 50px -28px rgba(16,18,22,.22)}
summary{cursor:pointer;font-weight:700;color:var(--ink);padding:1.15rem 1.4rem;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:1rem;min-height:52px;font-size:1.05rem}
summary::-webkit-details-marker{display:none}
summary .sig{flex:none;width:1.7rem;height:1.7rem;border-radius:99px;border:1px solid rgba(122,94,11,.35);color:var(--gold-deep);display:grid;place-items:center;font-family:var(--serif);font-size:1.15rem;transition:transform .5s var(--ease)}
details[open] summary .sig{transform:rotate(45deg)}
.answer{padding:0 1.4rem 1.25rem;font-size:1rem;color:var(--body-l)}
/* end CTA */
.endcta{text-align:center;position:relative;overflow:hidden;padding-block:clamp(3.5rem,7vw,5.5rem)}
.endcta::before{content:"";position:absolute;width:46rem;height:46rem;left:50%;top:-28rem;transform:translateX(-50%);border-radius:50%;background:radial-gradient(circle,rgba(212,167,44,.16),transparent 62%);filter:blur(70px);pointer-events:none}
.endcta h2{font-size:clamp(1.9rem,4.2vw,3rem);max-width:38rem;margin:0 auto 1rem;position:relative}
.endcta p{max-width:34rem;margin:0 auto 2rem;position:relative;color:var(--body-d)}
.endcta .cta-row{display:flex;flex-wrap:wrap;gap:1rem;justify-content:center;position:relative}
/* contact band */
.contact{background:var(--paper);border-top:1px solid var(--hair-l);padding-block:clamp(3rem,6vw,4.5rem)}
.contact h2{color:var(--ink);font-size:clamp(1.7rem,3.4vw,2.4rem);margin-bottom:1rem}
.contact-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:clamp(2rem,5vw,4rem);align-items:center}
@media(max-width:56rem){.contact-grid{grid-template-columns:1fr}}
.contact address{font-style:normal;font-size:1.05rem;line-height:2;color:var(--body-l)}
.contact address a{font-weight:700}
.contact .eyebrow{color:var(--gold-deep);background:rgba(122,94,11,.07);border-color:rgba(122,94,11,.25)}
.ccard{border-radius:1.4rem;padding:.4rem;background:rgba(16,18,22,.04);border:1px solid var(--hair-l)}
.ccard-in{border-radius:1rem;background:var(--white);border:1px solid rgba(16,18,22,.05);padding:1.8rem;text-align:center}
.ccard-in h3{color:var(--ink);font-size:1.25rem;margin-bottom:.5rem}
.ccard-in p{color:var(--body-l);font-size:.96rem;margin-bottom:1.2rem}
/* footer */
footer.site{background:#050506;border-top:1px solid var(--hair-d);font-size:.93rem;color:var(--mute-d)}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:2.4rem;padding-block:3.4rem}
.social{display:flex;gap:.55rem;margin-top:1.1rem;flex-wrap:wrap}
.social a{width:42px;height:42px;border-radius:999px;display:inline-flex;align-items:center;justify-content:center;color:var(--mute-d);border:1px solid var(--hair-d);transition:color .35s var(--ease),border-color .35s var(--ease),transform .35s var(--ease)}
.social a:hover{color:var(--gold-hi);border-color:var(--hair-g);transform:translateY(-2px)}
.greviews{display:inline-flex;align-items:center;gap:.4rem;margin-top:.9rem;font-weight:600;color:var(--gold-hi);text-decoration:none}
.greviews:hover{text-decoration:underline}
@media(max-width:56rem){.foot-grid{grid-template-columns:1fr 1fr}}
@media(max-width:34rem){.foot-grid{grid-template-columns:1fr}}
footer.site h3{color:var(--white);font-family:var(--sans);font-size:.78rem;text-transform:uppercase;letter-spacing:.2em;margin-bottom:1.1rem}
footer.site ul{list-style:none}footer.site li{margin-bottom:.6rem}
footer.site a{color:#cfcaba;text-decoration:none}footer.site a:hover{color:var(--gold-hi)}
footer.site address{font-style:normal;line-height:1.85}
.legal{border-top:1px solid rgba(255,255,255,.06);padding-block:1.5rem;font-size:.76rem;color:#6f6a5c}
/* sticky mobile call */
.callbar{position:fixed;bottom:.8rem;left:.8rem;right:.8rem;z-index:95;display:none;grid-template-columns:1.2fr 1fr;gap:.5rem}
.callbar a{display:flex;align-items:center;justify-content:center;gap:.5rem;padding:1rem;font-weight:800;text-decoration:none;font-size:1rem;min-height:54px;border-radius:999px;box-shadow:0 16px 40px rgba(0,0,0,.5)}
.callbar .c1{background:linear-gradient(155deg,var(--gold-hi),var(--gold));color:#151004}
.callbar .c2{background:rgba(13,13,16,.9);backdrop-filter:blur(14px);color:var(--white);border:1px solid var(--hair-d)}
@media(max-width:48rem){.callbar{display:grid}body{padding-bottom:4.6rem}}
@media(max-width:56rem){
  .topstrip{padding:.4rem .6rem 0}
  .langsw{gap:.1rem;padding:.2rem}
  .langsw button{padding:.5rem .62rem;font-size:.78rem;min-height:40px;display:inline-flex;align-items:center}
  .navwrap{top:3.6rem;padding-inline:.6rem}
  .pillnav{gap:.5rem;padding:.4rem .4rem .4rem .85rem;width:100%;justify-content:space-between}
  .brandlogo{height:1.5rem}
  .navcall{padding:0;min-height:44px;width:44px;height:44px;gap:0;justify-content:center;align-items:center;font-size:0;flex:none}
  .navcall .orb{width:1.7rem;height:1.7rem;margin:0}
  .phero h1{font-size:clamp(1.95rem,7.4vw,2.9rem);line-height:1.08}
  .phero .lede{font-size:1.05rem}
  .crumb{padding-top:7.5rem}
}
@media(max-width:22rem){ .langsw button{padding:.5rem .34rem;font-size:.7rem} }
/* team page */
.teamgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(18rem,1fr));gap:1.4rem}
.tcard{border-radius:1.5rem;padding:.45rem;background:rgba(255,255,255,.04);border:1px solid var(--hair-d)}
.tcard-in{border-radius:1.1rem;background:var(--coal);border:1px solid rgba(255,255,255,.05);padding:1.7rem;height:100%}
.tcard-in img{width:5.5rem;height:5.5rem;border-radius:50%;object-fit:cover;object-position:top;border:2px solid var(--hair-g);margin-bottom:1rem}
.tcard-in h3{color:var(--white);font-size:1.3rem;margin-bottom:.2rem}
.tcard-in .role{color:var(--gold-hi);font-size:.9rem;font-weight:700;font-family:var(--sans);margin-bottom:.9rem;display:block}
.tcard-in p{font-size:.95rem;color:var(--body-d);margin-bottom:.7rem}
.tcard-in .meta{font-size:.85rem;color:var(--mute-d);border-top:1px solid var(--hair-d);padding-top:.8rem;margin-top:.8rem}
.tcard-in .meta a{color:var(--gold-hi)}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}
"""

def head(title, desc, canonical, schema):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/png" sizes="512x512" href="./ucl-favicon.png">
<link rel="apple-touch-icon" href="./ucl-favicon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://uclaw.net/og/ucl-results-card.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#070708">
<script type="application/ld+json">{schema}</script>
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#main" data-i18n="skip">Skip to content</a>
<div class="topstrip">
  <div class="langsw" role="group" aria-label="Language">
    <button data-setlang="en" class="on">EN</button>
    <button data-setlang="es">ES</button>
    <button data-setlang="fa" lang="fa">دری</button>
    <button data-setlang="ur" lang="ur">اردو</button>
    <button data-setlang="ar" lang="ar">عربي</button>
  </div>
</div>
<div class="navwrap"><nav class="pillnav" aria-label="Main">
  <a class="brand" href="./index.html" aria-label="United Citizen Law — home">
    <img src="./ucl-logo-gold.svg" alt="United Citizen Law — a Fareed Injury Firm" class="brandlogo" width="188" height="37" decoding="async"></a>
  <ul>
    <li><a href="./index.html#practice-areas" data-i18n="nav.practice">Practice Areas</a></li>
    <li><a href="./index.html#results" data-i18n="nav.results">Results</a></li>
    <li><a href="./team.html" data-i18n="nav.team">Team</a></li>
    <li><a href="./index.html#faq" data-i18n="nav.faq">FAQ</a></li>
    <li><a href="#contact" data-i18n="nav.contact">Contact</a></li>
  </ul>
  <a class="btn btn-gold navcall" href="tel:{TEL}">{PHONE}
    <span class="orb" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.6 15.6 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.2 2.2Z"/></svg></span></a>
</nav></div>
"""

def review_btn(case, label="Start my free case review", cls="btn-gold"):
    return (f'<a class="btn {cls}" href="./index.html#review-{case}"><span>{label}</span>'
            f'<span class="orb" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 17 17 7M9 7h8v8"/></svg></span></a>')

def call_btn(label=f"Call {PHONE}", cls="btn-gold"):
    return (f'<a class="btn {cls}" href="tel:{TEL}"><span>{label}</span>'
            f'<span class="orb" aria-hidden="true"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.6 15.6 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.2 2.2Z"/></svg></span></a>')

def end_and_footer(case):
    return f"""
<section class="endcta" aria-labelledby="end-h">
  <div class="wrap">
    <span class="eyebrow" data-i18n="end.eyebrow">Free Consultation</span>
    <h2 id="end-h" data-i18n="end.h">You focus on healing. We'll handle the fight.</h2>
    <p data-i18n="end.p">Free consultation · No fee unless we win · Answered 24/7, in English, Español, دری, اردو &amp; العربية.</p>
    <div class="cta-row">{call_btn()}{review_btn(case, cls="btn-ghost")}</div>
  </div>
</section>

<section class="contact" id="contact" aria-labelledby="contact-h">
  <div class="wrap wide contact-grid">
    <div>
      <span class="eyebrow" data-i18n="contact.eyebrow">Contact Us</span>
      <h2 id="contact-h" data-i18n="contact.h">Come see us, call us, or we'll come to you</h2>
      <address itemscope itemtype="https://schema.org/PostalAddress">
        <strong>Office:</strong> <span itemprop="streetAddress">3301 Watt Ave, Suite 100</span>, <span itemprop="addressLocality">Sacramento</span>, <span itemprop="addressRegion">CA</span> <span itemprop="postalCode">95821</span><br>
        <strong>Phone:</strong> <a href="tel:{TEL}">{PHONE}</a> — answered 24/7<br>
        <strong>Email:</strong> <a href="mailto:clients@uclaw.net">clients@uclaw.net</a><br>
        <strong>Hours:</strong> Mon–Fri 8:00am–7:00pm (phones never close)<br>
        <a href="https://www.google.com/maps/search/?api=1&query=United+Citizen+Law+3301+Watt+Ave+Suite+100+Sacramento+CA+95821" target="_blank" rel="noopener">Open in Google Maps →</a>
      </address>
    </div>
    <div class="ccard"><div class="ccard-in">
      <h3>Not sure where to start?</h3>
      <p>Answer six quick questions and the right person will call you back — usually within minutes.</p>
      {review_btn(case)}
    </div></div>
  </div>
</section>

<footer class="site">
  <div class="wrap wide foot-grid">
    <div>
      <h3>United Citizen Law</h3>
      <address>
        3301 Watt Ave, Suite 100<br>Sacramento, CA 95821<br>
        <a href="tel:{TEL}">{PHONE}</a><br>
        <a href="mailto:clients@uclaw.net">clients@uclaw.net</a>
      </address>
      <p style="margin-top:.9rem">Office: Mon–Fri 8am–7pm<br>Phones answered 24/7 · Se habla español</p>
      <div class="social" role="group" aria-label="United Citizen Law on social media">
        <a href="https://www.instagram.com/unitedcitizenlaw/" target="_blank" rel="noopener" aria-label="Instagram — @unitedcitizenlaw"><svg viewBox="0 0 24 24" width="19" height="19" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5.2"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.15" fill="currentColor" stroke="none"/></svg></a>
        <a href="https://www.tiktok.com/@uclawca" target="_blank" rel="noopener" aria-label="TikTok — @uclawca"><svg viewBox="0 0 24 24" width="19" height="19" fill="currentColor" aria-hidden="true"><path d="M16.9 3c.35 2.2 1.72 3.78 3.85 4.06v2.55c-1.35.08-2.6-.32-3.83-1.05v6.36c0 3.5-2.83 6.08-6.19 5.86A5.87 5.87 0 0 1 5 14.9a5.86 5.86 0 0 1 6.35-5.32v2.72a3.17 3.17 0 0 0-3.5 3.05 3.17 3.17 0 0 0 6.32.2V3h2.73Z"/></svg></a>
        <a href="https://www.google.com/maps/search/?api=1&query=United+Citizen+Law+3301+Watt+Ave+Suite+100+Sacramento+CA+95821" target="_blank" rel="noopener" aria-label="Read our reviews on Google"><svg viewBox="0 0 24 24" width="19" height="19" fill="currentColor" aria-hidden="true"><path d="M12 2.6l2.63 5.72 6.27.72-4.66 4.23 1.25 6.18L12 16.98 6.51 19.45l1.25-6.18L3.1 9.04l6.27-.72L12 2.6Z"/></svg></a>
      </div>
      <a class="greviews" href="https://www.google.com/maps/search/?api=1&query=United+Citizen+Law+3301+Watt+Ave+Suite+100+Sacramento+CA+95821" target="_blank" rel="noopener">★★★★★ Read our Google reviews</a>
    </div>
    <div>
      <h3>Practice Areas</h3>
      <ul>
        <li><a href="./car-accident-lawyer-sacramento.html">Car Accidents</a></li>
        <li><a href="./truck-accident-lawyer-sacramento.html">Truck Accidents</a></li>
        <li><a href="./motorcycle-accident-lawyer-sacramento.html">Motorcycle Accidents</a></li>
        <li><a href="./rideshare-accident-lawyer-sacramento.html">Rideshare Accidents</a></li>
        <li><a href="./pedestrian-accident-lawyer-sacramento.html">Pedestrian &amp; Bicycle</a></li>
        <li><a href="./dog-bite-lawyer-sacramento.html">Dog Bites</a></li>
        <li><a href="./slip-and-fall-lawyer-sacramento.html">Slip &amp; Fall</a></li>
        <li><a href="./wrongful-death-lawyer-sacramento.html">Wrongful Death</a></li>
      </ul>
    </div>
    <div>
      <h3>Serving</h3>
      <ul><li>Sacramento</li><li>Elk Grove</li><li>Roseville</li><li>Folsom</li><li>Citrus Heights</li><li>Rancho Cordova</li></ul>
    </div>
    <div>
      <h3>Firm</h3>
      <ul>
        <li><a href="./index.html#sam-fareed">About Sam Fareed</a></li>
        <li><a href="./team.html">Our Team</a></li>
        <li><a href="./index.html#results">Case Results</a></li>
        <li><a href="./index.html#faq">FAQs</a></li>
        <li><a href="#contact" data-i18n="nav.contact">Contact</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap wide legal">
    <p>© 2026 United Citizen Law. Attorney advertising. Past results do not guarantee future outcomes. This website is for general information only and does not constitute legal advice; contacting the firm does not create an attorney-client relationship. Content reviewed by attorney Sam Fareed · Last updated July 11, 2026.</p>
  </div>
</footer>

<nav class="callbar" aria-label="Quick contact">
  <a class="c1" href="tel:{TEL}"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.6 15.6 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.4c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.4 0 .8-.2 1l-2.2 2.2Z"/></svg>Call now — free</a>
  <a class="c2" href="./index.html#review-{case}">Free case review</a>
</nav>

<script src="./i18n.js"></script>
</body></html>"""

def faq_schema(faqs):
    items=",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'%(_json(q),_json(a)) for q,a in faqs)
    return '{"@type":"FAQPage","mainEntity":['+items+']}'
def _json(s):
    import json; return json.dumps(s, ensure_ascii=False)

def page_schema(title, desc, canonical, service_name, service_type, faqs, crumb_name):
    graph = [
      '{"@type":"LegalService","@id":"https://uclaw.net/#firm","name":"United Citizen Law","telephone":"+1-916-800-8457","url":"https://uclaw.net/","address":{"@type":"PostalAddress","streetAddress":"3301 Watt Ave, Suite 100","addressLocality":"Sacramento","addressRegion":"CA","postalCode":"95821","addressCountry":"US"},"areaServed":{"@type":"AdministrativeArea","name":"Sacramento County"},"availableLanguage":["English","Spanish","Persian","Urdu","Hindi","Arabic"]}',
      '{"@type":"Service","name":%s,"serviceType":%s,"provider":{"@id":"https://uclaw.net/#firm"},"areaServed":{"@type":"City","name":"Sacramento"},"url":%s}'%(_json(service_name),_json(service_type),_json(canonical)),
      faq_schema(faqs),
      '{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://uclaw.net/"},{"@type":"ListItem","position":2,"name":%s,"item":%s}]}'%(_json(crumb_name),_json(canonical))
    ]
    return '{"@context":"https://schema.org","@graph":['+",".join(graph)+']}'

def steps_html(steps):
    return '<div class="steps">'+''.join(f'<div class="stepc"><div class="stepc-in"><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></div></div>' for t,p in steps)+'</div>'

def faq_html(faqs):
    out='<div class="wrap" style="max-width:52rem"><h2 style="margin-bottom:1.5rem">Common questions</h2>'
    for q,a in faqs:
        out+=f'<details><summary><span>{html.escape(q)}</span><span class="sig" aria-hidden="true">+</span></summary><div class="answer"><p>{html.escape(a)}</p></div></details>'
    return out+'</div>'

# ─────────────── PRACTICE PAGE DATA (original copy, grounded in the firm's real services) ───────────────
PAGES = [
{
 "case":"car","slug":"car-accident-lawyer-sacramento",
 "title":"Sacramento Car Accident Lawyer | United Citizen Law",
 "desc":"Injured in a Sacramento car accident? United Citizen Law fights insurers for maximum compensation — no fee unless we win. Free 24/7 consultation in 5 languages. (916) 800-8457.",
 "h1_pre":"Injured in a car accident?","h1_em":"We're on your side.",
 "service":"Car Accident Representation","stype":"Car accident personal injury law",
 "lede":"Whether you're the driver, passenger, or pedestrian, car accidents are traumatic events that can change the course of your life in an instant. On top of your injuries, you may feel scared to drive again or to walk down the street in your neighborhood. We understand your feelings of pain and fear, and we'll do everything we can to help you feel like your old self again. Our team has won enormous settlements for car accident victims, and we'll strive to do the same for you.",
 "answer":"United Citizen Law is a Sacramento car accident law firm that represents injured drivers, passengers, and pedestrians on a contingency basis — you pay nothing unless we win. Founding attorney Sam Fareed survived his own serious crash in 2017, so this fight is personal.",
 "why_h":"Why you need a lawyer before you call the insurance company",
 "why":[
   "After a collision you are not simply negotiating with the other driver — you are up against a corporation with trained adjusters, in-house lawyers, and a financial incentive to minimize your claim. The recorded statement they ask for on day one is designed to lock you into words that reduce your compensation later.",
   "An experienced car accident attorney levels that field. We handle every call, gather the police report and medical records, calculate the full value of your claim — including future treatment and lost earning capacity, not just today's bills — and refuse to let you be lowballed while you're still healing."
 ],
 "chips":["Rear-end collisions","Intersection & red-light crashes","Distracted & drunk drivers","Uninsured / hit-and-run","Multi-vehicle pileups","Passengers injured in any vehicle"],
 "steps":[
   ("We gather the evidence","From the moment you call, we preserve what matters — the police report, scene photos, vehicle damage, camera footage, and witness accounts — before it disappears."),
   ("We build the case","We document every injury and cost, coordinate your medical care, and prepare your claim as if it's going to trial, which is exactly what makes insurers take it seriously."),
   ("We win your recovery","We negotiate hard for full value and go to court if the insurer won't be fair. Our fee comes only out of what we recover for you."),
 ],
 "faqs":[
   ("How much does a car accident lawyer cost in Sacramento?","Nothing up front. We work on contingency — the consultation is free, and our fee comes only out of the compensation we recover. If we don't win, you owe no attorney fee."),
   ("How long does it take to settle a car accident claim?","With so many variables involved, estimating the length of a case can be difficult. Depending on the severity of your accident and the trajectory of the case, it could take upwards of two years to settle, though you may reach a resolution sooner. It's crucial to work with an experienced firm like United Citizen Law to ensure your case goes smoothly."),
   ("Should I contact the DMV after an accident?","In most cases, yes. If someone died in the accident, the DMV must be notified within ten days. Injuries and property damage over $1,000 also require involvement from the DMV. We can help you determine whether the DMV needs to be contacted and fill out any paperwork on your behalf, such as the SR-1 form."),
   ("How soon should I seek legal representation after a car accident?","Always reach out to an attorney as soon as possible. In California, you have two years to file a personal injury lawsuit, and three years for a property damage case. While that may seem like plenty of time, it can take months to build a strong case, so it's vital to seek help immediately after your incident so evidence can be discovered and documented."),
   ("Should I talk to the other driver's insurance company?","No — and never give a recorded statement before speaking with an attorney. Adjusters are trained to get you to say things that reduce your claim. Let us handle all communication."),
 ],
},
{
 "case":"truck","slug":"truck-accident-lawyer-sacramento",
 "title":"Sacramento Truck Accident Lawyer | United Citizen Law",
 "desc":"Hit by a commercial truck in Sacramento? Trucking companies send investigators within hours — you need the same speed. United Citizen Law, no fee unless we win. (916) 800-8457.",
 "h1_pre":"Hurt by a commercial truck?","h1_em":"Move as fast as they do.",
 "service":"Truck Accident Representation","stype":"Truck accident personal injury law",
 "lede":"A loaded semi can weigh 20 to 30 times more than your car, and the injuries reflect that. Trucking companies know it — which is why they dispatch rapid-response teams to the scene within hours to start building a defense. You deserve that same urgency working for you.",
 "answer":"United Citizen Law represents people seriously injured in commercial truck and big-rig crashes across the Sacramento region. We move immediately to preserve evidence like the truck's electronic logs and the carrier's records before they can be lost, and we pursue every liable party.",
 "why_h":"Truck cases are bigger, faster, and more complex than car crashes",
 "why":[
   "A truck wreck isn't just a bigger car crash. Liability can extend beyond the driver to the trucking company, the vehicle's owner, a maintenance contractor, or the company that loaded the cargo. Federal safety regulations govern driver hours, inspections, and record-keeping — and violations of those rules can be powerful evidence.",
   "Critical proof, like the truck's electronic control module data and the driver's logbooks, can be overwritten or discarded quickly. We act fast to send legal preservation notices and secure that evidence, then use it to hold every responsible party accountable for the full extent of your injuries."
 ],
 "chips":["Jackknife & rollover crashes","Rear-end by semi","Blind-spot & underride","Fatigued / overworked drivers","Improperly loaded cargo","Brake & maintenance failures"],
 "steps":[
   ("We secure the evidence","We immediately preserve the truck's data, driver logs, and inspection records before they can vanish, and document the scene while it's fresh."),
   ("We map the liability","We identify everyone responsible — driver, carrier, owner, loader, maintenance company — and the safety regulations they may have violated."),
   ("We pursue full value","Truck injuries are often catastrophic. We build for the long term — future surgeries, lost earning capacity, life care — and negotiate or try the case for everything it's worth."),
 ],
 "faqs":[
   ("Why do I need a special lawyer for a truck accident?","Truck cases involve federal trucking regulations, multiple potentially liable companies, and evidence that disappears quickly. Experience with commercial carriers and their insurers materially changes the outcome."),
   ("Who can be held responsible in a truck accident?","Potentially the driver, the trucking company, the vehicle owner, a maintenance provider, or the cargo loader. We investigate every link in the chain rather than settling with the first party who offers to pay."),
   ("How long do I have to file a truck accident claim in California?","Usually two years from the crash, but evidence like electronic logs can be lost far sooner. The earlier we're involved, the more we can preserve."),
   ("The trucking company already offered me a settlement — should I take it?","Speak with us first. Early offers are almost always far below the true long-term value of a serious truck-injury claim and are designed to close your case before that value is clear."),
   ("What does it cost to hire you?","Nothing unless we win. The consultation is free and our fee comes only from the compensation we recover for you."),
 ],
},
{
 "case":"moto","slug":"motorcycle-accident-lawyer-sacramento",
 "title":"Sacramento Motorcycle Accident Lawyer | United Citizen Law",
 "desc":"Injured riding in Sacramento? Insurers blame riders by default. United Citizen Law flips that script with evidence and relentless preparation. No fee unless we win. (916) 800-8457.",
 "h1_pre":"Injured on your motorcycle?","h1_em":"We flip the blame back.",
 "service":"Motorcycle Accident Representation","stype":"Motorcycle accident personal injury law",
 "lede":"Riders face a double injustice: they suffer the worst injuries in a crash, then get blamed for it by insurers who assume the motorcyclist must have been reckless. We reject that assumption and prove what actually happened.",
 "answer":"United Citizen Law represents injured motorcyclists throughout the Sacramento area. We counter the bias riders face by building claims on hard evidence — scene reconstruction, witness accounts, and the other driver's conduct — and we pursue full compensation for often life-altering injuries.",
 "why_h":"Bias against riders is real. Evidence beats it.",
 "why":[
   "Adjusters and juries often walk in assuming a motorcyclist was speeding or weaving. Left unchallenged, that assumption quietly cuts your compensation. A rider without an advocate is negotiating against a stereotype as much as an insurance company.",
   "We meet that head-on. By reconstructing the collision, securing independent witnesses, and documenting the at-fault driver's failure to look for riders, we replace assumption with fact — and fight for the full cost of injuries that, for riders, are frequently severe and permanent."
 ],
 "chips":["Left-turn & failure-to-yield","Lane-change & blind-spot","Dooring collisions","Road-hazard crashes","Distracted-driver impacts","Hit-and-run against riders"],
 "steps":[
   ("We reconstruct what happened","We document the scene, damage, and injuries and, where needed, work with reconstruction experts to show exactly how the other driver caused the crash."),
   ("We dismantle the blame","We gather the witnesses and evidence that counter the 'reckless rider' narrative before it can take hold with the insurer."),
   ("We fight for full recovery","Road rash, fractures, and traumatic injuries carry long-term costs. We build for all of them and hold the at-fault driver accountable."),
 ],
 "faqs":[
   ("Insurers say the crash was my fault because I ride. Is that true?","Often not. Many motorcycle crashes are caused by drivers who fail to see or yield to riders. We prove fault with evidence rather than letting bias decide your claim."),
   ("Does not wearing a helmet hurt my claim?","California requires helmets, and helmet use can become an issue — but it doesn't erase another driver's responsibility for causing the crash. We address it directly and keep the focus on their fault."),
   ("What compensation can I recover after a motorcycle accident?","Medical bills, lost income, future treatment and lost earning capacity, and pain and suffering. Rider injuries are frequently severe, and we build the claim for the long term."),
   ("How long do I have to file?","Generally two years from the date of the crash in California. Earlier is better so evidence and witness memories stay fresh."),
   ("What will it cost me?","Nothing unless we win. Free consultation, contingency fee."),
 ],
},
{
 "case":"rideshare","slug":"rideshare-accident-lawyer-sacramento",
 "title":"Sacramento Rideshare Accident Lawyer (Uber & Lyft) | United Citizen Law",
 "desc":"Hurt in an Uber or Lyft crash in Sacramento? Rideshare claims involve layered insurance most firms fumble. United Citizen Law knows which coverage applies. No fee unless we win.",
 "h1_pre":"Injured in a Lyft or Uber?","h1_em":"We're here to help.",
 "service":"Rideshare Accident Representation","stype":"Rideshare (Uber/Lyft) accident personal injury law",
 "lede":"Whether you were a passenger, another driver, or a pedestrian, a rideshare crash drops you into a maze of overlapping insurance policies — and the companies behind them have teams of lawyers whose job is to keep your settlement small.",
 "answer":"United Citizen Law handles Uber and Lyft accident claims across Sacramento. The coverage that applies depends on exactly what the rideshare driver was doing at the moment of the crash, and we know how to identify the right policy and hold a multinational company accountable.",
 "why_h":"Rideshare insurance is layered — and that's where claims go wrong",
 "why":[
   "Rideshare coverage changes based on the driver's status at the moment of impact: app off, app on but waiting for a ride, or actively carrying or en route to a passenger. Each phase can trigger a different policy with a different limit, and getting that wrong can leave real compensation on the table.",
   "Companies like Uber and Lyft staff their claims with adjusters and attorneys who understand these distinctions perfectly and use them to their advantage. We use that same knowledge for you — pinpointing every applicable policy and refusing to let a corporation minimize what you're owed."
 ],
 "chips":["Injured Uber/Lyft passengers","Hit by a rideshare driver","Pedestrians & cyclists struck","Multi-policy coverage disputes","App-status coverage gaps","Uninsured rideshare scenarios"],
 "steps":[
   ("We establish the coverage","We determine the driver's app status at the moment of the crash and identify every insurance policy that applies to your claim."),
   ("We build against the company","We document your injuries and losses and prepare a claim built to withstand a corporation's legal team, not just an individual driver."),
   ("We recover what you're owed","We negotiate against every applicable policy and litigate when needed so a complex coverage picture doesn't cost you your recovery."),
 ],
 "faqs":[
   ("What if I was the rideshare driver?","You can still be represented. Drivers injured in accidents they didn't cause can also pursue a settlement from the rideshare company's coverage. We'll evaluate your situation and fight for what you're owed."),
   ("Do rideshare companies have insurance?","Yes. These companies maintain sizable policies — Lyft, for example, provides up to $1 million in third-party liability coverage for accidents. Actual damages can exceed those limits, which is exactly why experienced representation matters."),
   ("What kind of compensation may I be entitled to?","Compensation can cover medical expenses, lost wages, and pain and suffering resulting from the crash. During your free consultation we'll give you a clearer picture based on your specific injuries and losses."),
   ("What if the rideshare driver wasn't technically 'on a trip'?","Coverage still may exist, but the applicable policy and limits change. This is exactly the distinction that trips up unrepresented claimants, and exactly what we sort out for you."),
   ("How long do I have to file a rideshare claim?","Generally two years in California. Because these claims involve corporate insurers, getting started early helps preserve evidence and app records."),
   ("What does representation cost?","Nothing unless we win. Free consultation, contingency fee."),
 ],
},
{
 "case":"ped","slug":"pedestrian-accident-lawyer-sacramento",
 "title":"Sacramento Pedestrian & Bicycle Accident Lawyer | United Citizen Law",
 "desc":"Struck as a pedestrian or cyclist in Sacramento? You had zero protection — and the law is on your side. United Citizen Law fights for full recovery. No fee unless we win.",
 "h1_pre":"Struck while walking or cycling?","h1_em":"The law is on your side.",
 "service":"Pedestrian & Bicycle Accident Representation","stype":"Pedestrian and bicycle accident personal injury law",
 "lede":"When a vehicle hits a person on foot or on a bike, there is no crumple zone, no airbag — just the human body against thousands of pounds of steel. The injuries are severe, and you deserve an advocate who treats them that way.",
 "answer":"United Citizen Law represents pedestrians and cyclists injured by vehicles throughout Sacramento. California law gives people crossing streets and riding in bike lanes strong protections, and we make sure those protections are enforced against the driver and their insurer.",
 "why_h":"Serious injuries, unfair assumptions — we correct both",
 "why":[
   "Drivers and their insurers sometimes claim the pedestrian 'came out of nowhere' or the cyclist 'wasn't visible.' In reality, drivers owe a duty to watch for people in crosswalks and bike lanes, and violating that duty is negligence. We gather the signal timing, witness accounts, and camera footage that establish what really happened.",
   "Because these injuries are frequently catastrophic — fractures, head injuries, long recoveries — the compensation must account for far more than the first hospital bill. We build claims around future treatment, lost income, and the lasting impact on your life."
 ],
 "chips":["Crosswalk collisions","Bike-lane & 'dooring' crashes","Failure-to-yield drivers","Distracted & speeding drivers","Hit-and-run victims","Injuries in parking lots"],
 "steps":[
   ("We prove the driver's fault","We collect signal timing, witness statements, and any available footage to establish the driver failed in their duty to watch for you."),
   ("We document the full injury","We coordinate your care and record the complete medical picture, including the long-term costs that early insurance offers ignore."),
   ("We enforce your recovery","We hold the driver and insurer accountable under California's protections for pedestrians and cyclists — through settlement or trial."),
 ],
 "faqs":[
   ("The driver says I stepped out suddenly. Does that end my claim?","No. Drivers have a legal duty to watch for pedestrians, especially near crosswalks. We use evidence to establish fault rather than accepting the driver's version."),
   ("Do I have a claim if I was jaywalking or outside a crosswalk?","Possibly yes. California's comparative fault rules mean you can still recover even if you were partly at fault; your recovery is reduced by your share. We work to minimize that share."),
   ("What if it was a hit-and-run?","You may be able to recover through uninsured motorist coverage. We pursue every available avenue so a fleeing driver doesn't leave you with the bill."),
   ("How long do I have to file?","Generally two years in California; shorter deadlines can apply if a government entity is involved. Call as soon as you can."),
   ("What will it cost me?","Nothing unless we win. Free consultation, contingency fee."),
 ],
},
{
 "case":"dog","slug":"dog-bite-lawyer-sacramento",
 "title":"Sacramento Dog Bite Lawyer | United Citizen Law",
 "desc":"Bitten by a dog in Sacramento? California holds owners strictly liable. United Citizen Law handles the claim while you heal. Free consultation, no fee unless we win. (916) 800-8457.",
 "h1_pre":"Bitten by an animal?","h1_em":"We'll help you fight back.",
 "service":"Dog Bite Representation","stype":"Dog bite and animal attack personal injury law",
 "lede":"“He's friendly” is what owners say right up until their dog isn't. A serious bite can leave lasting scars — physical and emotional — and change how you move through the world. We can't undo the attack, but we can pursue the compensation you deserve.",
 "answer":"United Citizen Law represents dog-bite and animal-attack victims across Sacramento. California is a strict-liability state, meaning a dog's owner is generally responsible for a bite even if the animal never showed aggression before — and we handle the claim so you can focus on healing.",
 "why_h":"Straightforward on paper, complicated in practice",
 "why":[
   "California's strict-liability rule sounds simple: the owner is responsible. But bites often happen on quiet streets or trails without cameras or witnesses, and some insurers now exclude certain breeds from coverage — complications that can quietly derail an unrepresented claim.",
   "An experienced dog-bite attorney cuts through that. We identify the responsible owner and their homeowner's or renter's insurance, gather what proof exists, consult experts where needed, and handle every detail so you can concentrate on recovering — physically and emotionally."
 ],
 "chips":["Serious & disfiguring bites","Scarring & nerve damage","Child victims","Attacks on walks & trails","Emotional trauma","Breed-exclusion disputes"],
 "steps":[
   ("We uncover the facts","We retrace what happened, identify the owner and their insurance, and gather any footage, witnesses, or records that support your account."),
   ("We build the narrative","We document the full injury, including scarring and emotional trauma, and consult experts where needed to establish the attack and its impact."),
   ("We pursue your settlement","We handle the insurer — including breed-exclusion tactics — and fight for compensation that reflects your pain, treatment, and lasting effects."),
 ],
 "faqs":[
   ("Is there a \"one-bite rule\" in California?","No. While some states give an animal a \"free bite\" before consequences, California is stricter. Even if you're the first person the dog has bitten, you can pursue a claim, because the owner is explicitly liable for their pet's actions."),
   ("What kind of damages can I claim in a dog attack case?","Every case is different, but generally you should be able to claim all medical bills related to your injury. You may also include lost wages, compensation for pain and suffering, and more. We'll give you a better idea of your potential compensation during your consultation."),
   ("What should I do after an animal attack?","First, seek medical attention for your injuries. Once you're well enough, contact a personal injury attorney experienced in dog-bite cases and keep all documentation — medical and otherwise — as evidence for your case."),
   ("The insurer says the breed is excluded from coverage. Now what?","Breed exclusions are a growing tactic. We work to identify all available coverage and hold the responsible party accountable despite them."),
   ("How long do I have to file a dog-bite claim?","Generally two years from the date of the attack in California. Earlier is better while evidence and witness memories are fresh."),
   ("What does it cost to hire you?","Nothing unless we win. Free consultation, contingency fee."),
 ],
},
{
 "case":"slip","slug":"slip-and-fall-lawyer-sacramento",
 "title":"Sacramento Slip & Fall / Premises Liability Lawyer | United Citizen Law",
 "desc":"Injured by a hazard on someone's property in Sacramento? Owners owe you a safe space. United Citizen Law holds negligent owners accountable. No fee unless we win. (916) 800-8457.",
 "h1_pre":"Slips, trips, and falls:","h1_em":"we handle them all.",
 "service":"Slip & Fall / Premises Liability Representation","stype":"Slip and fall and premises liability personal injury law",
 "lede":"From wet floors and broken stairs to poor lighting and neglected walkways, hazards can turn an ordinary errand into a life-changing injury. Property owners have a duty to keep their premises reasonably safe — and when they cut corners, they should answer for it.",
 "answer":"United Citizen Law handles slip-and-fall and premises-liability claims throughout Sacramento. We prove that a property owner or manager knew or should have known about a hazard and failed to fix it, and we pursue full compensation for the injuries that resulted.",
 "why_h":"“Just an accident” is what they want you to believe",
 "why":[
   "Property owners and their insurers love to frame a fall as your own clumsiness, or claim they had no idea the hazard existed. When the property belongs to a large corporation, expect a legal team dedicated to disputing your claim from day one.",
   "Premises cases turn on evidence and timing. We move quickly to secure maintenance logs, incident reports, and surveillance footage — the proof that shows the owner knew, or should have known, about the danger and failed to act. That's what turns 'just an accident' into accountability."
 ],
 "chips":["Wet & slippery floors","Broken stairs & railings","Poor lighting","Uneven walkways","Negligent security","Falling merchandise"],
 "steps":[
   ("We do our due diligence","We move fast to preserve maintenance logs, incident reports, and CCTV footage, and we speak with witnesses before details fade."),
   ("We build an airtight case","We establish that the owner knew or should have known about the hazard and failed to fix it, and we document the full extent of your injury."),
   ("We hold them accountable","We pursue the negligent owner and their insurer for the compensation you deserve — resolving by settlement where possible and by trial where necessary."),
 ],
 "faqs":[
   ("What do I have to prove in a slip-and-fall case?","Generally that the property owner or manager knew, or reasonably should have known, about a dangerous condition and failed to fix or warn about it — and that this caused your injury. We gather the evidence to establish each element."),
   ("The store says the fall was my fault. Does that end it?","No. Even if you were partly at fault, California's comparative fault rules let you recover, with your award reduced by your share. We work to keep that share low."),
   ("How quickly should I act?","Immediately. Surveillance footage is often overwritten within days or weeks, so the sooner we send preservation notices, the more evidence we can secure."),
   ("How long do I have to file?","Generally two years in California; claims against a government property owner can require notice within six months. Call as soon as possible."),
   ("What will representation cost?","Nothing unless we win. Free consultation, contingency fee."),
 ],
},
{
 "case":"other","slug":"wrongful-death-lawyer-sacramento",
 "title":"Sacramento Wrongful Death Lawyer | United Citizen Law",
 "desc":"Lost a loved one to someone's negligence in Sacramento? United Citizen Law pursues accountability and your family's security with compassion. No fee unless we win. (916) 800-8457.",
 "h1_pre":"Lost someone to negligence?","h1_em":"We pursue accountability.",
 "service":"Wrongful Death Representation","stype":"Wrongful death personal injury law",
 "lede":"No settlement can replace the person you've lost. But accountability, honest answers, and your family's financial security matter — and pursuing them can be part of how a family begins to move forward. We handle these cases with the care your loss demands.",
 "answer":"United Citizen Law represents families in Sacramento wrongful-death claims — losses caused by car and truck crashes, dangerous property, and other negligence. We pursue the responsible parties for the family's financial and emotional losses while handling the legal weight so you can grieve.",
 "why_h":"When your family is grieving, you shouldn't fight alone",
 "why":[
   "In the aftermath of a sudden loss, families face funeral costs, lost income, and a legal system that feels impossible to face while grieving. Insurers, meanwhile, move to limit what they pay. You should not have to carry that fight alone.",
   "We take on the investigation, the paperwork, and the negotiation so your family doesn't have to. We pursue the full range of losses California law allows — from financial support the person would have provided to the loss of their love, companionship, and guidance — with the sensitivity these cases require."
 ],
 "chips":["Fatal car & truck crashes","Pedestrian & bicycle deaths","Dangerous property","Negligent security","Catastrophic injury losses","Support for surviving families"],
 "steps":[
   ("We handle the weight","We take over the investigation, insurance communication, and paperwork so your family can focus on each other, not on a legal fight."),
   ("We establish responsibility","We gather the evidence needed to prove who caused your loss and how, building a claim that holds them fully accountable."),
   ("We pursue your family's future","We seek the full compensation California allows — financial support, funeral costs, and the loss of love and companionship — with compassion at every step."),
 ],
 "faqs":[
   ("Who can file a wrongful death claim in California?","Generally the spouse or domestic partner, children, and certain other dependents or heirs. We help your family understand who has the right to bring the claim in your specific situation."),
   ("What can a wrongful death claim recover?","It can include financial losses such as lost support and funeral costs, as well as the loss of the person's love, companionship, and guidance. We pursue the full range the law allows."),
   ("Is a wrongful death claim the same as a criminal case?","No. A wrongful death claim is a civil action for your family's losses and can proceed regardless of whether criminal charges are filed. The goal is accountability and your family's security."),
   ("How long do we have to file?","Generally two years in California, though shorter deadlines can apply when a government entity is involved. Speaking with us early protects your family's rights."),
   ("What does it cost our family?","Nothing unless we win. The consultation is free and our fee comes only from any recovery."),
 ],
},
{
 "case":"cat","slug":"catastrophic-injury-lawyer-sacramento",
 "title":"Sacramento Catastrophic Injury Lawyer | United Citizen Law",
 "desc":"Life-changing injury — spinal cord, brain, amputation, or burns? United Citizen Law builds the full life-care case for maximum recovery. No fee unless we win. (916) 800-8457.",
 "h1_pre":"A catastrophic injury?","h1_em":"We fight for your whole future.",
 "service":"Catastrophic Injury Representation","stype":"Catastrophic injury personal injury law",
 "lede":"Some injuries don't just heal and fade — they reshape the rest of your life. A spinal cord injury, traumatic brain injury, amputation, or severe burn can mean surgeries, therapy, adapted housing, and lost earning power for decades. When the stakes are this high, the case has to be built for a lifetime, not a season.",
 "answer":"United Citizen Law represents Sacramento clients and families facing the most serious, life-altering injuries — spinal cord damage, traumatic brain injury, amputation, severe burns, and other permanent harm. We build these cases around the full lifetime cost of the injury, on a contingency basis, so you pay nothing unless we win.",
 "why_h":"Why catastrophic cases demand a different level of preparation",
 "why":[
   "When an injury is permanent, the biggest number in your case isn't today's hospital bill — it's the decades of care, equipment, home modification, and lost income ahead. Insurers know this, which is why they move quickly to settle catastrophic claims cheaply before the true, lifelong cost is ever documented.",
   "We do the opposite. We bring in the medical, economic, and life-care experts needed to prove exactly what your future requires and what it will cost, and we prepare every case as if it is going to trial. That preparation is what forces insurers to value your recovery honestly instead of hoping you'll accept less while you're overwhelmed."
 ],
 "chips":["Spinal cord injury & paralysis","Traumatic brain injury (TBI)","Amputation & limb loss","Severe burns & scarring","Multiple fractures","Injuries requiring lifelong care"],
 "steps":[
   ("We preserve everything","We secure the evidence and get you connected with the right specialists immediately, documenting the injury and its trajectory from the very start."),
   ("We prove the lifetime cost","We work with medical and life-care experts and economists to build a complete picture of your future — surgeries, care, equipment, home changes, and lost earning capacity."),
   ("We pursue full value","We negotiate from a position of trial-ready strength and go to court when insurers won't be fair, so your recovery reflects a lifetime — not a moment."),
 ],
 "faqs":[
   ("What counts as a catastrophic injury?","Generally, an injury that causes permanent impairment or long-term disability — such as spinal cord injury, traumatic brain injury, amputation, or severe burns. These cases involve far higher lifetime costs, which is why they need specialized handling."),
   ("How is compensation different in a catastrophic case?","Beyond medical bills and lost wages, catastrophic claims account for future medical care, in-home assistance, assistive equipment, home and vehicle modifications, lost earning capacity, and the pain and loss of quality of life over your lifetime."),
   ("What is a life-care plan?","A life-care plan is a detailed, expert-prepared projection of every treatment, service, and piece of equipment you'll need for the rest of your life, with costs. It's central to proving the true value of a catastrophic injury claim."),
   ("How soon should we call after a serious injury?","As early as possible. Critical evidence and medical documentation are strongest early, and building a catastrophic case takes time. California generally allows two years to file, but earlier is always better."),
   ("What does it cost to hire you?","Nothing up front. We work on contingency — the consultation is free and our fee comes only out of what we recover for you. If we don't win, you owe no attorney fee."),
 ],
},
]

def build_practice(pg):
    canonical=f"https://uclaw.net/{pg['slug']}.html"
    schema=page_schema(pg['title'],pg['desc'],canonical,pg['service'],pg['stype'],pg['faqs'],pg['title'].split(' | ')[0])
    ik={'other':'wd'}.get(pg['case'], pg['case'])   # i18n key prefix (wrongful-death case is 'other')
    out=head(pg['title'],pg['desc'],canonical,schema)
    out+=f"""<main id="main">
<div class="wrap crumb"><a href="./index.html" data-i18n="crumb.home">Home</a> › <span>{html.escape(pg['title'].split(' | ')[0])}</span></div>
<section class="phero"><div class="wrap">
  <span class="eyebrow" data-i18n="pp.eyebrow">Sacramento Personal Injury</span>
  <h1><span data-i18n="p.{ik}.pre">{html.escape(pg['h1_pre'])}</span> <em data-i18n="p.{ik}.em">{html.escape(pg['h1_em'])}</em></h1>
  <p class="lede" data-i18n="p.{ik}.lede">{html.escape(pg['lede'])}</p>
  <div class="cta-row">{call_btn()}{review_btn(pg['case'], cls='btn-ghost')}</div>
  <p class="risk" data-i18n="pp.risk">No fee unless we win. Hospitalized? We come to you.</p>
</div></section>

<section class="prose light"><div class="wrap">
  <p class="lead-answer">{html.escape(pg['answer'])}</p>
  <h2>{html.escape(pg['why_h'])}</h2>
  {''.join(f'<p>{html.escape(x)}</p>' for x in pg['why'])}
  <div class="chips">{''.join(f'<span class="chip">{html.escape(c)}</span>' for c in pg['chips'])}</div>
</div></section>

<section class="prose"><div class="wrap">
  <h2 data-i18n="pp.process.h">Our proven three-step process</h2>
  <p data-i18n="pp.process.p">We bring the same tested framework to every case while accounting for the details of your unique situation.</p>
  {steps_html(pg['steps'])}
</div></section>

<section class="prose light"><div class="wrap">{faq_html(pg['faqs'])}</div></section>
</main>
"""
    out+=end_and_footer(pg['case'])
    return out

# ─────────────── TEAM PAGE ───────────────
TEAM=[
 ("sam-fareed","Sam Fareed","Founding Attorney","",
  "Sam Fareed founded United Citizen Law after surviving a serious car accident in 2017 while an undergraduate at UCLA. Navigating surgeries and insurance adjusters from the victim's side, he made a promise that no one should have to fight that battle alone — and built the firm he couldn't find. Super Lawyers Rising Star 2021–2026 and recognized by Forbes among Sacramento's top injury lawyers.",
  "Founding Attorney"),
 ("shereen-ghaith","Shereen Ghaith","Associate Attorney","Ext. 335",
  "Shereen holds a B.S. in Business with a concentration in Marketing and a B.A. in Communications focused on Public Relations, both from California State University, Sacramento, as well as a J.D. from McGeorge School of Law. Beyond her professional accomplishments, Shereen finds joy in life's simple pleasures, often spending time at the beach or lake with loved ones.",
  None),
 ("homaira-laila-fareed","Homaira Laila Fareed","Associate Attorney","Ext. 105",
  "Laila holds a B.A. from the University of California, Davis, and a J.D. from Lincoln Law School of Sacramento. She has been with United Citizen Law since the start of her career, beginning as a law clerk. Today she handles many aspects of personal injury cases — client consultations, legal research, drafting documents, negotiating settlements, and representing clients in court. Outside of work, Laila is a devoted mother of three who enjoys hiking and cooking with loved ones.",
  "lailaf@uclaw.net"),
 ("zahid-sher-fareed","Zahid “Sher” Fareed","Client Services Director","Ext. 102",
  "Zahid holds a B.A. in History from California State University, Sacramento. As Head of Client Liaison, he ensures clients receive attentive, professional service and oversees all pre-litigation cases, addressing clients' needs efficiently from the start. He also leads and trains his team with an emphasis on communication and client relationships. Outside of work, Zahid is a dedicated husband and father of three who enjoys traveling and fitness.",
  "clients@uclaw.net"),
 ("abdul-wardak","Abdul Wardak","Case Manager","Ext. 340",
  "Abdul is the first point of contact for clients and the face of the firm, handling new intakes and guiding clients through the process. Fluent in English, Dari, and Pashto, he connects with a diverse clientele and ensures smooth communication throughout case management. In his spare time he enjoys football and basketball — a big Warriors and 49ers fan.",
  "clients@uclaw.net"),
 ("richard-prasad","Richard Prasad","Paralegal","Ext. 334",
  "Richard began his studies at Sacramento City College and continues building his knowledge, particularly in legal and medical research. At the firm he drafts demands, analyzes records, and files complaints; his attention to detail and dedication to clients help keep everything running smoothly. Outside of work he enjoys reading, gardening, and cooking.",
  "sfareed@uclaw.net"),
 ("roya-fareed","Roya Fareed","Controller","Ext. 341",
  "Roya oversees all financial operations of the firm. With more than eight years of experience in banking — including wealth management and financial planning — she brings strategic, analytical strength to securing the capital that keeps the firm ready for trial and positioned for growth. An avid traveler who has visited more than 18 countries, she credits that experience with keeping her open-minded and approachable with a diverse clientele.",
  "reyah.ucl@outlook.com"),
 ("yasir-albadran","Yasir Albadran","Office Clerk","Ext. 103",
  "Yasir holds a B.A. in Physical Education from the University of Baghdad, Iraq. He supports daily office operations — managing documents, scheduling, and client communications — and, as a first point of contact for many clients, specializes in assisting Arabic-speaking individuals with clarity and precision. Outside of work he enjoys time with family, basketball, traveling, and hiking.",
  "clients@uclaw.net"),
 ("jesse-fareed","Jesse Fareed","Office Clerk","",
  "Jesse frequently works in the field, handling tasks for client cases and making sure everything is done on time, including driving clients to appointments and keeping them comfortable with the process. Outside of work he has a strong interest in culture and entertainment, enjoying classic films and classical music.",
  "clients@uclaw.net"),
]

def build_team():
    canonical="https://uclaw.net/team.html"
    members=",".join('{"@type":"Person","name":%s,"jobTitle":%s,"worksFor":{"@id":"https://uclaw.net/#firm"}}'%(_json(n),_json(r)) for _,n,r,_,_,_ in TEAM)
    schema='{"@context":"https://schema.org","@graph":[{"@type":"LegalService","@id":"https://uclaw.net/#firm","name":"United Citizen Law","telephone":"+1-916-800-8457","url":"https://uclaw.net/","employee":['+members+']},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://uclaw.net/"},{"@type":"ListItem","position":2,"name":"Our Team","item":"https://uclaw.net/team/"}]}]}'
    out=head("Meet Our Team | Sacramento Personal Injury Attorneys | United Citizen Law",
             "Meet the United Citizen Law team — attorneys, case managers, and staff serving Sacramento in English, Spanish, Dari, Pashto, Urdu, Hindi, and Arabic. Real people who answer your call and build your case.",
             canonical, schema)
    cards=""
    for slug,name,role,ext,bio,email in TEAM:
        meta=[]
        if ext: meta.append(html.escape(ext))
        if email and '@' in email: meta.append(f'<a href="mailto:{email}">{email}</a>')
        meta.append(f'<a href="tel:{TEL}">{PHONE}</a>')
        cards+=f'<div class="tcard"><div class="tcard-in"><img src="./team/{slug}.jpg" alt="{html.escape(name)}, {html.escape(role)} at United Citizen Law" width="88" height="88" loading="lazy" decoding="async"><h3>{html.escape(name)}</h3><span class="role">{html.escape(role)}</span><p>{html.escape(bio)}</p><div class="meta">{" · ".join(meta)}</div></div></div>'
    out+=f"""<main id="main">
<div class="wrap crumb"><a href="./index.html">Home</a> › <span>Our Team</span></div>
<section class="phero"><div class="wrap wide">
  <span class="eyebrow">The People In Your Corner</span>
  <h1>One team. Five languages. <em>Your case by name.</em></h1>
  <p class="lede">No call centers, no case mills. These are the actual people who answer your call, build your case, and fight for your recovery — and many of them speak your language.</p>
  <div class="cta-row">{call_btn()}{review_btn('car', cls='btn-ghost')}</div>
</div></section>
<section class="prose" style="padding-top:1rem"><div class="wrap wide">
  <div class="teamgrid">{cards}</div>
</div></section>
</main>
"""
    out+=end_and_footer('car')
    return out

# ─────────────── WRITE ───────────────
for pg in PAGES:
    with open(os.path.join(BASE, pg['slug']+'.html'),'w',encoding='utf-8') as f:
        f.write(build_practice(pg))
    print('wrote', pg['slug']+'.html')
with open(os.path.join(BASE,'team.html'),'w',encoding='utf-8') as f:
    f.write(build_team())
print('wrote team.html')
