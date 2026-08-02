package org.joychou.controller.office;

import org.apache.poi.xssf.usermodel.XSSFCell;
import org.apache.poi.xssf.usermodel.XSSFRow;
import org.apache.poi.xssf.usermodel.XSSFSheet;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Iterator;



@Controller
@RequestMapping("/office/ooxml")
public class OoxmlReader {


    private final Logger logger = LoggerFactory.getLogger(this.getClass());


    @GetMapping("/upload")
    public String index() {
        return "doc_upload";
    }


    @PostMapping("/readxlsx")
    @ResponseBody
    public String readOoxml(MultipartFile file) throws IOException {
        XSSFWorkbook wb = new XSSFWorkbook(file.getInputStream());

        XSSFSheet sheet = wb.getSheetAt(0);
        XSSFRow row;
        XSSFCell cell;

        Iterator rows = sheet.rowIterator();
        StringBuilder sbResult = new StringBuilder();

        while (rows.hasNext()) {

            row = (XSSFRow) rows.next();
            Iterator cells = row.cellIterator();

            while (cells.hasNext()) {
                cell = (XSSFCell) cells.next();

                if (cell.getCellType() == XSSFCell.CELL_TYPE_STRING) {
                    sbResult.append(cell.getStringCellValue()).append(" ");
                } else if (cell.getCellType() == XSSFCell.CELL_TYPE_NUMERIC) {
                    sbResult.append(cell.getNumericCellValue()).append(" ");
                } else {
                    logger.info("errors");
                }
            }
        }

        return sbResult.toString();
    }
}
