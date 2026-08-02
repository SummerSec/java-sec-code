package org.joychou.controller;

import cn.hutool.http.HttpUtil;
import org.joychou.security.SecurityUtil;
import org.joychou.security.netguard.UrlGuardException;
import org.joychou.service.HttpService;
import org.joychou.util.HttpUtils;
import org.joychou.util.WebUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.net.*;




@RestController
@RequestMapping("/proxy")
public class ResourceProxy {

    private static final Logger logger = LoggerFactory.getLogger(ResourceProxy.class);

    @Resource
    private HttpService httpService;

    
    @RequestMapping(value = "/urlConnection/fetch", method = {RequestMethod.POST, RequestMethod.GET})
    public String urlConnectionFetch(String url) {
        return HttpUtils.URLConnection(url);
    }


    @GetMapping("/urlConnection/fetchGuarded")
    public String urlConnectionSafe(String url) {

        // Decline not http/https protocol
        if (!SecurityUtil.isHttp(url)) {
            return "[-] url check failed";
        }

        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.URLConnection(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

    }


    /**
     * The default setting of followRedirects is true.
     * UserAgent is Java/1.8.0_102.
     */
    @GetMapping("/HttpURLConnection/fetchGuarded")
    public String httpURLConnection(@RequestParam String url) {
        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.HttpURLConnection(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }
    }


    @GetMapping("/HttpURLConnection/fetch")
    public String httpurlConnectionFetch(@RequestParam String url) {
        return HttpUtils.HttpURLConnection(url);
    }

    
    @GetMapping("/request/fetchGuarded")
    public String request(@RequestParam String url) {
        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.request(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }
    }


    
    @GetMapping("/openStream")
    public void openStream(@RequestParam String url, HttpServletResponse response) throws IOException {
        InputStream inputStream = null;
        OutputStream outputStream = null;
        try {
            String downLoadImgFileName = WebUtils.getNameWithoutExtension(url) + "." + WebUtils.getFileExtension(url);
            // download
            response.setHeader("content-disposition", "attachment;fileName=" + downLoadImgFileName);

            URL u = new URL(url);
            int length;
            byte[] bytes = new byte[1024];
            inputStream = u.openStream(); // send request
            outputStream = response.getOutputStream();
            while ((length = inputStream.read(bytes)) > 0) {
                outputStream.write(bytes, 0, length);
            }

        } catch (Exception e) {
            logger.error(e.toString());
        } finally {
            if (inputStream != null) {
                inputStream.close();
            }
            if (outputStream != null) {
                outputStream.close();
            }
        }
    }


    /**
     * The default setting of followRedirects is true.
     * UserAgent is Java/1.8.0_102.
     */
    @GetMapping("/ImageIO/fetchGuarded")
    public String ImageIO(@RequestParam String url) {
        try {
            SecurityUtil.startUrlHook();
            HttpUtils.imageIO(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

        return "ImageIO proxy ok";
    }


    @GetMapping("/okhttp/fetchGuarded")
    public String okhttp(@RequestParam String url) {

        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.okhttp(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

    }

    
    @GetMapping("/httpclient/fetchGuarded")
    public String HttpClient(@RequestParam String url) {

        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.httpClient(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

    }


    
    @GetMapping("/commonsHttpClient/fetchGuarded")
    public String commonsHttpClient(@RequestParam String url) {

        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.commonHttpClient(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

    }

    
    @GetMapping("/Jsoup/fetchGuarded")
    public String Jsoup(@RequestParam String url) {

        try {
            SecurityUtil.startUrlHook();
            return HttpUtils.Jsoup(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

    }


    
    @GetMapping("/IOUtils/fetchGuarded")
    public String IOUtils(String url) {
        try {
            SecurityUtil.startUrlHook();
            HttpUtils.IOUtils(url);
        } catch (UrlGuardException | IOException e) {
            return e.getMessage();
        } finally {
            SecurityUtil.stopUrlHook();
        }

        return "IOUtils proxy ok";
    }


    /**
     * The default setting of followRedirects is true.
     * UserAgent is <code>Apache-HttpAsyncClient/4.1.4 (Java/1.8.0_102)</code>.
     */
    @GetMapping("/HttpSyncClients/fetch")
    public String HttpSyncClients(@RequestParam("url") String url) {
        return HttpUtils.HttpAsyncClients(url);
    }


    /**
     * Only support HTTP protocol. <br>
     * GET HttpMethod follow redirects by default, other HttpMethods do not follow redirects. <br>
     * User-Agent is Java/1.8.0_102. <br>
     * <a href="http://127.0.0.1:8080/proxy/restTemplate/noRedirect?url=http://www.baidu.com">http://127.0.0.1:8080/proxy/restTemplate/noRedirect?url=http://www.baidu.com</a>
     */
    @GetMapping("/restTemplate/noRedirect")
    public String RestTemplateUrlBanRedirects(String url){
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON_UTF8);
        return httpService.RequestHttpBanRedirects(url, headers);
    }


    @GetMapping("/restTemplate/followRedirect")
    public String RestTemplateUrl(String url){
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON_UTF8);
        return httpService.RequestHttp(url, headers);
    }


    
    @GetMapping("/hutool/get")
    public String hutoolHttp(String url){
        return HttpUtil.get(url);
    }


    
    @GetMapping("/dnsrebind/check")
    public String DnsRebind(String url) {
        java.security.Security.setProperty("networkaddress.cache.negative.ttl" , "0");
        if (!SecurityUtil.checkUrlWithoutRedirect(url)) {
            return "URL not allowed";
        }
        return HttpUtil.get(url);
    }


}
