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
