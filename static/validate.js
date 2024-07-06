function validateForm() {
    var age = document.getElementById('age').value;
    var sex = document.getElementById('sex').value;
    var cp = document.getElementById('cp').value;
    var trestbps = document.getElementById('trestbps').value;
    var chol = document.getElementById('chol').value;
    var fbs = document.getElementById('fbs').value;
    var restecg = document.getElementById('restecg').value;
    var thalach = document.getElementById('thalach').value;
    var exang = document.getElementById('exang').value;
    var oldpeak = document.getElementById('oldpeak').value;
    var slope = document.getElementById('slope').value;
    var ca = document.getElementById('ca').value;
    var thal = document.getElementById('thal').value;

    // Check if any field is empty
    if (!age || !sex || !cp || !trestbps || !chol || !fbs || !restecg || !thalach || !exang || !oldpeak || !slope || !ca || !thal) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Please fill out all fields!',
            footer: '<span class="error-message">Bracket options only</span>'
        });
        return false;
    }

    // Validate specific values if needed
    // Example: Check if values are within a specific range

    // Validation successful
    return true;
}
