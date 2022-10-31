use regex::Regex;
use std::collections::HashMap;
use std::fs;

struct VariableStruct {
    name: String,
    type_var: variableTypesEnum,
    value: String,
}

#[derive(Clone, Copy, Debug)]
enum variableTypesEnum {
    Number,
    String,
    Boolean,
}

fn create_variable_struct(
    name: String,
    type_var: variableTypesEnum,
    value: String,
) -> VariableStruct {
    return VariableStruct {
        name,
        type_var,
        value,
    };
}

fn var_analyze(
    name: String,
    value: String,
    variables: &HashMap<String, VariableStruct>,
) -> VariableStruct {
    let value_trim = value.trim();

    if value_trim.starts_with("\"") {
        return create_variable_struct(name.to_string(), variableTypesEnum::String, value);
    } else if (value_trim == "false" || value_trim == "true") {
        return create_variable_struct(name, variableTypesEnum::Boolean, value);
    } else if (value_trim.parse::<f64>().is_ok()) {
        return create_variable_struct(name, variableTypesEnum::Number, value);
    } else {
        let key_name = &value.clone();

        return create_variable_struct(
            variables[key_name].name.clone(),
            variables[key_name].type_var,
            variables[key_name].value.clone(),
        );
    }
}

fn print_content(content: String, variables: &HashMap<String, VariableStruct>) -> bool {
    if content.starts_with("\"") {
        println!("-> {}", content);
    } else {
        println!("-> {}", variables[&content.to_string()].value);
    }
    return true;
}

fn main() {
    println!("Programm");
    let mut variables: HashMap<String, VariableStruct> = HashMap::new();

    let contents =
        fs::read_to_string("./hello.simple").expect("Should have been able to read the file");

    let split = contents.split("\n");

    for (_pos, a) in split.enumerate() {
        let variable: String = a.trim().to_string();

        let re = Regex::new(r"^print (.*)$").unwrap();
        let cap = re.captures(&variable);
        if cap.is_some() {
            let items = cap.unwrap();
            print_content(items[1].to_string().to_string(), &variables);
            continue;
        }

        let re2 = Regex::new(r"^var (\w{1,}) = (.*)$").unwrap();
        let cap2 = re2.captures(&variable);
        if cap2.is_some() {
            let items = cap2.unwrap();
            let response: VariableStruct =
                var_analyze(items[1].to_string(), items[2].to_string(), &variables);

            variables.insert(items[1].to_string(), response);
            continue;
        }
    }

    println!("--------------------------");
    println!("--------------------------");
    println!("--------------------------");

    for (key, value) in &variables {
        println!(
            "{} = {}, {}, {:?}",
            key, value.name, value.value, value.type_var
        );
    }
}
