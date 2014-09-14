define(function (require) {
    'use strict';

    var $ = require('jquery');
    var mpicTemplate = require('mpic.tmpl');
    var ns = {};

    ns.populateMPics = function (response) {
        response.results.forEach(function (mpic) {
            var $mpic = mpicTemplate(mpic);
            $('.mpic-section', ns.$container).append($mpic);
        });
    };

    ns.pullMPicInfo = function () {
        $.ajax({
            type: 'GET',
            url: '/api/mpics',
            success: ns.populateMPics;
        });
    };

    ns.initialize = function () {
        ns.pullMPicInfo();
    };

});
