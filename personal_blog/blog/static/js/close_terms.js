$( document ).ready(function() {
    $('i.fa-times').click(function() {
        $('section.terms').slideUp(1000);
        document.cookie = "accepted_terms=True"
    });
});
