const API_DETECT_URL = "http://localhost:8000/detect";
const API_ASK_URL = "http://localhost:8000/ask";

// const API_DETECT_URL = "https://r7sc5m17-8000.asse.devtunnels.ms/detect";
// const API_ASK_URL = "https://r7sc5m17-8000.asse.devtunnels.ms/ask";


let selectedFile = null;

function parseMarkdown(text) {
  if (!text) return "";
  let html = text;
  html = html.replace(/(?:^\|.*\|(?:\n|\r|$))+/gm, function(match) {
      let rows = match.trim().split('\n');
      let tableHtml = '<div class="overflow-x-auto my-5 rounded-xl ring-1 ring-slate-200 shadow-sm"><table class="w-full text-sm text-left text-slate-600">';
      
      rows.forEach((row, index) => {
          if (row.match(/^\|[\s\-\:]+\|/)) return;

          let cleanRow = row.replace(/^\||\|$/g, '');
          let cols = cleanRow.split('|').map(c => c.trim());

          tableHtml += '<tr class="border-b border-slate-200 last:border-0 hover:bg-slate-50 transition-colors">';
          cols.forEach(col => {
              if (index === 0) {
                  // Baris pertama jadi Header (TH)
                  tableHtml += `<th class="px-4 py-3 bg-slate-100 font-semibold text-slate-700 whitespace-nowrap">${col}</th>`;
              } else {
                  // Baris selanjutnya jadi Data (TD)
                  tableHtml += `<td class="px-4 py-3 align-top">${col}</td>`;
              }
          });
          tableHtml += '</tr>';
      });
      tableHtml += '</table></div>';
      return tableHtml;
  });

  // 2. Heading 3 (### Teks)
  html = html.replace(/^###\s+(.*$)/gim, '<h3 class="text-lg font-bold text-slate-800 mt-5 mb-2">$1</h3>');
  
  // 3. Heading 2 (## Teks)
  html = html.replace(/^##\s+(.*$)/gim, '<h2 class="text-xl font-bold text-slate-800 mt-5 mb-2">$1</h2>');

  // 4. Bold (**Teks**)
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-slate-800">$1</strong>');
  
  // 5. Bullet points (* Teks atau - Teks di awal baris)
  html = html.replace(/^[\*\-]\s+(.*$)/gim, '<div class="flex gap-2 mt-1.5"><span class="text-rose-500 font-bold shrink-0">•</span><span>$1</span></div>');

  // 6. Italic (*Teks*)
  html = html.replace(/(?<!^)\*(.*?)\*/g, '<em class="italic text-slate-700">$1</em>');

  // 7. Ubah Enter (\n) menjadi <br>
  html = html.replace(/\n/g, '<br/>');
  
  // 8. Bersihkan sisa <br> berlebih agar spasi tidak terlalu jauh
  html = html.replace(/<\/h3><br\/>/g, '</h3>');
  html = html.replace(/<\/h2><br\/>/g, '</h2>');
  html = html.replace(/<\/div><br\/>/g, '</div>');
  html = html.replace(/<\/div><br\/><br\/>/g, '</div>'); // Jaga jarak bawah tabel
  html = html.replace(/(<br\/>){3,}/g, '<br/><br/>');

  return html;
}

// --- 1. UPDATE FUNGSI NAVIGASI ---
function switchMenu(menu) {
  const secDetect = document.getElementById("section-detect");
  const secChat = document.getElementById("section-chat");
  const btnDetect = document.getElementById("btn-menu-detect");
  const btnChat = document.getElementById("btn-menu-chat");

  const activeClass =
    "flex-1 md:w-full flex items-center justify-center md:justify-start gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl font-medium transition-all bg-rose-50 text-rose-600 text-sm md:text-base whitespace-nowrap shadow-sm md:shadow-none";
  const inactiveClass =
    "flex-1 md:w-full flex items-center justify-center md:justify-start gap-2 md:gap-3 px-4 py-2.5 md:py-3 rounded-xl font-medium transition-all text-slate-500 hover:bg-slate-50 hover:text-slate-700 text-sm md:text-base whitespace-nowrap";

  if (menu === "detect") {
    secDetect.classList.remove("hidden");
    secChat.classList.add("hidden");
    secChat.classList.remove("flex");
    btnDetect.className = activeClass;
    btnChat.className = inactiveClass;
  } else {
    secDetect.classList.add("hidden");
    secChat.classList.remove("hidden");
    secChat.classList.add("flex");
    btnChat.className = activeClass;
    btnDetect.className = inactiveClass;
  }
}

// --- FUNGSI DETEKSI PENYAKIT ---
function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    selectedFile = file;
    const fileNameEl = document.getElementById("file-name");
    fileNameEl.textContent = `File: ${file.name}`;
    fileNameEl.classList.remove("hidden");
    document.getElementById("btn-upload").classList.remove("hidden");

    const previewContainer = document.getElementById("preview-container");
    const imagePreview = document.getElementById("image-preview");
    imagePreview.src = URL.createObjectURL(file);
    previewContainer.classList.remove("hidden");

    document.getElementById("detect-result").classList.add("hidden");
    document.getElementById("detect-error").classList.add("hidden");
  }
}

async function handleUpload() {
  if (!selectedFile) return;

  const btnUpload = document.getElementById("btn-upload");
  const errorContainer = document.getElementById("detect-error");
  const resultContainer = document.getElementById("detect-result");

  btnUpload.disabled = true;
  btnUpload.textContent = "Memproses...";
  errorContainer.classList.add("hidden");
  resultContainer.classList.add("hidden");

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(API_DETECT_URL, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error(`Error server: ${response.status}`);

    const data = await response.json();
    tampilkanHasilDeteksi(data);
  } catch (err) {
    errorContainer.textContent = "Gagal terhubung ke server.";
    errorContainer.classList.remove("hidden");
  } finally {
    btnUpload.disabled = false;
    btnUpload.textContent = "Mulai Analisis AI";
  }
}

// --- 2. UPDATE KOTAK HASIL DETEKSI ---
function tampilkanHasilDeteksi(data) {
  const resultContainer = document.getElementById("detect-result");
  const resultImage = document.getElementById("result-image");
  const resultDetails = document.getElementById("result-details");

  if (data.image_base64) {
    resultImage.src = `data:image/jpeg;base64,${data.image_base64}`;
  }

  resultDetails.innerHTML = "";
  if (data.total_detections > 0) {
    data.results.forEach((item) => {
      const confidencePercent = (item.confidence * 100).toFixed(0);

      // MENGGUNAKAN FUNGSI PARSE MARKDOWN
      const formattedNarrative = parseMarkdown(item.narrative);

      const div = document.createElement("div");
      div.className =
        "bg-white ring-1 ring-slate-200 shadow-sm rounded-2xl p-4 md:p-6 relative overflow-hidden";

      div.innerHTML = `
                <div class="absolute top-0 left-0 w-1 md:w-1.5 h-full bg-rose-500"></div>
                <h4 class="text-base md:text-lg font-bold text-slate-800 mb-2 flex flex-col md:flex-row md:items-center justify-between gap-1">
                    <span>${item.class}</span>
                    <span class="text-xs font-semibold bg-slate-100 text-slate-500 px-2 py-1 rounded-md w-fit">Keyakinan: ${confidencePercent}%</span>
                </h4>
                <div class="text-slate-600 text-xs md:text-sm leading-relaxed mt-2 md:mt-3">
                    ${formattedNarrative}
                </div>
            `;
      resultDetails.appendChild(div);
    });
  } else {
    resultDetails.innerHTML = `
            <div class="bg-emerald-50 text-emerald-700 p-4 rounded-2xl ring-1 ring-emerald-200 font-medium flex items-center gap-3 text-sm md:text-base">
                <span class="text-xl">✅</span> Tidak ada penyakit terdeteksi. Daun tampak sehat!
            </div>
        `;
  }

  resultContainer.classList.remove("hidden");
}

// --- FUNGSI CHATBOT ---
async function handleSendChat(event) {
  event.preventDefault();

  const inputEl = document.getElementById("chat-input");
  const btnSend = document.getElementById("btn-chat-send");
  const question = inputEl.value.trim();
  if (!question) return;

  document.getElementById("chat-empty").classList.add("hidden");

  appendMessage("user", question);
  inputEl.value = "";

  inputEl.disabled = true;
  btnSend.disabled = true;

  const loadingId = showChatLoading();

  try {
    const response = await fetch(API_ASK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question }),
    });

    if (!response.ok) throw new Error("Gagal");

    const data = await response.json();
    removeChatLoading(loadingId);
    appendMessage("assistant", data.answer);
  } catch (err) {
    removeChatLoading(loadingId);
    appendMessage("assistant", "❌ Gagal terhubung ke server.");
  } finally {
    inputEl.disabled = false;
    btnSend.disabled = false;
    inputEl.focus();
  }
}

// --- 3. UPDATE CHAT BUBBLE ---
function appendMessage(role, content) {
  const chatBox = document.getElementById("chat-messages");
  const wrapper = document.createElement("div");
  wrapper.className = `flex ${role === "user" ? "justify-end" : "justify-start"}`;

  const bubble = document.createElement("div");
  if (role === "user") {
    bubble.className =
      "max-w-[90%] md:max-w-[80%] p-3 md:p-4 rounded-2xl rounded-tr-sm bg-rose-500 text-white shadow-md shadow-rose-200 leading-relaxed text-sm md:text-[15px]";
    bubble.textContent = content; // User input tetap menggunakan text content murni demi keamanan
  } else {
    bubble.className =
      "max-w-[90%] md:max-w-[80%] p-3 md:p-4 rounded-2xl rounded-tl-sm bg-white ring-1 ring-slate-200 text-slate-700 shadow-sm leading-relaxed text-sm md:text-[15px]";

    bubble.innerHTML = parseMarkdown(content);
  }

  wrapper.appendChild(bubble);
  chatBox.appendChild(wrapper);
  scrollToBottom(chatBox);
}

function showChatLoading() {
  const chatBox = document.getElementById("chat-messages");
  const wrapper = document.createElement("div");
  const id = "loading-" + Date.now();
  wrapper.id = id;
  wrapper.className = `flex justify-start`;
  wrapper.innerHTML = `
        <div class="bg-white ring-1 ring-slate-200 text-slate-500 p-4 md:p-5 rounded-2xl rounded-tl-sm shadow-sm flex items-center">
            <div class="dot-flashing ml-2"></div>
        </div>
    `;
  chatBox.appendChild(wrapper);
  scrollToBottom(chatBox);
  return id;
}

function removeChatLoading(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function scrollToBottom(element) {
  element.scrollTo({
    top: element.scrollHeight,
    behavior: "smooth",
  });
}
