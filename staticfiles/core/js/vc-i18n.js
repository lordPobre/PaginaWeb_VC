/* VC — Diccionario ES / EN (cliente). Se aplica a elementos con:
   data-i18n (texto), data-i18n-html (HTML), data-i18n-ph (placeholder),
   data-i18n-alt (alt), data-i18n-aria (aria-label). */
(function () {
  var D = {
    es: {
      trabaja: 'Trabaja con nosotros', denuncias: 'Canal de denuncias', langAria: 'Idioma', homeAria: 'VC Ingeniería y Construcción, inicio', logoAlt: 'VC Ingeniería y Construcción',
      nav1: 'Nosotros', nav2: 'Especialidades', nav3: 'Proyectos', nav4: 'Sostenibilidad', nav5: 'Contacto', cta: 'Cotizar proyecto', menuAria: 'Abrir menú',
      slide1Alt: 'Supervisor frente a obra en construcción', slide2Alt: 'Planta industrial con correas transportadoras', slide3Alt: 'Puente de hormigón sobre río',
      heroTitle: 'Construimos y montamos la infraestructura que sostiene a la industria.',
      heroSub: 'Soluciones de infraestructura de alta complejidad con precisión técnica y compromiso sostenible en todo Chile.',
      heroCta1: 'Explorar proyectos', heroCta2: 'Contáctanos', slide1: 'Obras civiles', slide2: 'Montaje industrial', slide3: 'Infraestructura',
      statement: 'Impulsamos la transformación industrial mediante la <em>excelencia en montaje</em>. No solo construimos infraestructuras: forjamos relaciones de confianza.',
      about: 'Desde Puchuncaví, Región de Valparaíso, ejecutamos montaje industrial, obras civiles y mantención para los sectores de energía y minería.',
      history: 'Conoce nuestra historia',
      stat1: 'Accidentes FAT / LTI en 2025', stat2: 'Proveedores locales', stat3: 'Respuesta operativa', stat4: '9001 · 14001 · 45001 en calidad, ambiente y seguridad',
      areasTitle: 'Áreas de especialización', areasHint: 'Pasa el cursor o toca cada área para ver su alcance.', verServicio: 'Consultar servicio →',
      area1: 'Montaje Industrial', area1Text: 'Soluciones integrales en plantas industriales y faenas productivas con alta exigencia mecánica y estructural.',
      area2: 'Obras Civiles', area2Text: 'Ejecución de edificaciones, estructuras complejas y obras viales bajo las más estrictas normativas nacionales.',
      area3: 'Mantención Programada', area3Text: 'Prevención integral de fallas y aseguramiento de la continuidad operacional para equipos críticos e infraestructura.',
      projEyebrow: 'Experiencia en terreno', projTitle: 'Proyectos ejecutados', prev: 'Proyecto anterior', next: 'Proyecto siguiente',
      ubic: 'Ubicación', esp: 'Especialidad', ficha: 'Ver ficha del proyecto →',
      p1Tag: 'Energía', p1Text: 'Mejoramiento de mobiliario en sala de control U-3. Ejecución bajo estrictos protocolos de continuidad operacional y seguridad eléctrica.', p1Lugar: 'Quintero, V Región', p1Alc: 'Obras civiles · 2023',
      p2Tag: 'Montaje industrial', p2Text: 'Fabricación y montaje especializado de línea de succión para bomba dragadora en proyecto Foreway. Alta precisión en soldadura y ajuste mecánico.', p2Lugar: 'Cajón del Maipo, RM', p2Alc: 'Montaje mecánico',
      p3Tag: 'Mantención e hidráulica', p3Text: 'Reparación de filtros de retrolavado y fabricación de líneas de acero inoxidable para circuitos abiertos y cerrados de las unidades 1 y 2.', p3Alc: 'Fabricación en acero inoxidable',
      esgEyebrow: 'Sostenibilidad ESG', esgTitle: 'Cero accidentes con tiempo perdido en 2025.',
      esgSub: 'Compromiso ambiental, social y de gobernanza para construir un futuro industrial responsable y seguro en Chile.',
      pil1: 'Ambiente', pil1Text: 'Gestión de residuos, eficiencia energética y control de emisiones en obra.', pil1Dato: 'Emisiones CO₂e por HH',
      pil2Text: 'Cero daño a las personas, capacitación continua, empleabilidad local y relacionamiento comunitario transparente.', pil2Dato: 'Proveedores locales',
      pil3: 'Gobernanza', pil3Text: 'Cumplimiento normativo estricto, ética, integridad corporativa y cadena de suministro responsable con criterios ESG.', pil3Dato: 'Reciclaje de residuos',
      ods: 'Contribuimos a los ODS', esgCta: 'Ver compromiso ESG',
      contactAlt: 'Equipo VC en reunión técnica', lines: 'Líneas directas', office: 'Oficina', contactTitle: 'Hablemos de tu proyecto',
      contactSub: 'Completa el formulario y un especialista de VC Limitada se pondrá en contacto contigo a la brevedad.',
      fName: 'Nombre completo', fNamePh: 'Juan Pérez', fCompany: 'Empresa', fCompanyPh: 'Razón social', fEmail: 'Correo electrónico', fEmailPh: 'ejemplo@empresa.com',
      fService: 'Servicio', o1: 'Montaje industrial', o2: 'Obras civiles', o3: 'Mantención programada', o4: 'Otro',
      fMsg: 'Tu mensaje', fMsgPh: 'Cuéntanos sobre tu proyecto o requerimiento...', send: 'Enviar mensaje →',
      footCompany: 'Empresa', footCorp: 'Corporativo', footOrg: 'Equipo directivo', footQuality: 'Certificaciones ISO', footCert: 'Certificaciones',
      legal: 'Aviso legal · Políticas de privacidad', dev: 'Desarrollado por'
    },
    en: {
      trabaja: 'Careers', denuncias: 'Whistleblower channel', langAria: 'Language', homeAria: 'VC Engineering and Construction, home', logoAlt: 'VC Engineering and Construction',
      nav1: 'About us', nav2: 'Expertise', nav3: 'Projects', nav4: 'Sustainability', nav5: 'Contact', cta: 'Request a quote', menuAria: 'Open menu',
      slide1Alt: 'Supervisor in front of a construction site', slide2Alt: 'Industrial plant with conveyor belts', slide3Alt: 'Concrete bridge over a river',
      heroTitle: 'We build and install the infrastructure that keeps industry running.',
      heroSub: 'High-complexity infrastructure solutions delivered with technical precision and a commitment to sustainability across Chile.',
      heroCta1: 'Explore projects', heroCta2: 'Contact us', slide1: 'Civil works', slide2: 'Industrial installation', slide3: 'Infrastructure',
      statement: 'We drive industrial transformation through <em>excellence in installation</em>. We do more than build infrastructure: we build relationships of trust.',
      about: 'From Puchuncaví, in the Valparaíso Region, we deliver industrial installation, civil works and maintenance for the energy and mining sectors.',
      history: 'Our story',
      stat1: 'FAT / LTI incidents in 2025', stat2: 'Local suppliers', stat3: 'Operational response', stat4: '9001 · 14001 · 45001 for quality, environment and safety',
      areasTitle: 'Areas of expertise', areasHint: 'Hover over or tap each area to see its scope.', verServicio: 'Ask about this service →',
      area1: 'Industrial Installation', area1Text: 'End-to-end solutions for industrial plants and production sites with demanding mechanical and structural requirements.',
      area2: 'Civil Works', area2Text: 'Buildings, complex structures and road works delivered under the strictest national standards.',
      area3: 'Scheduled Maintenance', area3Text: 'Comprehensive failure prevention and operational continuity for critical equipment and infrastructure.',
      projEyebrow: 'Field experience', projTitle: 'Completed projects', prev: 'Previous project', next: 'Next project',
      ubic: 'Location', esp: 'Discipline', ficha: 'View project sheet →',
      p1Tag: 'Energy', p1Text: 'Furniture upgrade in the U-3 control room, carried out under strict operational-continuity and electrical-safety protocols.', p1Lugar: 'Quintero, Valparaíso Region', p1Alc: 'Civil works · 2023',
      p2Tag: 'Industrial installation', p2Text: 'Fabrication and installation of a dredge-pump suction line for the Foreway project, with high-precision welding and mechanical fitting.', p2Lugar: 'Cajón del Maipo, Santiago Metropolitan Region', p2Alc: 'Mechanical installation',
      p3Tag: 'Maintenance & hydraulics', p3Text: 'Repair of backwash filters and fabrication of stainless-steel lines for the open and closed circuits of units 1 and 2.', p3Alc: 'Stainless-steel fabrication',
      esgEyebrow: 'ESG Sustainability', esgTitle: 'Zero lost-time incidents in 2025.',
      esgSub: 'Environmental, social and governance commitments for a responsible, safe industrial future in Chile.',
      pil1: 'Environment', pil1Text: 'Waste management, energy efficiency and on-site emissions control.', pil1Dato: 'CO₂e emissions per man-hour',
      pil2Text: 'Zero harm to people, continuous training, local employment and transparent community relations.', pil2Dato: 'Local suppliers',
      pil3: 'Governance', pil3Text: 'Strict regulatory compliance, ethics, corporate integrity and a responsible supply chain with ESG criteria.', pil3Dato: 'Waste recycled',
      ods: 'We contribute to the SDGs', esgCta: 'See our ESG commitment',
      contactAlt: 'VC team in a technical meeting', lines: 'Direct lines', office: 'Office', contactTitle: "Let's talk about your project",
      contactSub: 'Fill in the form and a VC Limitada specialist will get back to you shortly.',
      fName: 'Full name', fNamePh: 'John Smith', fCompany: 'Company', fCompanyPh: 'Company name', fEmail: 'Email', fEmailPh: 'name@company.com',
      fService: 'Service', o1: 'Industrial installation', o2: 'Civil works', o3: 'Scheduled maintenance', o4: 'Other',
      fMsg: 'Your message', fMsgPh: 'Tell us about your project or requirement...', send: 'Send message →',
      footCompany: 'Company', footCorp: 'Corporate', footOrg: 'Leadership team', footQuality: 'ISO certifications', footCert: 'Certifications',
      legal: 'Legal notice · Privacy policy', dev: 'Developed by'
    }
  };

  var KEY = 'vc-lang';
  var originals = new WeakMap(); // guarda el texto original (ES) por si una clave no existe

  function apply(lang) {
    var dict = D[lang] || D.es;
    function each(attr, fn) {
      document.querySelectorAll('[' + attr + ']').forEach(function (el) {
        var k = el.getAttribute(attr);
        if (dict[k] != null) fn(el, dict[k]);
      });
    }
    each('data-i18n', function (el, v) { el.textContent = v; });
    each('data-i18n-html', function (el, v) { el.innerHTML = v; });
    each('data-i18n-ph', function (el, v) { el.setAttribute('placeholder', v); });
    each('data-i18n-alt', function (el, v) { el.setAttribute('alt', v); });
    each('data-i18n-aria', function (el, v) { el.setAttribute('aria-label', v); });
    // Contenido del admin: elementos con data-en="..." (el español queda en data-es)
    document.querySelectorAll('[data-en]').forEach(function (el) {
      var en = el.getAttribute('data-en');
      if (!en) return;
      if (!el.hasAttribute('data-es')) el.setAttribute('data-es', el.textContent.trim());
      el.textContent = lang === 'en' ? en : el.getAttribute('data-es');
    });
    document.querySelectorAll('[data-lang-only]').forEach(function (el) { el.hidden = el.getAttribute('data-lang-only') !== lang; });
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-lang]').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang));
    });
  }

  function set(lang) {
    try { localStorage.setItem(KEY, lang); } catch (e) {}
    apply(lang);
  }

  window.VCi18n = { apply: function () { apply(current()); }, set: set, current: current,
    extend: function (lang, obj) { D[lang] = D[lang] || {}; for (var k in obj) D[lang][k] = obj[k]; } };
  function current() { try { return localStorage.getItem(KEY) || 'es'; } catch (e) { return 'es'; } }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-lang]').forEach(function (b) {
      b.addEventListener('click', function () { set(b.getAttribute('data-lang')); });
    });
    if (current() !== 'es') apply(current());
  });
})();
