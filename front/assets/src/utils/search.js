// Make ajax search request and load results to table
export const search = (page=1) => {
    var table = $('#results');
    table.html('<div class="spinner-border" role="status"></div>');

    var query = $('#inputQuery').val();
    var period = $('#periodSelect').val();
    var campus = $('#campus').val();
    var formato = $('#formato').val();
    var escuela = $('#escuela').val();
    var tipos_mod = $('#tipos_modulo').val();
    var area = $('#area').val();
    var categoria = $('#categoria').val();
    var max_mod = $('#modulos').val();
    var creditos = $('#creditos').val();
    var requisitos = $('#requisitos').prop('checked');
    var tope = $('#tope_horario').prop('checked');
    var tope_excep = $('#tope_ayu').prop('checked');
    var free_quota = $('#quota').prop('checked');
    var horario = [];
    if (tope) {
        'LMWJVS'.split('').forEach(day => {
            '12345678'.split('').forEach(module => {
                if ($('#' + day + module).hasClass('table-secondary')) {
                    horario.push(day + module);
                }
            });
        });
        horario = horario.join(',');
    }

    var query_body = {
        q: query,
        period: period,
        campus: campus,
        format: formato,
        school: escuela,
        mod_types: tipos_mod,
        area: area,
        category: categoria,
        max_mod: max_mod,
        credits: creditos,
        without_req: requisitos,
        overlap: tope,
        overlap_except: tope_excep,
        schedule: horario,
        free_quota: free_quota,
        page: page
    }

    $.get('/p_search', query_body)
    .done(response => {
        if (response.error) {
            $('#resultsFoot').html('<tr><td>Error en la búsqueda</td></tr>');
            return false;
        }
        response = response.results;

        if (! response.length) {
            table.html('<tr><td colspan="5">No se encontaron resultados.</td></tr>');
            return false;
        }
        table.html('');

        response.forEach(result => {
            // Characteristics
            let row = '<tr class="border-top">';
            row += '<td><button class="btn p-0 m-1" onclick="wp.add(' + result.id + ')"><img src="/dist/images/add.svg" height="25"/></button>';
            row += '<button class="btn p-0 m-1" data-bs-toggle="modal" href="#quotaModal" onclick="wp.loadQuota(' + result.id + ')"><img src="/dist/images/chart.svg" height="25"/></button></td>';
            row += '<td><a class="badge bg-secondary" data-bs-toggle="modal" href="#infoModal" onclick="wp.loadInfo(' + result.id + ')">' + result.initials + '</a></td>';
            row += '<td>' + result.name + '</td>';
            row += '<td>' + result.teachers.replace(/,/g, '<br>') + '</td>';
            row += '<td>' + result.format + '</td>';
            row += '<td>' + result.available_quota + '</td>';

            // Schedule
            let horario = result.schedule.split('\n').slice(1);
            row += '<td>';
            horario.forEach(line => {
                line = line.substring(4);
                line = line.split('<>');
                row += '<b>' + line[1] + '</b>' + line[0] + '<br>';
            });
            row += '</td>';

            // Print
            row += '</tr>';
            table.append(row);
        });
        table.focus();

        var footer = $('#resultsFoot');
        footer.html('');
        if (page > 1) {
            footer.append('<button onclick="wp.search(' + (page - 1).toString() + ');" class="btn btn-outline-primary me-3"><< Anterior</button>')
        }
        if (response.length == 25) {
            footer.append('<button onclick="wp.search(' + (page + 1).toString() + ');" class="btn btn-outline-primary">Siguiente >></button>');
        }
    })
    .fail(error => {
        console.log(error);
        $('#resultsFoot').html('<tr><td>Error en la búsqueda</td></tr>');
    });

    // google analytics
    try {
        gtag('event', 'search', {
            'event_category': period,
            'event_label': query
        });
    } catch (error) {
        console.log('No analytics.');
    }
    return false;
};
