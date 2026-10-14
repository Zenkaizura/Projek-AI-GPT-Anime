const avatar = document.querySelector("#avatar-card");
const avatarHome = document.querySelector("#avatar-home");
const character = document.querySelector(".character");
const speech = document.querySelector("#speech");
const status = document.querySelector("#status");
const toggleButton = document.querySelector("#toggle-button");
const floatButton = document.querySelector("#float-button");
const chatForm = document.querySelector("#chat-form");
const chatInput = document.querySelector("#chat-input");
const chatLog = document.querySelector("#chat-log");
const chatHeading = document.querySelector("#chat-heading");
const chatDisclaimer = document.querySelector("#chat-disclaimer");
const chatSubmit = chatForm.querySelector('button[type="submit"]');
const aiApiUrl = (window.NEKO_API_URL || "").trim().replace(/\/$/, "");

if (aiApiUrl) {
  chatHeading.textContent = "Chat dengan AI";
  chatDisclaimer.textContent = "Balasan diproses melalui backend AI. Hindari mengirim data pribadi.";
  document.querySelector("#connection-note strong").textContent = "Backend AI dikonfigurasi.";
  document.querySelector("#connection-note span").textContent = "Jika balasan gagal, periksa layanan backend dan kuota API.";
}

const greetings = [
  "Halo! Senang bertemu denganmu.",
  "Aku siap menemanimu belajar hari ini!",
  "Istirahat sebentar juga boleh, ya.",
];

let greetingIndex = 0;
let pipWindow = null;

function setStatus(message) {
  status.textContent = message;
}

function speak(message) {
  speech.textContent = message;
  character.classList.remove("talking");
  void character.getBoundingClientRect();
  character.classList.add("talking");
}

function addChatMessage(sender, message, kind) {
  const item = document.createElement("p");
  item.className = `chat-message ${kind}`;
  const label = document.createElement("span");
  label.textContent = sender;
  item.append(label, document.createTextNode(message));
  chatLog.appendChild(item);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function demoReply(message) {
  const lower = message.toLocaleLowerCase("id-ID");
  if (/\b(halo|hai|hi|hello)\b/u.test(lower)) {
    return "Halo juga! Aku masih dalam mode demo, tapi senang bisa menyapamu.";
  }
  if (/\b(belajar|tugas|sekolah|kuliah)\b/u.test(lower)) {
    return "Semangat belajarnya! Nanti, setelah AI terhubung, aku bisa membantu membahas tugasmu.";
  }
  return "Pesanmu sudah masuk. Saat ini aku hanya punya balasan demo; percakapan AI akan ditambahkan nanti.";
}

function showAvatar() {
  avatar.hidden = false;
  toggleButton.textContent = "Sembunyikan avatar";
  setStatus(pipWindow ? "Avatar tampil di jendela kecil." : "Avatar sedang tampil di halaman.");
}

function hideAvatar() {
  avatar.hidden = true;
  toggleButton.textContent = "Tampilkan avatar";
  if (pipWindow) pipWindow.close();
  setStatus("Avatar disembunyikan. Klik Tampilkan avatar untuk membukanya lagi.");
}

function restoreFromPip() {
  if (avatar.parentElement !== avatarHome) avatarHome.appendChild(avatar);
  pipWindow = null;
  floatButton.textContent = "Buka jendela kecil";
  if (!avatar.hidden) setStatus("Avatar kembali tampil di halaman.");
}

toggleButton.addEventListener("click", () => {
  if (avatar.hidden) showAvatar();
  else hideAvatar();
});

document.querySelector("#hide-card-button").addEventListener("click", hideAvatar);

document.querySelector("#greet-button").addEventListener("click", () => {
  greetingIndex = (greetingIndex + 1) % greetings.length;
  speak(greetings[greetingIndex]);
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;
  addChatMessage("Kamu", message, "user");
  chatInput.value = "";
  chatSubmit.disabled = true;
  try {
    let reply;
    if (aiApiUrl) {
      const response = await fetch(`${aiApiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      if (typeof data.reply !== "string" || !data.reply.trim()) throw new Error("Jawaban kosong");
      reply = data.reply.trim();
    } else {
      reply = demoReply(message);
    }
    addChatMessage(aiApiUrl ? "Neko · AI" : "Neko · demo", reply, "bot");
    speak(reply);
  } catch (error) {
    console.error("Chat AI gagal:", error);
    addChatMessage("Neko", "Layanan AI belum tersedia. Coba lagi nanti.", "bot");
  } finally {
    chatSubmit.disabled = false;
    chatInput.focus();
  }
});

floatButton.addEventListener("click", async () => {
  if (pipWindow) {
    pipWindow.close();
    return;
  }
  if (!("documentPictureInPicture" in window)) {
    setStatus("Browser ini belum mendukung jendela kecil. Avatar tetap bisa dipakai di halaman.");
    return;
  }

  try {
    const openedWindow = await window.documentPictureInPicture.requestWindow({ width: 340, height: 440 });
    pipWindow = openedWindow;
    const pipDocument = openedWindow.document;
    pipDocument.documentElement.lang = "id";
    pipDocument.title = "Avatar Neko";
    pipDocument.body.classList.add("pip");

    const stylesheet = pipDocument.createElement("link");
    stylesheet.rel = "stylesheet";
    stylesheet.href = new URL("./styles.css", document.baseURI).href;
    pipDocument.head.appendChild(stylesheet);
    pipDocument.body.appendChild(avatar);
    openedWindow.addEventListener("pagehide", restoreFromPip, { once: true });

    showAvatar();
    floatButton.textContent = "Kembalikan ke halaman";
  } catch (error) {
    console.error("Jendela kecil tidak dapat dibuka:", error);
    setStatus("Jendela kecil tidak dapat dibuka. Avatar tetap bisa dipakai di halaman.");
  }
});
