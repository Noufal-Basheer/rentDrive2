 // Update slider value based on text box input
 document.getElementById("stt").addEventListener("input", function() {
    document.getElementById("stl").value = this.value;
});

// Update text box value based on slider input
document.getElementById("stl").addEventListener("input", function() {
    document.getElementById("stt").value = this.value;
});

document.querySelectorAll('input[type="radio"]').forEach(function(radio) {
    radio.addEventListener('change', function() {
        var inputField1 = document.getElementById('validity_date');
        var inputField2 = document.getElementById('duration');

        if (this.value === 'field1') {
            inputField1.disabled = false;
            inputField2.disabled = true;
        } else if (this.value === 'field2') {
            inputField1.disabled = true;
            inputField2.disabled = false;
        }
    });
});