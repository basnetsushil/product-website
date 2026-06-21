// ================================================================
// AI-SOLUTIONS — ADMIN JS
// ================================================================

document.addEventListener('DOMContentLoaded', function () {

  // ── Delete confirmation ────────────────────────────────────────
  window.confirmDelete = function(form) {
    if (confirm('Are you sure you want to delete this? This cannot be undone.')) {
      form.submit();
    }
  };

  // Also handle .delete-form class
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', function (e) {
      const item = this.dataset.item || 'this item';
      if (!confirm(`Delete ${item}? This cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });

  // ── initImageUpload — used by all add/edit form pages ─────────
  window.initImageUpload = function(inputId, zoneId, previewId, innerZoneId) {
    const input     = document.getElementById(inputId);
    const zone      = document.getElementById(zoneId);
    const preview   = document.getElementById(previewId);
    const innerZone = document.getElementById(innerZoneId);

    if (!input || !zone) return;

    // Click on zone triggers file picker
    zone.addEventListener('click', function(e) {
      if (e.target !== input) input.click();
    });

    // Drag over
    zone.addEventListener('dragover', function(e) {
      e.preventDefault();
      zone.style.borderColor = 'var(--acc)';
      zone.style.background  = 'rgba(232,75,47,0.05)';
    });
    zone.addEventListener('dragleave', function() {
      zone.style.borderColor = '';
      zone.style.background  = '';
    });

    // Drop
    zone.addEventListener('drop', function(e) {
      e.preventDefault();
      zone.style.borderColor = '';
      zone.style.background  = '';
      const file = e.dataTransfer.files[0];
      if (file) {
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
        showPreview(file);
      }
    });

    // File input change
    input.addEventListener('change', function() {
      if (this.files && this.files[0]) showPreview(this.files[0]);
    });

    function showPreview(file) {
      if (!file.type.startsWith('image/')) return;
      const reader = new FileReader();
      reader.onload = function(e) {
        if (preview) {
          preview.src = e.target.result;
          preview.style.display = 'block';
        }
        if (innerZone) {
          // Dim the inner zone text, keep it as background
          innerZone.style.opacity = '0.3';
        }
        zone.style.padding = '12px';
      };
      reader.readAsDataURL(file);
    }
  };

  // ── Legacy image preview (.file-preview-input) ────────────────
  document.querySelectorAll('.file-preview-input').forEach(input => {
    input.addEventListener('change', function () {
      const wrap    = this.closest('.upload-zone-wrap');
      const preview = wrap?.querySelector('.image-preview');
      if (preview && this.files && this.files[0]) {
        const reader = new FileReader();
        reader.onload = e => {
          preview.style.display = 'block';
          const img = preview.querySelector('img');
          if (img) img.src = e.target.result;
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  });

  // ── Mobile sidebar toggle ─────────────────────────────────────
  const sidebar          = document.querySelector('.admin-sidebar');
  const sidebarToggleBtn = document.getElementById('sidebarToggle');
  const topbarMenuBtn    = document.getElementById('topbarMenuBtn');

  function toggleSidebar() {
    if (sidebar) sidebar.classList.toggle('open');
  }

  if (sidebarToggleBtn) sidebarToggleBtn.addEventListener('click', toggleSidebar);
  if (topbarMenuBtn)    topbarMenuBtn.addEventListener('click', toggleSidebar);

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
      msg.style.opacity    = '0';
      setTimeout(() => msg.remove(), 400);
    });
  }, 5000);

  document.querySelectorAll('.flash-close').forEach(btn => {
    btn.addEventListener('click', function() {
      const msg = this.closest('.flash') || this.closest('.flash-msg');
      if (msg) msg.remove();
    });
  });

  // ── Textarea auto-resize (both class names) ───────────────────
  document.querySelectorAll('textarea.admin-form-control, textarea.form-input').forEach(ta => {
    const resize = () => { ta.style.height = 'auto'; ta.style.height = ta.scrollHeight + 'px'; };
    resize();
    ta.addEventListener('input', resize);
  });

  // ── Custom checkbox styling sync ─────────────────────────────
  // Ensure pre-checked boxes (edit forms) show as checked on load
  document.querySelectorAll('.checkbox-input').forEach(cb => {
    const custom = cb.nextElementSibling;
    if (!custom || !custom.classList.contains('checkbox-custom')) return;
    // The CSS handles :checked state, but we need to make sure
    // the native input is visually hidden and only custom shows
    cb.style.position = 'absolute';
    cb.style.opacity  = '0';
    cb.style.width    = '0';
    cb.style.height   = '0';
    cb.style.pointerEvents = 'none';
  });

});