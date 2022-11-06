use std::env;
use std::fs;

mod interpreter;

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut code_file: String = "".to_string();

    if (args.get(1).is_some()) {
        code_file = fs::read_to_string(&args[1]).expect("Should have been able to read the file");
    } else {
        code_file =
            fs::read_to_string("./example.safira").expect("Should have been able to read the file");
    }
    interpreter::interpreter(code_file)
}
