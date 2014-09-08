jQuery(function($) {
    $(".photo-list").sortable({
        "revert": true,
        "items": "> .photo",
        "helper": "clone",
        "forcePlaceholderSize": true,
        "cancel": "a.remove"
    }).disableSelection();
});
