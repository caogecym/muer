var nconf = require('nconf');

var jsFilePath = [
    'public/js/*.js',
    'public/js/spec/*.js',
];

module.exports = function(grunt) {
    nconf.argv().env().defaults({
        'karma-config': 'public/karma.conf.js'
    });

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        karma: {
            unit: {
                configFile: nconf.get('karma-config'),
            },
            //debug: {
            //    configFile: nconf.get('karma-debug'),
            //},
            //coverage: {
            //    configFile: nconf.get('karma-coverage'),
            //},
        },
        eslint: {
            options: {
                config: 'config/eslint.json',
            },
            target: jsFilePath
        },
        jade: {
            js: {
                options: {
                    namespace: false,
                    client: true,
                    amd: true,
                },
                files: [{
                    expand: true,
                    cwd: '.',
                    src: ['**/*.jade'],
                    ext: '.tmpl.js',
                }],
            }
        },
    });

    grunt.task.loadNpmTasks('grunt-karma');
    grunt.task.loadNpmTasks('grunt-eslint');
    grunt.task.loadNpmTasks('grunt-contrib-jade');

    grunt.registerTask('browser-test', '', function () {
        grunt.task.run('karma', ['karma:unit']);
    });

    grunt.registerTask('lint', ['eslint']);
    grunt.registerTask('build', ['jade']);

};
