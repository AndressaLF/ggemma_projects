(function () {
  var el = document.getElementById("last-update");
  if (!el) return;
  var d = new Date(document.lastModified);
  var meses = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
  ];
  el.textContent = meses[d.getMonth()] + "/" + d.getFullYear();
  el.setAttribute("datetime", d.toISOString().slice(0, 10));
})();
