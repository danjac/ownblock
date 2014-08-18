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
            template: '<span class="glyphicon glyphicon-{{name}}"></span>&nbsp;{{text}}'
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
                console.log("filesModel")
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
    directive('sendMessage', ['$modal', 'api', 'notifier', 'staticUrl',
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
