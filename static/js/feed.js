async function loadFeed() {

    const supplierId =
        document.getElementById("supplierSelect").value;

    const response =
        await fetch(`/api/feed/${supplierId}`);

    const feed =
        await response.json();

    const foodSelect =
        document.getElementById("foodSelect");

    const selectedFoodId =
        foodSelect.dataset.selectedFoodId;

    foodSelect.innerHTML = "";

    feed.forEach(item => {

        const option =
            document.createElement("option");

        option.value = item.id;

        option.textContent = item.name;

        if (selectedFoodId === String(item.id)) {
            option.selected = true;
        }

        foodSelect.appendChild(option);

    });

    delete foodSelect.dataset.selectedFoodId;

}

document
    .getElementById("supplierSelect")
    .addEventListener("change", loadFeed);

loadFeed();
