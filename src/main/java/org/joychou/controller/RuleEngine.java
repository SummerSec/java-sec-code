package org.joychou.controller;

import com.ql.util.express.DefaultContext;
import com.ql.util.express.ExpressRunner;
import com.ql.util.express.config.QLExpressRunStrategy;
import org.joychou.util.WebUtils;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

@RestController
@RequestMapping("/rules")
public class RuleEngine {

    @RequestMapping("/execute")
    public String execute(HttpServletRequest req) throws Exception{
        String express = WebUtils.getRequestBody(req);
        System.out.println(express);
        ExpressRunner runner = new ExpressRunner();
        DefaultContext<String, Object> context = new DefaultContext<String, Object>();
        Object r = runner.execute(express, context, null, true, false);
        System.out.println(r);
        return r.toString();
    }

    @RequestMapping("/safe")
    public String executeSafe(HttpServletRequest req) throws Exception{
        String express = WebUtils.getRequestBody(req);
        System.out.println(express);
        ExpressRunner runner = new ExpressRunner();
        QLExpressRunStrategy.setForbidInvokeSecurityRiskMethods(true);
        // Can only call java.lang.String#length()
        QLExpressRunStrategy.addSecureMethod(String.class, "length");
        DefaultContext<String, Object> context = new DefaultContext<String, Object>();
        Object r = runner.execute(express, context, null, true, false);
        System.out.println(r);
        return r.toString();
    }
}
