var gulp = require('gulp'),
    bowerFiles = require('main-bower-files'),
    gulpFilter = require('gulp-filter'),
    plumber = require('gulp-plumber'),
    debug = require('gulp-debug'),
    coffee = require('gulp-coffee'),
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
var appDir = 'app';

var dest = {
    coffee: appDir + '/js',
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

gulp.task('app-coffee', function() {
    return gulp.src('./app/coffee/**/*.coffee')
        .pipe(plumber())
        .pipe(coffee({
            bare: true
        }))
        .pipe(concat('app-coffee.js'))
        .pipe(gulp.dest(dest.coffee));
});

gulp.task('app-js', function() {
    return gulp.src('./app/js/*.js')
        .pipe(plumber())
        .pipe(concat('app.js'))
        .pipe(uglify({
            mangle: false
        }))
        .pipe(gulp.dest(dest.js));
});

gulp.task('app-css', function() {
    return gulp.src('./app/css/*.css')
        .pipe(plumber())
        .pipe(concat('app.css'))
        .pipe(minifyCss())
        .pipe(gulp.dest(dest.css));
});

gulp.task('default', function() {
    gulp.start('install', 'pkg');
    gulp.watch('app/**', {}, ['app-coffee', 'app-js', 'app-css']);
});
//
