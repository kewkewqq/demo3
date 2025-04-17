
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import get_file
import openpyxl
from io import BytesIO

class ThaiFood(Document):
    pass
@frappe.whitelist(allow_guest=False)  # หรือถ้าอยากเปิด public -> allow_guest=True
def upload_thaifood_excel():
    if "file" not in frappe.request.files:
        frappe.throw("No file uploaded.")
    
    file = frappe.request.files["file"]
    file_content = file.stream.read()

    workbook = openpyxl.load_workbook(filename=BytesIO(file_content))
    sheet = workbook.active

    # อ่าน Header แถวที่ 1
    headers = [cell.value for cell in sheet[1]]

    success = 0
    fail = 0
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not any(row):  # ข้ามแถวว่าง
            continue

        data = dict(zip(headers, row))

        try:
            doc = frappe.new_doc("ThaiFood")
            doc.foodname = data.get("FoodName")
            doc.foodtype = data.get("FoodType")
            # ใส่ฟิลด์อื่นๆตาม Doctype จริงที่คุณมี
            doc.insert()
            success += 1
        except Exception as e:
            frappe.log_error(message=str(e), title="ThaiFood Import Error")
            fail += 1

    return {
        "success": success,
        "fail": fail
    }
