function bool(value) {
    if(typeof(value) == "object") {
        for(var property in value)
            if(value.hasOwnProperty(property))
                return true;
        return false;
    }
    else if(value instanceof Date)
        return true;
    else
        return !!value;
}


function ValidationError(message) {
    this.name = "ValidationError";
    this.message = message;
}
ValidationError.prototype = new Error;


function StopValidation(message) {
    this.name = "StopValidation";
    this.message = message;
}
StopValidation.prototype = new Error;


var validators = {
    AnyOf: function(values, message) {
        return function(form, field) {
            if(values.indexOf(field.data) == -1)
                throw new ValidationError(message)
        }
    },

    DataRequired: function(message) {
        return function(form, field) {
            if(
                    !bool(field.data) || (
                        typeof(field.data) == "string" &&
                        !bool(field.data.trim())
                    )
            )
                throw new StopValidation(message)
        }
    },

    EqualTo: function(field_name, message, invalid_field_message) {
        return function(form, field) {
            var other = form[field_name]
            if(typeof(other) == "undefined")
                throw new ValidationError(invalid_field_message)
            if(field.data != other.data)
                throw new ValidationError(message)
        }
    },

    FileAllowed: function() {
        // pass for now (flask_wtf extension)
    },

    FileRequired: function() {
        // pass for now (flask_wtf extension)
    },

    IPAddress: function(use_ipv4, use_ipv6, message) {
        var // going to hell for this
            ipv4 = /^\s*((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\s*$/,
            ipv6 = /^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$/;

        return function(form, field) {
            var data = bool(field.data)? field.data: "",
                valid = (use_ipv4 && field.data.match(ipv4)) ||
                        (use_ipv6 && field.data.match(ipv6));
            if(!valid)
                throw new ValidationError(message);
        }
    },

    InputRequired: function(message) {
        return function(form, field) {
            if(!bool(field.raw_data) || !bool(field.raw_data[0]))
                throw new StopValidation(message);
        }
    },

    Length: function(min, max, message) {
        if(min == -1 && max == -1)
            throw new Error("At least one of `min` or `max` must be specified.");
        if(max != -1 && min > max)
            throw new Error("`min` cannot be more than `max`.");

        return function(form, field) {
            var l = bool(field.data)? field.data.length: 0;
            if(l < min || (max != -1 && l > max))
                throw new ValidationError(message);
        }
    },

    NoneOf: function(values, message) {
        return function(form, field) {
            if(values.indexOf(field.data) != -1)
                throw new ValidationError(message)
        }
    },

    NumberRange: function(min, max, message) {
        if(min === null && max === null)
            throw new Error("At least one of `min` or `max` must be specified.");
        if(max !== null && min !== null && min > max)
            throw new Error("`min` cannot be more than `max`.");

        return function(form, field) {
            if(
                    data === null ||
                    (min !== null && field.data < min) ||
                    (max !== null && field.data > max)
            )
                throw new ValidationError(message);
        }
    },

    Optional: function(strip_whitespace) {
        function string_check(s) {
            if(strip_whitespace)
                return s.trim();
            return s;
        }

        return function(form, field) {
            if(
                    !bool(field.raw_data) || (
                        typeof(field.raw_data[0]) == "string" &&
                        !bool(string_check(field.raw_data[0]))
                    )
            )
                throw new StopValidation();
        }
    },

    Regexp: function(regex, flags, message) {
        var pattern = new RegExp(regex, flags);

        return function(form, field) {
            var data = bool(field.data)? field.data: "";
            if(!data.match(pattern))
                throw new ValidationError(message);
        }
    },
};

validators.Required = validators.InputRequired;

validator.Email = function(message) {
    return validators.Regex("^.+@[^.].*\\.[a-z]{2,10}$", "i", message);
}

validators.MacAddress = function(message) {
    return validators.Regex("^(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$", "",
                            message);
} 

validators.URL = function(require_tld, message) {
    var regex = "^[a-z]+://([^/:]+|([0-9]{1,3}\\.){3}[0-9]{1,3})(:[0-9]+)?(\\/.*)?$";
    if(require_tld)
        regex = "^[a-z]+://([^/:]+\\.[a-z]{2,10}|([0-9]{1,3}\\.){3}[0-9]{1,3})(:[0-9]+)?(\\/.*)?$";

    return validators.Regex(regex, "i", message);
}

validators.UUID = function(message) {
    return validators.Regex("^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$",
                            "", message);
}


function Form(fields, prefix) {
    var self = this;

    self._prefix = prefix;
    self._errors = null;
    self._fields = [];
    self._fields_map = {};

    fields.forEach(function(entry) {
        var name = entry[0],
            unbound_field = entry[1];
        field = unbound_field.bind(self, name, prefix);
        self._fields.push(name);
        self._fields_map[name] = field;
    });

    self.process = function() {
        self._fields.forEach(function(name) {
            var field = self._fields_map[name];
            field.process();
        });
    }

    self.validate = function(extra_validators) {
        self._errors = null;
        success = true;
        self._fields.forEach(function(name) {
            var field = self._fields_map[name],
                extra = null;
            if(
                    typeof(extra_validators) == "object" &&
                    typeof(extra_validators[name]) == "function"
            )
                extra = extra_validators[name];

            if(!bool(field.validate(self, extra)))
                success = false;
        });
        return success;
    }
}


function coerce(value, type, message) {
    if(type == "int") {
        var pattern = /^[\+\-]?\d+$/,
            converter = parseInt;
    }
    else if(type == "float") {
        var pattern = /^[\-\+]?[0-9]*\.?[0-9]+([eE][\-\+]?[0-9]+)?$/,
            converter = parseFloat;
    }
    else
        throw new ValidationError("Only `int` and `float` values may be coerced.");

    if(!value.match(pattern))
        throw new ValidationError(message);
    return converter(value);
}


var fields = {
    BooleanField: function(false_values) {
        return function(field) {
            var widget = document.getElementById(field.id);

            if(widget.checked) {
                field.raw_data = [widget.value];
                field.data = false_values.indexOf(widget.value) == -1;
            }
            else {
                field.raw_data = [];
                field.data = false;
            }
        }
    },
    DateField: function(format, message) {
        var pattern = new RegExp(format, "");
        return function(field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];

            if(!widget.value.match(pattern))
                throw new ValidationError(message);

            field.data = new Date(widget.value);
        }
    },
    FieldList: function() {

    },
    FileField: function() {

    },
    FloatField: function(message) {
        return function(field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = coerce(widget.value, "float", message);
        }
    },
    FormField: function() {

    },
    IntegerField: function(message) {
        return function(field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = coerce(widget.value, "int", message);
        }
    },
    RadioField: function() {
        
    },
    SelectField: function(coerce, message) {
        return function(field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = coerce(widget.value, coerce, message);
        }
    },
    SelectMultipleField: function(coerce, message) {
        return function(field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [];
            field.data = [];
            widget.options.forEach(function(option) {
                if(option.selected) {
                    field.raw_data.push(option.value);
                    field.data.push(coerce(option.value, coerce, message));
                }
            });
        }
    },
    StringField: function() {
        return function(field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = widget.value;
        }
    },
}

fields.DateTimeField = fields.DateField;

fields.DateTimeLocalField = fields.DateField;

fields.DecimalField = fields.FloatField;

fields.DecimalRangeField = fields.DecimalField;

fields.EmailField = fields.StringField;

fields.HiddenField = fields.StringField;

fields.IntegerRangeField = fields.IntegerField;

fields.PasswordField = fields.StringField;

fields.SearchField = fields.StringField;

fields.SubmitField = fields.StringField;

fields.TelField = fields.StringField;

fields.TextField = fields.StringField;

fields.TextAreaField = fields.StringField;

fields.URLField = fields.StringField;


function Field(type, validators, id) {
    var self = this;

    self.type = type;
    self.raw_data = null;
    self.data = null;
    self.validators = validators;

    self.bind = function() {
    }

    self.process = function() {

    }

    self.validate = function(form, extra_validators) {

    }
}