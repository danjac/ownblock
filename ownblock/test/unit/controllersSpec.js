'use strict';

/* jasmine specs for controllers go here */

describe('controllers', function() {

    beforeEach(function() {
        module('ownblock');
        module('ownblock.services');
        module('ownblock.controllers');
    });

    beforeEach(module('stateMock'));

    it('should maybe show a list of notices', inject(
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
