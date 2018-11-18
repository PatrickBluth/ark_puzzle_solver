use std::io::BufReader;
use std::io::BufRead;
use std::fs::File;
use std::path::Path; 

fn get_word_list()->Vec<String>{
    let file = File::open("../bip39_words.txt").unwrap();
    return BufReader::new(file).lines();
}


fn main() {
    
}
