use anyhow::Result;
use std::fs::read_to_string;
use csv::Reader;

pub fn conver_csv() -> Result<()>
{
    // Read the file data
    let file_content = read_to_string("data/normales-rust.csv")?;

    let mut rdr = Reader::from_reader(file_content.as_bytes());
    for result in rdr.records() {
        // Notice that we need to provide a type hint for automatic
        // deserialization.
        let normales = result?;
        println!("{:?}", normales);
    }
    Ok(())
}