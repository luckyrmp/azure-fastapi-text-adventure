async function sendCmd(evt) {
  evt.preventDefault();
  const form = document.getElementById('cmdForm');
  const cmdInput = document.getElementById('cmd');
  const body = new FormData(form);
  const res = await fetch('/action', { method: 'POST', body });
  const html = await res.text();
  document.getElementById('game').innerHTML = html;
  cmdInput.value = '';
  cmdInput.focus();
  return false;
}