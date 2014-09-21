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


function coerce(value, type, message) {
    if(type == "int") {
        var pattern = /^[\+\-]?\d+$/,
            converter = parseInt;
    }
    else if(type == "float") {
        var pattern = /^[\-\+]?[0-9]*\.?[0-9]+([eE][\-\+]?[0-9]+)?$/,
            converter = parseFloat;
    }
    else {
        // Only `int` and `float` values may be coerced.
        return value;
    }

    if(!value.match(pattern))
        throw new ValidationError(message);
    return converter(value);
}


function ValidationWarning(message) {
    this.name = "ValidationWarning";
    this.message = message;
}
ValidationWarning.prototype = new Error;


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
            var other = form._fields_map[field_name]
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
            throw new Error("At least one of `min` or `max` " +
                            "must be specified.");
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
            throw new Error("At least one of `min` or `max` " +
                            "must be specified.");
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
    var regex = "^[a-z]+://([^/:]+|([0-9]{1,3}\\.){3}" +
                "[0-9]{1,3})(:[0-9]+)?(\\/.*)?$";
    if(require_tld)
        regex = "^[a-z]+://([^/:]+\\.[a-z]{2,10}|([0-9]{1,3}\\.){3}" +
                "[0-9]{1,3})(:[0-9]+)?(\\/.*)?$";

    return validators.Regex(regex, "i", message);
}

validators.UUID = function(message) {
    return validators.Regex("^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$",
                            "", message);
}


function Form(fields, prefix) {
    var self = this;
    self.state = "ok";
    self.messages = {};

    self._prefix = prefix;
    self._fields = [];
    self._fields_map = {};

    fields.forEach(function(entry) {
        var name = entry[0],
            unbound_field = entry[1];
        field = unbound_field.bind(self, name);
        self._fields.push(name);
        self._fields_map[name] = field;
    });

    self.validate = function(extra_validators) {
        self.messages = {};
        self.state = "ok";

        self._fields.forEach(function(name) {
            var field = self._fields_map[name],
                extra = [];
            if(
                    // extra_validators must be a dictionary but ...
                    typeof(extra_validators) == "object" && (
                        // ... values must either be functions ...
                        typeof(extra_validators[name]) == "function" || (
                            // ... or non-empty lists
                            typeof(extra_validators[name]) == "object" &&
                            extra_validators[name].length
                        )
                    )
            ) {
                // however field.validate always expects a list of callables
                if(typeof(extra_validators[name]) == "function")
                    extra = [extra_validators[name]];
                else
                    extra = extra_validators[name];
            }

            field.validate(self, extra);
            if(field.messages.length) {
                // either `error` or `warning`; update state unless the current
                // form state is already `error`.
                self.messages[name] = field.messages;
                if(self.state != "error")
                    self.state = field.state;
            }
        });
        return self.state != "error";
    }
}


var fields = {
    BooleanField: function(false_values) {
        return function(form, field) {
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
        return function(form, field) {
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
        return function(form, field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = coerce(widget.value, "float", message);
        }
    },
    FormField: function() {

    },
    IntegerField: function(message) {
        return function(form, field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = coerce(widget.value, "int", message);
        }
    },
    RadioField: function() {
        
    },
    SelectField: function(coerce_mode, message) {
        return function(form, field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [widget.value];
            field.data = coerce(widget.value, coerce_mode, message);
        }
    },
    SelectMultipleField: function(coerce_mode, message) {
        return function(form, field) {
            var widget = document.getElementById(field.id);
            field.raw_data = [];
            field.data = [];
            widget.options.forEach(function(option) {
                if(option.selected) {
                    field.raw_data.push(option.value);
                    field.data.push(coerce(option.value, coerce_mode, message));
                }
            });
        }
    },
    StringField: function() {
        return function(form, field) {
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


function Field(type, args, validators_, id) {
    var self = this;

    self.id = id;
    self.type = type;
    self.messages = [];
    self.state = "ok";

    self.raw_data = null;
    self.data = null;

    self.validators = [fields[type].call(args)];
    validators_.forEach(function(spec) {
        self.validators.push(validators[spec[0]].call(spec.slice(1)));
    });

    self.validate = function(form, extra_validators) {
        self.messages = [];
        self.state = "ok"

        try {
            validators.concat(extra_validators).forEach(function(validator) {
                try {
                    validator(form, self);
                }
                catch(e) {
                    if(e instanceof ValidationWarning) {
                        // on warning, switch state only if the current state
                        // was not error 
                        if(self.state != "error") {
                            self.messages.push(e.message);
                            self.state = "warning";
                        }
                    }
                    else if(e instanceof ValidationError) {
                        // on error, clear any warning messages and switch
                        // state to error
                        if(self.state == "warning")
                            self.messages = [];
                        self.messages.push(e.message);
                        self.state = "error";
                    }
                    else if(e instanceof StopValidation) {
                        // on stop validation, clear any previous messages,
                        // switch state to error and stop validation chain
                        self.messages = [e.message];
                        self.state = "error";
                        throw e;
                    }
                    else throw e;
                }
            });
        }
        catch(e) {
            if(!(e instanceof StopValidation))
                throw e;
        }
    }
}
