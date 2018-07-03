var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var minify = require('gulp-minify');
var cleancss = require('gulp-clean-css');
var rename = require('gulp-rename');

var config = {
  bowerDir: './bower_components',
  publicDir: './website/static',
  root: '.'
};

gulp.task('fonts', function() {
  return gulp.src([
    config.bowerDir + '/bootstrap/fonts/**/*',
  ])
  .pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('js', function() {
  return gulp.src([
    config.bowerDir + '/bootstrap/dist/js/*.js',
    config.bowerDir + '/bootstrap/assets/js/vendor/popper.min.js',
    config.bowerDir + '/jquery/dist/jquery.slim.min.js',
  ])
  .pipe(sourcemaps.write(config.publicDir + '/js'))
  .pipe(gulp.dest(config.publicDir + '/js'));
});

gulp.task('css', function() {
  gulp.src([
     config.bowerDir + '/bootstrap/scss/*.scss',
   ])
  .pipe(sourcemaps.init())
  .pipe(sass({
    outputStyle: 'compressed',
    includePaths: [config.bowerDir + '/bootstrap/scss'],
  }))
  .pipe(rename({suffix: '.min'}))
  .pipe(cleancss({specialComments: 0}))
  .pipe(sourcemaps.write())
  .pipe(gulp.dest(config.publicDir + '/css'));
});

gulp.task('default', ['css', 'js', 'fonts']);
