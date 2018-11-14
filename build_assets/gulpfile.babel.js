import gulp from 'gulp'
import debug from 'gulp-debug'
import path from 'path'
import gulpLoadPlugins from 'gulp-load-plugins'
import runSeq from 'run-sequence'
import flatten from 'gulp-flatten'
import sourcemaps from 'gulp-sourcemaps'
import noop from 'gulp-noop'
import cleanCSS from 'gulp-clean-css'


let plugins = gulpLoadPlugins()

// Plugins
import sass from 'gulp-sass'
import minifyCss from 'gulp-minify-css'

let buildEnv = plugins.util.env.environment || 'development'
let config = require('./config/' + buildEnv + '.json')

// Shared error handler
function handleError(err) {
    console.log(err.toString())
    this.emit('end')
}

gulp.task('sass-build', function() {
    return gulp
        .src([
            path.join(config.src, '**/scss/**/[^_]*.scss')
        ])
        .pipe(debug())
        .pipe(config.srcmap ? sourcemaps.init() : noop())
        .pipe(sass({
            sourceComments: config.srcmap ? 'map' : false
        }).on('error', sass.logError)).on('error', handleError)
        .pipe(flatten())
        .pipe(config.srcmap ? sourcemaps.write('./') : noop())
        .pipe(config.minify ? minifyCss() : plugins.util.noop())
        .pipe(gulp.dest(path.join(config.dest, 'css')))
})

gulp.task('fa-build', function () {
    return gulp
        .src('../tennisblock_client/node_modules/font-awesome/fonts/*')
        .pipe(gulp.dest(path.join(config.dest, 'fonts')))
})

gulp.task('build', ['sass-build', 'fa-build'], function() {

})

gulp.task('build-all', function(done) {
    runSeq('build', function() {
        done()
    })
})


gulp.task('watch', ['build-all'], function() {
    gulp.watch(path.join(config.src, '**/scss/**/*.scss'), ['sass-build'])
})

gulp.task('default', ['build-all'])
