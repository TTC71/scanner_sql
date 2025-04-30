let dataMap = {};

function afficherProductInfo(code) {
  fetch("/produit?code=" + code)
    .then(res => res.json())
    .then(data => {
      document.getElementById("code-lu").textContent = code;
      if (data.produit) {
        document.getElementById("produit").textContent = data.produit;
        document.getElementById("quantite").textContent = data.quantite;
        document.getElementById("prix").textContent = data.prix + " €";
      } else {
        document.getElementById("produit").textContent = "Non trouvé";
        document.getElementById("quantite").textContent = "-";
        document.getElementById("prix").textContent = "-";
      }
    });
}

function validerCodeManuel() {
  const input = document.getElementById("code-manuel");
  const code = input.value.trim().replace(/'/g, "").toUpperCase();
  if (code !== "") {
    afficherProductInfo(code);
    input.value = "";
  }
}

function importerCSV() {
  fetch("/importer")
    .then(res => res.json())
    .then(data => {
      document.getElementById("import-result").textContent = data.message || "Import terminé.";
    })
    .catch(() => {
      document.getElementById("import-result").textContent = "Erreur lors de l'import.";
    });
}

function demarrerScanner() {
  const readerElement = document.getElementById("reader");
  const readerWidth = readerElement.offsetWidth;
  const qrBoxSize = { width: Math.floor(readerWidth * 0.85), height: Math.floor(readerWidth * 0.3) };

  new Html5Qrcode("reader").start(
    { facingMode: "environment" },
    { fps: 10, qrbox: qrBoxSize },
    code => {
      const cleanCode = code.trim().replace(/'/g, "").toUpperCase();
      afficherProductInfo(cleanCode);
    },
    error => {}
  );
}

demarrerScanner();
