(function ($) {
    "use strict";

    // Spinner functionality
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

    // Initiate the wowjs animation library
    new WOW().init();

    // Sticky Navbar functionality
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

    // Skills progress bar animation
    $('.skill').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});

    // Facts counter animation
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });

    // Testimonials carousel functionality
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

    // Portfolio isotope and filter functionality
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
        const url = 'https://libretranslate.de/translate';  // Public instance of LibreTranslate
        const data = {
            q: text,
            source: 'en',  // Default source language (English)
            target: targetLanguage  // Dynamic target language (could be 'en', 'it', etc.)
        };

        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => data.translatedText)
        .catch(error => console.error('Error with LibreTranslate API:', error));
    }

    // Function to dynamically translate page content (text nodes and attributes)
    function loadTranslation(language) {
        // Loop through each element's text content
        $('body').find('*').contents().each(function() {
            if (this.nodeType === 3 && this.textContent.trim() !== '') {  // Check for text nodes
                const originalText = this.textContent.trim();
                translateTextLibre(originalText, language).then(translatedText => {
                    this.textContent = translatedText;  // Update text content with the translated text
                });
            }
        });

        // Translate 'alt' and 'title' attributes for accessibility
        $('body').find('[alt], [title]').each(function() {
            const element = $(this);
            const attributeName = element.is('[alt]') ? 'alt' : 'title';
            const originalText = element.attr(attributeName);
            if (originalText && originalText.trim() !== '') {
                translateTextLibre(originalText, language).then(translatedText => {
                    element.attr(attributeName, translatedText);  // Update attribute with translated text
                });
            }
        });
    }

    // Event listeners for language switcher icons
    $('.language-switcher').on('click', function (event) {
        event.preventDefault();  // Prevent default behavior (navigation)
        const language = $(this).data('language');  // Get the language from the data attribute
        loadTranslation(language);   // Load translations based on the selected language
    });

    // Initial translation (optional, can be removed if you want to manually control it)
    loadTranslation('en');  // Default translation to English on page load

})(jQuery);
