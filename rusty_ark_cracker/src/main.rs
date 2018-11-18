use std::io::BufReader;
use std::io::BufRead;
use std::fs::File;
use std::path::Path; 

fn get_word_list()->Vec<String>{
    let file = File::open("test_words.txt").unwrap();
    let words:Vec<String> = BufReader::new(file).lines().map(|l| l.unwrap());
    return words;
}


fn main() {
    println!("{:?}", get_word_list());
}
