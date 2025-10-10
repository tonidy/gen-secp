let pyodideReady = null;

const statusEl = document.querySelector("[data-status]");
const buttonEl = document.querySelector("[data-generate]");
const outputs = {
  private: document.querySelector("[data-output='private']"),
  compressed: document.querySelector("[data-output='compressed']"),
  uncompressed: document.querySelector("[data-output='uncompressed']"),
};

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

(async () => {
  try {
    await initPyodide();
  } catch (err) {
    console.error(err);
    setStatus("Unable to initialise Python runtime", "error");
    buttonEl.disabled = true;
  }
})();
