// CSS
import './css/entry';

// Dependencies
import 'bootstrap';
import 'multiple-select';

// Public functions
import {toggle, toggleRow, toggleDay, clearSelects} from './filters';
import {save, unsave, viewSaved, edit, share} from './save';
import {add, remove, loadRamo, loadFromCookie} from './schedule';
import {loadInfo} from './info';
import {search} from './search';
import {loadQuota} from './quota';

export {
    toggle, toggleRow, toggleDay, clearSelects,
    save, unsave, viewSaved, edit, share,
    add, remove, loadRamo, loadFromCookie,
    loadInfo,
    search,
    loadQuota,
};


// Automatic execution
$(() => {
    // Menu highlight
    $('a[name="menu_planner"]').addClass('active');

    // Load ramos from cookie
    wp.loadFromCookie();

    // Load filters dropdowns
    $('#campus').multipleSelect({
        selectAll: false,
        showClear: true
    });
    $('#formato').multipleSelect({
        selectAll: false,
        showClear: true
    });
    $('#escuela').multipleSelect({
        selectAll: false,
        filter: true,
        showClear: true
    });
    $('#tipos_modulo').multipleSelect({
        selectAll: false,
        showClear: true
    });
    $('#categoria').multipleSelect({
        selectAll: false,
        showClear: true
    });
    $('#area').multipleSelect({
        selectAll: false,
        showClear: true
    });
});