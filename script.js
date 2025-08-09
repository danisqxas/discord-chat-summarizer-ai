async function summarize() {
  const text = document.getElementById('chatInput').value;
  const res = await fetch('/api/index', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text})
  });
  const data = await res.json();
  document.getElementById('summaryOutput').textContent = data.summary || data.error || 'No summary returned';
}

document.getElementById('summarizeBtn').addEventListener('click', summarize);
