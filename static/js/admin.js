// ================================================================
// AI-SOLUTIONS — ADMIN JS
// ================================================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Delete confirmation ────────────────────────────────────────
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      const item = this.dataset.item || 'this item';
      if (!confirm(`Are you sure you want to delete ${item}? This cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });

  // ── Image preview ──────────────────────────────────────────────
  document.querySelectorAll('.file-preview-input').forEach(input => {
    input.addEventListener('change', function () {
      const wrap = this.closest('.upload-zone-wrap');
      const preview = wrap?.querySelector('.image-preview');
      if (preview && this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
          preview.style.display = 'block';
          const img = preview.querySelector('img');
          if (img) img.src = e.target.result;
          const uploadText = wrap.querySelector('.upload-text');
          if (uploadText) uploadText.textContent = this.files[0].name;
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  });

  // ── Mobile sidebar toggle ─────────────────────────────────────
  const sidebar = document.querySelector('.admin-sidebar');
  const sidebarToggleBtn = document.getElementById('sidebarToggle');
  const topbarMenuBtn    = document.getElementById('topbarMenuBtn');

  function toggleSidebar() {
    if (sidebar) sidebar.classList.toggle('open');
  }

  if (sidebarToggleBtn) sidebarToggleBtn.addEventListener('click', toggleSidebar);
  if (topbarMenuBtn)    topbarMenuBtn.addEventListener('click', toggleSidebar);

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', function(e) {
    if (window.innerWidth <= 768 && sidebar && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && e.target !== topbarMenuBtn) {
        sidebar.classList.remove('open');
      }
    }
  });

  // ── Auto-dismiss flash messages ───────────────────────────────
  setTimeout(() => {
    document.querySelectorAll('.flash, .flash-msg').forEach(msg => {
      msg.style.transition = 'opacity 0.4s';
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 400);
    });
  }, 5000);

  document.querySelectorAll('.flash-close').forEach(btn => {
    btn.addEventListener('click', function() {
      const msg = this.closest('.flash') || this.closest('.flash-msg');
      if (msg) msg.remove();
    });
  });

  // ── Textarea auto-resize ──────────────────────────────────────
  document.querySelectorAll('textarea.admin-form-control').forEach(ta => {
    ta.style.height = ta.scrollHeight + 'px';
    ta.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = this.scrollHeight + 'px';
    });
  });

});