'use strict';

module.exports = function(config) {
    config.set({

        basePath: '../',

        files: [
            'static/bower_components/jquery/dist/jquery.min.js',
            'static/bower_components/bootstrap/dist/js/bootstrap.min.js',
            'static/bower_components/angular/angular.js',
            'static/bower_components/angular-cookies/angular-cookies.js',
            'static/bower_components/angular-ui-router/release/angular-ui-router.min.js',
            'static/bower_components/angular-ui-calendar/src/calendar.js',
            'static/bower_components/angular-bootstrap/ui-bootstrap.min.js',
            'static/bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
            'static/bower_components/angular-sanitize/angular-sanitize.js',
            'static/bower_components/angular-resource/angular-resource.js',
            'static/bower_components/angular-mocks/angular-mocks.js',
            //'static/bower_components/angular-scenario/angular-scenario.js',
            'static/js/**/*.js',
            'test/mock/**/*.js',
            'test/unit/**/*.js'
        ],

        autoWatch: true,

        frameworks: ['jasmine'],

        browsers: ['PhantomJS'],

        plugins: [
            'karma-phantomjs-launcher',
            'karma-jasmine',
            'karma-junit-reporter'
        ],

        junitReporter: {
            outputFile: 'test_out/unit.xml',
            suite: 'unit'
        },

        logLevel: config.LOG_INFO

    });
};
