const form = document.getElementById("studentForm");

const spinner = document.getElementById("spinner");

const buttonText = document.getElementById("buttonText");

const submitBtn = document.getElementById("submitBtn");

const message = document.getElementById("message");

const termsCheckbox = document.getElementById("terms");

/* -------------------------------- */
/* ENABLE BUTTON WHEN TERMS CHECKED */
/* -------------------------------- */

termsCheckbox.addEventListener("change", function () {

    submitBtn.disabled = !termsCheckbox.checked;
});

/* ---------------- */
/* FORM SUBMISSION  */
/* ---------------- */

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Clear old message
    message.innerText = "";

    // Get values
    const name = document.getElementById("name").value;

    const email = document.getElementById("email").value;

    const course = document.getElementById("course").value;

    // Validate checkbox
    if (!termsCheckbox.checked) {

        message.style.color = "red";

        message.innerText =
            "You must accept the Terms & Conditions.";

        return;
    }

    // Create object
    const studentData = {
        name,
        email,
        course
    };

    /* ---------------- */
    /* START LOADING    */
    /* ---------------- */

    spinner.classList.remove("hidden");

    buttonText.innerText = "Submitting...";

    submitBtn.disabled = true;

    try {

        // Send data to backend
        const response = await fetch(
            "http://127.0.0.1:5000/submit",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(studentData)
            }
        );

        const result = await response.json();

        // Success message
        message.style.color = "green";

        message.innerText = result.message;

        // Reset form
        form.reset();

        // Disable button again
        submitBtn.disabled = true;

    } catch (error) {

        console.error(error);

        message.style.color = "red";

        message.innerText =
            "Server error. Please try again.";
    }

    /* ---------------- */
    /* STOP LOADING     */
    /* ---------------- */

    spinner.classList.add("hidden");

    buttonText.innerText = "Register";
});