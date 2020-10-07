const cgi_content_file = 'cgi-bin/content.cgi';

var currentContentID = 'map';

function langAlert(title, data) {
    var $_hiddenform = $('#hiddenForm');
    var __html = '<div class="modal-dialog" role="document">';
    __html += '<div class="modal-content">';

    __html += '<div class="modal-header">';
    __html += '<h5 class="modal-title">' + title + '</h5>';
    __html += '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'
    __html += '<span aria-hidden="true">&times;</span></button></div>';

    __html += '<div class="modal-body"><p>' + data + '</p></div>';
    __html += '<div class="modal-footer">';
    __html += '<button type="button" class="btn btn-secondary" data-dismiss="modal">';
    __html += 'Close';
    __html += '</button></div>';

    __html += '</div>';
    __html += '</div>';

    $_hiddenform.html(__html);
    $_hiddenform.modal('show');
}

function langFetchError() {
    langAlert("Internal error", "Can't fetch data");
}

function docReady() {
    $('.nav-link').removeClass('active');
    $('#nav-' + currentContentID).addClass('active');
}

var newContentID;

function loadContent(contentID, param) {
    newContentID = contentID;

    $.get('/content/' + contentID, function (data) {
        if (newContentID != contentID)
            return;

        currentContentID = contentID;

        $('#content').html(data);
        docReady();
    }).fail(function () {
        langFetchError();
    });
}

$(document).ready(function () {
    loadContent(currentContentID);
});