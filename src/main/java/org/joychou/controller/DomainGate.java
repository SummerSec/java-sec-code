package org.joychou.controller;


import org.joychou.security.SecurityUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;



@RestController
@RequestMapping("/domain")
public class DomainGate {


    private String domainwhitelist[] = {"joychou.org", "joychou.com"};
    private static final Logger logger = LoggerFactory.getLogger(DomainGate.class);

    
    @GetMapping("/basic/endsWith")
    public String endsWith(@RequestParam("url") String url) {

        String host = SecurityUtil.gethost(url);

        for (String domain : domainwhitelist) {
            if (host.endsWith(domain)) {
                return "Good url.";
            }
        }
        return "Bad url.";
    }


    
    @GetMapping("/basic/contains")
    public String contains(@RequestParam("url") String url) {

        String host = SecurityUtil.gethost(url);

        for (String domain : domainwhitelist) {
            if (host.contains(domain)) {
                return "Good url.";
            }
        }
        return "Bad url.";
    }


    
    @GetMapping("/basic/regex")
    public String regex(@RequestParam("url") String url) {

        String host = SecurityUtil.gethost(url);
        Pattern p = Pattern.compile("joychou\\.org$");
        Matcher m = p.matcher(host);

        if (m.find()) {
            return "Good url.";
        } else {
            return "Bad url.";
        }
    }


    
    @GetMapping("/basic/urlParse")
    public void url_parse(String url, HttpServletResponse res) throws IOException {

        logger.info("url:  " + url);

        if (!SecurityUtil.isHttp(url)) {
            return;
        }

        URL u = new URL(url);
        String host = u.getHost();
        logger.info("host:  " + host);

        // endsWith .
        for (String domain : domainwhitelist) {
            if (host.endsWith("." + domain)) {
                res.sendRedirect(url);
            }
        }

    }


    
    @GetMapping("/safe")
    public String checkWhitelist(@RequestParam("url") String url) {

        String whiteDomainlists[] = {"joychou.org", "joychou.com", "test.joychou.me"};

        if (!SecurityUtil.isHttp(url)) {
            return "SecurityUtil is not http or https";
        }

        String host = SecurityUtil.gethost(url);

        for (String whiteHost: whiteDomainlists){
            if (whiteHost.startsWith(".") && host.endsWith(whiteHost)) {
                return url;
            } else if (!whiteHost.startsWith(".") && host.equals(whiteHost)) {
                return url;
            }
        }

        return "Bad url.";
    }


    
    @GetMapping("/safe/arrayIndexOf")
    public String checkArrayIndexOf(@RequestParam("url") String url) {

        // Define muti-level host whitelist.
        ArrayList<String> whiteDomainlists = new ArrayList<>();
        whiteDomainlists.add("bbb.joychou.org");
        whiteDomainlists.add("ccc.bbb.joychou.org");

        if (!SecurityUtil.isHttp(url)) {
            return "SecurityUtil is not http or https";
        }

        String host = SecurityUtil.gethost(url);

        if (whiteDomainlists.indexOf(host) != -1) {
            return "Good url.";
        }
        return "Bad url.";
    }

}
