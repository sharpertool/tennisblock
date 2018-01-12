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

gulp.task('build', ['sass-build'], function() {

});

gulp.task('build-all', function(done) {
    runSeq('build', function() {
        done();
    });
});


gulp.task('watch', ['build-all'], function() {
    gulp.watch(path.join(config.src, 'scss/**/*.scss'), ['sass-build']);
});

gulp.task('default', ['build-all']);
