var currentContentID = 'map';

// override jquery validate plugin defaults
jQuery.validator.setDefaults({
    errorElement: 'span',
    errorPlacement: function (error, element) {
        error.addClass('invalid-feedback');
        element.closest('.form-group').append(error);
    },
    highlight: function (element, errorClass, validClass) {
        $(element).addClass('is-invalid');
    },
    unhighlight: function (element, errorClass, validClass) {
        $(element).removeClass('is-invalid');
    }
});

function showRequest(formData, jqForm, options) {
    // formData is an array; here we use $.param to convert it to a string to display it 
    // but the form plugin does this for you automatically when it submits the data 
    var queryString = $.param(formData);

    // jqForm is a jQuery object encapsulating the form element.  To access the 
    // DOM element for the form do this: 
    // var formElement = jqForm[0]; 
    alert('Submit:\n' + queryString);

    // here we could return false to prevent the form from being submitted; 
    // returning anything other than false will allow the form submit to continue 
    return true;
}

function formSubmitFromValidator(form, id, success_alert_en) {
    var options = {
        url: '/submit/' + id,
        type: 'post',
        // beforeSubmit: showRequest,  // pre-submit callback 
        dataType: 'json',
        success: function (json) {
            if (json.command == 1) {
                if (success_alert_en) {
                    langAlertResponseCommand(json.response, true);
                }
            } else {
                langAlertResponseCommand(json.response, false);
            }
            loadContent(currentContentID);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            langFetchError();
        }
    };

    $(form).ajaxSubmit(options);
}

function configValidator() {
    $('#config_form').validate({
        rules: {
            interval: {
                required: true,
                number: true,
            }
        },
        submitHandler: function (form) {
            formSubmitFromValidator(form, 'config', 1);
            // return false to prevent normal browser submit and page navigation 
            return false;
        }
    });
}

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

function langAlertResponseCommand(response, success) {
    var resp;
    var status;

    status = "Status";
    resp = success ? "Command success" : "Command failed";

    if (response)
        resp = response;

    langAlert(status, resp);
}

function langFetchError() {
    langAlert("Internal error", "Can't fetch data");
}

function docReady() {
    $('.nav-link').removeClass('active');
    $('#nav-' + currentContentID).addClass('active');

    if (currentContentID === 'config') {
        console.log("add valid");
        configValidator();
    }
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