window.setTimeout(() => {
  document.querySelectorAll('.flash').forEach((el) => {
    el.style.transition = 'opacity .4s ease';
    el.style.opacity = '0';
    window.setTimeout(() => el.remove(), 450);
  });
}, 2500);
