(function($) {

    $(document).ready(function() {
        gmaplocation.search_binder();
        gmaplocation.route_form_binder();
        gmaplocation.pick_location_binder();
        gmaplocation.set_zoom_binder();
        gmaplocation.location_form_binder();
    });
    
    // google maps related
    gmaplocation = {
        
        // default translation en
        i18n: {
            confirm_pick_location: 'Do you really want to set this Location?',
            confirm_change_zoom: 'Do you really want to set Zoom level?',
            UNKNOWN_ERROR: 'A geocoding request could not be processed due ' +
                           'to a server error. The request may succeed if ' +
                           'you try again.',
            REQUEST_DENIED: 'Request denied.',
            OVER_QUERY_LIMIT: 'The webpage has gone over the requests limit ' +
                              'in too short a period of time.',
            MAX_WAYPOINTS_EXCEEDED: '',
            INVALID_REQUEST: 'Invalid Request',
            NOT_FOUND: 'At least one of the origin, destination, or ' +
                       'waypoints could not be geocoded.',
            ZERO_RESULTS: 'No result was found.',
            ERROR: 'There was a problem contacting the Google servers.'
        },
        
        // current 'google.maps.Map' instance
        _map: null,
        
        // function to fetch current map. if inexistent, create
        map: function(options) {
            if (gmaplocation._map == null) {
                var map = new google.maps.Map($('#map_canvas').get(0), options);
                gmaplocation._map = map;
                gmaplocation.add_map_listener(map);
            }
            return gmaplocation._map;
        },
        
        // remove current 'google.maps.Map' instance
        // XXX: need to destroy?
        clear_map: function() {
            gmaplocation._map = null;
        },
        
        // map defaults
        defaults: {
            lat: null,
            lon: null,
            zoom: null,
            type: null,
            info: null,
            title: null,
            region: null,
            language: null
        },
        
        // set map defaults
        // XXX: do update instead of overwrite
        set_defaults: function(defaults) {
            gmaplocation.defaults = defaults;
        },
        
        // create map and show location. Definitions are taken from defaults
        show_location: function() {
            gmaplocation.clear_map();
            var defaults = gmaplocation.defaults;
            var latLon = new google.maps.LatLng(defaults.lat, defaults.lon);
            var options = {
                zoom: defaults.zoom,
                center: latLon,
                mapTypeId: defaults.type
            };
            var map = gmaplocation.map(options);
            var infowindow = new google.maps.InfoWindow({
                content: defaults.info
            });
            var marker = new google.maps.Marker({
                position: latLon, 
                map: map, 
                title: defaults.title
            });
            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(map, marker);
            });
        },
        
        // add pick location callback to map
        add_map_listener: function(map) {
            google.maps.event.addListener(
                map, 'click', gmaplocation.pick_location_callback);
        },
        
        // read picked location from maps api and store lat/lon on server
        pick_location_callback: function(event) {
            if (!gmaplocation._pick_selected) {
                return false;
            }
            var options = {
                message: gmaplocation.i18n.confirm_pick_location,
                event: event
            };
            bdajax.dialog(options, function(options) {
                var event = options.event;
                gmaplocation._pick_selected = false;
                var data = {
                    'lat': event.latLng.lat(),
                    'lon': event.latLng.lng()
                };
                var url = $('#gmaplocation_context').text() + '/@@set_location';
                $.getJSON(url, data, function(json) {
                    $('#pick_location_action').removeClass('selected');
                    switch(json.status) {
                        case 'ERROR':
                            bdajax.error(json.message);
                            break;
                        case 'SUCCESS':
                            var defaults = gmaplocation.defaults;
                            defaults.zoom = gmaplocation.map().getZoom();
                            defaults.lat = event.latLng.lat();
                            defaults.lon = event.latLng.lng();
                            $('input[name=gmaplocation_target_lat]')
                                .attr('value', defaults.lat);
                            $('input[name=gmaplocation_target_lon]')
                                .attr('value', defaults.lon);
                            gmaplocation.show_location();
                            bdajax.info(json.message);
                    }
                });
            });
        },
        
        // flag whether pick location action is selected
        _pick_selected: false,
        
        // bind pick location action
        pick_location_binder: function() {
            $('#pick_location_action').bind('click', function(event) {
                event.preventDefault();
                $('#pick_location_action').addClass('selected');
                gmaplocation._pick_selected = true;
                $(document).unbind('mousedown')
                           .bind('mousedown', function(event) {
                    if (!event) {
                        var event = window.event;
                    }
                    if (event.target) {
                        var target = event.target;
                    } else if (event.srcElement) {
                        var target = event.srcElement;
                    }   
                    if (!$(target).parents('#map_canvas').length) {
                        gmaplocation._pick_selected = false;
                        $('#pick_location_action').removeClass('selected');
                    };
                });
            });
        },
        
        // bins set zoom level action
        set_zoom_binder: function() {
            $('#set_zoom_action').bind('click', function(event) {
                event.preventDefault();
                $('#pick_location_action').removeClass('selected');
                gmaplocation._pick_selected = false;
                var options = {
                    message: gmaplocation.i18n.confirm_change_zoom
                };
                bdajax.dialog(options, function(options) {
                    $('#pick_location_action').removeClass('selected');
                    var zoom = gmaplocation.map().getZoom();
                    var data = {
                        'zoom': zoom
                    };
                    var url = $('#gmaplocation_context').text() + '/@@set_zoom';
                    $.getJSON(url, data, function(json) {
                        switch(json.status) {
                            case 'ERROR':
                                bdajax.error(json.message);
                                break;
                            case 'SUCCESS':
                                gmaplocation.defaults.zoom = zoom;
                                gmaplocation.show_location();
                                bdajax.info(json.message);
                        }
                    });
                });
            });
        },
        
        // perform route calculation and render result
        calculate_route: function(origin, destination) {
            var service = new google.maps.DirectionsService();
            var request = {
                origin: origin,
                destination: destination,
                travelMode: google.maps.DirectionsTravelMode.DRIVING,
                unitSystem: google.maps.DirectionsUnitSystem.METRIC,
                waypoints: [],
                optimizeWaypoints: false,
                provideRouteAlternatives: false,
                avoidHighways: false,
                avoidTolls: false,
                region: gmaplocation.defaults.region
            };
            service.route(request, function(result, status) {
                if (status == 'UNKNOWN_ERROR') {
                    bdajax.error(gmaplocation.i18n.UNKNOWN_ERROR);
                } else if (status == 'REQUEST_DENIED') {
                    bdajax.error(gmaplocation.i18n.REQUEST_DENIED);
                } else if (status == 'OVER_QUERY_LIMIT') {
                    bdajax.error(gmaplocation.i18n.OVER_QUERY_LIMIT);
                } else if (status == 'MAX_WAYPOINTS_EXCEEDED') {
                    bdajax.error(gmaplocation.i18n.MAX_WAYPOINTS_EXCEEDED);
                } else if (status == 'INVALID_REQUEST') {
                    bdajax.error(gmaplocation.i18n.INVALID_REQUEST);
                } else if (status == 'NOT_FOUND') {
                    bdajax.error(gmaplocation.i18n.NOT_FOUND);
                } else if (status == 'ZERO_RESULTS') {
                    bdajax.error(gmaplocation.i18n.ZERO_RESULTS);
                } else if (status == 'OK') {
                    gmaplocation.clear_map();
                    var options = {
                        mapTypeId: gmaplocation.defaults.type
                    };
                    var map = gmaplocation.map(options);
                    var renderer = new google.maps.DirectionsRenderer();
                    renderer.setMap(map);
                    var result_container = $('#route_result');
                    result_container.empty();
                    renderer.setPanel(result_container.get(0));
                    renderer.setDirections(result);
                    $('#route_result_heading').show();
                }
            });
        },
        
        // bind route calculation form
        route_form_binder: function() {
            $('#route_calculation').submit(function(event) {
                event.preventDefault();
                var form = $(this);
                var origin_elem = $('input[name=gmaplocation_origin]', form);
                var origin_lat = origin_elem.data('lat');
                var origin_lon = origin_elem.data('lon');
                if (!origin_lat || !origin_lon) {
                    // XXX: status message
                    return;
                }
                var origin = new google.maps.LatLng(origin_lat, origin_lon);
                var target_lat = $('input[name=gmaplocation_target_lat]',
                                   form).attr('value');
                var target_lon = $('input[name=gmaplocation_target_lon]',
                                   form).attr('value');
                if (!target_lat || !target_lon) {
                    // XXX: status message
                    return;
                }
                var target = new google.maps.LatLng(target_lat, target_lon);
                gmaplocation.calculate_route(origin, target);
            });
        },
        
        // bind location finder form
        location_form_binder: function() {
            $('#search_location_action').submit(function(event) {
                event.preventDefault();
                var form = $(this);
                var elem = $('input[name=gmaplocation_new_location]', form);
                var lat = elem.data('lat');
                var lon = elem.data('lon');
                if (!lat || !lon) {
                    // XXX: status message
                    return;
                }
                gmaplocation.clear_map();
                var defaults = gmaplocation.defaults;
                var latLon = new google.maps.LatLng(lat, lon);
                var options = {
                    zoom: defaults.zoom,
                    center: latLon,
                    mapTypeId: defaults.type
                };
                var map = gmaplocation.map(options);
            });
        },
        
        // bind search autocomplete widget to corresponding input fields
        search_binder: function() {
            $('input.gmaplocation_search').autocomplete({
                source: function(request, callback) {
                    var cb = callback;
                    var request = {
                        address: request.term,
                        language: gmaplocation.defaults.language,
                        region: gmaplocation.defaults.region
                    }
                    var geocoder = new google.maps.Geocoder();
                    geocoder.geocode(request, function(result, status) {
                        var data = new Array();
                        if (status == 'ERROR') {
                            bdajax.error(gmaplocation.i18n.ERROR);
                        } else if (status == 'INVALID_REQUEST') {
                            bdajax.error(gmaplocation.i18n.INVALID_REQUEST);
                        } else if (status == 'REQUEST_DENIED') {
                            bdajax.error(gmaplocation.i18n.REQUEST_DENIED);
                        } else if (status == 'UNKNOWN_ERROR') {
                            bdajax.error(gmaplocation.i18n.UNKNOWN_ERROR);
                        } else if (status == 'OVER_QUERY_LIMIT') {
                            bdajax.error(gmaplocation.i18n.OVER_QUERY_LIMIT);
                        } else if (status == 'ZERO_RESULTS') {
                        } else if (status == 'OK') {
                            $(result).each(function() {
                                var label = this.formatted_address;
                                var lat = this.geometry.location.lat();
                                var lon = this.geometry.location.lng();
                                var value = lat + ',' + lon;
                                var both = label + ' (' + value + ')';
                                data.push({
                                    'label': this.formatted_address,
                                    'value': value,
                                    'both': both,
                                    'lat': lat,
                                    'lon': lon
                                });
                            });
                        }
                        cb(data);
                        return false;
                    });
                },
                minLength: 3,
                select: function(event, ui) {
                    event.preventDefault();
                    var elem = $(this);
                    elem.attr('value', ui.item.label);
                    elem.data('lat', ui.item.lat);
                    elem.data('lon', ui.item.lon);
                    return false;
                },
                focus: function(event, ui) {
                    event.preventDefault();var elem = $(this);
                    elem = $(this);
                    elem.attr('value', ui.item.label);
                    return false;
                }
            });
        }
    }

})(jQuery);