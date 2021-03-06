/* global window require */
var tests = [];
for (var file in window.__karma__.files) {
    if (/-spec\.js$/.test(file)) {
        tests.push(file);
    }
}

require.config({
  // Karma serves files under /base, which is the basePath from your config file
  baseUrl: '/base/js',
  paths: {
      'jquery': '../libs/jquery/jquery',
  },

  deps: tests,

  // we have to kickoff jasmine, as it is asynchronous
  callback: window.__karma__.start
});
