// Totaux pour chaque caisse
let totalGrandeCaisse = 0;
let totalPetiteCaisse = 0;

function showPopup(type) {
    const containerId = type === 'gc' ? 'popup-container-gc' : 'popup-container-pc';
    document.getElementById(containerId).classList.remove('popup-hidden');
}

function hidePopup(type) {
    const containerId = type === 'gc' ? 'popup-container-gc' : 'popup-container-pc';
    document.getElementById(containerId).classList.add('popup-hidden');
}

function submitForm(type) {
    const prefix = type === 'gc' ? 'gc' : 'pc';
    const typeCaisse = type === 'gc' ? 'Grande Caisse' : 'Petite Caisse';

    const operationType = document.getElementById(`type-${prefix}`).value;
    const date = document.getElementById(`date-${prefix}`).value;
    const motif = document.getElementById(`motif-${prefix}`).value;
    const somme = parseFloat(document.getElementById(`somme-${prefix}`).value);

    if (type === 'gc') {
        totalGrandeCaisse = operationType === "Entrée" ? totalGrandeCaisse + somme : totalGrandeCaisse - somme;
        alert(`Total de la Grande Caisse : ${totalGrandeCaisse.toFixed(2)}`);
    } else {
        totalPetiteCaisse = operationType === "Entrée" ? totalPetiteCaisse + somme : totalPetiteCaisse - somme;
        alert(`Total de la Petite Caisse : ${totalPetiteCaisse.toFixed(2)}`);
    }

    console.log({
        type_caisse: typeCaisse,
        type: operationType,
        date: date,
        motif: motif,
        somme: somme,
        total: type === 'gc' ? totalGrandeCaisse : totalPetiteCaisse,
    });

    hidePopup(type);
}
