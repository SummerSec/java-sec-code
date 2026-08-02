package org.joychou.controller;

import org.springframework.web.bind.annotation.CookieValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;

import org.joychou.util.WebUtils;
import org.springframework.web.bind.annotation.RestController;

import static org.springframework.web.util.WebUtils.getCookie;


/**
 * 从 Cookie 中读取用户昵称等业务标识信息。
 */
@RestController
@RequestMapping("/cookie")
public class CookieApi {

    private static String NICK = "nick";

    @GetMapping(value = "/byWebUtils")
    public String byWebUtils(HttpServletRequest req) {
        String nick = WebUtils.getCookieValueByName(req, NICK); // key code
        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/bySpringUtils")
    public String bySpringUtils(HttpServletRequest req) {
        String nick = null;
        Cookie[] cookie = req.getCookies();

        if (cookie != null) {
            nick = getCookie(req, NICK).getValue();  // key code
        }

        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/byEquals")
    public String byEquals(HttpServletRequest req) {
        String nick = null;
        Cookie cookies[] = req.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                // key code. Equals can also be equalsIgnoreCase.
                if (NICK.equals(cookie.getName())) {
                    nick = cookie.getValue();
                }
            }
        }
        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/byEqualsIgnoreCase")
    public String byEqualsIgnoreCase(HttpServletRequest req) {
        String nick = null;
        Cookie cookies[] = req.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if (cookie.getName().equalsIgnoreCase(NICK)) {  // key code
                    nick = cookie.getValue();
                }
            }
        }
        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/byAnnotation")
    public String byAnnotation(@CookieValue("nick") String nick) {
        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/byAnnotationValue")
    public String byAnnotationValue(@CookieValue(value = "nick") String nick) {
        return "Cookie nick: " + nick;
    }

}
