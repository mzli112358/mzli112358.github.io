// SO-101 书法轨迹回放
// 优先 Three.js / WebGL；失败则自动跳 Canvas 2D（见控制台 llvmpipe / BindToCurrentSequence）

function canCreateWebGL() {
  try {
    const c = document.createElement("canvas");
    const gl =
      c.getContext("webgl2", { failIfMajorPerformanceCaveat: false }) ||
      c.getContext("webgl", { failIfMajorPerformanceCaveat: false }) ||
      c.getContext("experimental-webgl");
    return !!gl;
  } catch {
    return false;
  }
}

const overlayText = document.getElementById("overlayText");

if (!canCreateWebGL()) {
  overlayText.textContent =
    "检测到 WebGL 不可用（常见于 Intel + Mesa llvmpipe），切换 Canvas 2D…";
  await import("./main_canvas2d.js");
} else {
  try {
    await import("./main_webgl.js");
  } catch (e) {
    console.error(e);
    overlayText.innerHTML =
      `WebGL 初始化失败，切换 Canvas 2D…<br><span class="err">${e.message || e}</span>`;
    await import("./main_canvas2d.js");
  }
}
