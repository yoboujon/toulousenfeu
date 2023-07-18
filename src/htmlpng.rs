use headless_chrome::{
    protocol::cdp::Page::CaptureScreenshotFormatOption, Browser, LaunchOptionsBuilder,
};
use std::fs::write;
use std::env;

pub fn convert_picture() {
    // Create a new browser instance
    let browser = Browser::new(LaunchOptionsBuilder::default().build().unwrap()).unwrap();

    // Create a new tab
    let tab = browser.new_tab().unwrap();

    //Get the actual directory
    let current_dir = env::current_dir().expect("Failed to retrieve the current working directory");
    println!("Current working directory: {:?}", current_dir);

    // Convert the current directory to a string
    let current_dir_str = current_dir.to_str().expect("Failed to convert path to string");

    // Concatenate the strings using the + operator
    let full_path = current_dir_str.to_owned() + "\\template\\input.html";

    // Create the viewport
    let box_model = tab
        .navigate_to(full_path.as_str())
        .unwrap()
        .wait_for_element("body")
        .unwrap()
        .get_box_model()
        .unwrap();

    let png_data = tab
        .capture_screenshot(
            CaptureScreenshotFormatOption::Png,
            Some(1u32),
            Some(box_model.margin_viewport()),
            true,
        )
        .unwrap();

    write("output.png", &png_data).unwrap();
}
