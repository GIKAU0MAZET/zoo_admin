async function loadFeed() {

    const supplierId =
        document.getElementById("supplierSelect").value;

    const response =
        await fetch(`/api/feed/${supplierId}`);

    const feed =
        await response.json();

    const foodSelect =
        document.getElementById("foodSelect");

    foodSelect.innerHTML = "";

    feed.forEach(item => {

        const option =
            document.createElement("option");

        option.value = item.id;

        option.textContent = item.name;

        foodSelect.appendChild(option);

    });

}

document
    .getElementById("supplierSelect")
    .addEventListener("change", loadFeed);

loadFeed();