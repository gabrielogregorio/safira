use regex::{Captures, Regex};
use std::collections::HashMap;

use super::{process::discovery_value_from_unknown, VariableStruct};

const INSERT_OPERATOR_STRING: &str = "{}";
const SEPARATOR_PARAMS_OPERATOR: &str = ", ";

fn is_string_and_has_params(content: String) -> bool {
    let content_local = content.trim();
    let re_detect_string_with_params: Option<Captures> = Regex::new(r#"^(".{1,}?")"#)
        .unwrap()
        .captures(content_local);

    if re_detect_string_with_params.is_some() {
        let string_contains_params =
            re_detect_string_with_params.unwrap()[1].to_string().len() != content_local.len();
        return string_contains_params;
    }
    return false;
}

fn extract_params_and_insert_in_string(
    content: String,
    variables: &HashMap<String, VariableStruct>,
) -> String {
    let re_extract_string_and_params: Option<Captures> =
        Regex::new(r#"^"(.*?)"\s*([,]{1,}\s*)(.*)$"#)
            .unwrap()
            .captures(&content);

    if re_extract_string_and_params.is_some() {
        let string_and_params = re_extract_string_and_params.unwrap();

        let mut string_with_params: String = string_and_params[1].to_string();
        let params = &string_and_params[3].to_string();

        let list_params = params.split(SEPARATOR_PARAMS_OPERATOR);

        for (_, param) in list_params.enumerate() {
            string_with_params = string_with_params.replacen(
                INSERT_OPERATOR_STRING,
                &discovery_value_from_unknown(
                    param.to_string().clone().to_string().to_string(),
                    &variables,
                )
                .value,
                1,
            );
        }
        return string_with_params;
    }

    panic!("Error on process string");
}

fn process_print_content(content: String, variables: &HashMap<String, VariableStruct>) -> String {
    if is_string_and_has_params(content.clone()) {
        return extract_params_and_insert_in_string(content.clone(), variables);
    } else {
        return discovery_value_from_unknown(content, variables).value;
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
            process_print_content("\"my value is {}\", 123".to_string(), &variables);

        assert_eq!(return_print, "my value is 123");
    }

    #[test]
    fn insert_int_inside_string_with_string() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String =
            process_print_content("\"my value is {}\", \"abc\"".to_string(), &variables);

        assert_eq!(return_print, "my value is abc");
    }

    #[test]
    fn insert_int_inside_multiples_missing_params() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content(
            "\"my value is {} _ {} + {} \", \"abc\", 2, true, 321.23, true".to_string(),
            &variables,
        );

        assert_eq!(return_print, "my value is abc _ 2 + true ");
    }

    #[test]
    fn insert_int_inside_multiples_all_params() {
        let variables: HashMap<String, VariableStruct> = HashMap::new();

        let return_print: String = process_print_content(
            "\"my value !$ FIRST {} SECOND {} TH&E33 {} ***** '¨?four_4 {} {}\", \"abc\", 2, true, 321.23, true"
                .to_string(),
            &variables,
        );

        assert_eq!(
            return_print,
            "my value !$ FIRST abc SECOND 2 TH&E33 true ***** '¨?four_4 321.23 true"
        );
    }
}
