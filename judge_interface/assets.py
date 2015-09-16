from django_assets import Bundle, register

css = Bundle(
    'bootstrap/dist/css/bootstrap.css',
    'djangular/css/styles.css',
    'djangular/css/bootstrap3.css',
    'css/bootstrap-theme.sandstone.min.css',
    'css/app.css',
    filters='cssmin',
    output='packed/app.css'
)

js = Bundle(
    'jquery/dist/jquery.js',
    'angular/angular.js',
    'angular-cookies/angular-cookies.js',
    'angular-ui-router/release/angular-ui-router.js',
    'angular-route/angular-route.js',
    'angular-resource/angular-resource.js',
    'angular-animate/angular-animate.js',
    'angular-bootstrap/ui-bootstrap-tpls.js',
    'bootstrap/dist/js/bootstrap.js',
    'djangular/js/django-angular.js',
    'js/jquery.gracket.js',
    'js/app.js',
    filters='jsmin',
    output='packed/app.js'
)

register({'js': js, 'css': css})
