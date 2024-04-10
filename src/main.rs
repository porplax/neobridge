use std::str;
use std::time::Duration;

use serialport::{self, SerialPort};

pub struct Neobridge {
    port: Box<dyn SerialPort>, 
    number_of_leds: u32
}

pub struct RGB(u32, u32, u32);

impl Neobridge {

    pub fn new(port: &str, number_of_leds: u32) -> Neobridge {
        Neobridge {
            port: serialport::new(port, 115_200)
                .timeout(Duration::from_millis(10))
                .open().expect("Failed to open port"),
            number_of_leds: number_of_leds
        }
    }

    fn replace_with_color(&mut self, msg: &str, color: RGB) -> String {
        let mut replace = str::replace(msg, "{0}", color.0.to_string().as_str());
        replace = str::replace(replace.as_str(), "{1}", color.1.to_string().as_str());
        replace = str::replace(replace.as_str(), "{2}", color.2.to_string().as_str());
        return replace;
    }

    fn send_message(&mut self, message: &str) {
        self.port.write(message.as_bytes()).expect("could not write to serial port");
        self.port.write("\r\n".as_bytes()).expect("could not write to serial port");
        self.port.flush().expect("could not flush to serial port");
    }

    fn reset(&mut self) {
        self.send_message(r#"{"command": -2}"#);
    }

    pub fn show(&mut self) {
        self.send_message(r#"{"command": -3}"#);
    }

    pub fn set_all(&mut self, color: RGB) -> Result<(), &'static str> {
        let msg = self.replace_with_color(r#"{"command": 0, "r": {0}, "g": {1}, "b": {2}}"#, color);
        let binding = msg.as_str();

        self.send_message(binding);
        Ok(())
    }

    pub fn set_one(&mut self, color: RGB, index: u32) -> Result<(), &'static str> {
        if self.number_of_leds-1 < index
            {panic!("You give me an index greater than what you set as!");}
        let msg = self.replace_with_color(r#"{"command": 1, "r": {0}, "g": {1}, "b": {2}, "index": {3}}"#, color);
        let index_replace = msg.replace("{3}", index.to_string().as_str());
        let binding = index_replace.as_str();

        self.send_message(binding);
        Ok(())
    }
}

fn main() {
    let mut neobridge = Neobridge::new("COM3", 30);
    
    neobridge.set_all(RGB(0, 0, 0)).unwrap();
    neobridge.show();

    let mut i = 0;
    loop {
        if (i == 30) {
            i = 0;
        }

        neobridge.set_one(RGB(255, 0, 255), i).unwrap();
        neobridge.show();
        std::thread::sleep(std::time::Duration::from_millis(50));

        neobridge.set_all(RGB(0, 0, 0)).unwrap();

        i += 1;
    }
}
