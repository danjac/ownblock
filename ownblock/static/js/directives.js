(function() {
    'use strict';
    angular.module('ownblock.directives', []).
    directive('icon', function() {
        return {
            restrict: 'E',
            scope: {
                name: '@',
                text: '@'
            },
            template: '<i class="fa fa-{{name}}"></i>&nbsp;{{text}}'
            //template: '<span class="glyphicon glyphicon-{{name}}"></span>&nbsp;{{text}}'
        };
    }).
    directive('hasRole', ['auth',
        function(auth) {
            return {
                restrict: 'A',
                link: function(scope, element, attrs) {
                    if (!auth.hasRole(attrs.hasRole)) {
                        element.remove();
                    }
                }

            };
        }
    ]).
    directive('filesModel', function() {
        /* https://github.com/angular/angular.js/issues/1375#issuecomment-21933012 */
        return {
            controller: function($parse, $element, $attrs, $scope, $window) {
                var exp = $parse($attrs.filesModel);
                $element.on('change', function() {
                    exp.assign($scope, this.files);
                    if ($window.FileReader !== null) {
                        var file = this.files[0],
                            reader = new $window.FileReader();
                        reader.onload = function() {
                            $scope.upload = {
                                url: reader.result
                            };
                            $scope.$apply();
                        };
                        reader.readAsDataURL(file);
                    }

                    $scope.$apply();
                });
            }
        };
    }).
    directive('confirmDialog', ['$modal', 'staticUrl',
        function($modal, staticUrl) {
            var modalInstanceCtrl = function($scope, $modalInstance, header, text) {
                    $scope.header = header;
                    $scope.text = text;
                    $scope.confirm = function() {
                        $modalInstance.close(true);
                    };
                    $scope.cancel = function() {
                        $modalInstance.dismiss('cancel');
                    };
                },
                openModal = function(header, text, onConfirm) {
                    var modalInstance = $modal.open({
                        templateUrl: staticUrl + '/partials/confirmDialog.html',
                        controller: modalInstanceCtrl,
                        resolve: {
                            header: function() {
                                return header;
                            },
                            text: function() {
                                return text;
                            }
                        }
                    });
                    modalInstance.result.then(function(result) {
                        if (result) {
                            onConfirm();
                        }
                    });
                };
            return {
                restrict: 'E',
                scope: {
                    onConfirm: '&'
                },
                replace: true,
                transclude: true,
                template: '<button><ng-transclude></ng-transclude></button>',
                link: function(scope, element, attrs) {
                    element.bind('click', function(event) {
                        event.preventDefault();
                        openModal(attrs.header, attrs.text, scope.onConfirm);
                    });
                }
            };

        }
    ]).directive('sendMessage', ['$modal', 'api', 'notifier', 'staticUrl',
        function($modal, api, notifier, staticUrl) {
            var modalInstanceCtrl = function($scope, $modalInstance, recipient) {

                    $scope.recipient = recipient;
                    $scope.message = new api.Message({
                        recipient: recipient.id
                    });
                    $scope.send = function() {
                        $modalInstance.close($scope.message);
                    };
                    $scope.cancel = function() {
                        $modalInstance.dismiss('cancel');
                    };
                },
                openModal = function(user) {
                    var modalInstance = $modal.open({
                        templateUrl: staticUrl + '/partials/messages/modalForm.html',
                        controller: modalInstanceCtrl,
                        resolve: {
                            recipient: function() {
                                return user;
                            }
                        }
                    });
                    modalInstance.result.then(function(message) {
                        message.$save(function() {
                            notifier.success('Your message has been sent');
                        });
                    });

                };
            return {
                restrict: 'A',
                link: function(scope, element, attrs) {
                    element.bind('click', function(event) {
                        event.preventDefault();
                        openModal(scope.$eval(attrs.sendMessage));
                    });
                }
            };
        }
    ]);
}());
