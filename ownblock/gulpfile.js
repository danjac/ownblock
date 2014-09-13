var gulp = require('gulp'),
    bowerFiles = require('main-bower-files'),
    gulpFilter = require('gulp-filter'),
    shell = require('gulp-shell'),
    runSeq = require('run-sequence'),
    minifyCss = require('gulp-minify-css'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat');


var staticDir = 'static';

var dest = {
    js: staticDir + '/js',
    css: staticDir + '/css',
    fonts: staticDir + '/fonts'
};

gulp.task('install', shell.task([
    'bower cache clean',
    'bower install'
]));

gulp.task('pkg', function() {

    var jsFilter = gulpFilter('*.js');
    var cssFilter = gulpFilter('*.css');
    var fontFilter = gulpFilter(['*.eot', '*.woff', '*.svg', '*.ttf']);

    return gulp.src(bowerFiles({
            debugging: true,
            checkExistence: true,
            base: 'bower_components'
        }))
        .pipe(jsFilter)
        .pipe(concat('vendor.js'))
        .pipe(uglify())
        .pipe(gulp.dest(dest.js))
        .pipe(jsFilter.restore())
        .pipe(cssFilter)
        .pipe(concat('vendor.css'))
        .pipe(minifyCss())
        .pipe(gulp.dest(dest.css))
        .pipe(cssFilter.restore())
        .pipe(fontFilter)
        .pipe(gulp.dest(dest.fonts));
});


gulp.task('default', function(callback) {
    runSeq('install', 'pkg', callback);
});
