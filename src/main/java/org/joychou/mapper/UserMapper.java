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
    List<User> findByUserNameRaw(@Param("username") String username);

    List<User> findByUserNameXml(String username);
    List<User> findByUserNameOrder(@Param("order") String order);

    User findById(Integer id);

    User OrderByUsername();

}
