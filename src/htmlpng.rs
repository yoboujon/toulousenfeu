use std::env::current_dir;

use headless_chrome::{
    protocol::cdp::Page::CaptureScreenshotFormatOption, Browser, LaunchOptionsBuilder,
};
use anyhow::Result;

pub fn convert_picture() -> Result<()> {
    // Create a new browser instance
    let browser = Browser::new(LaunchOptionsBuilder::default().build()?)?;
    // Checking if headless chromium is installed
    let tab = browser.new_tab()?;

    // Current dir for the URL
    let path = "file://".to_string()+&(current_dir()?.as_os_str().to_str().unwrap().to_string());

    // Create the viewport
    let box_model = tab
        .navigate_to(&(path+"/template/input.html"))?
        .wait_for_element("body")?
        .get_box_model()?;
     
    // Get a screenshot of the tab and putting it in an output file
    let png_data = tab.capture_screenshot(
        CaptureScreenshotFormatOption::Png,
        None,
        Some(box_model.margin_viewport()),
        true,
    )?;
    
    std::fs::write("output.png", &png_data).unwrap();

    Ok(())
}
