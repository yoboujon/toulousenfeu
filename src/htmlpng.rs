use headless_chrome::{
    protocol::cdp::Page::CaptureScreenshotFormatOption, Browser, LaunchOptionsBuilder,
};
use std::env;
use anyhow::Result;

pub fn convert_picture() -> Result<()> {
    // Create a new browser instance
    let browser = Browser::new(LaunchOptionsBuilder::default().build()?)?;

    // Create a new tab
    let tab = browser.new_tab()?;

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
    let full_path = format!("{}\\template\\input.html", current_dir_str);

    // Create the viewport
    let box_model = tab
        .navigate_to(full_path.as_str())?
        .wait_for_element("body")?
        .get_box_model()?;

    let png_data = tab.capture_screenshot(
        CaptureScreenshotFormatOption::Png,
        None,
        Some(box_model.margin_viewport()),
        true,
    )?;

    std::fs::write("output.png", &png_data).unwrap();

    Ok(())
}
