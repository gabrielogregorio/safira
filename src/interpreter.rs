use regex::{Captures, Regex};
use std::collections::HashMap;

use self::create_var::create_var;
use self::print_content::print_content;

#[path = "./discovery_value_from_unknown.rs"]
mod discovery_value_from_unknown;

#[path = "./create_var.rs"]
mod create_var;

#[path = "./print_content.rs"]
mod print_content;

#[warn(dead_code)]
pub struct VariableStruct {
    pub name: String,
    pub type_var: VariableTypesEnum,
    pub value: String,
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum VariableTypesEnum {
    Number,
    String,
    Boolean,
}

pub fn interpreter(code_file: String) {
    let mut variables: HashMap<String, VariableStruct> = HashMap::new();

    let lines = code_file.split("\n");

    for (_pos, line) in lines.enumerate() {
        interpreter_line(line.clone().to_string(), &mut variables);
    }
}

fn interpreter_line(line: String, variables: &mut HashMap<String, VariableStruct>) {
    let variable: String = line.trim().to_string();

    let cap: Option<Captures> = Regex::new(r"^print (.*)$").unwrap().captures(&variable);

    if cap.is_some() {
        let items = cap.unwrap();
        print_content(items[1].to_string(), variables);
        return;
    }

    let cap2: Option<Captures> = Regex::new(r"^var (\w{1,}) = (.*)$")
        .unwrap()
        .captures(&variable);

    if cap2.is_some() {
        let items: Captures = cap2.unwrap();
        create_var(items[1].to_string(), items[2].to_string(), variables);
        return;
    }
}
