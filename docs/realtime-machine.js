const STORAGE_KEY = "cyntra-test-realtime-machine-v2";

const defaultState = {
  status: "idle",
  mode: "bot-testing",
  tickIntervalMs: 1000,
  tickCount: 0,
  startedAt: null,
  lastTickAt: null,
  lmStudioBase: "http://localhost:1234",
  lmStudioStatus: "unknown",
  backendUrl: "http://127.0.0.1:8787",
  backendStatus: "local",
  backendState: null,
  queue: [
    { id: crypto.randomUUID(), label: "Run LM Studio model list check", createdAt: new Date().toISOString(), status: "queued" },
    { id: crypto.randomUUID(), label: "Run bot behavior smoke test", createdAt: new Date().toISOString(), status: "queued" },
    { id: crypto.randomUUID(), label: "Record results into Wisebase / repo logs", createdAt: new Date().toISOString(), status: "queued" }
  ],
  events: []
};

let machine = loadState();
let timer = null;
let bootTime = Date.now();

const el = {
  machineLight: document.querySelector("#machineLight"),
  machineStateLabel: document.querySelector("#machineStateLabel"),
  machineSubtitle: document.querySelector("#machineSubtitle"),
  tickCount: document.querySelector("#tickCount"),
  uptime: document.querySelector("#uptime"),
  heartbeat: document.querySelector("#heartbeat"),
  backendStatus: document.querySelector("#backendStatus"),
  lmStudioStatus: document.querySelector("#lmStudioStatus"),
  tickInterval: document.querySelector("#tickInterval"),
  machineMode: document.querySelector("#machineMode"),
  lmStudioBase: document.querySelector("#lmStudioBase"),
  backendUrl: document.querySelector("#backendUrl"),
  backendSnapshot: document.querySelector("#backendSnapshot"),
  snapshot: document.querySelector("#snapshot"),
  eventLog: document.querySelector("#eventLog"),
  workQueue: document.querySelector("#workQueue"),
  startButton: document.querySelector("#startButton"),
  pauseButton: document.querySelector("#pauseButton"),
  tickButton: document.querySelector("#tickButton"),
  resetButton: document.querySelector("#resetButton"),
  pingLmStudio: document.querySelector("#pingLmStudio"),
  syncBackend: document.querySelector("#syncBackend"),
  copySnapshot: document.querySelector("#copySnapshot"),
  downloadSnapshot: document.querySelector("#downloadSnapshot"),
  addQueueItem: document.querySelector("#addQueueItem"),
  completeQueueItem: document.querySelector("#completeQueueItem"),
  clearLog: document.querySelector("#clearLog")
};

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (saved && typeof saved === "object") return { ...defaultState, ...saved, status: "idle" };
  } catch (error) {
    console.warn("State load failed", error);
  }
  return structuredClone(defaultState);
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(machine));
}

function logEvent(message, type = "info", detail = null) {
  machine.events.unshift({ id: crypto.randomUUID(), time: new Date().toISOString(), type, message, detail });
  machine.events = machine.events.slice(0, 80);
  saveState();
  render();
}

function formatDuration(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const hours = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const seconds = String(totalSeconds % 60).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
}

function buildSnapshot() {
  return {
    project: "Cynntra/test",
    machine: "cyntra-test-realtime-machine",
    status: machine.status,
    mode: machine.mode,
    tickIntervalMs: machine.tickIntervalMs,
    tickCount: machine.tickCount,
    startedAt: machine.startedAt,
    lastTickAt: machine.lastTickAt,
    lmStudioBase: machine.lmStudioBase,
    lmStudioStatus: machine.lmStudioStatus,
    backendUrl: machine.backendUrl,
    backendStatus: machine.backendStatus,
    backendTickCount: machine.backendState?.tick_count ?? null,
    backendLastDaemonReportAt: machine.backendState?.last_daemon_report_at ?? null,
    queueOpen: machine.queue.filter((item) => item.status !== "done").length,
    eventCount: machine.events.length,
    generatedAt: new Date().toISOString()
  };
}

function render() {
  const snapshot = buildSnapshot();
  el.machineStateLabel.textContent = capitalize(machine.status);
  el.machineSubtitle.textContent = machine.status === "running" ? `${machine.mode} · ${machine.tickIntervalMs}ms tick` : "Machine is not actively ticking.";
  el.machineLight.className = `light ${machine.status}`;
  el.tickCount.textContent = String(machine.tickCount);
  el.heartbeat.textContent = machine.lastTickAt ? new Date(machine.lastTickAt).toLocaleTimeString() : "silent";
  el.uptime.textContent = machine.startedAt ? formatDuration(Date.now() - new Date(machine.startedAt).getTime()) : formatDuration(Date.now() - bootTime);
  el.backendStatus.textContent = machine.backendStatus;
  el.lmStudioStatus.textContent = machine.lmStudioStatus;
  el.tickInterval.value = String(machine.tickIntervalMs);
  el.machineMode.value = machine.mode;
  el.lmStudioBase.value = machine.lmStudioBase;
  el.backendUrl.value = machine.backendUrl;
  el.snapshot.textContent = JSON.stringify(snapshot, null, 2);
  el.backendSnapshot.textContent = machine.backendState ? JSON.stringify(machine.backendState, null, 2) : "No backend state loaded yet.";

  el.workQueue.innerHTML = machine.queue.map((item) => `
    <li>
      <strong>${escapeHtml(item.label)}</strong>
      <small>${item.status} · ${new Date(item.createdAt).toLocaleString()}</small>
    </li>
  `).join("");

  el.eventLog.innerHTML = machine.events.map((event) => `
    <li>
      <strong>${escapeHtml(event.message)}</strong>
      <small>${event.type} · ${new Date(event.time).toLocaleString()}</small>
    </li>
  `).join("");
}

function capitalize(value) {
  return `${value.charAt(0).toUpperCase()}${value.slice(1)}`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function startMachine() {
  if (timer) clearInterval(timer);
  machine.status = "running";
  machine.startedAt ||= new Date().toISOString();
  timer = setInterval(tickMachine, machine.tickIntervalMs);
  logEvent("Machine started", "state");
}

function pauseMachine() {
  if (timer) clearInterval(timer);
  timer = null;
  machine.status = "paused";
  logEvent("Machine paused", "state");
}

function resetMachine() {
  if (timer) clearInterval(timer);
  timer = null;
  machine = structuredClone(defaultState);
  bootTime = Date.now();
  saveState();
  logEvent("Machine reset", "state");
}

function tickMachine() {
  machine.tickCount += 1;
  machine.lastTickAt = new Date().toISOString();
  if (machine.tickCount % 15 === 0) logEvent(`Major checkpoint reached at tick ${machine.tickCount}`, "checkpoint");
  else if (machine.tickCount % 5 === 0) logEvent(`Minor checkpoint reached at tick ${machine.tickCount}`, "checkpoint");
  else logEvent(`Tick ${machine.tickCount}`, "tick");
  saveState();
  render();
}

async function pingLmStudioModels() {
  const base = machine.lmStudioBase.replace(/\/$/, "");
  machine.lmStudioStatus = "checking";
  render();
  try {
    const response = await fetch(`${base}/v1/models`, { method: "GET" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    const payload = await response.json();
    const count = Array.isArray(payload.data) ? payload.data.length : "unknown";
    machine.lmStudioStatus = `online · ${count} models`;
    logEvent("LM Studio model endpoint responded", "lmstudio", payload);
  } catch (error) {
    machine.lmStudioStatus = "blocked/offline";
    logEvent(`LM Studio check failed: ${error.message}`, "error");
  }
  saveState();
  render();
}

async function syncFromBackend() {
  const base = machine.backendUrl.replace(/\/$/, "");
  machine.backendStatus = "checking";
  render();
  try {
    const response = await fetch(`${base}/state`, { method: "GET" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    const payload = await response.json();
    machine.backendState = payload;
    machine.backendStatus = "online";
    if (payload.lmstudio?.status) machine.lmStudioStatus = payload.lmstudio.status;
    if (typeof payload.tick_count === "number") machine.tickCount = Math.max(machine.tickCount, payload.tick_count);
    logEvent("Backend state synced", "backend", { tick_count: payload.tick_count, lmstudio: payload.lmstudio?.status });
  } catch (error) {
    machine.backendStatus = "offline";
    logEvent(`Backend sync failed: ${error.message}`, "error");
  }
  saveState();
  render();
}

function addQueueItem() {
  const label = `Realtime tick task ${machine.tickCount + 1}`;
  machine.queue.push({ id: crypto.randomUUID(), label, createdAt: new Date().toISOString(), status: "queued" });
  logEvent(`Added queue item: ${label}`, "queue");
}

function completeQueueItem() {
  const item = machine.queue.find((entry) => entry.status !== "done");
  if (!item) {
    logEvent("No open queue items to complete", "queue");
    return;
  }
  item.status = "done";
  logEvent(`Completed queue item: ${item.label}`, "queue");
}

async function copySnapshot() {
  await navigator.clipboard.writeText(JSON.stringify(buildSnapshot(), null, 2));
  logEvent("Copied machine snapshot", "snapshot");
}

function downloadSnapshot() {
  const blob = new Blob([JSON.stringify(buildSnapshot(), null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `cyntra-test-machine-${Date.now()}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  logEvent("Downloaded machine snapshot", "snapshot");
}

el.startButton.addEventListener("click", startMachine);
el.pauseButton.addEventListener("click", pauseMachine);
el.tickButton.addEventListener("click", tickMachine);
el.resetButton.addEventListener("click", resetMachine);
el.pingLmStudio.addEventListener("click", pingLmStudioModels);
el.syncBackend.addEventListener("click", syncFromBackend);
el.copySnapshot.addEventListener("click", copySnapshot);
el.downloadSnapshot.addEventListener("click", downloadSnapshot);
el.addQueueItem.addEventListener("click", addQueueItem);
el.completeQueueItem.addEventListener("click", completeQueueItem);
el.clearLog.addEventListener("click", () => {
  machine.events = [];
  saveState();
  render();
});

el.tickInterval.addEventListener("change", (event) => {
  machine.tickIntervalMs = Number(event.target.value);
  logEvent(`Tick interval set to ${machine.tickIntervalMs}ms`, "settings");
  if (machine.status === "running") startMachine();
});

el.machineMode.addEventListener("change", (event) => {
  machine.mode = event.target.value;
  logEvent(`Mode changed to ${machine.mode}`, "settings");
});

el.lmStudioBase.addEventListener("change", (event) => {
  machine.lmStudioBase = event.target.value.trim() || "http://localhost:1234";
  logEvent(`LM Studio base set to ${machine.lmStudioBase}`, "settings");
});

el.backendUrl.addEventListener("change", (event) => {
  machine.backendUrl = event.target.value.trim() || "http://127.0.0.1:8787";
  logEvent(`Backend URL set to ${machine.backendUrl}`, "settings");
});

setInterval(render, 1000);
setInterval(() => {
  if (machine.status === "running") syncFromBackend();
}, 30000);
render();
logEvent("Realtime machine page loaded", "state");
