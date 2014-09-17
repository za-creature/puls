jQuery(function($)
{
    window.modal_confirm = function(title, body, trigger) {
        $("#confirm .modal-header h4").html(title);
        $("#confirm .modal-body").html(body);
        $("#confirm .btn-primary").click(trigger);
        $("#confirm").modal();
    };

    function registerConfirmationDialogs($selector) {
        $(".confirm").each(function() {
            var $this = $(this);
            $this.click(function(e) {
                window.modal_confirm($this.attr("data-title"),
                                     $this.attr("data-content"),
                                     function() {
                                         window.location.href = $this.attr("href");
                                     });
                e.preventDefault();
                return false;
            });
        });
    }

    function registerPhotoWidgets($selector) {
        $(".photo-widget").each(function() {
            var $this = $(this),
                $photo = $("img", $this);

            if($photo.length) {
                var $icon = $("<i/>").addClass("glyphicon-pro")
                                     .addClass("glyphicon-pro-remove"),
                    $input = $("input[type=file]", $this),
                    $button = $("<span/>").addClass("text-danger")
                                          .append($icon)
                                          .appendTo($this);
                $input.hide();
                $button.on("click", function() {
                    $input.show(),
                    $("input[type=hidden]", $this).remove(),
                    $button.remove();
                    $photo.remove();
                });
            }
        });
    }    

    function registerComboboxes($selector) {
        $(".combobox", $selector).each(function() {
            var $this = $(this);
            if($this.is("[data-url]"))
                $this.select2({
                    minimumInputLength: 0,
                    multiple: $this.is("[data-multiple]"),
                    initSelection: function($el, cb) {
                        var multiple = $this.is("[data-multiple]"),
                            keys = $el.attr("data-caption").split(","),
                            values = $el.val().split(","),
                            result = [];
                        values.forEach(function(value, index) {
                            result.push({"text": keys[index],
                                         "id": value})
                        });
                        if(multiple)
                            cb(result);
                        else
                            cb(result[0]);
                    },
                    ajax: {
                        url: $this.attr("data-url"),
                        dataType: 'json',
                        type: "GET",
                        quietMillis: 200,
                        data: function(term) { return {term: term}; },
                        results: function(data) { return data; }
                    }
                });
            else {
                $this.select2();
            }
        });
    };

    function registerDropdowns($selector) {
        $(".btn-dropdown", $selector).each(function() {
            var $this = $(this),
                $input = $("input", $this),
                $caption = $(".caption", $this),
                $options = $(".dropdown-menu li", $this),
                defaultValue = $input.val();

            $("a", $options).on("click", function(e) {
                var $elem = $(this),
                    value = $elem.attr("data-value"),
                    caption = $elem.text();

                $options.removeClass("active");
                $elem.parent().addClass("active");
                $input.val(value);
                $caption.text(caption);

                e.preventDefault();
            }).each(function() {
                var $elem = $(this);
                if($elem.attr("data-value") == defaultValue)
                    $elem.trigger("click");
            });
        });
    }

    function registerAll($selector) {
        registerConfirmationDialogs($selector);
        registerPhotoWidgets($selector);
        registerComboboxes($selector);
        registerDropdowns($selector);
    }

    // register templates (global)
    $(".template[data-cloned-by]").each(function() {
        var $template = $(this),
            $position = $template.next();

        $($template.attr("data-cloned-by")).on("click", function(e) {
            registerAll($template.clone().insertBefore($position));
            e.preventDefault();
        });
        $template.remove();
    });

    $("body").on("click", ".btn-delete", function(e) {
        $(this).parents(".template").remove();
        e.preventDefault();
    });

    $(window).on("resize", function() {
        $(".embed-frame").height($(window).height());
    }).trigger("resize");

    registerAll($("body"));
});