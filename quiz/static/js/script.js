document.addEventListener("DOMContentLoaded", function () {

    console.log("Python Quiz Pro JavaScript loaded successfully!");

    // Quiz option selection
    const options = document.querySelectorAll(
        '.option input[type="radio"]'
    );

    options.forEach(function (option) {

        option.addEventListener("change", function () {

            const labels = document.querySelectorAll(".option label");

            labels.forEach(function (label) {
                label.classList.remove("selected");
            });

            const selectedLabel = this.closest("label");

            if (selectedLabel) {
                selectedLabel.classList.add("selected");
            }

        });

    });

});