use std::time::Duration;
use std::thread::sleep;

mod htmlpng;
mod csv;

fn main() {
    println!("Hello, Toulouse!");
    loop{
        match csv::conver_csv() {
            Err(error_message) => {
                println!("Error on conver_csv : {}",error_message);
            }
            _ => {
                println!("conver_csv successful.");
            }
        }

        match htmlpng::convert_picture() {
            Err(error_message) => {
                println!("Error on convert_picture : {}",error_message);
            }
            _ => {
                println!("convert_picture successful.");
            }
        }
        sleep(Duration::new(1800, 0));
    }


}
