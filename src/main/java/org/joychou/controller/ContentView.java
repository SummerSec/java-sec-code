package org.joychou.controller;

import org.apache.commons.lang.StringUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;


/**
 * @author JoyChou @2018-01-02
 */
@Controller
@RequestMapping("/content")
public class ContentView {

    
    @RequestMapping("/reflect")
    @ResponseBody
    public static String reflect(String text) {
        return text;
    }

    
    @RequestMapping("/stored/store")
    @ResponseBody
    public String store(String text, HttpServletResponse response) {
        Cookie cookie = new Cookie("msg", text);
        response.addCookie(cookie);
        return "Set param into cookie";
    }

    
    @RequestMapping("/stored/show")
    @ResponseBody
    public String show(@CookieValue("msg") String text) {
        return text;
    }

    
    @RequestMapping("/safe")
    @ResponseBody
    public static String safe(String text) {
        return encode(text);
    }

    private static String encode(String origin) {
        origin = StringUtils.replace(origin, "&", "&amp;");
        origin = StringUtils.replace(origin, "<", "&lt;");
        origin = StringUtils.replace(origin, ">", "&gt;");
        origin = StringUtils.replace(origin, "\"", "&quot;");
        origin = StringUtils.replace(origin, "'", "&#x27;");
        origin = StringUtils.replace(origin, "/", "&#x2F;");
        return origin;
    }
}
