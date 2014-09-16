(function() {
    'use strict';
    describe('homepage', function() {
        it('should have a title', function() {
            browser.get('/app');
            expect(browser.getTitle()).toEqual('Ownblock');
        });
    });

}());
