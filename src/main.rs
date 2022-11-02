use crate::interpreter::interpreter;
use std::fs;

mod interpreter;
fn main() {
    let code_file: String =
        fs::read_to_string("./hello.simple").expect("Should have been able to read the file");

    interpreter(code_file)
}
