package org.joychou.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.joychou.config.Constants;
import org.joychou.security.AntObjectInputStream;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InvalidClassException;
import java.io.ObjectInputStream;
import java.util.Base64;

import static org.springframework.web.util.WebUtils.getCookie;


@RestController
@RequestMapping("/object")
public class ObjectStore {

    protected final Logger logger = LoggerFactory.getLogger(this.getClass());

    
    @RequestMapping("/rememberMe/restore")
    public String restoreRememberMe(HttpServletRequest request)
            throws IOException, ClassNotFoundException {

        Cookie cookie = getCookie(request, Constants.REMEMBER_ME_COOKIE);
        if (null == cookie) {
            return "No rememberMe cookie.";
        }

        String rememberMe = cookie.getValue();
        byte[] decoded = Base64.getDecoder().decode(rememberMe);

        ByteArrayInputStream bytes = new ByteArrayInputStream(decoded);
        ObjectInputStream in = new ObjectInputStream(bytes);
        in.readObject();
        in.close();

        return "OK";
    }

    
    @RequestMapping("/rememberMe/restoreChecked")
    public String restoreRememberMeChecked(HttpServletRequest request)
            throws IOException, ClassNotFoundException {

        Cookie cookie = getCookie(request, Constants.REMEMBER_ME_COOKIE);

        if (null == cookie) {
            return "No rememberMe cookie.";
        }
        String rememberMe = cookie.getValue();
        byte[] decoded = Base64.getDecoder().decode(rememberMe);

        ByteArrayInputStream bytes = new ByteArrayInputStream(decoded);

        try {
            AntObjectInputStream in = new AntObjectInputStream(bytes);  // throw InvalidClassException
            in.readObject();
            in.close();
        } catch (InvalidClassException e) {
            logger.info(e.toString());
            return e.toString();
        }

        return "OK";
    }

    @RequestMapping("/jackson")
    public void parseJackson(String content) {
        ObjectMapper mapper = new ObjectMapper();
        mapper.enableDefaultTyping();
        try {
            Object obj = mapper.readValue(content, Object.class);
            mapper.writeValueAsString(obj);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
