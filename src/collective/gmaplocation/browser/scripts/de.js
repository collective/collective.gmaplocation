(function($) {

    $(document).ready(function() {
        // german javascript messages translation.
        // XXX: do update instead of overwrite
        gmaplocation.i18n = {
            confirm_pick_location: 'Wollen Sie den Ort überschreiben?',
            confirm_change_zoom: 'Wollen Sie den Zoom Faktor überschreiben?',
            UNKNOWN_ERROR: 'Eine Geocodierungsanfrage konnte aufgrund eines ' +
                           'Serverfehlers nicht verarbeitet werden. Die ' +
                           'Anfrage ist möglicherweise erfolgreich, wenn Sie ' +
                           'es erneut versuchen.',
            REQUEST_DENIED: 'Anfrage abgewiesen.',
            OVER_QUERY_LIMIT: 'Die Anfragebeschränkungen wurden von der ' +
                              'Webseite in einem zu geringen Zeitraum ' +
                              'überschritten.',
            MAX_WAYPOINTS_EXCEEDED: '',
            INVALID_REQUEST: 'Ungültige Anfrage',
            NOT_FOUND: 'Mindestens einer der Orte (Ursprungsort, Zielort ' +
                       'oder Wegpunkte) konnte nicht geocodiert werden.',
            ZERO_RESULTS: 'Es wurde kein Ergebnis gefunden',
            ERROR: 'Beim Aufbau der Verbindung zu den Google-Servern ist ' +
                   'ein Problem aufgetreten.'
        };
    });

})(jQuery);