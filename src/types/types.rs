pub struct VariableStruct {
    pub name: String,
    pub type_var: VariableTypesEnum,
    pub value: String,
}

#[derive(Clone, Copy, Debug)]
pub enum VariableTypesEnum {
    Number,
    String,
    Boolean,
}
