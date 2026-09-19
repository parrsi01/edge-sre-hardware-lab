const $ = (id) => document.getElementById(id);
const ui = {
  pill: $('live-pill'), availability: $('availability'), temperature: $('temperature'),
  voltage: $('voltage'), samples: $('samples'), sequence: $('sequence'),
  log: $('operator-log'), chart: $('chart'), inject: $('inject'), recover: $('recover')
};

function paintChart(samples) {
  const canvas = ui.chart;
  const rect = canvas.getBoundingClientRect();
  const scale = window.devicePixelRatio || 1;
  canvas.width = Math.max(500, rect.width * scale);
  canvas.height = 240 * scale;
  const ctx = canvas.getContext('2d');
  ctx.scale(scale, scale);
  const width = canvas.width / scale, height = canvas.height / scale;
  ctx.clearRect(0, 0, width, height);
  ctx.strokeStyle = '#263532'; ctx.lineWidth = 1;
  for (let y = 20; y < height; y += 50) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke(); }
  const values = samples.map(s => s.temperature_c).filter(Number.isFinite);
  if (values.length < 2) return;
  const min = Math.min(...values) - .5, max = Math.max(...values) + .5, range = Math.max(max - min, 1);
  ctx.strokeStyle = '#79f2c0'; ctx.lineWidth = 3; ctx.lineJoin = 'round'; ctx.beginPath();
  values.forEach((value, index) => {
    const x = index / (values.length - 1) * width;
    const y = height - 18 - ((value - min) / range) * (height - 36);
    index ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
  });
  ctx.stroke();
}

async function refresh() {
  try {
    const [statusResponse, sampleResponse] = await Promise.all([fetch('/api/status'), fetch('/api/samples?limit=30')]);
    const status = await statusResponse.json();
    const history = await sampleResponse.json();
    const sample = status.latest_sample;
    ui.pill.className = `pill ${status.connected ? 'ok' : 'fault'}`;
    ui.pill.querySelector('b').textContent = status.connected ? 'System healthy' : 'Fault detected';
    ui.availability.textContent = status.availability_percent == null ? '--' : `${status.availability_percent}%`;
    ui.temperature.textContent = Number.isFinite(sample?.temperature_c) ? `${sample.temperature_c.toFixed(1)}°C` : 'n/a';
    ui.voltage.textContent = Number.isFinite(sample?.voltage_v) ? `${sample.voltage_v.toFixed(2)}V` : 'n/a';
    ui.samples.textContent = status.sample_count;
    ui.sequence.textContent = sample ? `Sequence ${sample.sequence}` : 'Sequence --';
    ui.log.textContent = JSON.stringify({
      connected: status.connected,
      device_status: status.device_status,
      last_error: status.last_error,
      polls: `${status.polls_successful}/${status.polls_total}`,
      latest_observation: sample?.observed_at_unix ?? null
    }, null, 2);
    paintChart(history.samples);
  } catch (error) {
    ui.pill.className = 'pill fault';
    ui.pill.querySelector('b').textContent = 'Control plane unavailable';
    ui.log.textContent = String(error);
  }
}

async function setFault(enabled) {
  ui.inject.disabled = ui.recover.disabled = true;
  try {
    await fetch('/api/fault', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({enabled})});
    setTimeout(refresh, 2200);
  } finally {
    setTimeout(() => { ui.inject.disabled = ui.recover.disabled = false; }, 800);
  }
}

ui.inject.addEventListener('click', () => setFault(true));
ui.recover.addEventListener('click', () => setFault(false));
window.addEventListener('resize', refresh);
refresh();
setInterval(refresh, 2000);
