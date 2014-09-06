/* global define describe beforeEach it spyOn expect xit */

define(function (require) {
    'use strict';
    var muer = require('muer');

    describe('muer', function() {
        beforeEach(function() {
        });

        it('initializes', function() {
            spyOn(muer, 'initialize');
            muer.initialize();
            expect(muer.initialize).toHaveBeenCalled();
        });

        xit('inits kudo', function() {
            spyOn(muer, 'initKudo');
            muer.initialize();
            expect(muer.initKudo).toHaveBeenCalled();
        });
    });
});
