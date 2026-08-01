package org.joychou.controller;



import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;




public class PathPatternDemo {


    
    public static void main(String[] args) throws Exception{
        Pattern path_pattern = Pattern.compile("/black_path.*");
        Pattern sec_pattern = Pattern.compile("/black_path.*", Pattern.DOTALL);

        String sample = URLDecoder.decode("/black_path%0a/xx", StandardCharsets.UTF_8.toString());
        System.out.println("sample: " + sample);
        System.out.println("Not dotall: " + path_pattern.matcher(sample).matches());    // false，非dotall无法匹配\r\n
        System.out.println("Dotall: " + sec_pattern.matcher(sample).matches());         // true，dotall可以匹配\r\n
    }
}
