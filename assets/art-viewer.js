(function () {
  var links = document.querySelectorAll('a.art-zoom');
  if (!links.length) return;

  var hint = document.body.getAttribute('data-viewer-hint') || 'Pinch or scroll to zoom. Escape closes.';
  var closeLabel = document.body.getAttribute('data-viewer-close') || 'Close';

  var dialog = document.createElement('dialog');
  dialog.className = 'art-viewer';
  dialog.innerHTML =
    '<button type="button" class="art-viewer-close"></button>' +
    '<div class="art-viewer-stage"><img alt=""></div>' +
    '<p class="art-viewer-hint"></p>';
  document.body.appendChild(dialog);

  var closeBtn = dialog.querySelector('.art-viewer-close');
  var stage = dialog.querySelector('.art-viewer-stage');
  var img = stage.querySelector('img');
  var hintEl = dialog.querySelector('.art-viewer-hint');
  closeBtn.textContent = closeLabel;
  hintEl.textContent = hint;

  var scale = 1;
  var x = 0;
  var y = 0;
  var pointers = new Map();
  var lastTap = 0;
  var opener = null;
  var pinch = null;

  function fit() {
    var nw = img.naturalWidth || img.width || 1;
    var nh = img.naturalHeight || img.height || 1;
    var ratio = Math.min(stage.clientWidth / nw, stage.clientHeight / nh, 1);
    var w = nw * ratio;
    var h = nh * ratio;
    img.style.width = w + 'px';
    img.style.height = h + 'px';
    scale = 1;
    x = (stage.clientWidth - w) / 2;
    y = (stage.clientHeight - h) / 2;
    draw();
  }

  function draw() {
    img.style.transform = 'translate(' + x + 'px,' + y + 'px) scale(' + scale + ')';
  }

  function clampScale(value) {
    return Math.min(5, Math.max(1, value));
  }

  function zoomAt(next, cx, cy) {
    next = clampScale(next);
    var rect = stage.getBoundingClientRect();
    var px = cx - rect.left;
    var py = cy - rect.top;
    var ratio = next / scale;
    x = px - (px - x) * ratio;
    y = py - (py - y) * ratio;
    scale = next;
    if (scale === 1) fit();
    else draw();
  }

  function open(anchor) {
    opener = anchor;
    var full = anchor.getAttribute('href');
    var image = anchor.querySelector('img');
    img.alt = image ? image.alt : '';
    dialog.setAttribute('aria-label', img.alt || closeLabel);
    img.onload = function () { fit(); };
    if (img.getAttribute('src') !== full) img.src = full;
    else fit();
    if (!dialog.open) dialog.showModal();
    closeBtn.focus();
  }

  links.forEach(function (anchor) {
    anchor.addEventListener('click', function (event) {
      event.preventDefault();
      open(anchor);
    });
  });

  closeBtn.addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('close', function () {
    scale = 1;
    if (opener) opener.focus();
  });
  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener('keydown', function (event) {
    var step = 40;
    if (event.key === 'Escape') return;
    if (event.key === '+' || event.key === '=') {
      event.preventDefault();
      zoomAt(scale * 1.2, stage.clientWidth / 2, stage.clientHeight / 2);
    } else if (event.key === '-' || event.key === '_') {
      event.preventDefault();
      zoomAt(scale / 1.2, stage.clientWidth / 2, stage.clientHeight / 2);
    } else if (event.key === '0') {
      event.preventDefault();
      fit();
    } else if (event.key === 'ArrowLeft') { event.preventDefault(); x += step; draw(); }
    else if (event.key === 'ArrowRight') { event.preventDefault(); x -= step; draw(); }
    else if (event.key === 'ArrowUp') { event.preventDefault(); y += step; draw(); }
    else if (event.key === 'ArrowDown') { event.preventDefault(); y -= step; draw(); }
  });

  stage.addEventListener('wheel', function (event) {
    event.preventDefault();
    var next = scale * (event.deltaY < 0 ? 1.12 : 1 / 1.12);
    zoomAt(next, event.clientX, event.clientY);
  }, { passive: false });

  stage.addEventListener('pointerdown', function (event) {
    try { stage.setPointerCapture(event.pointerId); } catch (err) {}
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    if (pointers.size === 1) {
      stage.classList.add('is-panning');
      var now = Date.now();
      if (now - lastTap < 300) {
        zoomAt(scale > 1 ? 1 : 2.2, event.clientX, event.clientY);
        lastTap = 0;
      } else lastTap = now;
    }
    if (pointers.size === 2) {
      var pts = Array.from(pointers.values());
      pinch = {
        dist: Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y),
        scale: scale,
        cx: (pts[0].x + pts[1].x) / 2,
        cy: (pts[0].y + pts[1].y) / 2
      };
    }
  });

  stage.addEventListener('pointermove', function (event) {
    if (!pointers.has(event.pointerId)) return;
    var prev = pointers.get(event.pointerId);
    pointers.set(event.pointerId, { x: event.clientX, y: event.clientY });
    if (pointers.size === 1 && scale > 1 && pinch === null) {
      x += event.clientX - prev.x;
      y += event.clientY - prev.y;
      draw();
    } else if (pointers.size === 2 && pinch) {
      var pts = Array.from(pointers.values());
      var dist = Math.hypot(pts[0].x - pts[1].x, pts[0].y - pts[1].y);
      if (pinch.dist > 0) zoomAt(pinch.scale * (dist / pinch.dist), pinch.cx, pinch.cy);
    }
  });

  function endPointer(event) {
    pointers.delete(event.pointerId);
    if (pointers.size < 2) pinch = null;
    if (pointers.size === 0) stage.classList.remove('is-panning');
  }
  stage.addEventListener('pointerup', endPointer);
  stage.addEventListener('pointercancel', endPointer);

  window.addEventListener('resize', function () {
    if (dialog.open) fit();
  });
})();
