odoo.define('das.GanttControllerFictional', function (require) {
    "use strict";

/**
 * This file inherit planning.PlanningGanttController to add button fictional
 */


    var FictionalGanttController = require('web_gantt.GanttController');
    var core = require('web.core');


    var QWeb = core.qweb;

    var NewPlanningGanttController = FictionalGanttController.include({
        events: _.extend({}, FictionalGanttController.prototype.events, {
        'click .o_gantt_button_fictional': '_onAddFicClick'
    }),
    _onAddFicClick: function() {
        var action = {
            type: 'ir.actions.act_window',
            name: 'Generate Planning',
            res_model: 'planning.fictional.wizard',
            views: [[false, 'form']],
            target: 'new',

        }
        this.do_action(action)
    }
    });

    return NewPlanningGanttController;

});
