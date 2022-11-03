use regex::Regex;
use std::collections::HashMap;

use self::discovery_value_from_unknown::discovery_value_from_unknown;

use super::{VariableStruct, VariableTypesEnum};

#[path = "./discovery_value_from_unknown.rs"]
mod discovery_value_from_unknown;

fn create_variable_struct(
    name: String,
    type_var: VariableTypesEnum,
    value: String,
) -> VariableStruct {
    let re3 = Regex::new(r"^[\w]{1,}$").unwrap().captures(&name);
    if re3.is_none() {
        panic!("'{}' is not valid variable", &name);
    }

    return VariableStruct {
        name,
        type_var,
        value,
    };
}

pub fn create_var(name: String, value: String, variables: &mut HashMap<String, VariableStruct>) {
    let var_processed = discovery_value_from_unknown(value, &variables);

    let response =
        create_variable_struct(name.clone(), var_processed.type_var, var_processed.value);

    variables.insert(name.clone(), response);
}

mod test {
    use super::*;

    #[test]
    fn create_string_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();
        create_var(
            "name".to_string(),
            "\"Santana\"".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("name").is_some(), true);
        assert_eq!(variables.get("name").unwrap().name, "name");
        assert_eq!(variables.get("name").unwrap().value, "Santana",);
        assert_eq!(
            variables.get("name").unwrap().type_var,
            VariableTypesEnum::String
        );
    }

    #[test]
    fn create_number_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        create_var("age".to_string(), "26".to_string(), &mut variables);

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

        create_var(
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

        create_var(
            "name".to_string(),
            "\"Santana\"".to_string(),
            &mut variables,
        );

        create_var("clone_name".to_string(), "name".to_string(), &mut variables);

        assert_eq!(variables.get("clone_name").is_some(), true);
        assert_eq!(variables.get("clone_name").unwrap().name, "clone_name");
        assert_eq!(variables.get("clone_name").unwrap().value, "Santana",);
        assert_eq!(
            variables.get("clone_name").unwrap().type_var,
            VariableTypesEnum::String
        );
    }

    #[test]
    fn create_snake_case_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        create_var(
            "is_correctly".to_string(),
            "true".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("is_correctly").is_some(), true);
    }

    #[test]
    fn create_camel_case_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        create_var(
            "isCorrectly".to_string(),
            "true".to_string(),
            &mut variables,
        );

        assert_eq!(variables.get("isCorrectly").is_some(), true);
    }

    #[test]
    #[should_panic(expected = "'invalid var' is not valid variable")]
    fn denny_create_invalid_var() {
        let mut variables: HashMap<String, VariableStruct> = HashMap::new();

        create_var(
            "invalid var".to_string(),
            "true".to_string(),
            &mut variables,
        )
    }
}
