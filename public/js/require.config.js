/* global requirejs */

requirejs.config({
    baseUrl: '../',
    paths: {
        // 3rd party libs
        'jquery': 'libs/jquery/jquery',
        //'jquery-ui': 'libs/jquery-ui/js/jquery-ui.min',
        //'jquery.cookie': 'libs/jquery.cookie/js/jquery.cookie',
        //'underscore': 'libs/underscore/js/underscore.min',
        //'jade': 'libs/jade/js/jade',

        // resource modules
        //'muer': 'js/muer',
    },

    //shim: {
    //    'jquery-ui' : ['jquery'],

    //    'jquery.cookie': {
    //        deps: ['jquery'],
    //        exports: 'jQuery.fn.cookie',
    //    },

    //    'jquery.growl': {
    //        deps: ['jquery'],
    //        exports: 'jQuery.fn.growl',
    //    },
    //}
});
