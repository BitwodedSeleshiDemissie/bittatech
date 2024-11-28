$(document).ready(function () {
    $('#contactForm').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission behavior

        // Collect form data
        const formData = $(this).serialize(); // Serializes the form fields into key-value pairs

        $.ajax({
            url: 'php/form-handler.php', // Path to your PHP script
            type: 'POST',
            data: formData,
            success: function (response) {
                // Show success message
                $('#formFeedback').html('<div class="alert alert-success">' + response + '</div>');
                $('#contactForm')[0].reset(); // Clear the form after successful submission
            },
            error: function () {
                // Show error message
                $('#formFeedback').html('<div class="alert alert-danger">An error occurred. Please try again.</div>');
            }
        });
    });
});
