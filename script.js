let dataMap = {};

function afficherProductInfo(code) {
  fetch("/produit?code=" + code)
    .then((r) => r.json())
    .then((res) => {
      if (res.error) {
        document.getElementById("produit").textContent = "Non trouvé";
        document.getElementById("quantite").textContent = "-";
        document.getElementById("prix").textContent = "-";
      } else {
        document.getElementById("produit").textContent = res.produit;
        document.getElementById("quantite").textContent = res.quantite;
        document.getElementById("prix").textContent = res.prix + " €";
      }
    });
}

function validerCodeManuel() {
  const input = document.getElementById("code-manuel");
  const code = input.value.trim().replace(/'/g, "").toUpperCase();
  document.getElementById("code-lu").textContent = code;
  afficherProductInfo(code);
  input.value = "";
}

function demarrerScanner() {
  const readerElement = document.getElementById("reader");
  const qrBoxSize = {
    width: 300,
    height: 100,
  };

  new Html5Qrcode("reader").start(
    { facingMode: "environment" },
    { fps: 10, qrbox: qrBoxSize },
    (code) => {
      const cleanCode = code.trim().replace(/'/g, "").toUpperCase();
      document.getElementById("code-lu").textContent = cleanCode;
      afficherProductInfo(cleanCode);
    },
    (error) => {}
  );
}

demarrerScanner();