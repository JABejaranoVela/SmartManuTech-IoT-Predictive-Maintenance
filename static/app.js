const state = {
  machines: [],
  alerts: [],
  readings: [],
};

async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function formatTime(value) {
  return new Date(value).toLocaleTimeString("es-ES", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function renderKpis() {
  const totalAlerts = state.alerts.length;
  const criticalMachines = state.machines.filter((m) => m.status === "critical").length;
  const warningMachines = state.machines.filter((m) => m.status === "warning").length;
  const avgRisk = state.machines.length
    ? Math.round(state.machines.reduce((sum, m) => sum + m.risk_score, 0) / state.machines.length)
    : 0;

  document.querySelector("#kpis").innerHTML = `
    <div class="kpi"><span>Máquinas monitorizadas</span><strong>${state.machines.length}</strong></div>
    <div class="kpi"><span>Riesgo medio</span><strong>${avgRisk}</strong></div>
    <div class="kpi"><span>Máquinas en aviso</span><strong>${warningMachines}</strong></div>
    <div class="kpi"><span>Máquinas críticas</span><strong>${criticalMachines}</strong></div>
    <div class="kpi"><span>Alertas recientes</span><strong>${totalAlerts}</strong></div>
  `;
}

function renderAlertSummary() {
  const labels = {
    TEMP_HIGH: "Temperatura alta",
    VIBRATION_HIGH: "Vibracion excesiva",
    SPEED_LOW: "Velocidad baja",
    ENERGY_HIGH: "Consumo alto",
    ERROR_EVENT: "Error critico",
    PREDICTIVE_RISK_HIGH: "Riesgo predictivo",
  };
  const counts = Object.fromEntries(Object.keys(labels).map((code) => [code, 0]));
  state.alerts.forEach((alert) => {
    counts[alert.code] = (counts[alert.code] || 0) + 1;
  });
  document.querySelector("#alertSummary").innerHTML = Object.entries(labels)
    .map(
      ([code, label]) => `
      <div class="alert-type">
        <span>${label}</span>
        <strong>${counts[code] || 0}</strong>
      </div>
    `,
    )
    .join("");
}

function renderMachines() {
  const html = state.machines
    .map(
      (machine) => `
      <div class="machine ${machine.status}">
        <h3>${machine.machine_id}</h3>
        <dl>
          <dt>Estado</dt><dd>${machine.status}</dd>
          <dt>Riesgo</dt><dd>${machine.risk_score}/100</dd>
          <dt>Temperatura</dt><dd>${machine.temperature_c} ºC</dd>
          <dt>Vibración</dt><dd>${machine.vibration_mm_s} mm/s</dd>
          <dt>Velocidad</dt><dd>${machine.production_speed_pct}%</dd>
          <dt>Alertas</dt><dd>${machine.total_alerts}</dd>
        </dl>
      </div>
    `,
    )
    .join("");
  document.querySelector("#machines").innerHTML = html || "<p>No hay lecturas todavía.</p>";
}

function renderAlerts() {
  const html = state.alerts
    .map(
      (alert) => `
      <tr>
        <td>${formatTime(alert.timestamp)}</td>
        <td>${alert.machine_id}</td>
        <td>${alert.message}</td>
        <td><span class="badge ${alert.severity}">${alert.severity}</span></td>
        <td>${alert.recommendation}</td>
      </tr>
    `,
    )
    .join("");
  document.querySelector("#alerts").innerHTML =
    html || '<tr><td colspan="5">No hay alertas registradas.</td></tr>';
}

function drawRiskChart() {
  const canvas = document.querySelector("#riskChart");
  const ctx = canvas.getContext("2d");
  const readings = [...state.readings].reverse().slice(-30);
  const width = canvas.width;
  const height = canvas.height;
  const padding = 36;

  ctx.clearRect(0, 0, width, height);
  ctx.strokeStyle = "#dbe3ed";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padding, padding);
  ctx.lineTo(padding, height - padding);
  ctx.lineTo(width - padding, height - padding);
  ctx.stroke();

  [40, 70].forEach((level) => {
    const y = height - padding - (level / 100) * (height - padding * 2);
    ctx.strokeStyle = level === 70 ? "#c53030" : "#b7791f";
    ctx.setLineDash([6, 4]);
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(width - padding, y);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = level === 70 ? "#c53030" : "#b7791f";
    ctx.font = "12px Arial";
    ctx.fillText(level === 70 ? "Critico 70" : "Aviso 40", width - padding - 72, y - 6);
  });
  ctx.setLineDash([]);

  if (readings.length < 2) {
    ctx.fillStyle = "#657285";
    ctx.fillText("Sin datos suficientes para graficar.", padding + 12, height / 2);
    return;
  }

  const step = (width - padding * 2) / (readings.length - 1);
  ctx.strokeStyle = "#2266aa";
  ctx.lineWidth = 3;
  ctx.beginPath();
  readings.forEach((reading, index) => {
    const x = padding + index * step;
    const y = height - padding - (reading.risk_score / 100) * (height - padding * 2);
    if (index === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  ctx.fillStyle = "#18212f";
  ctx.font = "13px Arial";
  ctx.fillText("0", 10, height - padding + 4);
  ctx.fillText("100", 6, padding + 4);
  ctx.fillText("Riesgo de fallo", padding, 18);
}

async function refresh() {
  const [machines, alerts, readings] = await Promise.all([
    fetchJson("/api/machines"),
    fetchJson("/api/alerts?limit=50"),
    fetchJson("/api/readings?limit=80"),
  ]);
  state.machines = machines;
  state.alerts = alerts;
  state.readings = readings;
  renderKpis();
  renderAlertSummary();
  renderMachines();
  renderAlerts();
  drawRiskChart();
  document.querySelector("#updatedAt").textContent = `Actualizado ${new Date().toLocaleTimeString("es-ES")}`;
}

document.querySelector("#simulateBtn").addEventListener("click", async () => {
  await fetchJson("/api/simulate", { method: "POST" });
  await refresh();
});

document.querySelector("#demoBtn").addEventListener("click", async () => {
  await fetchJson("/api/reset-demo", { method: "POST" });
  await refresh();
});

refresh();
setInterval(refresh, 3000);
