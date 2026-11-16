// Canvas 2D 回退：读启元同款 tips/pen（无网格），俯视墨迹 + 粗连杆示意

const $ = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

const state = {
  meta: null,
  tips: null,
  pen: null,
  poses: null,
  numFrames: 0,
  numBodies: 0,
  fps: 30,
  duration: 0,
  time: 0,
  playing: true,
  rate: 1,
  loop: true,
  bodyOrder: [],
};

const canvas = $("c");
const ctx = canvas.getContext("2d");
const overlay = $("overlay");
const overlayText = $("overlayText");

function resize() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.floor(window.innerWidth * dpr);
  canvas.height = Math.floor(window.innerHeight * dpr);
  canvas.style.width = window.innerWidth + "px";
  canvas.style.height = window.innerHeight + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
window.addEventListener("resize", resize);
resize();

function paperCenter() {
  const pc = state.meta?.props?.paper_center || [0.25, 0, 0];
  return { x: pc[0], y: pc[1] };
}

function worldToScreen(x, y) {
  const pc = paperCenter();
  const span = 0.32;
  const w = window.innerWidth;
  const h = window.innerHeight;
  const s = Math.min(w, h) / span;
  const cx = w * 0.55;
  const cy = h * 0.48;
  return { sx: cx + (x - pc.x) * s, sy: cy - (y - pc.y) * s, scale: s };
}

function drawCapsule(ctx, x0, y0, x1, y1, width, fill, stroke) {
  const dx = x1 - x0;
  const dy = y1 - y0;
  const len = Math.hypot(dx, dy) || 1;
  const ux = dx / len;
  const uy = dy / len;
  const px = -uy * (width / 2);
  const py = ux * (width / 2);
  ctx.beginPath();
  ctx.moveTo(x0 + px, y0 + py);
  ctx.lineTo(x1 + px, y1 + py);
  ctx.arc(x1, y1, width / 2, Math.atan2(py, px), Math.atan2(-py, -px));
  ctx.lineTo(x0 - px, y0 - py);
  ctx.arc(x0, y0, width / 2, Math.atan2(-py, -px), Math.atan2(py, px));
  ctx.closePath();
  ctx.fillStyle = fill;
  ctx.fill();
  ctx.strokeStyle = stroke;
  ctx.lineWidth = 1;
  ctx.stroke();
}

function bodyXY(fi, bodyName) {
  const bi = state.bodyOrder.indexOf(bodyName);
  if (bi < 0) return null;
  const o = (fi * state.numBodies + bi) * 7;
  return { x: state.poses[o], y: state.poses[o + 1], z: state.poses[o + 2] };
}

function drawFrame(fi) {
  const w = window.innerWidth;
  const h = window.innerHeight;
  ctx.clearRect(0, 0, w, h);
  const g = ctx.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0, "#1a2438");
  g.addColorStop(1, "#0b1220");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, w, h);

  const pc = paperCenter();
  const paperHalf = 0.09;
  const a = worldToScreen(pc.x - paperHalf, pc.y - paperHalf);
  const b = worldToScreen(pc.x + paperHalf, pc.y + paperHalf);
  const x0 = Math.min(a.sx, b.sx);
  const y0 = Math.min(a.sy, b.sy);
  const pw = Math.abs(b.sx - a.sx);
  const ph = Math.abs(b.sy - a.sy);
  ctx.fillStyle = "#3a3228";
  ctx.fillRect(x0 - 40, y0 - 40, pw + 80, ph + 80);
  ctx.fillStyle = "#f4efe4";
  ctx.fillRect(x0, y0, pw, ph);

  // ink
  ctx.strokeStyle = "#111";
  ctx.lineWidth = 2.2;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  let pen = false;
  ctx.beginPath();
  for (let i = 0; i <= fi; i++) {
    if (!state.pen[i]) {
      pen = false;
      continue;
    }
    const o = i * 3;
    const p = worldToScreen(state.tips[o], state.tips[o + 1]);
    if (!pen) {
      ctx.moveTo(p.sx, p.sy);
      pen = true;
    } else ctx.lineTo(p.sx, p.sy);
  }
  ctx.stroke();

  // arm chain from body poses (xy)
  const chain = ["base", "shoulder", "upper_arm", "lower_arm", "wrist", "gripper", "brush"];
  const pts = chain.map((n) => bodyXY(fi, n)).filter(Boolean);
  const widths = [16, 14, 12, 10, 8, 5];
  for (let k = 0; k < pts.length - 1; k++) {
    const p0 = worldToScreen(pts[k].x, pts[k].y);
    const p1 = worldToScreen(pts[k + 1].x, pts[k + 1].y);
    drawCapsule(ctx, p0.sx, p0.sy, p1.sx, p1.sy, widths[k] || 5, "#c5ccd1", "#8a9399");
  }
  if (pts[0]) {
    const base = worldToScreen(pts[0].x, pts[0].y);
    ctx.fillStyle = "#4a5560";
    ctx.beginPath();
    ctx.ellipse(base.sx, base.sy, 18, 14, 0, 0, Math.PI * 2);
    ctx.fill();
  }
  const tip = worldToScreen(state.tips[fi * 3], state.tips[fi * 3 + 1]);
  ctx.fillStyle = state.pen[fi] ? "#111" : "#ff6b4a";
  ctx.beginPath();
  ctx.arc(tip.sx, tip.sy, 5, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "rgba(12,20,34,0.78)";
  ctx.fillRect(w - 260, 18, 240, 64);
  ctx.strokeStyle = "rgba(255,255,255,0.14)";
  ctx.strokeRect(w - 260.5, 18.5, 239, 63);
  ctx.fillStyle = "#7ef0b2";
  ctx.font = "11px sans-serif";
  ctx.fillText("Canvas 2D fallback（无 WebGL）", w - 248, 38);
  ctx.fillStyle = "#9fb0c8";
  ctx.fillText("网格版需 WebGL；本机仅示意臂+墨迹", w - 248, 56);
  ctx.fillText("有 WebGL 的机器会自动播 STL", w - 248, 72);
}

function updateTimeUI() {
  $("time").textContent = `${state.time.toFixed(2)} / ${state.duration.toFixed(2)} s`;
  $("seek").value = String(Math.round((state.duration > 0 ? state.time / state.duration : 0) * 1000));
}

async function loadEpisode() {
  overlayText.textContent = "WebGL 不可用，Canvas 2D 加载 tip 轨迹…";
  const meta = await fetch("./data/kai_ao.json").then((r) => r.json());
  const bin = await fetch(`./data/${meta.bin}`).then((r) => r.arrayBuffer());
  state.meta = meta;
  state.numFrames = meta.num_frames;
  state.numBodies = meta.num_bodies;
  state.fps = meta.fps;
  state.duration = (meta.num_frames - 1) / meta.fps;
  state.bodyOrder = meta.body_order;
  const off = meta.byte_offsets;
  state.poses = new Float32Array(bin, off.poses, meta.poses.count);
  state.tips = new Float32Array(bin, off.tips, meta.tips.count);
  state.pen = new Uint8Array(bin, off.pen_down, meta.pen_down.count);

  $("taskName").textContent = (meta.title || "SO-101") + " · 2D";
  $("ckpt").textContent = `Canvas2D fallback · ${meta.num_frames} frames @ ${meta.fps} fps`;
  $("ep").textContent = meta.episode_name;
  $("hudCam").textContent = "俯视（2D）";
  document.querySelectorAll("button.cam").forEach((b) => {
    b.disabled = true;
    b.style.opacity = "0.35";
  });
  overlay.classList.add("hidden");
}

$("play").onclick = () => {
  state.playing = !state.playing;
  $("play").textContent = state.playing ? "⏸" : "▶";
};
$("loop").onchange = (e) => {
  state.loop = !!e.target.checked;
};
document.querySelectorAll("button.rate").forEach((btn) => {
  btn.onclick = () => {
    document.querySelectorAll("button.rate").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.rate = Number(btn.dataset.rate);
  };
});
$("seek").oninput = () => {
  state.playing = false;
  $("play").textContent = "▶";
  state.time = (Number($("seek").value) / 1000) * state.duration;
};
window.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    $("play").click();
  }
});

let last = performance.now();
function tick(now) {
  const dt = Math.min((now - last) / 1000, 0.1);
  last = now;
  if (state.numFrames) {
    if (state.playing) {
      state.time += dt * state.rate;
      if (state.time >= state.duration) {
        if (state.loop) state.time = 0;
        else {
          state.time = state.duration;
          state.playing = false;
          $("play").textContent = "▶";
        }
      }
    }
    const fi = clamp(Math.floor(state.time * state.fps), 0, state.numFrames - 1);
    drawFrame(fi);
    const phase = state.meta.phases?.[fi] || "—";
    $("hudTime").textContent = `${state.time.toFixed(2)} s`;
    $("hudPhase").textContent = `${phase}${state.pen[fi] ? " · 着墨" : ""}`;
    $("hudFrame").textContent = `${fi + 1} / ${state.numFrames}`;
    updateTimeUI();
  }
  requestAnimationFrame(tick);
}

loadEpisode()
  .then(() => requestAnimationFrame(tick))
  .catch((e) => {
    overlayText.innerHTML = `<span class="err">${e.message || e}</span>`;
  });
