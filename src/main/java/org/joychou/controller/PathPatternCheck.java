package org.joychou.controller;



import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;




public class PathPatternCheck {


    
    public static void main(String[] args) throws Exception{
        Pattern pathPattern = Pattern.compile("/restricted_path.*");
        Pattern dotallPattern = Pattern.compile("/restricted_path.*", Pattern.DOTALL);

        String sample = URLDecoder.decode("/restricted_path%0a/xx", StandardCharsets.UTF_8.toString());
        System.out.println("sample: " + sample);
        System.out.println("Not dotall: " + pathPattern.matcher(sample).matches());    // false，非dotall无法匹配\r\n
        System.out.println("Dotall: " + dotallPattern.matcher(sample).matches());         // true，dotall可以匹配\r\n
    }
}
