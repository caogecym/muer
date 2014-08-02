define(function (require) {
    'use strict';
    var muer = require('js/muer');

    describe("muer", function() {
        beforeEach(function() {
            spyOn(muer, 'initialize');
            muer.initialize();
        });

        it("initialize controller", function() {
            expect(muer.initialize).toHaveBeenCalled();
        });
    });
});
