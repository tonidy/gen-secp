let pyodideReady = null;

const statusEl = document.querySelector("[data-status]");
const buttonEl = document.querySelector("[data-generate]");
const outputs = {
  private: document.querySelector("[data-output='private']"),
  compressed: document.querySelector("[data-output='compressed']"),
  uncompressed: document.querySelector("[data-output='uncompressed']"),
};
const copyButtons = document.querySelectorAll(".copy-btn");
const copyFeedbacks = document.querySelectorAll(".copy-feedback");
const COPY_FEEDBACK_DURATION = 500;
const COPY_FEEDBACK_FADE = 180;
const feedbackTimers = new WeakMap();
const feedbackHideTimers = new WeakMap();

function setStatus(message, state = "info") {
  statusEl.textContent = message;
  statusEl.dataset.state = state;
}

async function initPyodide() {
  if (pyodideReady) {
    return pyodideReady;
  }
  setStatus("Loading Python runtime…");
  pyodideReady = loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/",
  }).then(async (pyodide) => {
    const code = await fetch("python/app.py").then((r) => r.text());
    await pyodide.runPythonAsync(code);
    setStatus("Runtime ready");
    return pyodide;
  });
  return pyodideReady;
}

async function generateKeys() {
  buttonEl.disabled = true;
  buttonEl.textContent = "Generating…";
  try {
    const pyodide = await initPyodide();
    const jsonResult = await pyodide.runPythonAsync("generate_json()");
    const data = JSON.parse(jsonResult);
    outputs.private.textContent = data.private;
    outputs.compressed.textContent = data.compressed;
    outputs.uncompressed.textContent = data.uncompressed;
    copyButtons.forEach((btn) => {
      btn.hidden = false;
      btn.classList.remove("copied");
    });
    copyFeedbacks.forEach((box) => {
      const timer = feedbackTimers.get(box);
      if (timer) {
        clearTimeout(timer);
      }
      const hideTimer = feedbackHideTimers.get(box);
      if (hideTimer) {
        clearTimeout(hideTimer);
      }
      feedbackTimers.delete(box);
      feedbackHideTimers.delete(box);
      box.classList.remove("visible");
      box.hidden = true;
    });
    setStatus("New keypair generated", "success");
  } catch (err) {
    console.error(err);
    setStatus("Failed to generate keypair", "error");
  } finally {
    buttonEl.disabled = false;
    buttonEl.textContent = "Generate Keypair";
  }
}

buttonEl.addEventListener("click", generateKeys);

async function handleCopy(event) {
  const button = event.currentTarget;
  const key = button.dataset.copy;
  const valueEl = outputs[key];
  if (!valueEl) {
    return;
  }
  const text = valueEl.textContent.trim();
  if (!text || text === "—") {
    setStatus("Generate a keypair before copying", "error");
    return;
  }
  try {
    await navigator.clipboard.writeText(text);
    copyButtons.forEach((btn) => {
      btn.classList.remove("copied");
      btn.hidden = false;
    });
    button.classList.add("copied");
    const labelEl = valueEl.closest(".output")?.querySelector(".output-label");
    const label = labelEl ? labelEl.textContent.trim() : key;
    const feedbackEl = valueEl.closest(".output")?.querySelector(".copy-feedback");
    if (feedbackEl) {
      copyFeedbacks.forEach((box) => {
        if (box !== feedbackEl) {
          const timer = feedbackTimers.get(box);
          if (timer) {
            clearTimeout(timer);
          }
          const hideTimer = feedbackHideTimers.get(box);
          if (hideTimer) {
            clearTimeout(hideTimer);
          }
          feedbackTimers.delete(box);
          feedbackHideTimers.delete(box);
          box.classList.remove("visible");
          box.hidden = true;
        }
      });
      const existingTimer = feedbackTimers.get(feedbackEl);
      if (existingTimer) {
        clearTimeout(existingTimer);
      }
      const existingHide = feedbackHideTimers.get(feedbackEl);
      if (existingHide) {
        clearTimeout(existingHide);
      }
      feedbackTimers.delete(feedbackEl);
      feedbackHideTimers.delete(feedbackEl);
      feedbackEl.hidden = false;
      requestAnimationFrame(() => feedbackEl.classList.add("visible"));
      const timer = window.setTimeout(() => {
        feedbackEl.classList.remove("visible");
        const hideTimer = window.setTimeout(() => {
          feedbackEl.hidden = true;
          feedbackHideTimers.delete(feedbackEl);
        }, COPY_FEEDBACK_FADE);
        feedbackHideTimers.set(feedbackEl, hideTimer);
        feedbackTimers.delete(feedbackEl);
      }, COPY_FEEDBACK_DURATION);
      feedbackTimers.set(feedbackEl, timer);
    }
    setStatus(`${label} copied`, "success");
    window.setTimeout(() => button.classList.remove("copied"), COPY_FEEDBACK_DURATION);
  } catch (err) {
    console.error(err);
    setStatus("Copy failed. Copy manually instead.", "error");
  }
}

copyButtons.forEach((button) => {
  button.addEventListener("click", handleCopy);
});

(async () => {
  try {
    await initPyodide();
  } catch (err) {
    console.error(err);
    setStatus("Unable to initialise Python runtime", "error");
    buttonEl.disabled = true;
  }
})();
