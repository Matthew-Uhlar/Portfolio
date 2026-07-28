function config($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, IdleProvider, KeepaliveProvider) {

    // Configure Idle settings
    IdleProvider.idle(5); // in seconds
    IdleProvider.timeout(120); // in seconds

    $urlRouterProvider.otherwise("/app/overview");

    $ocLazyLoadProvider.config({
        // Set to true if you want to see what and when is dynamically loaded
        debug: false
    });

    $stateProvider
        .state('app', {
            abstract: true,
            url: "/app",
            templateUrl: "views/common/content.html",
        })
        .state('app.main', {
            url: "/main",
            templateUrl: "views/dashboard_1.html"
            // resolve: {
            //     loadPlugin: function ($ocLazyLoad) {
            //         return $ocLazyLoad.load([
            //             {
            //
            //                 serie: true,
            //                 name: 'angular-flot',
            //                 files: [ 'js/plugins/flot/jquery.flot.js', 'js/plugins/flot/jquery.flot.time.js', 'js/plugins/flot/jquery.flot.tooltip.min.js', 'js/plugins/flot/jquery.flot.spline.js', 'js/plugins/flot/jquery.flot.resize.js', 'js/plugins/flot/jquery.flot.pie.js', 'js/plugins/flot/curvedLines.js', 'js/plugins/flot/angular-flot.js', ]
            //             },
            //             {
            //                 name: 'angles',
            //                 files: ['js/plugins/chartJs/angles.js', 'js/plugins/chartJs/Chart.min.js']
            //             },
            //             {
            //                 name: 'angular-peity',
            //                 files: ['js/plugins/peity/jquery.peity.min.js', 'js/plugins/peity/angular-peity.js']
            //             }
            //         ]);
            //     }
            // }
        })
        .state('app.overview', {
            url: '/overview',
            templateUrl: "views/overview.html"
        })
        .state('app.map',{
            url: "/map",
            templateUrl: "views/map.html"
        })
        .state('app.list_view',{
            url: "/list_view",
            templateUrl: "views/list_view.html"
        })



        .state('landing', {
            url: "/",
            templateUrl: "views/landing.html",
            data: { pageTitle: 'Brains4Drones', specialClass: 'landing-page' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['js/plugins/wow/wow.min.js']
                        }
                    ]);
                }
            }
        })
        .state('login', {
            url: "/login",
            templateUrl: "views/login.html",
            controller: loginCtrl,
            data: { pageTitle: 'Login', specialClass: 'gray-bg' }
        })
        .state('register', {
            url: "/register",
            templateUrl: "views/register.html",
            data: { pageTitle: 'Register', specialClass: 'gray-bg' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['js/plugins/sweetalert/sweetalert.min.js', 'css/plugins/sweetalert/sweetalert.css']
                        },
                        {
                            name: 'oitozero.ngSweetAlert',
                            files: ['js/plugins/sweetalert/angular-sweetalert.min.js']
                        }
                    ]);
                }
            }
        })
        .state('artist_register', {
            url: "/artist_register",
            templateUrl: "views/registration2.html",
            data: { pageTitle: 'Register', specialClass: 'gray-bg' },
            controller: register2Ctrl,
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            files: ['js/plugins/sweetalert/sweetalert.min.js', 'css/plugins/sweetalert/sweetalert.css']
                        },
                        {
                            name: 'oitozero.ngSweetAlert',
                            files: ['js/plugins/sweetalert/angular-sweetalert.min.js']
                        }
                    ]);
                }
            }
        })



}
angular
    .module('inspinia')
    .config(config)
    .run(function($rootScope, $state, $http) {


        $http.get('data/poles.json').success(function(data){
            //$rootScope.lines = data.lines;
            $rootScope.lines = data;
            //console.log("LOOK HERE");
            console.log($rootScope.lines);
            //console.log($rootScope.lines[0])
        })




        $rootScope.$state = $state;



    });
