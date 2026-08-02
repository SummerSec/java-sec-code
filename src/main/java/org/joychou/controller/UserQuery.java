package org.joychou.controller;


import org.joychou.mapper.UserMapper;
import org.joychou.dao.User;
import org.joychou.security.SecurityUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.sql.*;
import java.util.List;




@SuppressWarnings("Duplicates")
@RestController
@RequestMapping("/query")
public class UserQuery {

    private static final Logger logger = LoggerFactory.getLogger(UserQuery.class);

    // com.mysql.jdbc.Driver is deprecated. Change to com.mysql.cj.jdbc.Driver.
    private static final String driver = "com.mysql.cj.jdbc.Driver";

    @Value("${spring.datasource.url}")
    private String url;

    @Value("${spring.datasource.username}")
    private String user;

    @Value("${spring.datasource.password}")
    private String password;

    @Resource
    private UserMapper userMapper;


    
    @RequestMapping("/jdbc/query")
    public String jdbcQuery(@RequestParam("username") String username) {

        StringBuilder result = new StringBuilder();

        try {
            Class.forName(driver);
            Connection con = DriverManager.getConnection(url, user, password);

            if (!con.isClosed())
                System.out.println("Connect to database successfully.");

            Statement statement = con.createStatement();
            String sql = "select * from users where username = '" + username + "'";
            logger.info(sql);
            ResultSet rs = statement.executeQuery(sql);

            while (rs.next()) {
                String res_name = rs.getString("username");
                String res_pwd = rs.getString("password");
                String info = String.format("%s: %s\n", res_name, res_pwd);
                result.append(info);
                logger.info(info);
            }
            rs.close();
            con.close();


        } catch (ClassNotFoundException e) {
            logger.error("Sorry, can't find the Driver!");
        } catch (SQLException e) {
            logger.error(e.toString());
        }
        return result.toString();
    }


    
    @RequestMapping("/jdbc/queryPrepared")
    public String jdbcQueryPrepared(@RequestParam("username") String username) {

        StringBuilder result = new StringBuilder();
        try {
            Class.forName(driver);
            Connection con = DriverManager.getConnection(url, user, password);

            if (!con.isClosed())
                System.out.println("Connect to database successfully.");

            String sql = "select * from users where username = ?";
            PreparedStatement st = con.prepareStatement(sql);
            st.setString(1, username);

            logger.info(st.toString());  // sql after prepare statement
            ResultSet rs = st.executeQuery();

            while (rs.next()) {
                String res_name = rs.getString("username");
                String res_pwd = rs.getString("password");
                String info = String.format("%s: %s\n", res_name, res_pwd);
                result.append(info);
                logger.info(info);
            }

            rs.close();
            con.close();

        } catch (ClassNotFoundException e) {
            logger.error("Sorry, can't find the Driver!");
            e.printStackTrace();
        } catch (SQLException e) {
            logger.error(e.toString());
        }
        return result.toString();
    }


    
    @RequestMapping("/jdbc/ps/query")
    public String jdbcPsQuery(@RequestParam("username") String username) {

        StringBuilder result = new StringBuilder();
        try {
            Class.forName(driver);
            Connection con = DriverManager.getConnection(url, user, password);

            if (!con.isClosed())
                System.out.println("Connecting to Database successfully.");

            String sql = "select * from users where username = '" + username + "'";
            PreparedStatement st = con.prepareStatement(sql);

            logger.info(st.toString());
            ResultSet rs = st.executeQuery();

            while (rs.next()) {
                String res_name = rs.getString("username");
                String res_pwd = rs.getString("password");
                String info = String.format("%s: %s\n", res_name, res_pwd);
                result.append(info);
                logger.info(info);
            }

            rs.close();
            con.close();

        } catch (ClassNotFoundException e) {
            logger.error("Sorry, can't find the Driver!");
            e.printStackTrace();
        } catch (SQLException e) {
            logger.error(e.toString());
        }
        return result.toString();
    }


    
    @GetMapping("/mybatis/listByName")
    public List<User> mybatisListByName(@RequestParam("username") String username) {
        return userMapper.findByUserNameRaw(username);
    }

    
    @GetMapping("/mybatis/listByNameXml")
    public List<User> mybatisListByNameXml(@RequestParam("username") String username) {
        return userMapper.findByUserNameXml(username);
    }

    
    @GetMapping("/mybatis/orderby/list")
    public List<User> mybatisOrderBy(@RequestParam("sort") String sort) {
        return userMapper.findByUserNameOrder(sort);
    }


    
    @GetMapping("/mybatis/getByName")
    public User mybatisGetByName(@RequestParam("username") String username) {
        return userMapper.findByUserName(username);
    }

    
    @GetMapping("/mybatis/getById")
    public User mybatisGetById(@RequestParam("id") Integer id) {
        return userMapper.findById(id);
    }


    
    @GetMapping("/mybatis/orderByName")
    public User mybatisOrderByName() {
        return userMapper.OrderByUsername();
    }

    
    @GetMapping("/mybatis/orderby/listFiltered")
    public List<User> mybatisOrderByFiltered(@RequestParam("sort") String sort) {
        return userMapper.findByUserNameOrder(SecurityUtil.sqlFilter(sort));
    }

}
