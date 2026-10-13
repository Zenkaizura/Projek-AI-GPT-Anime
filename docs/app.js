const avatar = document.querySelector("#avatar-card");
const avatarHome = document.querySelector("#avatar-home");
const character = document.querySelector(".character");
const speech = document.querySelector("#speech");
const status = document.querySelector("#status");
const toggleButton = document.querySelector("#toggle-button");
const floatButton = document.querySelector("#float-button");

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
  speech.textContent = greetings[greetingIndex];
  character.classList.remove("talking");
  void character.getBoundingClientRect();
  character.classList.add("talking");
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
