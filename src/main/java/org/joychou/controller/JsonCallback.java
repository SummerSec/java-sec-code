package org.joychou.controller;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import com.alibaba.fastjson.JSONPObject;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang.StringUtils;
import org.joychou.util.LoginUtils;
import org.joychou.security.SecurityUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.security.web.csrf.CookieCsrfTokenRepository;
import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.view.json.MappingJackson2JsonView;
import org.joychou.config.WebConfig;
import org.joychou.util.WebUtils;

import javax.servlet.http.HttpServletRequest;
import java.security.Principal;


/**
 * @author JoyChou (joychou@joychou.org) @ 2018.10.24
 * https://github.com/JoyChou93/java-sec-code/wiki/JSONP
 */

@Slf4j
@RestController
@RequestMapping("/callback")
public class JsonCallback {

    private String callback = WebConfig.getBusinessCallback();

    @Autowired
    CookieCsrfTokenRepository cookieCsrfTokenRepository;
    
    @RequestMapping(value = "/case/referer", produces = "application/javascript")
    public String referer(HttpServletRequest request) {
        String callback = request.getParameter(this.callback);
        return WebUtils.json2Jsonp(callback, LoginUtils.getUserInfo2JsonStr(request));
    }

    
    @RequestMapping(value = "/case/emptyReferer", produces = "application/javascript")
    public String emptyReferer(HttpServletRequest request) {
        String referer = request.getHeader("referer");

        if (null != referer && SecurityUtil.checkURL(referer) == null) {
            return "error";
        }
        String callback = request.getParameter(this.callback);
        return WebUtils.json2Jsonp(callback, LoginUtils.getUserInfo2JsonStr(request));
    }

    
    @RequestMapping(value = "/object2jsonp", produces = MediaType.APPLICATION_JSON_VALUE)
    public JSONObject advice(HttpServletRequest request) {
        return JSON.parseObject(LoginUtils.getUserInfo2JsonStr(request));
    }


    
    @RequestMapping(value = "/case/mappingJackson2JsonView", produces = MediaType.APPLICATION_JSON_VALUE)
    public ModelAndView mappingJackson2JsonView(HttpServletRequest req) {
        ModelAndView view = new ModelAndView(new MappingJackson2JsonView());
        Principal principal = req.getUserPrincipal();
        view.addObject("username", principal.getName());
        return view;
    }


    
    @RequestMapping(value = "/sec/checkReferer", produces = "application/javascript")
    public String safecode(HttpServletRequest request) {
        String referer = request.getHeader("referer");

        if (SecurityUtil.checkURL(referer) == null) {
            return "error";
        }
        String callback = request.getParameter(this.callback);
        return WebUtils.json2Jsonp(callback, LoginUtils.getUserInfo2JsonStr(request));
    }

    
    @GetMapping("/getToken")
    public CsrfToken getCsrfToken1(CsrfToken token) {
        return token;
    }

    
    @GetMapping(value = "/jsonapip/getToken", produces = "application/javascript")
    public String getCsrfToken2(HttpServletRequest request) {
        CsrfToken csrfToken = cookieCsrfTokenRepository.loadToken(request); // get csrf token

        String callback = request.getParameter("apiCallback");
        if (StringUtils.isNotBlank(callback)) {
            JSONPObject jsonpObj = new JSONPObject(callback);
            jsonpObj.addParameter(csrfToken);
            return jsonpObj.toString();
        } else {
            return csrfToken.toString();
        }
    }

}