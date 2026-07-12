/* United Citizen Law — shared language engine for the practice + team pages.
   Same model as the homepage: English is cached from the DOM, so only es/fa/ur/ar
   are supplied below. Any key missing in a language falls back to English per-key.
   The chosen language persists in localStorage('ucl_lang') and is shared with the
   homepage, so a visitor's choice follows them across every page.
   ⚠️ FA (Dari), UR (Urdu/Hindi) and AR (Arabic) are a conversion layer — have a
   native speaker review before production. */
(function(){
  "use strict";
  var RTL = {fa:1, ur:1, ar:1};
  var $$ = function(s,r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); };

  /* ── translations (EN comes from the page itself) ── */
  var I18N = {
    es:{
      "skip":"Saltar al contenido",
      "nav.practice":"Áreas de práctica","nav.results":"Resultados","nav.team":"Equipo","nav.faq":"Preguntas","nav.contact":"Contacto",
      "crumb.home":"Inicio",
      "pp.eyebrow":"Lesiones personales en Sacramento",
      "pp.risk":"Sin honorarios a menos que ganemos. ¿Hospitalizado? Vamos a usted.",
      "pp.process.h":"Nuestro proceso comprobado de tres pasos",
      "pp.process.p":"Aplicamos el mismo marco probado en cada caso, tomando en cuenta los detalles de su situación particular.",
      "end.eyebrow":"Consulta gratis",
      "end.h":"Usted concéntrese en sanar. Nosotros peleamos la batalla.",
      "end.p":"Consulta gratis · Sin honorarios a menos que ganemos · Contestamos 24/7, en inglés, español, دری, اردو y العربية.",
      "end.call":"Llame al (916) 800-8457","end.review":"Inicie su evaluación gratis",
      "contact.eyebrow":"Contáctenos","contact.h":"Visítenos, llámenos, o vamos a usted",
      "foot.tag":"Abogados de lesiones personales al servicio de Sacramento y todo el Valle Central.",
      "foot.practice":"Áreas de práctica","foot.firm":"El bufete","foot.contact":"Contacto",
      /* practice hero H1s */
      "p.car.pre":"¿Lesionado en un accidente de auto?","p.car.em":"Estamos de su lado.",
      "p.truck.pre":"¿Accidente con un camión?","p.truck.em":"Igualamos su velocidad.",
      "p.moto.pre":"¿Accidente de motocicleta?","p.moto.em":"Cambiamos el guion.",
      "p.rideshare.pre":"¿Accidente en Uber o Lyft?","p.rideshare.em":"Sabemos qué cobertura aplica.",
      "p.ped.pre":"¿Peatón o ciclista atropellado?","p.ped.em":"La ley está de su lado.",
      "p.dog.pre":"¿Le mordió un perro?","p.dog.em":"El dueño es responsable.",
      "p.slip.pre":"¿Se cayó en una propiedad?","p.slip.em":"Los hacemos responsables.",
      "p.wd.pre":"¿Perdió a un ser querido?","p.wd.em":"Buscamos respuestas y justicia.",
      "p.cat.pre":"¿Lesión catastrófica?","p.cat.em":"Peleamos por su futuro.",
      /* practice ledes (Spanish, full) */
      "p.car.lede":"Ya sea que fuera el conductor, pasajero o peatón, un accidente de auto puede cambiar su vida en un instante. La aseguradora ya asignó un ajustador cuyo trabajo es pagarle menos — el nuestro es lo contrario.",
      "p.truck.lede":"Las empresas de transporte envían equipos de respuesta rápida en cuestión de horas. Usted necesita la misma velocidad de su lado — preservamos la evidencia antes de que desaparezca.",
      "p.moto.lede":"A los motociclistas se les culpa por defecto. Nosotros cambiamos ese guion con evidencia y una preparación implacable.",
      "p.rideshare.lede":"Los choques con Uber y Lyft involucran pólizas de seguro en capas que la mayoría de los bufetes no entienden. Nosotros sabemos qué cobertura aplica — y cuándo.",
      "p.ped.lede":"Las colisiones en cruces peatonales y ciclovías causan lesiones devastadoras sin protección alguna. La ley de California está de su lado — y nosotros la hacemos valer por completo.",
      "p.dog.lede":"California responsabiliza estrictamente a los dueños. Nosotros manejamos el reclamo mientras usted se concentra en sanar.",
      "p.slip.lede":"Los dueños de propiedades le deben un entorno seguro — pisos mojados, escaleras rotas, mala iluminación. Cuando toman atajos, los hacemos responsables.",
      "p.wd.lede":"Ninguna cantidad reemplaza una vida — pero la rendición de cuentas, las respuestas y la seguridad de su familia importan. Estamos a su lado con compasión y fuerza.",
      "p.cat.lede":"Cuando una lesión cambia la vida para siempre — cerebral, medular, quemaduras, amputación — el valor del caso y la atención de por vida son enormes. Construimos el expediente que su futuro exige."
    },
    fa:{
      "skip":"رفتن به محتوا",
      "nav.practice":"زمینه‌های کاری","nav.results":"نتایج","nav.team":"تیم","nav.faq":"پرسش‌ها","nav.contact":"تماس",
      "crumb.home":"خانه",
      "pp.eyebrow":"صدمات شخصی در ساکرامنتو",
      "pp.risk":"تا زمانی که نبریم، هزینه‌ای نیست. بستری هستید؟ ما نزد شما می‌آییم.",
      "pp.process.h":"روند اثبات‌شدهٔ سه‌مرحله‌ای ما",
      "pp.process.p":"ما همان چارچوب آزموده را در هر پرونده به کار می‌بریم و جزئیات وضعیت خاص شما را در نظر می‌گیریم.",
      "end.eyebrow":"مشاورهٔ رایگان",
      "end.h":"شما بر بهبودی تمرکز کنید. مبارزه با ما.",
      "end.p":"مشاورهٔ رایگان · تا نبریم هزینه‌ای نیست · پاسخگویی ۲۴ ساعته به انگلیسی، اسپانیایی، دری، اردو و عربی.",
      "end.call":"تماس: (916) 800-8457","end.review":"ارزیابی رایگان پروندهٔ خود را شروع کنید",
      "contact.eyebrow":"تماس با ما","contact.h":"به دفتر ما بیایید، زنگ بزنید، یا ما نزد شما می‌آییم",
      "foot.practice":"زمینه‌های کاری","foot.firm":"دفتر حقوقی","foot.contact":"تماس",
      "p.car.pre":"در تصادف رانندگی صدمه دیدید؟","p.car.em":"ما در کنار شما هستیم.",
      "p.truck.pre":"تصادف با کامیون؟","p.truck.em":"ما هم‌سرعت شما می‌شویم.",
      "p.moto.pre":"تصادف موترسایکل؟","p.moto.em":"ورق را برمی‌گردانیم.",
      "p.rideshare.pre":"تصادف اوبر یا لیفت؟","p.rideshare.em":"می‌دانیم کدام بیمه اعمال می‌شود.",
      "p.ped.pre":"عابر یا دوچرخه‌سوار زخمی؟","p.ped.em":"قانون در کنار شماست.",
      "p.dog.pre":"سگ شما را گاز گرفت؟","p.dog.em":"صاحب حیوان مسئول است.",
      "p.slip.pre":"در ملکی زمین خوردید؟","p.slip.em":"آنها را پاسخگو می‌کنیم.",
      "p.wd.pre":"عزیزی را از دست دادید؟","p.wd.em":"پاسخ و عدالت می‌جوییم.",
      "p.cat.pre":"صدمهٔ فاجعه‌بار؟","p.cat.em":"برای آیندهٔ شما می‌جنگیم."
    },
    ur:{
      "skip":"مواد پر جائیں",
      "nav.practice":"شعبہ جات","nav.results":"نتائج","nav.team":"ٹیم","nav.faq":"سوالات","nav.contact":"رابطہ",
      "crumb.home":"ہوم",
      "pp.eyebrow":"سیکرامنٹو میں ذاتی چوٹ",
      "pp.risk":"جب تک ہم نہ جیتیں کوئی فیس نہیں۔ ہسپتال میں ہیں؟ ہم آپ کے پاس آتے ہیں۔",
      "pp.process.h":"ہمارا آزمودہ تین مرحلوں کا عمل",
      "pp.process.p":"ہم ہر کیس میں وہی آزمودہ طریقہ اپناتے ہیں اور آپ کی مخصوص صورتحال کی تفصیلات کا خیال رکھتے ہیں۔",
      "end.eyebrow":"مفت مشاورت",
      "end.h":"آپ صحت یابی پر توجہ دیں۔ لڑائی ہم پر چھوڑ دیں۔",
      "end.p":"مفت مشاورت · جب تک ہم نہ جیتیں کوئی فیس نہیں · 24/7 جواب، انگریزی، ہسپانوی، دری، اردو اور عربی میں۔",
      "end.call":"کال کریں (916) 800-8457","end.review":"اپنے کیس کا مفت جائزہ شروع کریں",
      "contact.eyebrow":"ہم سے رابطہ","contact.h":"ہمارے دفتر آئیں، کال کریں، یا ہم آپ کے پاس آئیں",
      "foot.practice":"شعبہ جات","foot.firm":"فرم","foot.contact":"رابطہ",
      "p.car.pre":"کار حادثے میں زخمی؟","p.car.em":"ہم آپ کے ساتھ ہیں۔",
      "p.truck.pre":"ٹرک حادثہ؟","p.truck.em":"ہم آپ کی رفتار سے چلتے ہیں۔",
      "p.moto.pre":"موٹرسائیکل حادثہ؟","p.moto.em":"ہم کہانی بدل دیتے ہیں۔",
      "p.rideshare.pre":"اوبر یا لِفٹ حادثہ؟","p.rideshare.em":"ہم جانتے ہیں کون سا انشورنس لاگو ہے۔",
      "p.ped.pre":"پیدل یا سائیکل سوار زخمی؟","p.ped.em":"قانون آپ کے ساتھ ہے۔",
      "p.dog.pre":"کتے نے کاٹا؟","p.dog.em":"مالک ذمہ دار ہے۔",
      "p.slip.pre":"کسی جائیداد پر گر گئے؟","p.slip.em":"ہم انہیں جوابدہ بناتے ہیں۔",
      "p.wd.pre":"کسی عزیز کو کھو دیا؟","p.wd.em":"ہم جواب اور انصاف مانگتے ہیں۔",
      "p.cat.pre":"سنگین چوٹ؟","p.cat.em":"ہم آپ کے مستقبل کے لیے لڑتے ہیں۔"
    },
    ar:{
      "skip":"تخطَّ إلى المحتوى",
      "nav.practice":"مجالات العمل","nav.results":"النتائج","nav.team":"الفريق","nav.faq":"الأسئلة","nav.contact":"اتصل",
      "crumb.home":"الرئيسية",
      "pp.eyebrow":"إصابات شخصية في ساكرامنتو",
      "pp.risk":"لا رسوم ما لم نربح. في المستشفى؟ نأتي إليك.",
      "pp.process.h":"عمليتنا المثبتة من ثلاث خطوات",
      "pp.process.p":"نطبّق الإطار المجرَّب نفسه في كل قضية مع مراعاة تفاصيل وضعك الخاص.",
      "end.eyebrow":"استشارة مجانية",
      "end.h":"ركّز أنت على التعافي. ونحن نتولّى المعركة.",
      "end.p":"استشارة مجانية · لا رسوم ما لم نربح · نردّ على مدار الساعة بالإنجليزية والإسبانية والدرية والأردية والعربية.",
      "end.call":"اتصل على (916) 800-8457","end.review":"ابدأ تقييم قضيتك المجاني",
      "contact.eyebrow":"اتصل بنا","contact.h":"زُرنا، اتصل بنا، أو نأتي إليك",
      "foot.practice":"مجالات العمل","foot.firm":"المكتب","foot.contact":"اتصل",
      "p.car.pre":"أُصبت في حادث سيارة؟","p.car.em":"نحن إلى جانبك.",
      "p.truck.pre":"حادث شاحنة؟","p.truck.em":"نجاري سرعتهم.",
      "p.moto.pre":"حادث دراجة نارية؟","p.moto.em":"نقلب الرواية.",
      "p.rideshare.pre":"حادث أوبر أو ليفت؟","p.rideshare.em":"نعرف أي تأمين ينطبق.",
      "p.ped.pre":"مشاة أو دراجة هوائية؟","p.ped.em":"القانون في صفك.",
      "p.dog.pre":"عضّك كلب؟","p.dog.em":"المالك مسؤول.",
      "p.slip.pre":"سقطت في عقار؟","p.slip.em":"نُحمّلهم المسؤولية.",
      "p.wd.pre":"فقدت عزيزًا؟","p.wd.em":"نطلب الإجابات والعدالة.",
      "p.cat.pre":"إصابة كارثية؟","p.cat.em":"نقاتل من أجل مستقبلك."
    }
  };

  var EN_CACHE = {};
  function cacheEnglish(){
    $$('[data-i18n]').forEach(function(el){ EN_CACHE[el.getAttribute('data-i18n')] = el.textContent; });
    $$('[data-i18n-html]').forEach(function(el){ EN_CACHE['html:'+el.getAttribute('data-i18n-html')] = el.innerHTML; });
  }
  function t(key, lang){
    if(lang==='en') return EN_CACHE[key];
    var d = I18N[lang];
    if(d && d[key]!=null) return d[key];
    return EN_CACHE[key]; /* per-key English fallback */
  }
  function applyLang(code){
    if(code!=='en' && !I18N[code]) code='en';
    try{ localStorage.setItem('ucl_lang', code); }catch(e){}
    document.documentElement.lang = code==='en'?'en-US':code;
    document.documentElement.dir  = RTL[code] ? 'rtl' : 'ltr';
    $$('[data-i18n]').forEach(function(el){ var v=t(el.getAttribute('data-i18n'),code); if(v!=null) el.textContent=v; });
    $$('[data-i18n-html]').forEach(function(el){ var v=t('html:'+el.getAttribute('data-i18n-html'),code); if(v!=null) el.innerHTML=v; });
    $$('[data-setlang]').forEach(function(b){ b.classList.toggle('on', b.getAttribute('data-setlang')===code); b.setAttribute('aria-pressed', b.getAttribute('data-setlang')===code?'true':'false'); });
  }

  function boot(){
    cacheEnglish();
    $$('[data-setlang]').forEach(function(b){
      b.addEventListener('click', function(){ applyLang(b.getAttribute('data-setlang')); });
    });
    var saved='en';
    try{ saved=localStorage.getItem('ucl_lang')||'en'; }catch(e){}
    applyLang(saved);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
