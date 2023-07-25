use anyhow::Result;
use image::EncodableLayout;
use std::env;
use std::fs;
use csv::Reader;

#[derive(Debug, serde::Deserialize)]
struct Normales {
    month: f64,
    temp: f64,
    max_temp: f64,
    max_temp_date: String,
    min_temp: f64,
    min_temp_date: String,
    moy_temp_max: f64,
    moy_temp_min: f64,
}

pub fn conver_csv() -> Result<()>
{
    // Get the actual directory
    let current_dir_str;
    match env::current_dir()?.to_str() {
        Some(result_str) => {
            current_dir_str = result_str.to_string();
        }
        None => {
            return Err(anyhow::Error::msg("Could not convert current dir to string."))
        }
    }

    // Concatenate the strings using the + operator
    let full_path = format!("{}\\data\\normales-rust.csv", current_dir_str);

    // Read the file data
    let file_data = fs::read(full_path)?;

    let mut rdr = csv::Reader::from_reader(file_data.as_bytes());
    for result in rdr.deserialize() {
        // Notice that we need to provide a type hint for automatic
        // deserialization.
        let normales: Normales = result?;
        println!("{:?}", normales);
    }
    Ok(())
}