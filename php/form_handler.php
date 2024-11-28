<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Sanitize input data
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $subject = htmlspecialchars($_POST['subject']);
    $message = htmlspecialchars($_POST['message']);

    // Validate email
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo "Invalid email address.";
        exit;
    }

    // Save data to a file or handle it as needed (e.g., send email)
    $file = '../contacts.db';
    $entry = "Name: $name\nEmail: $email\nSubject: $subject\nMessage: $message\n\n";

    if (file_put_contents($file, $entry, FILE_APPEND)) {
        echo "Thank you for contacting us, $name!";
    } else {
        echo "Failed to save your message. Please try again.";
    }
} else {
    echo "Invalid request.";
}
?>
