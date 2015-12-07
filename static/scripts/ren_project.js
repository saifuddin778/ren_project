$(document).ready(function(){
	console.log('i am ready to go');
	activate_clicks();
});


function get_ranges(min_, max_){
    var colors_palette = d3.scale.category20c();
    var all_ = [{'from': min_, 'color': colors_palette(1-min_)}];
    var k = 0;
    var delta = max_-min_;
    var steps = 8;
    var b = Math.round( delta/steps * 100) / 100; //javascript rounding is weird..mult and div by 100..else its just delta/steps.
    while (k < delta){
        k += b;
        if ((min_+k) < max_){
            all_.push({'from': min_+k, 'color': colors_palette(1-(min_+k))});
        }
    }
    return all_;
}


function activate_clicks (){
    $('.block').unbind('click').bind('click', function(){
        var block_id = this.id;
        $(this).parent().fadeOut(500, function(){
            var tool_id = block_id+'_tool';
            $('#'+tool_id).show();
            activate_functions(tool_id);
        });
    });
}


function activate_functions(tool_id){
    console.log(tool_id);
    var functions_mapper = {heatmap_tool: {
            heatmap_tool_pv_panel_select: function (){
                $('#heatmap_tool_pv_panel_select').multipleSelect({single: true});
            },
            heatmap_tool_year_window_select: function(){
                $('#heatmap_tool_year_window_select').multipleSelect({single: true});
            },
            heatmap_tool_month_select: function(){
                $('#heatmap_tool_month_select').multipleSelect({single: true});
            },
            heatmap_tool_submit: function(){
                $('#heatmap_tool_submit').unbind('click').bind('click', function(){
                    var pv_panel_selected = $('#heatmap_tool_pv_panel_select').multipleSelect('getSelects')[0];
                    var year_window_selected = $('#heatmap_tool_year_window_select').multipleSelect('getSelects')[0];
                    var month_selected = parseInt($('#heatmap_tool_month_select').multipleSelect('getSelects')[0]);
                    console.log('heatmap_selection', pv_panel_selected, year_window_selected, month_selected);
                    var obj_ = {
                            type_: 'heatmap', 
                            pv_panel_selected: pv_panel_selected,
                            year_window_selected: year_window_selected,
                            month_selected: month_selected
                            };
                    get_data(obj_);
                });
            }
        },
        timeseries_tool: {
            timeseries_tool_pv_panel_select: function (){
                $('#timeseries_tool_pv_panel_select').multipleSelect({single: true});
            },
            timeseries_tool_year_window_select: function(){
                $('#timeseries_tool_year_window_select').multipleSelect({single: true});
            },
            timeseries_tool_location_select: function(){
                $('#timeseries_tool_location_select').multipleSelect({single: true});
            }, 
            timeseries_tool_submit: function(){
                $('#timeseries_tool_submit').unbind('click').bind('click', function(){
                    var pv_panel_selected = $('#timeseries_tool_pv_panel_select').multipleSelect('getSelects')[0];
                    var year_window_selected = $('#timeseries_tool_year_window_select').multipleSelect('getSelects')[0];
                    var location_selected = $('#timeseries_tool_location_select').multipleSelect('getSelects')[0];
                    console.log('timeseries_selection', pv_panel_selected, year_window_selected);
                    var obj_ = {
                            type_: 'timeseries', 
                            pv_panel_selected: pv_panel_selected,
                            year_window_selected: year_window_selected,
                            location_selected: location_selected,
                            };
                    get_data(obj_);
                });
            }
        }
    }

    for (each_func in functions_mapper[tool_id]){
        functions_mapper[tool_id][each_func]();
    }
}


function get_data(object_){
    var action_mapper = {
                        heatmap: {route: '/get_heatmap_data/', callback: plot_heatmap },
                        timeseries: {route: '/get_timeseries_data/', callback: plot_timeseries},
                        };

    console.log(object_, action_mapper[object_.type_]);
    var key_ = object_.type_.split('_')[0];

    $('#'+key_+'_containers').hide();
    $('.'+key_+'_plot').empty();
    $('.'+key_+'_button').css('background-color', '#2574A9');

    $.ajax({url: action_mapper[object_.type_].route,
            type:'GET',
            data: object_,
            success: function(resp){
                resp = JSON.parse(resp);
                //console.log(resp);
                action_mapper[object_.type_].callback(resp);
            }
    });
}

function plot_timeseries(data){
    console.log('timeseries data here', data);

    $('#timeseries_containers').show();

    $('.timeseries_button').unbind('click').bind('click', function(){
        var button_id = this.id;
        var variable_ = button_id.split('_')[0];
        var plot_id = variable_+'_plot_ts';

        console.log(button_id);
        $('.timeseries_button').css('background-color', '#2574A9');
        $('#'+button_id).css('background-color', 'darkseagreen');
        $('.timeseries_plot').hide();
        $('#'+plot_id).show();
        main_ts(data, plot_id, variable_);
    });
}


function plot_heatmap(data){
    console.log(data, 'data is here');
    
    $('#heatmap_containers').show();
    $('.heatmap_button').unbind('click').bind('click', function(){
        var variable_;
        var min_ = Number.POSITIVE_INFINITY;
        var max_ = Number.NEGATIVE_INFINITY;

        var button_id = this.id;
        variable_ = button_id.split('_')[0];
        var plot_id = variable_+'_plot_hm';
        $('.heatmap_button').css('background-color', '#2574A9');
        $('#'+button_id).css('background-color', 'darkseagreen');
        $('.heatmap_plot').hide();
        $('#'+plot_id).show();

        var plot_data = [];
        for (var i=0; i<data.length; i++){
            var k = data[i];
            var var_val =  k[variable_];
            k['value'] = var_val
            if (var_val > max_){
                max_ = var_val;
            }
            if (var_val < min_){
                min_ = var_val;
            }

            plot_data.push(k);
        }

        ranges = get_ranges(min_, max_);
        console.log(ranges, min_, max_);
        main_hm(plot_data, plot_id, ranges);
    });
    
}


function main_ts(data, plot_id, key_){
    console.log(data, plot_id, key_);
    console.log(data[0][key_]);
    $('#'+plot_id).empty();
    $('#'+plot_id).highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'Monthly Average Temperature'
        },
        subtitle: {
            text: 'Source: WorldClimate.com'
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: 'London',
            data: data[0][key_]//[3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
        }]
    });


    console.log(data, plot_id, key_, 'yes');
}


function main_hm(data, plot_id, ranges){
    console.log(data, plot_id, ranges);
    console.log('helpless');
    var naming_map = {
        'voc': {name: 'Voc', title: 'Open Circuit Voltage (Voc)', legend: 'Voc'},
        'isc': {name: 'Isc', title: 'Short Circuit Current (Isc)', legend: 'Isc'},
        'pmax': {name: 'Pmax', title: 'Power Max (Voc) - W', legend: 'Pmax'},
        'solarradiation': {name: 'SRad', title: 'Solar Radiation - ', legend: 'SRad'},
        'airtemperature': {name: 'AirTemp', title: 'Air Temperature - ', legend: 'AirTemp'},
    };

    var ident = plot_id.split('_')[0];

    var countiesMap = Highcharts.geojson(Highcharts.maps['countries/us/us-all-all']),
        lines = Highcharts.geojson(Highcharts.maps['countries/us/us-all-all'], 'mapline'),
        options;

    // Add state acronym for tooltip
    Highcharts.each(countiesMap, function (mapPoint) {
        mapPoint.name = mapPoint.name + ', ' + mapPoint.properties['hc-key'].substr(3, 2);
    });

    console.log(countiesMap);

    options = {
        chart: {
            borderWidth: 0,
            marginRight: 50, // for the legend
        },
        credits: {enabled: false},
        title: {
            text: naming_map[ident].title
        },

        legend: {
            title: {
                text: naming_map[ident].name,
                style: {
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'black'
                }
            },
            layout: 'vertical',
            align: 'right',
            floating: true,
            valueDecimals: 2,
            valueSuffix: '',
            symbolRadius: 0,
            symbolHeight: 14
        },

        mapNavigation: {
            enabled: true
        },

        colorAxis: {
            dataClasses: ranges
        },

        plotOptions: {
            mapline: {
                showInLegend: false,
                enableMouseTracking: false
            }
        },

        series: [{
            mapData: countiesMap,
            data: data,
            joinBy: ['hc-key', 'code'],
            name: naming_map[ident].name,
            tooltip: {
                valueSuffix: ''
            },
            borderWidth: 0.5,
            states: {
                hover: {
                    color: '#bada55'
                }
            }
        }, {
            type: 'mapline',
            name: 'State borders',
            data: [lines[0]],
            color: 'white'
        }, {
            type: 'mapline',
            name: 'Separator',
            data: [lines[1]],
            color: 'gray'
        }]
    };

    // Instanciate the map
    //$('#container').highcharts('Map', options);
    console.log('#'+plot_id);
    $('#'+plot_id).empty();
    $('#'+plot_id).highcharts('Map', options);
}
