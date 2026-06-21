// ================================================================
// AI-SOLUTIONS — MAIN JS
// ================================================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Flash Messages ─────────────────────────────────────────────
  document.querySelectorAll('.flash-close').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.flash-msg').remove();
    });
  });

  setTimeout(() => {
    document.querySelectorAll('.flash-msg').forEach(msg => {
      msg.style.transition = 'opacity 0.4s, transform 0.4s';
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(20px)';
      setTimeout(() => msg.remove(), 400);
    });
  }, 5000);

  // ── Navbar Hamburger ───────────────────────────────────────────
  const hamburger = document.querySelector('.nav-hamburger');
  const navLinks = document.querySelector('.nav-links');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const bars = hamburger.querySelectorAll('span');
      if (navLinks.classList.contains('open')) {
        bars[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        bars[1].style.opacity = '0';
        bars[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
      } else {
        bars[0].style.transform = '';
        bars[1].style.opacity = '';
        bars[2].style.transform = '';
      }
    });
  }

  // ── Navbar scroll style (handled by .scrolled class in CSS) ──────
  // kept empty — scroll logic now lives in the Scroll Reveal block above

  // ── Marquee duplicate ──────────────────────────────────────────
  document.querySelectorAll('.marquee-track').forEach(track => {
    const content = track.innerHTML;
    track.innerHTML = content + content;
  });

  // ── Chatbot ────────────────────────────────────────────────────
  const chatBtn = document.getElementById('chatbot-btn');
  const chatPanel = document.getElementById('chatbot-panel');
  const chatClose = document.getElementById('chatbot-close');
  const chatInput = document.getElementById('chatbot-input');
  const chatSend = document.getElementById('chatbot-send');
  const chatMessages = document.getElementById('chatbot-messages');

  const botReplies = {
    'hello': '👋 Hi there! Welcome to AI-Solutions. How can I help you today?',
    'hi': '👋 Hi there! Welcome to AI-Solutions. How can I help you today?',
    'hey': '👋 Hey! Great to hear from you. What can I help you with?',
    'solutions': '🤖 We offer six core AI services: Process Automation, Predictive Analytics, NLP, Computer Vision, AI Consulting, and Custom ML Development. <a href="/solutions" style="color:var(--acc)">Explore all solutions →</a>',
    'services': '🤖 Our services include AI automation, data analytics, NLP, computer vision, strategic consulting and custom model development. <a href="/solutions" style="color:var(--acc)">See details →</a>',
    'contact': '📬 You can reach us at info@ai-solutions.uk or call +44 (0)191 123 4567. We\'re based in Sunderland, UK. <a href="/contact" style="color:var(--acc)">Send enquiry →</a>',
    'about': '🏢 AI-Solutions is a Sunderland-based AI company helping businesses automate, analyse, and innovate. We believe enterprise AI should be accessible to every organisation.',
    'company': '🏢 AI-Solutions is a Sunderland-based AI company helping businesses automate, analyse, and innovate. We believe enterprise AI should be accessible to every organisation.',
    'pricing': '💬 Our pricing is tailored to each project\'s scope and requirements. <a href="/contact" style="color:var(--acc)">Contact us for a quote →</a>',
    'price': '💬 Pricing varies by project. <a href="/contact" style="color:var(--acc)">Get in touch →</a> and we\'ll discuss your needs.',
    'case studies': '📊 We\'ve delivered AI solutions across manufacturing, retail, logistics, and healthcare. <a href="/case-studies" style="color:var(--acc)">View case studies →</a>',
    'events': '📅 We host regular summits, workshops, and webinars. <a href="/events" style="color:var(--acc)">See upcoming events →</a>',
    'articles': '📰 Our team publishes insights on AI strategy and technology. <a href="/articles" style="color:var(--acc)">Read the blog →</a>',
    'blog': '📰 Check out our articles on AI trends and practical guides. <a href="/articles" style="color:var(--acc)">Visit the blog →</a>',
    'team': '👥 Our team includes AI researchers, data scientists, and industry consultants. <a href="/#team" style="color:var(--acc)">Meet the team →</a>',
    'sunderland': '📍 We\'re proud to be headquartered in Sunderland, SR1 1AA, UK — at the heart of the North East tech scene.',
    'automation': '⚙️ Our process automation solutions use RPA and AI to eliminate repetitive tasks, reducing operational costs by up to 70%. <a href="/solutions#automation" style="color:var(--acc)">Learn more →</a>',
    'nlp': '💬 Our NLP solutions handle sentiment analysis, document processing, and intelligent chatbots at scale. <a href="/solutions#nlp" style="color:var(--acc)">Learn more →</a>',
    'machine learning': '🧠 We build custom ML models trained on your data, for your industry. <a href="/solutions#custom-ml" style="color:var(--acc)">Learn more →</a>',
  };

  function addMessage(text, type) {
    const msg = document.createElement('div');
    msg.className = `chat-msg ${type}`;
    msg.innerHTML = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function getReply(input) {
    const lower = input.toLowerCase().trim();
    for (const [key, reply] of Object.entries(botReplies)) {
      if (lower.includes(key)) return reply;
    }
    return '🤔 I\'m not sure about that. <a href="/contact" style="color:var(--acc)">Contact our team →</a> for a detailed answer.';
  }

  function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    chatInput.value = '';
    setTimeout(() => addMessage(getReply(text), 'bot'), 500);
  }

  if (chatBtn) {
    chatBtn.addEventListener('click', () => {
      chatPanel.classList.toggle('open');
      if (chatPanel.classList.contains('open') && chatMessages.children.length === 0) {
        setTimeout(() => addMessage('👋 Hi! I\'m the AI-Solutions assistant. Ask me about our services, pricing, team, or events!', 'bot'), 300);
      }
    });
  }

  if (chatClose) chatClose.addEventListener('click', () => chatPanel.classList.remove('open'));
  if (chatSend) chatSend.addEventListener('click', sendMessage);
  if (chatInput) {
    chatInput.addEventListener('keypress', e => {
      if (e.key === 'Enter') sendMessage();
    });
  }

  // ── Image Preview for file uploads ────────────────────────────
  document.querySelectorAll('.file-preview-input').forEach(input => {
    input.addEventListener('change', function () {
      const previewWrap = this.closest('.upload-zone-wrap')?.querySelector('.image-preview');
      if (previewWrap && this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
          previewWrap.style.display = 'block';
          const img = previewWrap.querySelector('img');
          if (img) img.src = e.target.result;
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  });

  // ── Scroll Reveal (data-reveal) ────────────────────────────────
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('[data-reveal]').forEach(el => revealObserver.observe(el));

  // ── Section title reveal (legacy .fade-in support) ─────────────
  const legacyObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible', 'is-visible');
        legacyObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => legacyObserver.observe(el));

  // ── Section title word-reveal stagger ──────────────────────────
  const titleObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        titleObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.section-title, .reveal-word').forEach(el => titleObserver.observe(el));

  // ── Navbar: add scrolled class on scroll ────────────────────────
  const navbar2 = document.querySelector('.navbar');
  if (navbar2) {
    window.addEventListener('scroll', () => {
      navbar2.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });
  }

  // ── Subtle parallax on hero ghost text ─────────────────────────
  const heroGhost = document.querySelector('.hero-ghost');
  const heroTicker = document.querySelector('.hero-ticker');
  if (heroGhost || heroTicker) {
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          const y = window.scrollY;
          if (heroGhost) heroGhost.style.transform = `translate(-50%, calc(-50% + ${y * 0.18}px))`;
          if (heroTicker) heroTicker.style.transform = `translateY(${y * 0.08}px)`;
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  // ── Auto-add data-reveal to main content blocks ─────────────────
  // Solution cards — stagger each child
  document.querySelectorAll('.grid-3 .solution-card, .grid-3 .testimonial-card, .grid-3 .article-card').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal')) {
      el.setAttribute('data-reveal', '');
      const delay = (i % 3) + 1;
      el.setAttribute('data-reveal-delay', String(delay));
      revealObserver.observe(el);
    }
  });

  // Stats row items
  document.querySelectorAll('.stat-item').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal')) {
      el.setAttribute('data-reveal', '');
      el.setAttribute('data-reveal-delay', String(i + 1));
      revealObserver.observe(el);
    }
  });

  // Section labels + titles
  document.querySelectorAll('.section-label, .section-title, .section-subtitle').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal')) {
      el.setAttribute('data-reveal', '');
      el.setAttribute('data-reveal-delay', String(i % 3 + 1));
      revealObserver.observe(el);
    }
  });

  // Case cards, team cards, event cards
  document.querySelectorAll('.case-card, .team-card, .event-card').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal')) {
      el.setAttribute('data-reveal', '');
      el.setAttribute('data-reveal-delay', String((i % 4) + 1));
      revealObserver.observe(el);
    }
  });

  // Page heroes
  document.querySelectorAll('.page-hero h1, .page-hero p, .page-hero .page-label').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal')) {
      el.setAttribute('data-reveal', '');
      el.setAttribute('data-reveal-delay', String(i + 1));
      revealObserver.observe(el);
    }
  });

  // CTA section
  document.querySelectorAll('.section-full h2, .section-full p, .section-full .btn').forEach((el, i) => {
    if (!el.hasAttribute('data-reveal')) {
      el.setAttribute('data-reveal', '');
      el.setAttribute('data-reveal-delay', String(i + 1));
      revealObserver.observe(el);
    }
  });

  // ── Counter animation ──────────────────────────────────────────
  function animateCounter(el) {
    const target = parseInt(el.dataset.target || el.textContent);
    const suffix = el.dataset.suffix || '';
    const duration = 1600;
    const step = target / (duration / 16);
    let current = 0;
    el.closest('.stat-number')?.classList.add('counting');

    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = Math.round(current) + suffix;
    }, 16);
  }

  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.count-up').forEach(el => counterObserver.observe(el));

});