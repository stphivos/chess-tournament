$(document).ready(function () {
    $(function () {
        $(document).on('scroll', function (e) {
            $('.navbar-default').each(function () {
                var css = {opacity: $(document).scrollTop() > $(this).height() ? 0.8 : 1};
                css['transition'] = 'opacity 0.5s ease-in-out';
                $(this).css(css);
            });
        });

        $('body').popover({
            trigger: 'hover',
            selector: '[data-toggle="popover"]'
        });

        function detectEnv() {
            var body = $('body');
            var envs = ['xs', 'sm', 'md', 'lg'];

            var el = $('<div>');
            el.appendTo($(body));

            for (var i = envs.length - 1; i >= 0; i--) {
                var env = envs[i];

                el.addClass('hidden-' + env);
                if (el.is(':hidden')) {
                    el.remove();
                    $(body).removeClass('xs sm md lg').addClass(env);
                    return;
                }
            }
        }

        $(window).resize(function () {
            detectEnv();
        });

        detectEnv();
    })
});

Array.prototype.clean = function (text) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == text) {
            this.splice(i, 1);
            i--;
        }
    }
    return this;
};

var home = null;
var app = angular.module('ChessApp', ['ngRoute', 'ngAnimate', 'ngResource', 'ngCookies', 'ui.router', 'ui.bootstrap', 'ng.django.forms']);

app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
}]);

app.config(['$routeProvider', '$locationProvider', '$resourceProvider', '$modalProvider',
    function ($routeProvider, $locationProvider, $resourceProvider, $modalProvider) {
        $routeProvider
            .when('/participants', {
                templateUrl: 'participants',
                controller: 'ParticipantController'
            })
            .when('/login', {
                templateUrl: 'login',
                controller: 'LoginController'
            })
            .otherwise({
                templateUrl: 'tournament',
                controller: 'TournamentController'
            });
        $locationProvider.html5Mode(true);
        $resourceProvider.defaults.stripTrailingSlashes = false;
        $modalProvider.options.animation = false;
    }]);

app.service('utils', function ($http, $modal) {
    var _service = this;

    this.showMessage = function (title, body) {
        if (body && body['message'])
            body = body['message'];

        if (!home.modal) {
            home.modal = {};
        }

        home.modal.title = title;
        home.modal.body = body;

        if (!home.modal.isOpen) {
            $modal.open({
                scope: home,
                templateUrl: 'common-modal',
                controller: function ($scope, $http, $window, $modalInstance) {
                    home.modal.instance = $modalInstance;
                    $modalInstance.opened.then(function () {
                        home.modal.isOpen = true;
                    });
                    $modalInstance.result.then(function () {
                        home.modal.isOpen = false;
                    });
                    $scope.ok = function () {
                        $modalInstance.close();
                    };
                }
            });
        }
    };

    this.httpGet = function (url, successAction, startProgress, stopProgress) {
        var options = {method: 'GET', url: url};
        this.http(options, successAction, undefined, startProgress, stopProgress);
    };

    this.httpPost = function (url, fields, encoded, successAction, startProgress, stopProgress) {
        var options = {
            method: 'POST',
            url: url,
            data: fields
        };
        if (encoded) {
            options.data = $.param(fields);
            options.headers = {'Content-Type': 'application/x-www-form-urlencoded'};
        }
        this.http(options, successAction, undefined, startProgress, stopProgress);
    };

    this.http = function (options, successAction, errorAction, startProgress, stopProgress) {
        startProgress = startProgress == undefined ? true : startProgress;
        stopProgress = stopProgress == undefined ? true : stopProgress;
        if (startProgress) {
            this.showProgress();
        }
        $http(options)
            .success(function (data, status, headers, config) {
                if (stopProgress) {
                    _service.hideProgress();
                }
                successAction(data, status, headers, config);
            })
            .error(function (data, status, headers, config) {
                _service.hideProgress();
                if (errorAction == undefined) {
                    //console.log(data);
                    _service.showMessage(options.url, data);
                }
                else {
                    errorAction(data, status, headers, config);
                }
            });
    };

    this.showProgress = function (scope) {
        home.loading = true;
        if (scope) {
            scope.loading = true;
        }
    };

    this.hideProgress = function (scope) {
        home.loading = false;
        if (scope) {
            scope.loading = false;
        }
    };

    this.openModal = function (scope, templateUrl, submitCallback, cancelCallback) {
        $modal.open({
            scope: scope,
            templateUrl: templateUrl,
            controller: function ($scope, $modalInstance) {
                $scope.submit = function (request) {
                    $modalInstance.close();
                    if (submitCallback)
                        submitCallback(request);
                };
                $scope.cancel = function () {
                    $modalInstance.dismiss();
                    if (cancelCallback)
                        cancelCallback();
                };
            }
        });
    }
});

app.factory('Auth', function ($http, $cookies, $location) {
    var service = {};
    service.globals = globals;
    service.setUser = setUser;
    service.clearUser = clearUser;
    service.isLoggedIn = isLoggedIn;
    service.verifyLoggedIn = verifyLoggedIn;

    var globals = null;

    function setUser(credentials) {
        clearUser();
        var token = btoa(credentials.username + ':' + credentials.password);
        globals = {
            username: credentials.username,
            token: token
        };
        home.user = credentials.username;
        $cookies.put('auth', JSON.stringify(globals));
        $http.defaults.headers.common['Authorization'] = 'Basic ' + token;
    }

    function clearUser() {
        globals = null;
        home.user = '';
        $cookies.remove('auth');
        $http.defaults.headers.common.Authorization = null;
    }

    function isLoggedIn() {
        if (!globals) {
            var auth = $cookies.get('auth');
            globals = auth ? JSON.parse(auth) : null;
        }
        if (globals && !$http.defaults.headers.common['Authorization']) {
            home.user = globals.username;
            $http.defaults.headers.common['Authorization'] = 'Basic ' + globals.token;
        }
        return (globals) ? globals.username : false;
    }

    function verifyLoggedIn() {
        var result = isLoggedIn();
        if (!result) {
            var current = $location.path();
            $location.path('/login').search('next', current);
        }
        return result;
    }

    return service;
});

app.controller('HomeController', function ($scope, Auth) {
    home = $scope;
    Auth.isLoggedIn();
    $scope.logout = function () {
        Auth.clearUser();
    };
});

app.controller('LoginController', function ($scope, $location, utils, Auth) {
    $scope.login = function (credentials) {
        utils.httpPost('/login', credentials, true, function (result) {
            if (!result || !result.error) {
                Auth.setUser(credentials);
                $location.path($location.search().next || '/');
                $location.search('next', null);
            }
            else {
                // Display auth error
            }
        });
    };
});

app.factory('Tournament', function ($resource) {
    return $resource('/api/tournament/:id/', {id: '@id'}, {
        update: {
            method: 'PUT'
        },
        gameFind: {
            method: 'GET',
            params: {round: '@round', no: '@no'},
            url: '/api/tournament/:id/round/:round/game/:no'
        },
        gameEnd: {
            method: 'PUT',
            params: {p1: '@p1', p2: '@p2'},
            url: '/api/game/:id/p1/:p1/p2/:p2'
        }
    });
});

app.controller('TournamentController', function ($scope, $location, $compile, utils, Auth, Tournament) {
    $scope.scores = {
        0: '0',
        0.5: '0.5',
        1: '1'
    };
    $scope.add = function () {
        if (!Auth.verifyLoggedIn()) return;
        $scope.request = new Tournament();
        utils.openModal($scope, '/tournament/edit', function () {
            utils.showProgress();
            $scope.request.$save(function () {
                $scope.selectParticipants();
            }, function (err) {
                utils.hideProgress();
                utils.showMessage('Start Tournament', err.data.detail ? err.data.detail : err.data);
            });
        });
    };
    $scope.load = function () {
        utils.showProgress();
        $scope.tournament = home.tournament = Tournament.get({id: 'latest'}, function () {
            utils.hideProgress();
        });
    };
    $scope.showGame = function (round, no) {
        utils.showProgress();
        var game = Tournament.gameFind({id: $scope.tournament.id, round: round, no: no}, function () {
            if (game.start_date) {
                $scope.game = game;
            }
            utils.hideProgress();
        });
    };
    $scope.hideGame = function () {
        $scope.game = null;
    };
    $scope.updateP1score = function () {
        switch ($scope.game.p2_score) {
            case 0:
                $scope.game.p1_score = 1;
                break;
            case 0.5:
                $scope.game.p1_score = 0.5;
                break;
            case 1:
                $scope.game.p1_score = 0;
                break;
        }
    };
    $scope.updateP2score = function () {
        switch ($scope.game.p1_score) {
            case 0:
                $scope.game.p2_score = 1;
                break;
            case 0.5:
                $scope.game.p2_score = 0.5;
                break;
            case 1:
                $scope.game.p2_score = 0;
                break;
        }
    };
    $scope.endGame = function () {
        if (!Auth.verifyLoggedIn()) return;
        utils.showProgress();
        Tournament.gameEnd({id: $scope.game.id, p1: $scope.game.p1_score, p2: $scope.game.p2_score}, function () {
            $scope.hideGame();
            $scope.load();
        });
    };
    $scope.selectParticipants = function () {
        $location.path('/participants');
    };
    $scope.load();
});

app.factory('Participant', function ($resource) {
    return $resource('/api/participants/:id/', {id: '@id'}, {
        update: {
            method: 'PUT'
        }
    });
});

app.controller('ParticipantController', function ($scope, $location, $http, utils, Auth, Participant, Tournament) {
    $scope.load = function () {
        utils.showProgress();
        $scope.selected = 0;
        $scope.participants = Participant.query(function () {
            $scope.tournament = home.tournament;
            utils.hideProgress();
        });
    };
    $scope.add = function () {
        if (!Auth.verifyLoggedIn()) return;
        $scope.request = new Participant();
        utils.openModal($scope, '/participant/edit', function () {
            utils.showProgress();
            $scope.request.$save(function () {
                $scope.participants.push($scope.request);
                utils.hideProgress();
            });
        });
    };
    $scope.edit = function (index) {
        if (!Auth.verifyLoggedIn()) return;
        $scope.request = $scope.participants[index];
        utils.openModal($scope, '/participant/edit?id=' + $scope.request.id, function () {
            utils.showProgress();
            $scope.request.$update(function () {
                utils.hideProgress();
            });
        });
    };
    $scope.delete = function (index) {
        if (!Auth.verifyLoggedIn()) return;
        $scope.item = $scope.participants[index];

        utils.showProgress();
        $scope.item.$delete(function () {
            $scope.participants.splice(index, 1);
            utils.hideProgress();
        });
    };
    $scope.select = function (index) {
        if (!Auth.verifyLoggedIn()) return;
        $scope.participants[index].selected = !$scope.participants[index].selected;
        $scope.selected += $scope.participants[index].selected ? 1 : -1;
    };
    $scope.start = function () {
        if (!Auth.verifyLoggedIn()) return;
        var fields = {'ids': ''};
        fields.ids = $scope.participants.map(function (x) {
            return x.selected ? x.id : '';
        }).clean('').join(',');
        if (fields.ids.length > 0) {
            utils.httpPost('/tournament/start', fields, true, function () {
                $location.path('/tournament');
            });
        }
    };
    $scope.load();
});