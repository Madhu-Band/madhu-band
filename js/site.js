(function () {
  var dataEl = document.getElementById('shows-data');
  if (!dataEl) return;
  var shows = [];
  try { shows = JSON.parse(dataEl.textContent).shows || []; } catch (e) { shows = []; }

  var today = new Date(); today.setHours(0, 0, 0, 0);
  function parse(s) { var p = String(s).split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  var upcoming = shows
    .filter(function (s) { return s && s.date && parse(s.date) >= today; })
    .sort(function (a, b) { return parse(a.date) - parse(b.date); });

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text) n.textContent = text;
    return n;
  }

  document.querySelectorAll('[data-shows]').forEach(function (target) {
    var limit = parseInt(target.getAttribute('data-limit') || '0', 10);
    var list = limit ? upcoming.slice(0, limit) : upcoming;
    target.textContent = '';
    if (!list.length) {
      var box = el('div', 'empty');
      box.appendChild(el('p', '', 'No upcoming shows are scheduled right now. Check back soon, or contact us about booking.'));
      target.appendChild(box);
      return;
    }
    var ul = el('ul', 'show-list');
    list.forEach(function (s) {
      var d = parse(s.date);
      var li = el('li', 'show');
      var date = el('div', 'date');
      date.appendChild(document.createTextNode(d.toLocaleDateString('en-US', { month: 'short' })));
      date.appendChild(el('span', 'day', String(d.getDate())));
      date.appendChild(document.createTextNode(d.toLocaleDateString('en-US', { weekday: 'short' })));
      li.appendChild(date);
      var info = el('div');
      info.appendChild(el('div', 'venue', s.venue || 'Venue to be announced'));
      var meta = [s.city, s.time].filter(Boolean).join(' · ');
      if (meta) info.appendChild(el('p', 'meta', meta));
      if (s.notes) info.appendChild(el('p', 'meta', s.notes));
      if (s.tickets && /^https:\/\//.test(s.tickets)) {
        var a = el('a', '', 'Tickets / details');
        a.href = s.tickets; a.rel = 'noopener';
        var p = el('p', 'meta'); p.appendChild(a); info.appendChild(p);
      }
      li.appendChild(info);
      ul.appendChild(li);
    });
    target.appendChild(ul);
  });
})();
