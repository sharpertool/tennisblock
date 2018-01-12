var gulp = require('gulp');
var debug = require('gulp-debug');
var path = require('path');
var plugins = require('gulp-load-plugins')();
var runSeq = require('run-sequence');

// Plugins
var sass = require('gulp-sass');
var minifyCss = require('gulp-minify-css');

var buildEnv = plugins.util.env.environment || 'development';
var config = require('./config/'+buildEnv+'.json');

// Shared error handler
function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}

gulp.task('bootstrap-install', function() {
    return gulp
        .src('./node_modules/bootstrap/scss/**/*.scss')
        .pipe(gulp.dest(path.join(config.src, 'scss/libs/bootstrap')));
});

gulp.task('sass-build', function() {
    return gulp
        .src([
            path.join(config.src, 'scss/*.scss')
        ])
        .pipe(debug())
        .pipe(sass({
            sourceComments: config.srcmap ? 'map' : false
        }).on('error', sass.logError)).on('error', handleError)
        .pipe(config.minify ? minifyCss() : plugins.util.noop())
        .pipe(gulp.dest(path.join(config.dest, 'css')));
});

gulp.task('copy-css', function() {
    return gulp
        .src([path.join(config.src, 'css/**/*')])
        .pipe(gulp.dest(path.join(config.dest, 'css')));
});

gulp.task('build', ['bootstrap-install', 'sass-build'], function() {

});

gulp.task('build-all', function(done) {
    runSeq('bootstrap-install', 'build', function() {
        done();
    });
});


gulp.task('watch', ['build-all'], function() {
    gulp.watch(path.join(config.src, 'scss/**/*.scss'), ['sass-build']);
});

gulp.task('default', ['build-all']);
