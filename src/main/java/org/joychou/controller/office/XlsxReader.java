package org.joychou.controller.office;

import com.monitorjbl.xlsx.StreamingReader;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.multipart.MultipartFile;

import java.io.FileInputStream;
import java.io.IOException;



@Controller
@RequestMapping("/office/xlsx")
public class XlsxReader {


    @GetMapping("/upload")
    public String index() {
        return "doc_upload";
    }


    @PostMapping("/readxlsx")
    public void readXlsxStream(MultipartFile file) throws IOException {
        StreamingReader.builder().open(file.getInputStream());
    }


    public static void main(String[] args) throws Exception {
        StreamingReader.builder().open((new FileInputStream("sample.xlsx")));
    }
}
