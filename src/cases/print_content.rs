use std::collections::HashMap;

#[path = "../types/types.rs"]
mod types;
use crate::types::VariableStruct;

pub fn print_content(content: String, variables: &HashMap<String, VariableStruct>) -> bool {
    if content.starts_with("\"") {
        println!("-> {}", content);
    } else {
        println!("-> {}", variables[&content.to_string()].value);
    }
    return true;
}
