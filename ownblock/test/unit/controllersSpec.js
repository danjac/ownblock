'use strict';

/* jasmine specs for controllers go here */

describe('controllers', function() {

    beforeEach(function() {
        module('ownblock');
        module('ownblock.services');
        module('ownblock.controllers');
    });

    beforeEach(module('stateMock'));

    it('should add a new notice', inject(
        function($rootScope, $controller, $state, _$httpBackend_) {
            var scope = $rootScope.$new(),
                httpBackend = _$httpBackend_,
                state = $state;

            httpBackend.when('POST', '/api/notices/notices').respond('OK');

            $controller('notices.NewCtrl', {
                $scope: scope
            });

            scope.save();
            state.expectTransitionTo('notices.list');

        }
    ));

    it('should show a single notice', inject(
        function($rootScope, $controller, _$httpBackend_) {

            var scope = $rootScope.$new(),
                httpBackend = _$httpBackend_,
                state = {
                    params: {
                        id: 1
                    }
                };

            httpBackend.when('GET', '/api/notices/notices/1').
            respond({
                id: 1,
                title: 'test',
                author: {
                    full_name: 'tester'
                }
            });
            $controller('notices.DetailCtrl', {
                $scope: scope,
                $state: state
            });
            httpBackend.flush();
            expect(scope.notice.title).toBe('test');
        }));

    it('should show a list of notices', inject(
        function($rootScope,
            $controller, _$httpBackend_) {
            var scope = $rootScope.$new(),
                httpBackend = _$httpBackend_;

            httpBackend.when('GET', '/api/notices/notices').
            respond(
                [{
                    id: 1,
                    title: 'test this sucka',
                    author: {
                        full_name: 'Tester'
                    }
                }]
            );
            $controller('notices.ListCtrl', {
                $scope: scope
            });

            httpBackend.flush();
            expect(scope.paginator.total).toBe(1);
        }));

});
