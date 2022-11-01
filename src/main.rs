use regex::Regex;
use std::collections::HashMap;
use std::fs;

#[path = "./types/types.rs"]
mod types;
use crate::types::VariableStruct;

#[path = "./cases/create_var.rs"]
mod var_analyze;
use crate::var_analyze::var_analyze;

#[path = "./cases/print_content.rs"]
mod print_content;
use crate::print_content::print_content;

fn main() {
    println!("Programm");
    let mut variables: HashMap<String, VariableStruct> = HashMap::new();

    let contents =
        fs::read_to_string("./hello.simple").expect("Should have been able to read the file");

    let split = contents.split("\n");

    for (_pos, a) in split.enumerate() {
        let variable: String = a.trim().to_string();

        let cap = Regex::new(r"^print (.*)$").unwrap().captures(&variable);
        if cap.is_some() {
            let items = cap.unwrap();
            print_content(items[1].to_string(), &variables);
            continue;
        }

        let cap2 = Regex::new(r"^var (\w{1,}) = (.*)$")
            .unwrap()
            .captures(&variable);
        if cap2.is_some() {
            let items = cap2.unwrap();
            var_analyze(items[1].to_string(), items[2].to_string(), &mut variables);
            continue;
        }
    }

    // println!("--------------------------");
    // println!("--------------------------");
    // println!("--------------------------");

    // for (key, value) in &variables {
    //     println!(
    //         "{} = {}, {}, {:?}",
    //         key, value.name, value.value, value.type_var
    //     );
    // }
}
