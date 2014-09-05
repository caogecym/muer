var nconf = require('nconf');

var jsFilePath = [
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
    });

    // Default task(s).
    grunt.registerTask('test', '', function () {
        grunt.task.loadNpmTasks('grunt-karma');
        grunt.task.run(['karma:unit']);
    });

};
