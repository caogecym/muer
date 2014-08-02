requirejs.config({
    baseUrl: url('/static'),
    paths: {
        // 3rd party libs
        'jquery': 'libs/jquery/js/jquery.min',
        'jquery-ui': 'libs/jquery-ui/js/jquery-ui.min',
        'jquery.growl': 'libs/jquery.growl/js/jquery.growl',
        'jquery.cookie': 'libs/jquery.cookie/js/jquery.cookie',
        'underscore': 'libs/underscore/js/underscore.min',
        'tween': 'libs/tween/js/tween.min',
        'dat-gui': 'libs/dat-gui/js/dat.gui.min',
        'threejs': 'libs/three/js/three.min',
        'vis-controls': 'libs/bp-three/js/VisualizationControls',
        'jade': 'libs/jade/js/jade',

        // resource modules
        //'muer': 'js/muer',
    },

    shim: {
        'jquery-ui' : ['jquery'],

        'jquery.cookie': {
            deps: ['jquery'],
            exports: 'jQuery.fn.cookie',
        },

        'jquery.growl': {
            deps: ['jquery'],
            exports: 'jQuery.fn.growl',
        },
    }
});
