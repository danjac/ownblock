(function() {
    'use strict';
    describe('homepage', function() {
        it('should have a title', function() {
            browser.get('http://demo.ownblock.com/app/');
            expect(browser.getTitle()).toEqual('Ownblock');
        });
    });

}());
