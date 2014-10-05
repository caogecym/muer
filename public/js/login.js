define(function (require) {
    var $ = require('jquery');
    var ns = {};

    ns.setupRedirect = function () {
        $('.signinBtn').each(function (_, $signinBtn) {
            $signinBtn.href = $signinBtn.href + '?next=' + document.URL;
        });
    };

    ns.initialize = function () {
        ns.setupRedirect();
    };
    return ns;
});
