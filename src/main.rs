pub mod htmlpng;

fn main() {
    println!("Hello, Toulouse!");

    match htmlpng::convert_picture() {
        Err(error_message) => {
            println!("Error on convert_picture : {}",error_message);
        }
        _ => {
            println!("convert_picture successful.");
        }
    }
}
