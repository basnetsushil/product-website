// ================================================================
// AI-SOLUTIONS — MAIN JS
// ================================================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Custom Cursor ──────────────────────────────────────────────
  const dot = document.getElementById('cursor-dot');
  const ring = document.getElementById('cursor-ring');

  if (dot && ring) {
    let mouseX = 0, mouseY = 0;
    let ringX = 0, ringY = 0;

    document.addEventListener('mousemove', e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + 'px';
      dot.style.top = mouseY + 'px';
    });

    (function animateRing() {
      ringX += (mouseX - ringX) * 0.12;
      ringY += (mouseY - ringY) * 0.12;
      ring.style.left = ringX + 'px';
      ring.style.top = ringY + 'px';
      requestAnimationFrame(animateRing);
    })();

    document.querySelectorAll('a, button, .btn, .admin-action-btn, .chatbot-btn').forEach(el => {
      el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });
  }

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

  // ── Navbar scroll style ────────────────────────────────────────
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.style.borderBottomColor = window.scrollY > 40 ? '#333' : 'var(--bdr)';
    });
  }

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

  // ── Scroll-in animation (Intersection Observer) ────────────────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

  // ── Counter animation ──────────────────────────────────────────
  function animateCounter(el) {
    const target = parseInt(el.dataset.target || el.textContent);
    const suffix = el.dataset.suffix || '';
    const duration = 1500;
    const step = target / (duration / 16);
    let current = 0;

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