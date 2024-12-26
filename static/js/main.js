(function ($) {
    "use strict";

    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

    new WOW().init();

    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.navbar').addClass('sticky-top shadow-sm');
        } else {
            $('.navbar').removeClass('sticky-top shadow-sm');
        }
    });

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

    $('.skill').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {offset: '80%'});

    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });

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

    var portfolioIsotope = $('.portfolio-container').isotope({
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
    });
    $('#portfolio-flters li').on('click', function () {
        $("#portfolio-flters li").removeClass('active');
        $(this).addClass('active');
        portfolioIsotope.isotope({ filter: $(this).data('filter') });
    });

    function translateTextAzure(text, targetLanguage) {
        const url = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0';
        const region = 'italynorth';  // Correct region name
        const subscriptionKey = '4Q40w3KM8TuqK8LJ0ataejTWkZnJWu6sBeGTTAIhqbggvLusmqB5JQQJ99ALACgEuAYXJ3w3AAAbACOGkm8d';

        const headers = {
            'Ocp-Apim-Subscription-Key': subscriptionKey,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Region': italynorth
        };

        const body = [{
            Text: text,
        }];

        const params = new URLSearchParams({
            'to': targetLanguage,
        });

        return fetch(`${url}&${params.toString()}`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body),
        })
        .then(response => {
            if (!response.ok) {
                console.error(`Error with API response: ${response.statusText}`);
                throw new Error(`Error with API response: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data && data[0] && data[0].translations[0]) {
                return data[0].translations[0].text;
            } else {
                console.error('Translation error:', data);
                return text;
            }
        })
        .catch(error => {
            console.error('Error with Azure Translation API:', error);
            return text;
        });
    }

    function translatePageContent(language) {
        $('.translate').each(function () {
            const originalText = $(this).text();
            translateTextAzure(originalText, language).then(translatedText => {
                $(this).text(translatedText);
            });
        });
    }

    // Event listener for language switcher
    $('.language-switcher').click(function (e) {
        e.preventDefault();
        const language = $(this).data('language');
        translatePageContent(language);
    });

})(jQuery);
