use regex::{Captures, Regex};
use std::collections::HashMap;

use self::discovery_variable::discovery_variable;
use super::{VariableStruct, VariableTypesEnum};

#[path = "./discovery_variable.rs"]
mod discovery_variable;

fn process_print_content(content: String, variables: &HashMap<String, VariableStruct>) -> String {
    let stringContainsInsertCommand: bool =
        content.trim().starts_with("\"") && content.trim().ends_with("\"") == false;
    if stringContainsInsertCommand {
        let cap2: Option<Captures> = Regex::new(r#"^"(.*?)"\s*([,]{1,}\s*)(.*)$"#)
            .unwrap()
            .captures(&content);
        if cap2.is_some() {
            let items = cap2.unwrap();
            let mut string_complete: String = items[1].to_string();

            let params = &items[3].to_string();

            let list_items = params.split(", ");

            for (_, param) in list_items.enumerate() {
                string_complete = string_complete.replacen(
                    "%",
                    &discovery_variable(
                        param.to_string().clone().to_string().to_string(),
                        &variables,
                    )
                    .value,
                    1,
                );
            }

            return string_complete;
        }
        panic!("Error on process string");
    } else {
        return discovery_variable(content, variables).value;
    }
}

pub fn print_content(content: String, variables: &HashMap<String, VariableStruct>) {
    println!("-> {}", process_print_content(content, variables));
}

mod test {
    use super::*;

    #[test]
    fn return_string_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("\"abc\"".to_string(), &variables);

        assert_eq!(return_print, "abc");
    }

    #[test]
    fn return_boolean_true_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("true".to_string(), &variables);

        assert_eq!(return_print, "true");
    }

    #[test]
    fn return_boolean_false_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("false".to_string(), &variables);

        assert_eq!(return_print, "false");
    }

    #[test]
    fn return_numeric_int_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("123".to_string(), &variables);

        assert_eq!(return_print, "123");
    }

    #[test]
    fn return_numeric_float_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("123.15".to_string(), &variables);

        assert_eq!(return_print, "123.15");
    }

    #[test]
    fn return_numeric_float_negative_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("-123.15".to_string(), &variables);

        assert_eq!(return_print, "-123.15");
    }

    #[test]
    fn return_numeric_float_positive_value() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content("+123.15".to_string(), &variables);

        assert_eq!(return_print, "+123.15");
    }

    #[test]
    fn insert_int_inside_string() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String =
            process_print_content("\"my value is %\", 123".to_string(), &variables);

        assert_eq!(return_print, "my value is 123");
    }
}
