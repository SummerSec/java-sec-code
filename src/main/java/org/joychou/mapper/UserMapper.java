package org.joychou.mapper;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.joychou.dao.User;

import java.util.List;

@Mapper
public interface UserMapper {

    @Select("select * from users where username = #{username}")
    User findByUserName(@Param("username") String username);

    @Select("select * from users where username = '${username}'")
    List<User> findByUserNameCase01(@Param("username") String username);

    List<User> findByUserNameCase02(String username);
    List<User> findByUserNameCase03(@Param("order") String order);

    User findById(Integer id);

    User OrderByUsername();

}
