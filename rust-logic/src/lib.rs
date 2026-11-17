use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn parse_jumlah(text: &str) -> i32 {
    let t = text.to_lowercase()
        .replace("rp", "")
        .replace(".", "")
        .replace(",", "")
        .replace("rupiah", "");
    
    let t = t.trim();

    // Handle jutaan
    if t.contains("jt") || t.contains("juta") {
        let num_str: String = t.chars().take_while(|c| c.is_numeric() || *c == '.').collect();
        if let Ok(num) = num_str.parse::<f64>() {
            return (num * 1_000_000.0) as i32;
        }
    }

    // Handle ribuan
    if t.contains("rb") || t.contains("ribu") {
        let num_str: String = t.chars().take_while(|c| c.is_numeric() || *c == '.').collect();
        if let Ok(num) = num_str.parse::<f64>() {
            return (num * 1_000.0) as i32;
        }
    }

    // Handle mentah
    let num_str: String = t.chars().filter(|c| c.is_numeric()).collect();
    num_str.parse::<i32>().unwrap_or(0)
}

#[wasm_bindgen]
pub fn hitung_gaji(hari: i32) -> i32 {
    hari * 245_000
}

#[wasm_bindgen]
pub fn sapa_user(name: &str) -> String {
    format!("Halo {}, semangat kerja di SPX!", name)
}
