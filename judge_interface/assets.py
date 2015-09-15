from django_assets import Bundle, register

css_3rd = Bundle(
    'bootstrap/dist/css/bootstrap.css',
    'djangular/css/styles.css',
    'djangular/css/bootstrap3.css',
    filters='cssmin',
    output='packed/lib.css'
)

css_custom = Bundle(
    'css/app.css',
    filters='cssmin',
    output='packed/app.css'
)

js_3rd = Bundle(
    'jquery/dist/jquery.js',
    'angular/angular.js',
    'angular-route/angular-route.js',
    'angular-resource/angular-resource.js',
    'angular-animate/angular-animate.js',
    'angular-bootstrap/ui-bootstrap-tpls.js',
    'bootstrap/dist/js/bootstrap.js',
    'djangular/js/django-angular.js',
    'js/jquery.gracket.js',
    filters='jsmin',
    output='packed/lib.js'
)

js_custom = Bundle(
    'js/app.js',
    filters='jsmin',
    output='packed/app.js'
)

register({'js_3rd': js_3rd, 'js_custom': js_custom, 'css_3rd': css_3rd, 'css_custom': css_custom})
