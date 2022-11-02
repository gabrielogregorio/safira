use regex::Regex;
use std::collections::HashMap;
use std::fs;

use super::{VariableStruct, VariableTypesEnum};

pub struct DiscoveryStruct {
    pub value: String,
    pub type_var: VariableTypesEnum,
}

pub fn discovery_variable(
    content: String,
    variables: &HashMap<String, VariableStruct>,
) -> DiscoveryStruct {
    return discovery_variable_item(content, variables);
}

fn value_is_boolean(content: &String) -> bool {
    return content.trim() == "true" || content.trim() == "false";
}

fn value_is_numeric(content: &String) -> bool {
    return content.trim().parse::<f64>().is_ok();
}

fn value_is_only_string(content: &String) -> bool {
    return content.trim().starts_with("\"") && content.trim().ends_with("\"");
}

fn discovery_variable_item(
    content: String,
    variables: &HashMap<String, VariableStruct>,
) -> DiscoveryStruct {
    if value_is_boolean(&content) {
        return DiscoveryStruct {
            value: content.trim().to_string(),
            type_var: VariableTypesEnum::Boolean,
        };
    }

    if value_is_numeric(&content) {
        return DiscoveryStruct {
            value: content.trim().to_string(),
            type_var: VariableTypesEnum::Number,
        };
    }

    if value_is_only_string(&content) {
        return DiscoveryStruct {
            value: content.trim()[1..content.trim().len() - 1].to_string(),
            type_var: VariableTypesEnum::String,
        };
    }

    return DiscoveryStruct {
        value: variables[&content.to_string()].value.to_string(),
        type_var: variables[&content.to_string()].type_var,
    };
}

mod test {
    use super::*;

    #[test]
    fn return_string_value() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print = discovery_variable("\"abc\"".to_string(), &variables);

        assert_eq!(return_print.value, "abc");
        assert_eq!(return_print.type_var, VariableTypesEnum::String);
    }

    #[test]
    fn return_number_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print = discovery_variable("123".to_string(), &variables);

        assert_eq!(return_print.value, "123");
        assert_eq!(return_print.type_var, VariableTypesEnum::Number);
    }

    #[test]
    fn return_boolean_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print = discovery_variable("false".to_string(), &variables);

        assert_eq!(return_print.value, "false");
        assert_eq!(return_print.type_var, VariableTypesEnum::Boolean);
    }

    #[test]
    fn return_variable_value() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        variables.insert(
            "myVariable".to_string(),
            VariableStruct {
                name: "myVariable".to_string(),
                type_var: VariableTypesEnum::String,
                value: "aq123fbc".to_string(),
            },
        );

        let return_print = discovery_variable("myVariable".to_string(), &variables);

        assert_eq!(return_print.value, "aq123fbc");
        assert_eq!(return_print.type_var, VariableTypesEnum::String);
    }
}
