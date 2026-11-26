(function () {
  var root = document.documentElement;
  var KEY = "doorUnlocked";
  var bolt = document.getElementById("bolt");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var boltMs = reduce ? 0 : 350;
  var doorMs = reduce ? 0 : 550;
  var dragging = false;
  var startX = 0;
  var moved = 0;
  var timer = 0;

  if (root.classList.contains("is-unlocked") && bolt) bolt.classList.add("is-clear");

  function persist(open) {
    try {
      if (open) localStorage.setItem(KEY, "1");
      else localStorage.removeItem(KEY);
    } catch (err) {}
  }

  function openDoors() {
    if (root.classList.contains("is-unlocked") || root.classList.contains("is-opening")) return;
    window.clearTimeout(timer);
    root.classList.add("is-opening");
    root.classList.remove("is-closing");
    if (bolt) bolt.classList.add("is-clear");
    timer = window.setTimeout(function () {
      root.classList.add("is-unlocked");
      persist(true);
      timer = window.setTimeout(function () {
        root.classList.remove("is-opening");
      }, doorMs + 40);
    }, boltMs);
  }

  function lockDoors() {
    if (!root.classList.contains("is-unlocked") && !root.classList.contains("is-opening")) return;
    window.clearTimeout(timer);
    root.classList.remove("is-unlocked", "is-opening");
    root.classList.add("is-closing");
    window.scrollTo(0, 0);
    timer = window.setTimeout(function () {
      if (bolt) bolt.classList.remove("is-clear");
      timer = window.setTimeout(function () {
        root.classList.remove("is-closing");
        persist(false);
      }, boltMs);
    }, doorMs);
  }

  if (bolt) {
    bolt.addEventListener("click", function () {
      if (moved > 10) {
        moved = 0;
        return;
      }
      openDoors();
    });
    bolt.addEventListener("pointerdown", function (event) {
      dragging = true;
      startX = event.clientX;
      moved = 0;
      if (bolt.setPointerCapture) bolt.setPointerCapture(event.pointerId);
    });
    bolt.addEventListener("pointermove", function (event) {
      if (!dragging || root.classList.contains("is-unlocked")) return;
      var dx = event.clientX - startX;
      moved = Math.max(moved, Math.abs(dx));
      var x = Math.max(-52, Math.min(18, -52 + dx));
      bolt.style.transform = "translate(" + x + "px, -50%)";
      if (dx > 40) {
        dragging = false;
        bolt.style.transform = "";
        openDoors();
      }
    });
    function endDrag() {
      dragging = false;
      if (!root.classList.contains("is-unlocked") && !root.classList.contains("is-opening")) {
        bolt.style.transform = "";
      }
    }
    bolt.addEventListener("pointerup", endDrag);
    bolt.addEventListener("pointercancel", endDrag);
  }

  var bypass = document.getElementById("enterDirect");
  if (bypass) {
    bypass.addEventListener("click", function (event) {
      event.preventDefault();
      openDoors();
    });
  }
  var lock = document.getElementById("lockBolt");
  if (lock) lock.addEventListener("click", lockDoors);

  var regions = {
    record: {
      kicker: "The double ring",
      title: "Las Crónicas and Los Papeles",
      copy: "Primary documentary evidence and the verified family chronicles. Past, present, and future in one ring.",
      links: [["Las Crónicas", "/historia.html"], ["Artifacts", "/artifacts.html"], ["La Familia", "/familia.html"]]
    },
    novels: {
      kicker: "The lower gold-leaf spine",
      title: "The prose novels",
      copy: "Dramatized literature. Book One is listed first.",
      links: [["The Harness-Maker’s Son", "/the-harness-makers-son.html"], ["PASADOR", "/pasador.html"], ["CONCORDIA: la heredera", "/concordia.html"]]
    },
    plays: {
      kicker: "The upper-left gold leaf",
      title: "The plays",
      copy: "The dramatic stage, including the epic play cycle.",
      links: [["La Toma", "/la-toma.html"], ["The Modern Play", "/modern-play.html"], ["From Ship to Ship", "/from-ship-to-ship.html"], ["Belmont Road", "/belmont-road.html"], ["The epic play cycle", "/pasador.html"]]
    },
    manifest: {
      kicker: "The upper-right gold leaf",
      title: "The Manifest",
      copy: "The far horizon. The family cycle six centuries forward among the stars.",
      links: [["The Manifest", "/the-manifest.html"]]
    },
    poems: {
      kicker: "The stream and the stars",
      title: "What’s in the Air and the poems",
      copy: "The living current across centuries.",
      links: [["What’s in the Air", "/whats-in-the-air.html"], ["The Poems", "/poems.html"]]
    },
    studio: {
      kicker: "The signature",
      title: "Author and studio",
      copy: "The maker. Biography, the gallery, articles, and rights.",
      links: [["Author", "/author.html"], ["Art", "/art.html"], ["Articles", "/articles.html"], ["Rights", "/rights.html"]]
    }
  };

  var card = document.getElementById("readingCard");
  var hot = null;

  function clearHot() {
    if (!hot) return;
    hot.querySelectorAll(".hit").forEach(function (shape) { shape.classList.remove("is-hot"); });
    hot = null;
  }

  function showCard(key) {
    var data = regions[key];
    if (!card || !data) return;
    var links = data.links.map(function (pair) {
      return '<a href="' + pair[1] + '">' + pair[0] + "</a>";
    }).join('<span class="sep">·</span>');
    card.innerHTML = '<p class="card-kicker">' + data.kicker + '</p><p class="card-title">' + data.title + '</p><p class="card-copy">' + data.copy + '</p><p class="card-links">' + links + "</p>";
    card.classList.add("is-on");
  }

  document.querySelectorAll("[data-region]").forEach(function (link) {
    var key = link.getAttribute("data-region");
    function light() {
      clearHot();
      hot = link;
      link.querySelectorAll(".hit").forEach(function (shape) { shape.classList.add("is-hot"); });
      showCard(key);
    }
    link.addEventListener("pointerenter", light);
    link.addEventListener("focus", light);
    link.addEventListener("click", function (event) {
      event.preventDefault();
      light();
    });
  });
})();
