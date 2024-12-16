(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

    // Initiate the wowjs
    new WOW().init();

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });

    // Back to top button
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

    // Skills
    $('.skill').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});

    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });

    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        dots: false,
        loop: true,
        nav : true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0:{
                items:1
            },
            992:{
                items:2
            }
        }
    });

    // Portfolio isotope and filter
    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');
        portfolioIsotope.isotope({filter: $(this).data('filter')});
    });

    // Function to translate text using LibreTranslate API
    function translateTextLibre(text, targetLanguage) {
        const url = 'https://libretranslate.de/translate';  // Public instance URL of LibreTranslate
        const data = {
            q: text,
            source: 'en',  // Default source language (English)
            target: targetLanguage  // Dynamic target language
        };

        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            return data.translatedText;
        })
        .catch(error => console.error('Error with LibreTranslate API:', error));
    }

    // Function to load and translate page content dynamically
    function loadTranslation(language) {
        // Select all text nodes that are not inside any element with specific classes
        $('body').find('*').contents().each(function() {
            if (this.nodeType === 3 && this.textContent.trim() !== '') {  // Check for text nodes
                const originalText = this.textContent.trim();
                translateTextLibre(originalText, language).then(translatedText => {
                    this.textContent = translatedText;  // Replace the text content with the translation
                });
            }
        });
    }

    // Event listeners for language change (for flags)
    // For the English flag
    document.querySelector('[href*="language=en"]').addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default behavior
        loadTranslation('en');   // Load English translations
    });

    // For the Italian flag
    document.querySelector('[href*="language=it"]').addEventListener('click', function (event) {
        event.preventDefault();  // Prevent the default behavior
        loadTranslation('it');   // Load Italian translations
    });

    // Example: Initial translation for English (optional)
    loadTranslation('en');
})(jQuery);
