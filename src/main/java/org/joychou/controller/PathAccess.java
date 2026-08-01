package org.joychou.controller;


import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.util.AntPathMatcher;
import org.springframework.util.PathMatcher;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;



@RestController
@RequestMapping("/access")
public class PathAccess {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @GetMapping(value = "/exclued/case")
    public String exclued(HttpServletRequest request) {

        String[] excluedPath = {"/css/**", "/js/**"};
        String uri = request.getRequestURI(); // Security: request.getServletPath()
        PathMatcher matcher = new AntPathMatcher();

        logger.info("getRequestURI: " + uri);
        logger.info("getServletPath: " + request.getServletPath());

        for (String path : excluedPath) {
            if (matcher.match(path, uri)) {
                return "ok";
            }
        }
        return "This is a login page >..<";
    }
}
