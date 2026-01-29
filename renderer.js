function renderRouters() {
  routersEl.innerHTML = '';
  routers.forEach(r => {
    const div = document.createElement('div');
    div.className = 'router';
    div.id = 'router-' + r.id;

    div.innerHTML = `
      <div class="name">${r.id}</div>
      <div class="ip">${r.ip}:${r.port}</div>
      <div>
        <span class="dot ${r.status === 'connected' ? 'green' : r.status === 'unauthorized' ? 'red' : ''}"></span>
        <span class="stat">${r.status}</span>
      </div>
      <div style="margin-top:8px;">
        <button class="connect-btn">Connect</button>
        <button class="view-btn">View</button>
        <button class="restart-btn">Restart Router</button>
        <button class="interfaces-btn">Show Interfaces</button>
      </div>
    `;
    routersEl.appendChild(div);

    // Add event listeners for dynamic buttons
    div.querySelector('.connect-btn').addEventListener('click', () => connectRouter(r.id));
    div.querySelector('.view-btn').addEventListener('click', () => viewRouter(r.id));
    div.querySelector('.restart-btn').addEventListener('click', () => {
      log(`${r.id}: Restart command simulated`);
      r.status = 'restarting (sim)';
      renderRouters();
      setTimeout(() => {
        r.status = 'connected (sim)';
        renderRouters();
        log(`${r.id}: Restart complete`);
      }, 2000);
    });
    div.querySelector('.interfaces-btn').addEventListener('click', () => {
      log(`${r.id}: Interfaces => Gig0/0, Gig0/1, Gig0/2 (simulated)`);
    });
  });
}
