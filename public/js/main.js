/**
 * @file main entry for muer
*/
/* global requirejs require */
requirejs.config({
    //baseUrl: '../',
    paths: {
        // 3rd party libs
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min',
        'jquery-cookie': '//cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie',
        'bootstrap': '//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min'
    },

    shim: {
        'bootstrap': {
            deps: ['jquery']
        }
    }
});

require(['muer', 'jquery-cookie', 'bootstrap'], function (muer) {
    'use strict';
    muer.initialize();
});
