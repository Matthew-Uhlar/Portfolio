/**
 * INSPINIA - Responsive Admin Theme
 *
 */
(function () {
    angular.module('inspinia', [
        'ui.router',                    // Routing
        'oc.lazyLoad',                  // ocLazyLoad
        'ui.bootstrap',                 // Ui Bootstrap
        'pascalprecht.translate',       // Angular Translate
        'ngIdle',                       // Idle timer
        'ngSanitize',                    // ngSanitize
        'flow',
        'angularFileUpload',
        'ngFileUpload'

    ])
        .directive('ngThumb', ['$window', function($window) {
            var helper = {
                support: !!($window.FileReader && $window.CanvasRenderingContext2D),
                isFile: function(item) {
                    return angular.isObject(item) && item instanceof $window.File;
                },
                isImage: function(file) {
                    var type =  '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
                    return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
                }
            };

            return {
                restrict: 'A',
                template: '<canvas/>',
                link: function(scope, element, attributes) {
                    if (!helper.support) return;

                    var params = scope.$eval(attributes.ngThumb);

                    if (!helper.isFile(params.file)) return;
                    if (!helper.isImage(params.file)) return;

                    var canvas = element.find('canvas');
                    var reader = new FileReader();

                    reader.onload = onLoadFile;
                    reader.readAsDataURL(params.file);

                    function onLoadFile(event) {
                        var img = new Image();
                        img.onload = onLoadImage;
                        img.src = event.target.result;
                    }

                    function onLoadImage() {
                        var width = params.width || this.width / this.height * params.height;
                        var height = params.height || this.height / this.width * params.width;
                        canvas.attr({ width: width, height: height });
                        canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
                    }
                }
            };
        }])
        .factory('ImageService', function Formulator() {
            var Formulator = {
                readImageFile: function(file, cb){
                    if (window.FileReader) {
                        if(file.size > 4000000) {
                            return cb('Error, file too large')
                        }
                        if (!file.type.match('image.*')) {
                            return cb('Please upload Image Only')
                        }
                        var reader = new FileReader();
                        reader.onloadend = function (event) {
                            if (event.target.error !== null) {
                                return cb('Error, please try again')
                            }
                            else {
                                return cb(null, reader.result);
                            }
                        };
                        reader.readAsDataURL(file);
                    } else {
                        return cb('Sorry this browser does not support image upload.')
                    }
                }
            };
            return Formulator;
        })
        .directive("fileInput", function($parse){
            return{
                link: function($scope, element, attrs){
                    element.on("change", function(event){
                        var files = event.target.files;
                        //console.log(files[0].name);
                        $parse(attrs.fileInput).assign($scope, element[0].files);
                        $scope.$apply();
                    });
                }
            }
        });
})();

// Other libraries are loaded dynamically in the config.js file using the library ocLazyLoad