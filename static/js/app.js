const featureSelect = document.getElementById('feature-select');
const promptInput = document.getElementById('prompt-input');
const submitBtn = document.getElementById('submit-btn');
const resultBox = document.getElementById('result-box');

function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatStructuredResponse(rawText) {
  const text = (rawText || '').trim();
  if (!text) {
    return '<p>No output generated.</p>';
  }

  const lines = text.split(/\n+/).map((line) => line.trim()).filter(Boolean);
  const blocks = [];
  let listType = null;
  let listItems = [];

  const flushList = () => {
    if (!listType || listItems.length === 0) return;
    blocks.push(`<${listType}>${listItems.map((item) => `<li>${item}</li>`).join('')}</${listType}>`);
    listType = null;
    listItems = [];
  };

  for (const line of lines) {
    if (/^#{1,3}\s+/.test(line)) {
      flushList();
      blocks.push(`<h3>${escapeHtml(line.replace(/^#{1,3}\s+/, ''))}</h3>`);
      continue;
    }

    if (/^[-*]\s+/.test(line)) {
      const item = line.replace(/^[-*]\s+/, '');
      if (listType !== 'ul') {
        flushList();
        listType = 'ul';
      }
      listItems.push(item.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'));
      continue;
    }

    if (/^\d+\.\s+/.test(line)) {
      const item = line.replace(/^\d+\.\s+/, '');
      if (listType !== 'ol') {
        flushList();
        listType = 'ol';
      }
      listItems.push(item.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'));
      continue;
    }

    if (/^[A-Z][A-Za-z0-9\s&()/-]+:$/.test(line)) {
      flushList();
      blocks.push(`<h4>${escapeHtml(line.replace(/:$/, ''))}</h4>`);
      continue;
    }

    flushList();
    const clean = escapeHtml(line).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    blocks.push(`<p>${clean}</p>`);
  }

  flushList();
  return blocks.join('');
}

function showError(message) {
  resultBox.innerHTML = `<div class="result-box"><h3>Something went wrong</h3><p>${escapeHtml(message)}</p></div>`;
}

async function callApi(endpoint, text) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Something went wrong.');
  }

  return data.result;
}

submitBtn.addEventListener('click', async () => {
  const selectedFeature = featureSelect.value;
  const text = promptInput.value.trim();

  if (!text) {
    showError('Please enter some content first.');
    return;
  }

  resultBox.innerHTML = '<p>Working on it...</p>';

  try {
    const endpoint = `/${selectedFeature}`;
    const result = await callApi(endpoint, text);
    resultBox.innerHTML = formatStructuredResponse(result);
  } catch (error) {
    showError(error.message || 'Unable to complete the request. Please try again later.');
  }
});
