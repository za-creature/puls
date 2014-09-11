jQuery(function($)
{
    window.modal_confirm = function(title, body, trigger) {
        $("#confirm .modal-header h4").html(title);
        $("#confirm .modal-body").html(body);
        $("#confirm .btn-primary").click(trigger);
        $("#confirm").modal();
    };
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

    $(".combobox").each(function() {
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
                    keys.forEach(function(_, id) {
                        result.push({"text": keys[id],
                                     "id": values[id]})
                    });
                    cb(result);
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
});