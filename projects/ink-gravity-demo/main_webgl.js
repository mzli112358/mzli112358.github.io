// SO-101 书法网格回放 —— 数据格式对齐启元 Q1 webdemo（.json + .bin mesh/poses）

import * as THREE from "three";
import { OrbitControls } from "./vendor/OrbitControls.js";

const $ = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

const CAM_LABEL = {
  free: "自由视角",
  third: "第三人称",
  top: "俯视纸面",
  side: "侧面",
};

const state = {
  meta: null,
  bin: null,
  poses: null,
  tips: null,
  pen: null,
  numFrames: 0,
  numBodies: 0,
  fps: 30,
  duration: 0,
  time: 0,
  playing: true,
  rate: 1,
  loop: true,
  camMode: "free",
  bodyGroups: [],
  bodyIndex: {},
  inkLine: null,
};

const canvas = $("c");
const overlay = $("overlay");
const overlayText = $("overlayText");

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
scene.background = new THREE.Color("#9eb6c9");
scene.fog = new THREE.Fog("#9eb6c9", 2.5, 6.5);

const camera = new THREE.PerspectiveCamera(
  48,
  window.innerWidth / window.innerHeight,
  0.01,
  40
);
camera.position.set(0.55, 0.42, 0.55);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0.25, 0.06, 0.0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 0.12;
controls.maxDistance = 4.0;
controls.update();

scene.add(new THREE.HemisphereLight(0xfff2dc, 0x3a3228, 1.05));
const sun = new THREE.DirectionalLight(0xfff4e2, 1.85);
sun.position.set(0.7, 1.3, 0.5);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
scene.add(sun);

// MuJoCo z-up → three y-up
const root = new THREE.Group();
root.rotation.x = -Math.PI / 2;
scene.add(root);

function mjToThree(x, y, z) {
  return new THREE.Vector3(x, z, -y);
}
function setQuatWxyz(target, w, x, y, z) {
  return target.set(x, y, z, w);
}

const _q0 = new THREE.Quaternion();
const _q1 = new THREE.Quaternion();

function addGround() {
  // 地板 = 桌腿底面高度（MJCF floor / 腿底 z=-0.75），不是桌面、不是 z=0
  // 中性深灰（对齐仿真 groundplane），不要草地绿
  const geo = new THREE.PlaneGeometry(2.4, 2.4);
  const mat = new THREE.MeshStandardMaterial({
    color: 0x2c3036,
    roughness: 0.94,
    metalness: 0.03,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(0.25, 0, -0.75);
  mesh.receiveShadow = true;
  root.add(mesh);
}

function buildRobot(meta) {
  while (root.children.length) root.remove(root.children[0]);
  addGround();

  const bodyEntries = meta.bodies;
  const bodyOrder = meta.body_order;
  state.bodyIndex = {};
  bodyOrder.forEach((name, i) => (state.bodyIndex[name] = i));

  const off = meta.byte_offsets;
  const buf = state.bin;

  state.bodyGroups = bodyOrder.map((name, bodyIdx) => {
    const group = new THREE.Group();
    group.name = name;
    const entries = bodyEntries[name] || [];
    for (const e of entries) {
      if (e.num_verts === 0 || e.num_faces === 0) continue;
      const posByte = off.vertices + e.vert_offset;
      const idxByte = off.indices + e.face_offset;
      const positions = new Float32Array(buf, posByte, e.num_verts * 3);
      const indices = new Uint32Array(buf, idxByte, e.num_faces * 3);
      const geo = new THREE.BufferGeometry();
      // copy — shared TypedArray views can be GC-sensitive across engines
      geo.setAttribute(
        "position",
        new THREE.BufferAttribute(new Float32Array(positions), 3)
      );
      geo.setIndex(new THREE.BufferAttribute(new Uint32Array(indices), 1));
      geo.computeVertexNormals();
      const rgba = e.rgba || [0.55, 0.55, 0.58, 1];
      const tint = 0.9 + 0.2 * ((bodyIdx * 37) % 5) / 4;
      let color = new THREE.Color(rgba[0] * tint, rgba[1] * tint, rgba[2] * tint);
      if (name === "paper_sheet") color = new THREE.Color(0xf4efe4);
      if (name === "brush") color = new THREE.Color(rgba[0], rgba[1], rgba[2]);
      if (name === "table") color = new THREE.Color(0x6b5a45);
      const mat = new THREE.MeshStandardMaterial({
        color,
        roughness: name === "paper_sheet" ? 0.92 : 0.55,
        metalness: name.startsWith("sts") || name.includes("motor") ? 0.25 : 0.08,
        side: THREE.DoubleSide,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.castShadow = name !== "paper_sheet";
      mesh.receiveShadow = true;
      group.add(mesh);
    }
    root.add(group);
    return group;
  });

  const inkGeom = new THREE.BufferGeometry();
  state.inkLine = new THREE.LineSegments(
    inkGeom,
    new THREE.LineBasicMaterial({ color: 0x0a0a0a, linewidth: 2 })
  );
  root.add(state.inkLine);
}

function rebuildInk(upto) {
  if (!state.inkLine || !state.tips) return;
  const pts = [];
  let prev = null;
  const inkLift = 0.0018; // 略抬离纸面，避免与纸 z-fight
  for (let i = 0; i <= upto; i++) {
    if (!state.pen[i]) {
      prev = null;
      continue;
    }
    const o = i * 3;
    const p = [state.tips[o], state.tips[o + 1], state.tips[o + 2] + inkLift];
    if (prev) pts.push(...prev, ...p);
    prev = p;
  }
  const arr = new Float32Array(pts);
  const geo = state.inkLine.geometry;
  geo.setAttribute("position", new THREE.BufferAttribute(arr, 3));
  geo.setDrawRange(0, pts.length / 3);
  geo.computeBoundingSphere();
}

function applyPose(frameFloat) {
  const n = state.numFrames;
  const i0 = clamp(Math.floor(frameFloat), 0, n - 1);
  const i1 = Math.min(i0 + 1, n - 1);
  const alpha = clamp(frameFloat - i0, 0, 1);
  const stride = state.numBodies * 7;
  const poses = state.poses;
  const base0 = i0 * stride;
  const base1 = i1 * stride;

  for (let b = 0; b < state.numBodies; b++) {
    const o0 = base0 + b * 7;
    const o1 = base1 + b * 7;
    const g = state.bodyGroups[b];
    if (!g) continue;
    const x = poses[o0] + (poses[o1] - poses[o0]) * alpha;
    const y = poses[o0 + 1] + (poses[o1 + 1] - poses[o0 + 1]) * alpha;
    const z = poses[o0 + 2] + (poses[o1 + 2] - poses[o0 + 2]) * alpha;
    g.position.set(x, y, z);
    setQuatWxyz(_q0, poses[o0 + 3], poses[o0 + 4], poses[o0 + 5], poses[o0 + 6]);
    setQuatWxyz(_q1, poses[o1 + 3], poses[o1 + 4], poses[o1 + 5], poses[o1 + 6]);
    g.quaternion.slerpQuaternions(_q0, _q1, alpha);
  }
  rebuildInk(i0);
  return i0;
}

function updateCamera() {
  if (state.camMode === "free" || !state.tips) {
    controls.enabled = true;
    return;
  }
  controls.enabled = false;
  const fi = clamp(Math.floor(state.time * state.fps), 0, state.numFrames - 1);
  const o = fi * 3;
  const tip3 = mjToThree(state.tips[o], state.tips[o + 1], state.tips[o + 2]);
  const pc = state.meta?.props?.paper_center || [0.25, 0, 0.001];
  const paper3 = mjToThree(pc[0], pc[1], pc[2] + 0.05);

  if (state.camMode === "top") {
    camera.position.set(paper3.x, 0.55, paper3.z);
    controls.target.copy(paper3);
  } else if (state.camMode === "side") {
    camera.position.set(paper3.x + 0.05, 0.25, paper3.z + 0.55);
    controls.target.copy(paper3);
  } else if (state.camMode === "third") {
    camera.position.set(tip3.x + 0.38, tip3.y + 0.3, tip3.z + 0.38);
    controls.target.copy(tip3);
  }
  camera.lookAt(controls.target);
}

function updateTimeUI() {
  $("time").textContent = `${state.time.toFixed(2)} / ${state.duration.toFixed(2)} s`;
  const pct = state.duration > 0 ? (state.time / state.duration) * 1000 : 0;
  $("seek").value = String(Math.round(pct));
}

async function loadEpisode(name) {
  overlayText.textContent = "正在加载网格 episode…";
  overlay.classList.remove("hidden");
  const meta = await fetch(`./data/${name}.json`).then((r) => {
    if (!r.ok) throw new Error(`meta HTTP ${r.status}`);
    return r.json();
  });
  const bin = await fetch(`./data/${meta.bin}`).then((r) => {
    if (!r.ok) throw new Error(`bin HTTP ${r.status}`);
    return r.arrayBuffer();
  });

  state.meta = meta;
  state.bin = bin;
  state.numFrames = meta.num_frames;
  state.numBodies = meta.num_bodies;
  state.fps = meta.fps;
  state.duration = (meta.num_frames - 1) / meta.fps;

  const off = meta.byte_offsets;
  state.poses = new Float32Array(bin, off.poses, meta.poses.count);
  state.tips = new Float32Array(bin, off.tips, meta.tips.count);
  state.pen = new Uint8Array(bin, off.pen_down, meta.pen_down.count);

  buildRobot(meta);

  $("taskName").textContent = meta.title || "SO-101 · 书法写字";
  $("ckpt").textContent = `${meta.task} · ${meta.num_frames} frames @ ${meta.fps} fps · STL mesh`;
  $("ep").textContent = meta.episode_name;
  $("hudCam").textContent = CAM_LABEL[state.camMode];
  $("play").textContent = "⏸";
  state.time = 0;
  state.playing = true;

  const pc = meta.props?.paper_center;
  if (pc) {
    controls.target.copy(mjToThree(pc[0], pc[1], 0.06));
    controls.update();
  }
  applyPose(0);
  updateTimeUI();
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
document.querySelectorAll("button.cam").forEach((btn) => {
  btn.onclick = () => {
    document.querySelectorAll("button.cam").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    state.camMode = btn.dataset.cam;
    $("hudCam").textContent = CAM_LABEL[state.camMode];
    if (state.camMode === "free") controls.enabled = true;
    updateCamera();
  };
});
$("seek").oninput = () => {
  state.playing = false;
  $("play").textContent = "▶";
  state.time = (Number($("seek").value) / 1000) * state.duration;
  const fi = applyPose(state.time * state.fps);
  const phase = state.meta?.phases?.[fi] || "—";
  $("hudTime").textContent = `${state.time.toFixed(2)} s`;
  $("hudPhase").textContent = `${phase}${state.pen[fi] ? " · 着墨" : ""}`;
  $("hudFrame").textContent = `${fi + 1} / ${state.numFrames}`;
  updateCamera();
};
window.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    $("play").click();
  }
});
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

const clock = new THREE.Clock();
let uiAccum = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  if (state.meta) {
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
    const fi = applyPose(state.time * state.fps);
    updateCamera();
    uiAccum += dt;
    if (uiAccum > 0.05) {
      uiAccum = 0;
      const phase = state.meta.phases?.[fi] || "—";
      $("hudTime").textContent = `${state.time.toFixed(2)} s`;
      $("hudPhase").textContent = `${phase}${state.pen[fi] ? " · 着墨" : ""}`;
      $("hudFrame").textContent = `${fi + 1} / ${state.numFrames}`;
      updateTimeUI();
    }
  }
  controls.update();
  renderer.render(scene, camera);
}

try {
  await loadEpisode("kai_ao");
  animate();
} catch (e) {
  console.error(e);
  overlayText.innerHTML = `<span class="err">网格加载失败：${e.message || e}</span>`;
  throw e;
}
