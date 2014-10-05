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
        'bootstrap': '//netdna.bootstrapcdn.com/bootstrap/2.3.2/js/bootstrap.min'
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

// load login.js file, so that DOM can reference its functions
require(["login"], function(login) {
    login.initialize();
});
