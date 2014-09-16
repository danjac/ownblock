var gulp = require('gulp'),
    bowerFiles = require('main-bower-files'),
    gulpFilter = require('gulp-filter'),
    debug = require('gulp-debug'),
    shell = require('gulp-shell'),
    runSeq = require('run-sequence'),
    minifyCss = require('gulp-minify-css'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat');

// Handle the error
function errorHandler(error) {
    console.log(error.toString());
    this.emit('end');
}

var staticDir = 'static';

var dest = {
    js: staticDir + '/js',
    css: staticDir + '/css',
    fonts: staticDir + '/fonts'
};

var jsFilter = gulpFilter('*.js');
var cssFilter = gulpFilter('*.css');
var fontFilter = gulpFilter(['*.eot', '*.woff', '*.svg', '*.ttf']);


gulp.task('install', shell.task([
    'bower cache clean',
    'bower install'
]));

gulp.task('pkg', function() {

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

gulp.task('app-js', function() {
    return gulp.src('./app/js/*.js')
        .pipe(concat('app.js'))
        .pipe(uglify({
            mangle: false
        }))
        .pipe(gulp.dest(dest.js));
});

gulp.task('app-css', function() {
    return gulp.src('./app/css/*.css')
        .pipe(concat('app.css'))
        .pipe(minifyCss())
        .pipe(gulp.dest(dest.css));
});

gulp.task('default', function() {
    gulp.start('install', 'pkg');
    gulp.watch('app/**', {}, ['app-js', 'app-css']);
});
//
