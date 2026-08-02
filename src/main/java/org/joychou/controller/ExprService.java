package org.joychou.controller;

import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.common.TemplateParserContext;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.SimpleEvaluationContext;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;



@RestController
public class ExprService {

    
    @RequestMapping("/expr/evaluate")
    public String evaluate(String value) {
        ExpressionParser parser = new SpelExpressionParser();
        return parser.parseExpression(value).getValue().toString();
    }

    
    @RequestMapping("/expr/evaluateTyped")
    public String evaluateTyped(String value) {
        StandardEvaluationContext context = new StandardEvaluationContext();
        SpelExpressionParser parser = new SpelExpressionParser();
        Expression expression = parser.parseExpression(value, new TemplateParserContext());
        Object x = expression.getValue(context);
        return x.toString();   // response
    }

    @RequestMapping("/expr/evaluateChecked")
    public String evaluateChecked(String value) {
        SimpleEvaluationContext context = SimpleEvaluationContext.forReadOnlyDataBinding().build();
        SpelExpressionParser parser = new SpelExpressionParser();
        Expression expression = parser.parseExpression(value, new TemplateParserContext());
        Object x = expression.getValue(context);
        return x.toString();
    }

    public static void main(String[] args) {
        ExpressionParser parser = new SpelExpressionParser();
        String expression = "1+1";
        String result = parser.parseExpression(expression).getValue().toString();
        System.out.println(result);
    }

}

