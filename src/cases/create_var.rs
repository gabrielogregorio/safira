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
    } else if (value_trim == "false" || value_trim == "true") {
        let response = create_variable_struct(name.clone(), VariableTypesEnum::Boolean, value);
        variables.insert(name.clone(), response);

        return;
    } else if (value_trim.parse::<f64>().is_ok()) {
        let response = create_variable_struct(name.clone(), VariableTypesEnum::Number, value);
        variables.insert(name.clone(), response);

        return;
    } else {
        let key_name = &value.clone();

        let response = create_variable_struct(
            variables[key_name].name.clone(),
            variables[key_name].type_var,
            variables[key_name].value.clone(),
        );

        variables.insert(name, response);

        return;
    }
}
