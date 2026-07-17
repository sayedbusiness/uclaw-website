/* UCL Assistant — United Citizen Law website concierge.
 * Strictly scoped to the firm: FAQs, lead qualification, document intake,
 * appointment requests, SMS confirmations. Anything off-topic is redirected.
 * Works with zero server config via the on-page rules engine; if the
 * chat-llm edge function has an API key configured it answers low-confidence
 * questions with the LLM (same strict scope, enforced server-side).
 * Data: Supabase (chat_leads / appointments / chat_docs / storage intake-docs).
 */
(function () {
  'use strict';
  if (window.__UCL_ASSIST__) return; window.__UCL_ASSIST__ = 1;
  var SB = window.UCL_SB || {}; var KB = window.UCL_KB || null;
  if (!SB.u || !SB.k || !KB) return;

  var PHONE = KB.firm.phone, TEL = KB.firm.tel;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── styles ── */
  var css = ''
  + '.ucla-btn{position:fixed;z-index:96;right:1rem;bottom:1.1rem;width:58px;height:58px;border-radius:50%;border:1px solid rgba(240,207,106,.5);background:linear-gradient(155deg,#f0cf6a,#d4a72c);color:#151004;cursor:pointer;box-shadow:0 14px 38px rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;transition:transform .5s cubic-bezier(.16,1,.3,1),box-shadow .5s}'
  + '.ucla-btn:hover{transform:translateY(-3px)}.ucla-btn:active{transform:scale(.94)}'
  + '.ucla-btn svg{pointer-events:none}'
  + '.ucla-btn .ucla-dot{position:absolute;top:2px;right:2px;width:13px;height:13px;border-radius:50%;background:#3ddc84;border:2px solid #0a0a0c}'
  + '@media(max-width:48rem){.ucla-btn{bottom:calc(5.9rem + env(safe-area-inset-bottom));right:.8rem;width:54px;height:54px}}'
  + '.ucla-panel{position:fixed;z-index:120;right:1rem;bottom:1.1rem;width:min(392px,calc(100vw - 1.6rem));height:min(640px,calc(100dvh - 2.4rem));display:none;flex-direction:column;background:#0d0d10;border:1px solid rgba(212,167,44,.28);border-radius:1.25rem;box-shadow:0 40px 90px rgba(0,0,0,.7);overflow:hidden}'
  + '.ucla-panel.open{display:flex}'
  + 'html.js .ucla-panel{opacity:0;transform:translateY(18px) scale(.98);transition:opacity .45s cubic-bezier(.16,1,.3,1),transform .45s cubic-bezier(.16,1,.3,1)}'
  + 'html.js .ucla-panel.in{opacity:1;transform:none}'
  + '@media(prefers-reduced-motion:reduce){html.js .ucla-panel{transition:none;opacity:1;transform:none}}'
  + '@media(max-width:48rem){.ucla-panel{right:.5rem;left:.5rem;width:auto;bottom:calc(.55rem + env(safe-area-inset-bottom));height:min(78dvh,600px)}}'
  + '.ucla-head{display:flex;align-items:center;gap:.7rem;padding:.95rem 1.05rem;background:linear-gradient(160deg,#141418,#0d0d10);border-bottom:1px solid rgba(212,167,44,.22)}'
  + '.ucla-head img{height:30px;width:auto}'
  + '.ucla-head-t{flex:1;min-width:0}'
  + '.ucla-head-t b{display:block;font-family:Georgia,serif;font-weight:500;color:#fff;font-size:1.02rem;letter-spacing:.02em}'
  + '.ucla-head-t span{display:flex;align-items:center;gap:.35rem;font-size:.74rem;color:#9a9483}'
  + '.ucla-head-t span i{width:7px;height:7px;border-radius:50%;background:#3ddc84;display:inline-block}'
  + '.ucla-x{width:2.1rem;height:2.1rem;border-radius:50%;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);color:#fff;cursor:pointer;font-size:.95rem;line-height:1}'
  + '.ucla-x:focus-visible,.ucla-btn:focus-visible{outline:2px solid #f0cf6a;outline-offset:2px}'
  + '.ucla-log{flex:1;overflow-y:auto;padding:1rem 1rem 0.4rem;display:flex;flex-direction:column;gap:.6rem;scroll-behavior:smooth}'
  + '@media(prefers-reduced-motion:reduce){.ucla-log{scroll-behavior:auto}}'
  + '.ucla-m{max-width:86%;padding:.68rem .9rem;border-radius:1rem;font-size:.95rem;line-height:1.55;white-space:pre-wrap;word-wrap:break-word}'
  + 'html.js .ucla-m{animation:uclaIn .4s cubic-bezier(.16,1,.3,1) both}'
  + '@keyframes uclaIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}'
  + '@media(prefers-reduced-motion:reduce){html.js .ucla-m{animation:none}}'
  + '.ucla-m.bot{align-self:flex-start;background:#17171c;color:#d9d4c6;border:1px solid rgba(255,255,255,.07);border-bottom-left-radius:.3rem}'
  + '.ucla-m.bot a{color:#f0cf6a}'
  + '.ucla-m.user{align-self:flex-end;background:linear-gradient(155deg,#f0cf6a,#d4a72c);color:#181204;font-weight:600;border-bottom-right-radius:.3rem}'
  + '.ucla-typing{align-self:flex-start;display:flex;gap:.28rem;padding:.75rem 1rem;background:#17171c;border:1px solid rgba(255,255,255,.07);border-radius:1rem;border-bottom-left-radius:.3rem}'
  + '.ucla-typing i{width:7px;height:7px;border-radius:50%;background:#8d8672;animation:uclaB 1.1s infinite}'
  + '.ucla-typing i:nth-child(2){animation-delay:.18s}.ucla-typing i:nth-child(3){animation-delay:.36s}'
  + '@keyframes uclaB{0%,60%,100%{opacity:.35;transform:none}30%{opacity:1;transform:translateY(-4px)}}'
  + '@media(prefers-reduced-motion:reduce){.ucla-typing i{animation:none}}'
  + '.ucla-chips{display:flex;flex-wrap:wrap;gap:.45rem;padding:.15rem 0 .2rem}'
  + '.ucla-chip{border:1px solid rgba(212,167,44,.4);background:rgba(212,167,44,.08);color:#f0cf6a;border-radius:999px;padding:.5rem .92rem;font-size:.86rem;font-weight:700;cursor:pointer;transition:transform .35s cubic-bezier(.16,1,.3,1),background .35s;min-height:38px}'
  + '.ucla-chip:hover{transform:translateY(-2px);background:rgba(212,167,44,.16)}'
  + '.ucla-chip:focus-visible{outline:2px solid #f0cf6a;outline-offset:2px}'
  + '.ucla-in{display:flex;gap:.5rem;padding:.8rem;border-top:1px solid rgba(255,255,255,.08);background:#0a0a0d}'
  + '.ucla-in input{flex:1;min-width:0;background:#15151a;border:1px solid rgba(255,255,255,.12);color:#fff;border-radius:.8rem;padding:.72rem .9rem;font-size:16px}'
  + '.ucla-in input:focus{outline:2px solid rgba(240,207,106,.6);outline-offset:1px}'
  + '.ucla-send{width:46px;height:46px;flex:none;border-radius:50%;border:none;background:linear-gradient(155deg,#f0cf6a,#d4a72c);color:#151004;cursor:pointer;display:flex;align-items:center;justify-content:center}'
  + '.ucla-send:disabled{opacity:.45;cursor:default}'
  + '.ucla-file{display:none}'
  + '.ucla-note{font-size:.72rem;color:#77715f;text-align:center;padding:.25rem .9rem .6rem;background:#0a0a0d}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  /* ── dom ── */
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  var btn = el('button', 'ucla-btn');
  btn.setAttribute('aria-label', 'Chat with United Citizen Law — free case questions 24/7');
  btn.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><path d="M21 11.5c0 4.1-4 7.5-9 7.5-1 0-2-.14-2.9-.4L4 20l1.3-3.1C3.9 15.6 3 13.7 3 11.5 3 7.4 7 4 12 4s9 3.4 9 7.5Z"/><path d="M8.5 10h7M8.5 13h4.5"/></svg><span class="ucla-dot" aria-hidden="true"></span>';
  var panel = el('div', 'ucla-panel');
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'United Citizen Law assistant');
  panel.innerHTML =
    '<div class="ucla-head"><img src="./ucl-favicon.png" alt="" width="30" height="30">'
    + '<div class="ucla-head-t"><b>United Citizen Law</b><span><i aria-hidden="true"></i>Concierge — here 24/7</span></div>'
    + '<button class="ucla-x" aria-label="Close chat">&#10005;</button></div>'
    + '<div class="ucla-log" aria-live="polite"></div>'
    + '<div class="ucla-in"><input type="text" autocomplete="off" placeholder="Ask about your case, fees, our team…" aria-label="Message">'
    + '<input type="file" class="ucla-file" multiple accept=".pdf,.jpg,.jpeg,.png,.heic,.webp">'
    + '<button class="ucla-send" aria-label="Send"><svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.4 20.6 21.8 12 3.4 3.4l.01 6.6L15 12 3.41 14z"/></svg></button></div>'
    + '<div class="ucla-note">General information only — not legal advice. For advice on your case, the consultation is free.</div>';
  document.body.appendChild(btn); document.body.appendChild(panel);
  var log = panel.querySelector('.ucla-log'), input = panel.querySelector('.ucla-in input'),
      send = panel.querySelector('.ucla-send'), fileIn = panel.querySelector('.ucla-file'),
      closeX = panel.querySelector('.ucla-x');

  /* ── state ── */
  var S = { open: false, transcript: [], ctx: {}, flow: null, step: 0, leadId: null, busy: false, greeted: false };
  try { var saved = sessionStorage.getItem('ucla_s'); if (saved) { var sv = JSON.parse(saved); S.transcript = sv.t || []; S.ctx = sv.c || {}; S.leadId = sv.l || null; } } catch (e) {}
  function persist() { try { sessionStorage.setItem('ucla_s', JSON.stringify({ t: S.transcript.slice(-40), c: S.ctx, l: S.leadId })); } catch (e) {} }

  /* ── rendering ── */
  function scrollEnd() { log.scrollTop = log.scrollHeight; }
  function say(html, cls) { var m = el('div', 'ucla-m ' + (cls || 'bot'), html); log.appendChild(m); scrollEnd(); return m; }
  function bot(text, html) { S.transcript.push({ role: 'assistant', content: text }); persist(); return say(html || esc(text), 'bot'); }
  function user(text) { S.transcript.push({ role: 'user', content: text }); persist(); return say(esc(text), 'user'); }
  function esc(s) { var d = document.createElement('div'); d.textContent = String(s); return d.innerHTML.replace(/\n/g, '<br>'); }
  function typing() { var t = el('div', 'ucla-typing', '<i></i><i></i><i></i>'); log.appendChild(t); scrollEnd(); return t; }
  function chips(list) {
    var wrap = el('div', 'ucla-chips');
    list.forEach(function (c) {
      var b = el('button', 'ucla-chip'); b.type = 'button'; b.textContent = c.label;
      b.addEventListener('click', function () { wrap.remove(); handle(c.label, c.action); });
      wrap.appendChild(b);
    });
    log.appendChild(wrap); scrollEnd(); return wrap;
  }
  function clearChips() { var c = log.querySelectorAll('.ucla-chips'); c.forEach(function (x) { x.remove(); }); }

  /* ── supabase (raw fetch; anon key is public by design, RLS enforces limits) ── */
  function sbFetch(path, opts) {
    opts = opts || {}; opts.headers = Object.assign({ apikey: SB.k, Authorization: 'Bearer ' + SB.k }, opts.headers || {});
    return fetch(SB.u + path, opts);
  }
  function uuid() {
    if (crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 3 | 8)).toString(16);
    });
  }
  /* anon can INSERT but (by design) not SELECT these tables, so we generate the
     id client-side and ask PostgREST for return=minimal */
  function sbInsert(table, row) {
    if (!row.id) row.id = uuid();
    return sbFetch('/rest/v1/' + table, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Prefer: 'return=minimal' },
      body: JSON.stringify(row)
    }).then(function (r) { if (!r.ok) throw new Error(table + ' ' + r.status); return row; });
  }
  function sbFn(name, body) {
    return sbFetch('/functions/v1/' + name, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
    }).then(function (r) { return r.json(); }).catch(function () { return { ok: false }; });
  }

  /* ── knowledge engine ── */
  function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9\s$]/g, ' ').replace(/\s+/g, ' ').trim(); }
  var INTENTS = [
    { id: 'greet', kw: ['hi', 'hello', 'hey', 'salaam', 'salam', 'hola', 'good morning', 'good afternoon', 'good evening'], t: 1.3 },
    { id: 'thanks', kw: ['thank', 'thanks', 'gracias', 'appreciate'], t: 1.3 },
    { id: 'fees', kw: ['fee', 'fees', 'cost', 'price', 'charge', 'expensive', 'afford', 'pay', 'money', 'contingency', 'free'], t: 1.3 },
    { id: 'deadline', kw: ['statute', 'limitations', 'deadline', 'too late', 'how long do i have', 'time limit', 'expire'], t: 1.3 },
    { id: 'process', kw: ['process', 'steps', 'how does it work', 'what happens', 'timeline', 'how long does a case'], t: 1.3 },
    { id: 'languages', kw: ['language', 'spanish', 'espanol', 'dari', 'farsi', 'pashto', 'urdu', 'hindi', 'arabic', 'translator', 'interpreter'], t: 1.3 },
    { id: 'location', kw: ['where', 'address', 'office', 'located', 'location', 'hours', 'open', 'directions', 'parking'], t: 1.3 },
    { id: 'human', kw: ['human', 'person', 'call me', 'talk to someone', 'speak to', 'phone number', 'call you', 'representative', 'agent'], t: 1.3 },
    { id: 'results', kw: ['results', 'won', 'win', 'settlement amounts', 'how much have', 'track record', 'reviews', 'rating', 'million'], t: 1.3 },
    { id: 'team', kw: ['team', 'who works', 'attorney', 'lawyer name', 'sam fareed', 'staff', 'who will handle'], t: 1.3 },
    { id: 'worth', kw: ['worth', 'how much can i get', 'compensation', 'value of my case', 'payout', 'damages'], t: 1.3 },
    { id: 'insurance', kw: ['insurance called', 'adjuster', 'recorded statement', 'insurance company wants', 'should i talk to insurance', 'offer from insurance'], t: 1.3 },
    { id: 'hospitalized', kw: ['hospital', 'hospitalized', 'cant come in', 'can not travel', 'come to me', 'home visit'], t: 1.3 },
    { id: 'schedule', kw: ['appointment', 'schedule', 'book', 'consultation', 'meet', 'come in', 'visit'], t: 1.3 },
    { id: 'docs', kw: ['document', 'upload', 'send photos', 'police report', 'medical bills', 'records', 'send you', 'attach'], t: 1.3 },
    { id: 'qualify', kw: ['case review', 'free review', 'do i have a case', 'start my case', 'sign up', 'get started', 'evaluate'], t: 1.3 }
  ];
  KB.pages.forEach(function (p) { INTENTS.push({ id: 'page:' + p.slug, kw: p.kw, t: 1.3 }); });

  function detect(text) {
    var q = ' ' + norm(text) + ' ', best = null, bestScore = 0;
    INTENTS.forEach(function (it) {
      var s = 0;
      it.kw.forEach(function (k) { if (q.indexOf(' ' + k + ' ') >= 0 || (k.length > 5 && q.indexOf(k) >= 0)) s += (k.indexOf(' ') > 0 ? 2.2 : 1.4); });
      if (s >= it.t && s > bestScore) { best = it; bestScore = s; }
    });
    return best ? { id: best.id, score: bestScore } : null;
  }

  var F = KB.firm;
  var ANSWERS = {
    fees: function () { return 'Simple: the consultation is free, and we work on contingency — you pay $0 unless we win your case. No hourly bills, no retainer, ever.'; },
    deadline: function () { return 'In California you generally have 2 years from the injury to file (3 for property damage), and claims against a government entity need notice within 6 months. Deadlines can be shorter than people think — the free case review takes about a minute and tells you where you stand.'; },
    process: function () { return 'Three steps: 1) we gather the evidence fast — police report, photos, camera footage, witnesses. 2) We build your case like it’s going to trial. 3) We negotiate for full value, and if the insurer won’t be fair, we take them to court. You focus on healing.'; },
    languages: function () { return 'We serve clients in English, Español, دری/فارسی (Dari/Farsi), Pashto, اردو/हिन्दी (Urdu/Hindi), and العربية (Arabic). Call ' + PHONE + ' and a team member who speaks your language will help you.'; },
    location: function () { return 'We’re at 3301 Watt Ave, Suite 100, Sacramento, CA 95821. Office hours Mon–Fri 8am–7pm — and phones are answered 24/7 at ' + PHONE + '. If you’re hospitalized, we come to you.'; },
    results: function () { return 'We’ve recovered $13 million+ for injured Californians — including a $5,000,000 catastrophic-injury settlement. 4.9★ on Google, BBB A+. Past results don’t guarantee outcomes, but they show how we fight.'; },
    team: function () { return 'Your case is handled by real people, not a call center: founding attorney Sam Fareed (a serious-crash survivor himself), attorneys Shereen Ghaith and Laila Fareed, and a team that speaks 6+ languages. You speak directly with your attorney — always.'; },
    worth: function () { return 'It depends on your injuries, treatment, lost income, and how the crash happened — that’s exactly what the free consultation figures out. What we can promise: we don’t settle for the insurer’s first lowball number.'; },
    insurance: function () { return 'Please don’t give the insurance company a recorded statement before talking to a lawyer — those calls are designed to shrink your claim. It costs $0 to talk to us first: ' + PHONE + '.'; },
    hospitalized: function () { return 'If you’re hospitalized or can’t travel, we come to you — hospital, rehab, or home, anywhere in the Sacramento area. Call ' + PHONE + ' and we’ll arrange it.'; },
    greet: function () { return 'Hello! I’m the United Citizen Law concierge. I can answer questions about fees, deadlines, and our practice areas — or start your free case review right here.'; },
    thanks: function () { return 'You’re very welcome. If anything else comes up — day or night — we’re at ' + PHONE + '.'; }
  };

  function mainChips() {
    return chips([
      { label: 'Start free case review', action: function () { startQualify(); } },
      { label: 'Book a consultation', action: function () { startSchedule(); } },
      { label: 'Send documents', action: function () { startDocs(); } },
      { label: 'Fees & how it works', action: function () { botDelay(ANSWERS.fees(), function () { mainChips(); }); } },
      { label: 'Call ' + PHONE, action: function () { location.href = 'tel:' + TEL; } }
    ]);
  }
  function botDelay(text, after, html) {
    var t = typing(); S.busy = true;
    setTimeout(function () { t.remove(); bot(text, html); S.busy = false; if (after) after(); }, reduce ? 60 : 520 + Math.min(700, text.length * 4));
  }
  var OFFSCOPE = 'I’m only able to help with United Citizen Law — injury cases, our fees, our team, or booking your free case review. For anything about a potential case, the fastest answer is ' + PHONE + ' (free, 24/7). What can I help you with?';

  /* ── flows ── */
  function validPhone(p) { var d = String(p).replace(/\D/g, ''); return d.length === 10 || (d.length === 11 && d[0] === '1'); }

  function startQualify() {
    S.flow = 'qualify'; S.step = 0; clearChips();
    botDelay('Let’s see how we can help — takes about a minute. What kind of accident was it?', function () {
      chips(KB.cases.map(function (c) { return { label: c.label, action: function () { S.ctx.case_type = c.label; qual2(); } }; }));
    });
  }
  function qual2() {
    S.step = 1;
    botDelay('I’m sorry that happened. When did it happen?', function () {
      chips([
        { label: 'Within the last year', action: function () { S.ctx.when = '<1 year'; qual3(); } },
        { label: '1–2 years ago', action: function () { S.ctx.when = '1-2 years'; qual3(); } },
        { label: 'Over 2 years ago', action: function () { S.ctx.when = '>2 years'; qual3(true); } }
      ]);
    });
  }
  function qual3(late) {
    S.step = 2;
    var pre = late ? 'Over two years can be past California’s usual filing deadline — but exceptions exist (government claims, minors, late discovery), so it’s absolutely worth checking. ' : '';
    botDelay(pre + 'Were you (or your loved one) injured and treated by a doctor?', function () {
      chips([
        { label: 'Yes, treated', action: function () { S.ctx.injured = 'treated'; qual4(); } },
        { label: 'Injured, not seen yet', action: function () { S.ctx.injured = 'not-yet'; qual4(); } },
        { label: 'Not sure', action: function () { S.ctx.injured = 'unsure'; qual4(); } }
      ]);
    });
  }
  function qual4() {
    S.step = 3;
    botDelay('Got it. What’s your first and last name?');
  }
  function qual5() {
    S.step = 4;
    botDelay('Thanks, ' + S.ctx.name.split(' ')[0] + '. Best phone number for a quick call back? (We answer 24/7 and never spam.)');
  }
  function finishQualify() {
    S.flow = null; S.step = 0;
    var t = typing();
    var row = {
      name: S.ctx.name || null, phone: S.ctx.phone || null, email: S.ctx.email || null,
      case_type: S.ctx.case_type || null,
      summary: 'When: ' + (S.ctx.when || '?') + ' | Injured: ' + (S.ctx.injured || '?') + ' | Lang: ' + (document.documentElement.lang || 'en'),
      transcript: S.transcript.slice(-30), lang: document.documentElement.lang || 'en',
      page: location.pathname.split('/').pop() || 'index.html', status: 'new'
    };
    sbInsert('chat_leads', row).then(function (lead) {
      S.leadId = lead.id; persist();
      return sbFn('chat-notify', { kind: 'lead', phone: S.ctx.phone, name: S.ctx.name });
    }).then(function (n) {
      t.remove();
      var sms = n && n.sms ? ' I’ve texted you a confirmation.' : ' You’ll get a text confirmation shortly.';
      bot('Perfect — your free case review is in. A team member (in your language if you prefer) will call you back, usually within minutes during business hours.' + sms + '\n\nWant to do anything else while you’re here?');
      chips([
        { label: 'Book a time that suits me', action: function () { startSchedule(); } },
        { label: 'Send documents now', action: function () { startDocs(); } },
        { label: 'No thanks, all set', action: function () { botDelay('We’re on it, ' + (S.ctx.name || '').split(' ')[0] + '. Rest up — we’ll take it from here. ⚖️'); } }
      ]);
    }).catch(function () {
      t.remove();
      bot('I couldn’t reach our system just now — but don’t worry: call ' + PHONE + ' (free, 24/7) or tap "Start my free case review" on the page and we’ll take care of you.');
    });
  }

  function startSchedule() {
    S.flow = 'schedule'; clearChips();
    /* always know WHY they're coming in before booking */
    if (!S.ctx.case_type) {
      S.step = -1;
      botDelay('Happy to set that up. So the right attorney prepares for you — what kind of accident is this about?', function () {
        chips(KB.cases.map(function (c) {
          return { label: c.label, action: function () { S.ctx.case_type = c.label; schedAfterCase(); } };
        }));
      });
      return;
    }
    schedAfterCase();
  }
  function schedAfterCase() {
    S.flow = 'schedule';
    if (S.ctx.name && S.ctx.phone) { schedDay(); return; }
    S.step = 0;
    botDelay('Got it — ' + S.ctx.case_type.toLowerCase() + '. What’s your first and last name?');
  }
  function schedDay() {
    S.flow = 'schedule'; S.step = 2;
    botDelay('When works best? We meet Mon–Fri, 8am–7pm (and come to you if you’re hospitalized).', function () {
      var days = [], d = new Date();
      for (var i = 0; i < 5; i++) {
        d = new Date(Date.now() + i * 86400000);
        var dow = d.getDay(); if (dow === 0 || dow === 6) continue;
        var label = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : d.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
        (function (dd, lb) { days.push({ label: lb, action: function () { S.ctx.day = dd.toDateString(); S.ctx.dayLabel = lb; schedTime(); } }); })(new Date(d), label);
        if (days.length >= 3) break;
      }
      days.push({ label: 'Another day', action: function () { S.step = 21; botDelay('Sure — type the day that works (e.g. "next Tuesday" or "July 24").'); } });
      chips(days);
    });
  }
  function schedTime() {
    S.step = 3;
    botDelay('And what time of day?', function () {
      chips(['9:00 AM', '11:00 AM', '2:00 PM', '4:00 PM', '6:00 PM'].map(function (tm) {
        return { label: tm, action: function () { S.ctx.time = tm; finishSchedule(); } };
      }));
    });
  }
  function finishSchedule() {
    S.flow = null; S.step = 0;
    var whenText = (S.ctx.dayLabel || S.ctx.dayText || 'requested day') + ' at ' + (S.ctx.time || 'a time that suits');
    var preferredAt = null;
    try {
      if (S.ctx.day && S.ctx.time) {
        var dt = new Date(S.ctx.day + ' ' + S.ctx.time); if (!isNaN(dt)) preferredAt = dt.toISOString();
      }
    } catch (e) {}
    var t = typing();
    /* a booking without a lead still becomes a CRM lead — the team's pipeline
       is the source of truth, so every scheduler lands there too */
    var leadFirst = S.leadId ? Promise.resolve(null) : sbInsert('chat_leads', {
      name: S.ctx.name || null, phone: S.ctx.phone || null, email: S.ctx.email || null,
      case_type: S.ctx.case_type || null,
      summary: 'Booked a consultation via website chat (' + whenText + ')',
      transcript: S.transcript.slice(-30), lang: document.documentElement.lang || 'en',
      page: location.pathname.split('/').pop() || 'index.html', status: 'new'
    }).then(function (lead) { S.leadId = lead.id; persist(); }).catch(function () {});
    leadFirst.then(function () { return sbInsert('appointments', {
      lead_id: S.leadId, name: S.ctx.name || null, phone: S.ctx.phone || null, email: S.ctx.email || null,
      case_type: S.ctx.case_type || null, preferred_at: preferredAt, preferred_text: whenText,
      status: 'requested', sms_status: 'pending'
    }); }).then(function (appt) {
      return sbFn('chat-notify', { kind: 'appointment', phone: S.ctx.phone, name: S.ctx.name, when_text: whenText, appointment_id: appt.id });
    }).then(function (n) {
      t.remove();
      var sms = n && n.sms ? 'A text confirmation is on its way to your phone.' : 'You’ll receive a text confirmation shortly.';
      bot('✅ Requested: ' + whenText + '. A team member will call to confirm the exact time. ' + sms + '\n\nAnything else I can do?');
      chips([
        { label: 'Send documents', action: function () { startDocs(); } },
        { label: 'That’s everything', action: function () { botDelay('Wonderful. See you ' + (S.ctx.dayLabel || 'soon') + ' — and remember, the consultation is completely free.'); } }
      ]);
    }).catch(function () {
      t.remove();
      bot('I couldn’t save that just now — please call ' + PHONE + ' and we’ll lock in your time on the spot (we answer 24/7).');
    });
  }

  function startDocs() {
    S.flow = 'docs'; clearChips();
    botDelay('You can send me photos of the scene or vehicles, the police report, medical bills, or insurance letters — PDF or photos, up to 25MB each. Tap below to choose files.', function () {
      chips([
        { label: '📎 Choose files', action: function () { fileIn.click(); } },
        { label: 'Back to menu', action: function () { S.flow = null; mainChips(); } }
      ]);
    });
  }
  fileIn.addEventListener('change', function () {
    var files = [].slice.call(fileIn.files, 0, 5); fileIn.value = '';
    if (!files.length) return;
    user(files.length + ' file' + (files.length > 1 ? 's' : '') + ' selected');
    var t = typing(); var done = 0, fail = 0, names = [];
    var folder = 'chat/' + (S.leadId || ('anon-' + Math.random().toString(36).slice(2, 10)));
    var next = function (i) {
      if (i >= files.length) {
        t.remove();
        if (done) bot('✅ Received ' + done + ' file' + (done > 1 ? 's' : '') + ' (' + names.join(', ') + '). Your legal team can see them securely.' + (fail ? ' ' + fail + ' file(s) failed — you can retry or bring them to your consultation.' : '') + (S.leadId ? '' : '\n\nSo we can match these to your case, let’s grab your name and number:'));
        else bot('Those uploads didn’t go through — no problem, you can bring everything to your free consultation, or email clients@uclaw.net.');
        if (done && !S.leadId) startQualify(); else if (done) mainChips();
        return;
      }
      var f = files[i];
      if (f.size > 25 * 1024 * 1024) { fail++; next(i + 1); return; }
      var path = folder + '/' + Date.now() + '-' + f.name.replace(/[^\w.\-]+/g, '_');
      sbFetch('/storage/v1/object/intake-docs/' + path, {
        method: 'POST', headers: { 'Content-Type': f.type || 'application/octet-stream', 'x-upsert': 'false' }, body: f
      }).then(function (r) {
        if (!r.ok) throw 0;
        return sbInsert('chat_docs', { lead_id: S.leadId, path: path, filename: f.name, size_bytes: f.size, mime: f.type });
      }).then(function () { done++; names.push(f.name); next(i + 1); })
        .catch(function () { fail++; next(i + 1); });
    };
    next(0);
  });

  /* ── LLM fallback for free-typed questions the rules engine isn't sure about ── */
  function tryLLM(text, fallback) {
    var t = typing();
    sbFn('chat-llm', { messages: S.transcript.slice(-10).concat([{ role: 'user', content: text }]) })
      .then(function (r) {
        t.remove();
        if (r && r.ok && r.text) { bot(r.text); mainChips(); }
        else { bot(fallback); mainChips(); }
      });
  }

  /* ── input routing ── */
  function handle(text, action) {
    if (S.busy) return;
    user(text);
    if (action) { action(); return; }
    route(text);
  }
  function route(text) {
    clearChips();
    /* flow steps that consume free text */
    if (S.flow === 'qualify' && S.step === 3) {
      if (norm(text).split(' ').length < 2) { botDelay('Could I get your first and last name?'); return; }
      S.ctx.name = text.trim(); qual5(); return;
    }
    if (S.flow === 'qualify' && S.step === 4) {
      if (!validPhone(text)) { botDelay('That number doesn’t look complete — a 10-digit US number works best, like (916) 555-0123.'); return; }
      S.ctx.phone = text.trim(); finishQualify(); return;
    }
    if (S.flow === 'schedule' && S.step === 0) {
      if (norm(text).split(' ').length < 2) { botDelay('Your first and last name, please?'); return; }
      S.ctx.name = text.trim(); S.step = 1; botDelay('And the best phone number to confirm your time?'); return;
    }
    if (S.flow === 'schedule' && S.step === 1) {
      if (!validPhone(text)) { botDelay('Hmm — could you give me a 10-digit US number, like (916) 555-0123?'); return; }
      S.ctx.phone = text.trim(); schedDay(); return;
    }
    if (S.flow === 'schedule' && S.step === 21) {
      S.ctx.dayText = text.trim(); S.ctx.dayLabel = text.trim(); schedTime(); return;
    }
    /* intent detection */
    var hit = detect(text);
    if (hit) {
      if (hit.id.indexOf('page:') === 0) {
        var slug = hit.id.slice(5), p = null;
        KB.pages.forEach(function (x) { if (x.slug === slug) p = x; });
        botDelay(p.blurb, function () {
          bot('Read more: ' + p.title, 'You can read the full guide here: <a href="./' + p.slug + '.html">' + esc(p.title) + '</a>. Or skip the reading — the free case review takes a minute.');
          chips([
            { label: 'Start free case review', action: function () { startQualify(); } },
            { label: 'Call ' + PHONE, action: function () { location.href = 'tel:' + TEL; } }
          ]);
        });
        return;
      }
      switch (hit.id) {
        case 'schedule': startSchedule(); return;
        case 'docs': startDocs(); return;
        case 'qualify': startQualify(); return;
        case 'human':
          botDelay('Of course — real people answer 24/7 at ' + PHONE + '. Or leave your number and we’ll call you.', function () {
            chips([
              { label: 'Call ' + PHONE, action: function () { location.href = 'tel:' + TEL; } },
              { label: 'Call me back', action: function () { startQualify(); } }
            ]);
          });
          return;
        default:
          if (ANSWERS[hit.id]) { botDelay(ANSWERS[hit.id](), function () { if (hit.id !== 'thanks') mainChips(); }); return; }
      }
    }
    /* unknown → try the (optional) LLM, else scoped redirect */
    tryLLM(text, OFFSCOPE);
  }

  /* ── open/close ── */
  function greet() {
    if (S.greeted) return; S.greeted = true;
    var lang = document.documentElement.lang || 'en';
    var hello = {
      es: '¡Hola! Chat en inglés — pero nuestro equipo habla español: ' + PHONE + '.',
      fa: 'سلام! تیم ما دری صحبت می‌کند: ' + PHONE,
      ur: 'سلام! ہماری ٹیم اردو بولتی ہے: ' + PHONE,
      ar: 'مرحباً! فريقنا يتحدث العربية: ' + PHONE
    }[lang];
    if (S.transcript.length) {
      S.transcript.slice(-12).forEach(function (m) { say(esc(m.content), m.role === 'user' ? 'user' : 'bot'); });
      bot('Welcome back — where were we?'); mainChips(); return;
    }
    bot('Hi, I’m the United Citizen Law concierge ⚖️ Injured in an accident? I can answer your questions, start your free case review, or book you in — 24/7, no fee unless we win.' + (hello ? '\n\n' + hello : ''));
    mainChips();
  }
  function openPanel() {
    S.open = true; panel.classList.add('open'); btn.style.display = 'none';
    requestAnimationFrame(function () { panel.classList.add('in'); });
    greet(); setTimeout(function () { input.focus(); }, reduce ? 0 : 250);
  }
  function closePanel() {
    S.open = false; panel.classList.remove('in');
    setTimeout(function () { panel.classList.remove('open'); btn.style.display = 'flex'; btn.focus(); }, reduce ? 0 : 300);
  }
  btn.addEventListener('click', openPanel);
  closeX.addEventListener('click', closePanel);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && S.open) closePanel(); });
  function submit() { var v = input.value.trim(); if (!v || S.busy) return; input.value = ''; handle(v); }
  send.addEventListener('click', submit);
  input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); submit(); } });
})();
