use std::collections::HashMap;

#[path = "../types/types.rs"]
mod types;

use crate::types::VariableStruct;
use crate::types::VariableTypesEnum;

fn create_variable_struct(
    name: String,
    type_var: VariableTypesEnum,
    value: String,
) -> VariableStruct {
    return VariableStruct {
        name,
        type_var,
        value,
    };
}

pub fn var_analyze(name: String, value: String, variables: &mut HashMap<String, VariableStruct>) {
    let value_trim = value.trim();

    if value_trim.starts_with("\"") {
        let response = create_variable_struct(name.clone(), VariableTypesEnum::String, value);

        variables.insert(name.clone(), response);
    } else if value_trim == "false" || value_trim == "true" {
        let response = create_variable_struct(name.clone(), VariableTypesEnum::Boolean, value);
        variables.insert(name.clone(), response);

        return;
    } else if value_trim.parse::<f64>().is_ok() {
        let response = create_variable_struct(name.clone(), VariableTypesEnum::Number, value);
        variables.insert(name.clone(), response);

        return;
    } else {
        let key_name = &value.clone();

        let response = create_variable_struct(
            name.clone(),
            variables[key_name].type_var,
            variables[key_name].value.clone(),
        );

        variables.insert(name.clone(), response);

        return;
    }
}

mod test {
    use crate::{types::VariableTypesEnum, VariableStruct};
    use std::collections::HashMap;

    use crate::var_analyze::var_analyze;

    #[test]
    fn create_string_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();
        var_analyze(
            "name".to_string(),
            "\"Santana\"".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("name").is_some(), true);
        assert_eq!(variables.get("name").unwrap().name, "name");
        assert_eq!(variables.get("name").unwrap().value, "\"Santana\"",);
        assert_eq!(
            variables.get("name").unwrap().type_var,
            VariableTypesEnum::String
        );
    }

    #[test]
    fn create_number_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        var_analyze("age".to_string(), "26".to_string(), &mut variables);

        assert_eq!(variables.get("age").is_some(), true);
        assert_eq!(variables.get("age").unwrap().name, "age");
        assert_eq!(variables.get("age").unwrap().value, "26",);
        assert_eq!(
            variables.get("age").unwrap().type_var,
            VariableTypesEnum::Number
        );
    }

    #[test]
    fn create_boolean_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        var_analyze(
            "isCorrectly".to_string(),
            "true".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("isCorrectly").is_some(), true);
        assert_eq!(variables.get("isCorrectly").unwrap().name, "isCorrectly");
        assert_eq!(variables.get("isCorrectly").unwrap().value, "true",);
        assert_eq!(
            variables.get("isCorrectly").unwrap().type_var,
            VariableTypesEnum::Boolean
        );
    }

    #[test]
    fn create_reference_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        var_analyze(
            "name".to_string(),
            "\"Santana\"".to_string(),
            &mut variables,
        );

        var_analyze("clone_name".to_string(), "name".to_string(), &mut variables);

        assert_eq!(variables.get("clone_name").is_some(), true);
        assert_eq!(variables.get("clone_name").unwrap().name, "clone_name");
        assert_eq!(variables.get("clone_name").unwrap().value, "\"Santana\"",);
        assert_eq!(
            variables.get("clone_name").unwrap().type_var,
            VariableTypesEnum::String
        );
    }

    #[test]
    fn create_snake_case_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        var_analyze(
            "is_correctly".to_string(),
            "true".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("is_correctly").is_some(), true);
    }

    #[test]
    fn create_camel_case_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        var_analyze(
            "isCorrectly".to_string(),
            "true".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("isCorrectly").is_some(), true);
    }
}
