// Gallery Filter + Search

const filterButtons = document.querySelectorAll(".filter-btn");
const galleryCards = document.querySelectorAll(".gallery-card");
const searchInput = document.querySelector("#searchInput");

let currentFilter = "all";

// Filter Function
function filterGallery() {

    const searchValue = searchInput.value.toLowerCase();

    galleryCards.forEach(card => {

        const monumentName = card.querySelector("h3").textContent.toLowerCase();
        const category = card.dataset.category;

        const matchSearch = monumentName.includes(searchValue);
        const matchCategory = currentFilter === "all" || category === currentFilter;

        if (matchSearch && matchCategory) {

            card.style.display = "block";

        } else {

            card.style.display = "none";

        }

    });

}

// Category Buttons
filterButtons.forEach(button => {

    button.addEventListener("click", () => {

        filterButtons.forEach(btn => btn.classList.remove("active"));

        button.classList.add("active");

        currentFilter = button.dataset.filter;

        filterGallery();

    });

});

// Live Search
searchInput.addEventListener("keyup", filterGallery);