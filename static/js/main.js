(function ($) {
    "use strict";

    // Spinner - Hide it after page load
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

    // Initiate the wowjs (animation on scroll)
    new WOW().init();

    // Sticky Navbar - Add class on scroll
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });

    // Back to top button functionality
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Skills Progress Bars - Animate on scroll
    $('.skill').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});

    // Counter-Up for number increment
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });

    // Testimonials carousel using OwlCarousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0: { items: 1 },
            992: { items: 2 }
        }
    });

    // Portfolio isotope and filter (filter items)
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');
        portfolioIsotope.isotope({ filter: $(this).data('filter') });
    });

   // Function to translate text using Azure Cognitive Translation API
function translateTextAzure(text, targetLanguage) {
    const url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0';
    const region = 'italynorth';  // Your region: 'italynorth'
    const subscriptionKey = '4Q40w3KM8TuqK8LJ0ataejTWkZnJWu6sBeGTTAIhqbggvLusmqB5JQQJ99ALACgEuAYXJ3w3AAAbACOGkm8d';  // Use Key 1

    const headers = {
        'Ocp-Apim-Subscription-Key': subscriptionKey,
        'Content-Type': 'application/json',
    };

    const body = [{
        Text: text,
    }];

    const params = new URLSearchParams({
        'to': targetLanguage,  // Target language code (e.g., 'it' for Italian)
    });

    return fetch(`${url}&${params.toString()}`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body),
    })
    .then(response => response.json())
    .then(data => {
        if (data[0] && data[0].translations[0]) {
            return data[0].translations[0].text;  // Get translated text
        } else {
            console.error('Translation error:', data);
            return text;  // Fallback to original text
        }
    })
    .catch(error => {
        console.error('Error with Azure Translation API:', error);
        return text;  // Fallback to original text
    });
}

// Function to load and translate page content dynamically
function loadTranslation(language) {
    // Loop through each text node in the body
    $('body').find('*').contents().each(function () {
        if (this.nodeType === 3 && this.textContent.trim() !== '') {  // Check for text nodes
            const originalText = this.textContent.trim();
            translateTextAzure(originalText, language).then(translatedText => {
                this.textContent = translatedText;  // Update text content with translation
            });
        }
    });

    // Translate 'alt' and 'title' attributes for images and links
    $('body').find('[alt], [title]').each(function () {
        const element = $(this);
        const attributeName = element.is('[alt]') ? 'alt' : 'title';
        const originalText = element.attr(attributeName);
        if (originalText && originalText.trim() !== '') {
            translateTextAzure(originalText, language).then(translatedText => {
                element.attr(attributeName, translatedText);  // Update the attribute with translated text
            });
        }
    });
}

// Event listener for language switcher - triggered when a flag is clicked
$('.language-switcher').on('click', function (event) {
    event.preventDefault();  // Prevent default navigation
    const language = $(this).data('language');  // Get the selected language (from data attribute)
    console.log(`Language selected: ${language}`);  // Debugging log for selected language
    loadTranslation(language);  // Load translations for the selected language
});

    // Initialize with default language (e.g., English) on page load
    loadTranslation('en');

})(jQuery);
