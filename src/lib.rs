use std::str;
use std::time::Duration;

use serialport::{self, SerialPort};
pub struct Neobridge {
    port: Box<dyn SerialPort>, 
    number_of_leds: u32
}

#[derive(Debug)]
pub struct RGB {
    r: u8,
    g: u8,
    b: u8
}

impl RGB {
    pub fn to_string(&self) -> String {
        return format!("({0}, {1}, {2})", self.r, self.g, self.b);
    }
}

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
        let mut replace = str::replace(msg, "{0}", color.r.to_string().as_str());
        replace = str::replace(replace.as_str(), "{1}", color.g.to_string().as_str());
        replace = str::replace(replace.as_str(), "{2}", color.b.to_string().as_str());
        return replace;
    }

    fn send_message(&mut self, message: &str) {
        self.port.write(message.as_bytes()).expect("could not write to serial port");
        self.port.write("\r\n".as_bytes()).expect("could not write to serial port");
        self.port.flush().expect("could not flush to serial port");
    }
    
    pub fn show(&mut self) {
        self.send_message(r#"{"command": -3}"#);
    }

    pub fn set_all(&mut self, color: RGB) {
        let msg = self.replace_with_color(r#"{"command": 0, "r": {0}, "g": {1}, "b": {2}}"#, color);
        let binding = msg.as_str();

        self.send_message(binding);
    }

    pub fn set_one(&mut self, color: RGB, index: u32) {
        if self.number_of_leds < index
            {panic!("You give me an index greater than what you set as!");}
        let msg = self.replace_with_color(r#"{"command": 1, "r": {0}, "g": {1}, "b": {2}, "index": {3}}"#, color);
        let index_replace = msg.replace("{3}", index.to_string().as_str());
        let binding = index_replace.as_str();

        self.send_message(binding);
    }

    
    pub fn set_list(&mut self, colors: &Vec<RGB>)  {
        // xxx: this is extremely inefficient, but this will work for now.
        let result: Vec<String> = colors.into_iter().map(|x| x.to_string()).collect();
        
        let msg = r#"{"command": 2, "rgb_list": [{0}]}"#.replace("{0}", &result.join(", ").replace("(", "[").replace(")", "]"));
        let binding = msg.as_str();

        self.send_message(binding);
    }
}
