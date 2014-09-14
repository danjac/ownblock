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
    directive('paginatedTable', function(urls) {
        return {
            restrict: 'E',
            scope: {
                paginator: '=',
                cols: '='
            },
            transclude: true,
            replace: true,
            templateUrl: urls.partials + 'dataTable.html'
        };
    }).
    directive('rowDef', function() {
        return {
            restrict: 'A',
            link: function(scope, element, attrs, ctrl, transclude) {

                transclude(scope, function(clone) {
                    angular.forEach(clone, function(item) {
                        if (item.nodeName === 'CELL') {
                            var newElement = angular.element('<table><tr><td></td></tr></table>').find('td');
                            newElement.append(item);
                            element.append(newElement);
                        }
                    });
                });
            }
        };
    }).
    directive('searchForm', function(urls) {
        var SearchForm = function() {
            this.visible = false;
            this.filter = {
                value: ''
            };
        };
        SearchForm.prototype.toggle = function() {
            this.visible = !this.visible;
            if (!this.visible) {
                this.filter.value = '';
            }
        };
        return {
            restrict: 'E',
            scope: {
                paginator: '=',
                ifEmpty: '@'
            },
            replace: true,
            templateUrl: urls.partials + 'searchForm.html',
            compile: function() {
                return {
                    pre: function(scope, element, attrs) {
                        attrs.ifEmpty = attrs.ifEmpty || 'Sorry, no results found for your search';
                    },
                    post: function(scope, element, attrs) {
                        var form = new SearchForm();
                        if (angular.isDefined(attrs.isVisible)) {
                            form.visible = true;
                        }
                        if (attrs.name) {
                            scope.$parent[attrs.name] = scope[attrs.name] = form;
                        }
                        scope.$watch(attrs.name + '.filter.value', function(newValue) {
                            var filterObj = {};
                            filterObj[attrs.filter] = newValue;
                            if (scope.paginator) {
                                scope.paginator.filter(filterObj);
                            }
                        });

                    }
                };
            }
        };
    }).
    directive('userLink', function() {
        return {
            restrict: 'E',
            scope: {
                user: '='
            },
            replace: true,
            template: '<span><span ng-if="!user.is_active">{{user.full_name}} <span class="label label-warning">Removed</span></span><img ng-src="{{user.gravatar}}" ng-if="user.gravatar"> <a ng-if="user.is_active" ui-sref="residents.detail({id: user.id})">{{user.full_name}}</a></span>'
        };
    }).
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
    directive('confirmDialog', ['$modal', 'urls',
        function($modal, urls) {
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
                        templateUrl: urls.partials + 'confirmDialog.html',
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
                template: '<button><div ng-transclude></div></button>',
                link: function(scope, element, attrs) {
                    element.bind('click', function(event) {
                        event.preventDefault();
                        openModal(attrs.header, attrs.text, scope.onConfirm);
                    });
                }
            };

        }
    ]).directive('sendMessage', ['$modal', 'auth', 'api', 'notifier', 'urls',
        function($modal, auth, api, notifier, urls) {
            var modalInstanceCtrl = function($scope, $modalInstance, recipient, header) {

                    $scope.recipient = recipient;
                    $scope.message = new api.Message({
                        recipient: recipient.id,
                        header: header || ''
                    });
                    $scope.send = function() {
                        $modalInstance.close($scope.message);
                    };
                    $scope.cancel = function() {
                        $modalInstance.dismiss('cancel');
                    };
                },
                openModal = function(recipient, header) {
                    var modalInstance = $modal.open({
                        templateUrl: urls.partials + 'messages/modalForm.html',
                        controller: modalInstanceCtrl,
                        resolve: {
                            recipient: function() {
                                return recipient;
                            },
                            header: function() {
                                return header;
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
                restrict: 'E',
                scope: {
                    recipient: '=recipient',
                    header: '@'
                },
                replace: true,
                transclude: true,
                template: '<button role="button"><div ng-transclude></div></button>',
                link: function(scope, element, attrs) {
                    scope.$watch('recipient', function(newVal) {
                        if (newVal && newVal.id === auth.user.id) {
                            //attrs.$set('ngDisabled', true);
                            //element.addClass('disabled');
                            element.remove();
                        }
                    });
                    element.bind('click', function(event) {
                        event.preventDefault();
                        openModal(scope.recipient, scope.header);
                    });
                }
            };
        }
    ]);
}());
