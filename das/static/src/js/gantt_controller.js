odoo.define('das.GanttController', function (require) {
"use strict";

/**
 * This file inherit web_gantt.GanttController to delete default date_start and date_stop on gantt view
 */

var GanttController = require('web_gantt.GanttController');

GanttController.include({
    /**
     * @private
     * @param {MouseEvent} ev
     */
    _onAddClicked: function (ev) {
        ev.preventDefault();
        var context = {};
        var state = this.model.get();
        // Comment this line to unable default date_start and date_stop
        // context[state.dateStartField] = this.model.convertToServerTime(state.focusDate.clone().startOf(state.scale));
        // context[state.dateStopField] = this.model.convertToServerTime(state.focusDate.clone().endOf(state.scale));
        for (var k in context) {
            context[_.str.sprintf('default_%s', k)] = context[k];
        }
        this._onCreate(context);
    }
});

return GanttController;

});
