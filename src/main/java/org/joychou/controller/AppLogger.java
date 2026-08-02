package org.joychou.controller;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class AppLogger {

    private static final Logger logger = LogManager.getLogger("AppLogger");

    
    @RequestMapping(value = "/applog")
    public String writeLog(String token) {
        logger.error(token);
        return token;
    }

    public static void main(String[] args) {
        String message = "application started";
        logger.error(message);
    }

}
