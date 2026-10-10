/* Nutrition & Market — script commun à toutes les pages */
(function () {
  'use strict';

  var NM = window.NM || { products: {}, whatsapp: '', shop: '' };
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var fmt = function (n) { return n.toLocaleString('fr-FR').replace(/\u202f|\u00a0/g, '\u00a0') + '\u00a0FCFA'; };

  /* ---------- Menu mobile ---------- */
  var toggle = $('#mobileToggle');
  var nav = $('#mainNav');
  function setMenu(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle('active', open);
    toggle.setAttribute('aria-expanded', String(open));
    var icon = $('i', toggle);
    if (icon) { icon.className = open ? 'fas fa-times' : 'fas fa-bars'; }
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('active')); });
    $$('a', nav).forEach(function (a) {
      a.addEventListener('click', function () { setMenu(false); });
    });
  }

  /* ---------- Ombre de l'en-tête ---------- */
  var header = $('#header');
  if (header) {
    var onScroll = function () {
      header.style.boxShadow = window.scrollY > 50
        ? '0 4px 20px rgba(0,0,0,0.1)' : '0 1px 2px rgba(0,0,0,0.05)';
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Apparition au scroll ---------- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Panier (envoyé par WhatsApp) ---------- */
  var KEY = 'nm-cart';
  var memory = {};
  function readCart() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return memory; }
  }
  function writeCart(cart) {
    memory = cart;
    try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (e) { /* stockage indisponible */ }
  }

  var drawer = $('#cartDrawer');
  var overlay = $('#cartOverlay');
  var body = $('#cartBody');
  var totalEl = $('#cartTotal');
  var countEl = $('#cartCount');
  var orderBtn = $('#cartOrder');

  function openCart(open) {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    overlay.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('no-scroll', open);
  }

  function renderCart() {
    if (!body) return;
    var cart = readCart();
    var ids = Object.keys(cart).filter(function (id) { return NM.products[id] && cart[id] > 0; });
    var total = 0, count = 0, lines = [];
    body.innerHTML = '';

    if (!ids.length) {
      body.innerHTML = '<p class="empty-state">Votre panier est vide.</p>';
    }
    ids.forEach(function (id) {
      var p = NM.products[id], qty = cart[id], sub = p.price * qty;
      total += sub; count += qty;
      lines.push('- ' + qty + ' x ' + p.name + ' (' + fmt(sub) + ')');
      var row = document.createElement('div');
      row.className = 'cart-item';
      row.innerHTML =
        '<div class="cart-item-info"><strong></strong><span>' + fmt(p.price) + '</span></div>' +
        '<div class="cart-qty">' +
        '<button type="button" data-act="dec" aria-label="Retirer un">&minus;</button>' +
        '<span>' + qty + '</span>' +
        '<button type="button" data-act="inc" aria-label="Ajouter un">+</button></div>' +
        '<button type="button" class="cart-remove" data-act="del" aria-label="Supprimer">&times;</button>';
      $('strong', row).textContent = p.name;
      row.addEventListener('click', function (e) {
        var act = e.target.closest('[data-act]');
        if (!act) return;
        var c = readCart();
        if (act.dataset.act === 'inc') c[id] = (c[id] || 0) + 1;
        if (act.dataset.act === 'dec') c[id] = Math.max(0, (c[id] || 0) - 1);
        if (act.dataset.act === 'del') c[id] = 0;
        if (!c[id]) delete c[id];
        writeCart(c); renderCart();
      });
      body.appendChild(row);
    });

    if (totalEl) totalEl.textContent = fmt(total);
    if (countEl) { countEl.textContent = count; countEl.classList.toggle('has-items', count > 0); }
    if (orderBtn) {
      var msg = 'Bonjour ' + NM.shop + ', je souhaite commander :\n' + lines.join('\n') +
                '\nTotal : ' + fmt(total) + '\nPaiement à la livraison.';
      orderBtn.href = 'https://wa.me/' + NM.whatsapp + '?text=' + encodeURIComponent(msg);
      orderBtn.classList.toggle('disabled', !ids.length);
      orderBtn.setAttribute('aria-disabled', String(!ids.length));
    }
  }

  if (drawer) {
    $('#cartOpen').addEventListener('click', function () { openCart(true); });
    $('#cartClose').addEventListener('click', function () { openCart(false); });
    overlay.addEventListener('click', function () { openCart(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') openCart(false); });
    if (orderBtn) {
      orderBtn.addEventListener('click', function (e) {
        if (orderBtn.classList.contains('disabled')) e.preventDefault();
      });
    }
    $$('[data-add]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.dataset.add, c = readCart();
        c[id] = (c[id] || 0) + 1;
        writeCart(c); renderCart();
        var icon = $('i', btn);
        if (icon) {
          icon.className = 'fas fa-check';
          btn.classList.add('added');
          setTimeout(function () { icon.className = 'fas fa-shopping-cart'; btn.classList.remove('added'); }, 1200);
        }
      });
    });
    renderCart();
  }

  /* ---------- Boutique : filtre + tri ---------- */
  var catalog = $('#catalog');
  if (catalog) {
    var cards = $$('.product-card', catalog);
    var original = cards.slice();
    var filter = 'all';
    var sortSel = $('#sortSelect');
    var empty = $('#catalogEmpty');

    var apply = function () {
      var list = original.slice();
      if (sortSel && sortSel.value !== 'default') {
        list.sort(function (a, b) {
          var d = Number(a.dataset.price) - Number(b.dataset.price);
          return sortSel.value === 'asc' ? d : -d;
        });
      }
      var shown = 0;
      list.forEach(function (card) {
        var ok = filter === 'all' || card.dataset.new === '1';
        card.hidden = !ok;
        if (ok) shown++;
        catalog.appendChild(card);
      });
      if (empty) empty.hidden = shown > 0;
    };

    $$('.filter-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        filter = b.dataset.filter;
        $$('.filter-btn').forEach(function (x) { x.classList.toggle('active', x === b); });
        apply();
      });
    });
    if (sortSel) sortSel.addEventListener('change', apply);

    if (new URLSearchParams(location.search).get('filtre') === 'nouveau') {
      var nb = $('.filter-btn[data-filter="new"]');
      if (nb) nb.click();
    }
  }

  /* ---------- Annonces : marquer les annonces terminées ---------- */
  $$('.annonce-card[data-end]').forEach(function (card) {
    var end = new Date(card.dataset.end + 'T23:59:59');
    if (end < new Date()) {
      card.classList.add('is-ended');
      var tag = $('.tag-ended', card);
      if (tag && card.dataset.endedLabel) {
        tag.textContent = card.dataset.endedLabel;
        tag.hidden = false;
      }
    }
  });

  /* ---------- Newsletter (démo : aucune donnée enregistrée) ---------- */
  var nl = $('#newsletterForm');
  var nlMsg = $('#newsletterFeedback');
  if (nl) {
    nl.addEventListener('submit', function (e) {
      e.preventDefault();
      var input = $('input', nl);
      if (!input.value) return;
      input.value = '';
      nlMsg.textContent = 'Merci ! Ce site est une démonstration : aucune inscription n\'est enregistrée.';
      nlMsg.hidden = false;
    });
  }

  /* ---------- Contact : message préparé dans WhatsApp ---------- */
  var cf = $('#contactForm');
  if (cf) {
    var cfMsg = $('#contactFeedback');
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = cf.elements.name.value.trim();
      var message = cf.elements.message.value.trim();
      if (!name || !message) {
        cfMsg.textContent = 'Merci de renseigner votre nom et votre message.';
        cfMsg.hidden = false;
        return;
      }
      var phone = cf.elements.phone.value.trim();
      var text = 'Bonjour ' + NM.shop + ',\nSujet : ' + cf.elements.subject.value +
                 '\n\n' + message + '\n\n' + name + (phone ? ' — ' + phone : '');
      window.open('https://wa.me/' + NM.whatsapp + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
      cfMsg.textContent = 'WhatsApp s\'ouvre avec votre message prêt à être envoyé.';
      cfMsg.hidden = false;
    });
  }
})();
