var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');

var config = {
  bowerDir: './bower_components',
  publicDir: './website/static',
};

gulp.task('fonts', function() {
  return gulp.src([
    config.bowerDir + '/bootstrap/fonts/**/*',
  ])
  .pipe(gulp.dest(config.publicDir + '/fonts'));
});

gulp.task('js', function() {
  return gulp.src([
    config.bowerDir + '/jquery/dist/jquery.min.js',
    config.bowerDir + '/bootstrap/dist/js/*.js',
  ])
  .pipe(sourcemaps.write())
  .pipe(gulp.dest(config.publicDir + '/js'));
});

gulp.task('css', function() {
  gulp.src(config.bowerDir + '/bootstrap/scss/*.scss')
  .pipe(sourcemaps.init())
  .pipe(sass({
    outputStyle: 'compressed',
    includePaths: [config.bowerDir + '/bootstrap/scss'],
  }))
  .pipe(sourcemaps.write())
  .pipe(gulp.dest(config.publicDir + '/css'));
});

gulp.task('default', ['css', 'js', 'fonts']);
