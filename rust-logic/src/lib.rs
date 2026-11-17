use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn hitung_gaji(hari_kerja: u32, upah_harian: u32) -> u32 {
    hari_kerja * upah_harian
}

#[wasm_bindgen]
pub fn sapa_user(name: &str) -> String {
    format!("Halo {}, semangat kerja di SPX!", name)
}
