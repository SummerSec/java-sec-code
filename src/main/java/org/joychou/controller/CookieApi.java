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
 * 某些应用获取用户身份信息可能会直接从cookie中直接获取明文的nick或者id，导致越权问题。
 */
@RestController
@RequestMapping("/cookie")
public class CookieApi {

    private static String NICK = "nick";

    @GetMapping(value = "/case01")
    public String case01(HttpServletRequest req) {
        String nick = WebUtils.getCookieValueByName(req, NICK); // key code
        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/case02")
    public String case02(HttpServletRequest req) {
        String nick = null;
        Cookie[] cookie = req.getCookies();

        if (cookie != null) {
            nick = getCookie(req, NICK).getValue();  // key code
        }

        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/case03")
    public String case03(HttpServletRequest req) {
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


    @GetMapping(value = "/case04")
    public String case04(HttpServletRequest req) {
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


    @GetMapping(value = "/case05")
    public String case05(@CookieValue("nick") String nick) {
        return "Cookie nick: " + nick;
    }


    @GetMapping(value = "/case06")
    public String case06(@CookieValue(value = "nick") String nick) {
        return "Cookie nick: " + nick;
    }

}
