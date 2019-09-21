(function() {

    amplify.request.decoders.customError = function(data, status, xhr, success, error) {
        if (status === "success") {
            success(data, status);
        } else if (status === "fail" || status === "error") {
            error(xhr, status, error);
        } else {
            error(xhr, status, error);
        }
    };

    amplify.request.define('save', 'ajax', {
        url: basepath + "/api/project{saveUrl}",
        cache: false,
        dataType: 'json',
        type: 'POST',
        decoder: 'customError'
    });

    amplify.request.define('permissions', 'ajax', {
        url: basepath + "/api/project/",
        cache: false,
        dataType: 'json',
        type: 'PUT'
    });

})();

