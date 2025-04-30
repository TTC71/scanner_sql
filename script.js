
function validerCodeManuel() {
  const input = document.getElementById("code-manuel");
  const code = input.value.trim().toUpperCase();
  if (code === "") {
    alert("Veuillez entrer un code-barres.");
    return;
  }

  document.getElementById("code-lu").textContent = code;

  fetch("/produit?code=" + code)
    .then(response => response.json())
    .then(data => {
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
  input.value = "";
}
