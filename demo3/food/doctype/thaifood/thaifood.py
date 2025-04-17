
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import get_file
import openpyxl
from io import BytesIO

class ThaiFood(Document):
    pass
# @frappe.whitelist(allow_guest=False)  # หรือถ้าอยากเปิด public -> allow_guest=True
# def upload_thaifood_excel():
#     if "file" not in frappe.request.files:
#         frappe.throw("No file uploaded.")
    
#     file = frappe.request.files["file"]
#     file_content = file.stream.read()

#     workbook = openpyxl.load_workbook(filename=BytesIO(file_content))
#     sheet = workbook.active

#     # อ่าน Header แถวที่ 1
#     headers = [cell.value for cell in sheet[1]]

#     success = 0
#     fail = 0
#     inserted_docs = []
#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         if not any(row):  # ข้ามแถวว่าง
#             continue

#         data = dict(zip(headers, row))

#         try:
#             doc = frappe.new_doc("ThaiFood")
#             doc.foodname = data.get("FoodName")
#             doc.foodtype = data.get("FoodType")
#             # ใส่ฟิลด์อื่นๆตาม Doctype จริงที่คุณมี
#             doc.insert()
#             inserted_docs.append({
#                 "name": doc.name,
#                 "foodname": doc.foodname,
#                 "foodtype": doc.foodtype
#             }) 
#             success += 1
#         except Exception as e:
#             frappe.log_error(message=str(e), title="ThaiFood Import Error")
#             fail += 1

#     return {
#         "success": success,
#         "fail": fail,
#         "inserted_records": inserted_docs
#     }



@frappe.whitelist(allow_guest=False)
def upload_thaifood_excel():
    if "file" not in frappe.request.files:
        frappe.throw("No file uploaded.")
    
    file = frappe.request.files["file"]
    file_content = file.stream.read()

    workbook = openpyxl.load_workbook(filename=BytesIO(file_content))
    sheet = workbook.active

    headers = [cell.value for cell in sheet[1]]

    success = 0
    fail = 0
    import_log = []

    for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):  # start=2 แถวที่ 2 จริง ๆ
        if not any(row):
            continue

        data = dict(zip(headers, row))

        try:
            # ตรวจสอบก่อน insert ว่ามีซ้ำไหม
            if frappe.db.exists("ThaiFood", {"foodname": data.get("FoodName")}):
                import_log.append({
                    "row": idx,
                    "status": "Fail",
                    "message": f"Duplicate Name: ThaiFood {data.get('FoodName')} already exists"
                })
                fail += 1
                continue

            # ถ้าไม่มีซ้ำ Insert ใหม่
            doc = frappe.new_doc("ThaiFood")
            doc.foodname = data.get("FoodName")
            doc.foodtype = data.get("FoodType")
            doc.insert()

            import_log.append({
                "row": idx,
                "status": "Success",
                "message": "Inserted successfully"
            })
            success += 1

        except Exception as e:
            frappe.log_error(message=str(e), title="ThaiFood Import Error")
            import_log.append({
                "row": idx,
                "status": "Fail",
                "message": str(e)
            })
            fail += 1

    return {
        "success": success,
        "fail": fail,
        "import_log": import_log
    }


@frappe.whitelist(allow_guest=False)
def preview_thaifood_excel():
    if "file" not in frappe.request.files:
        frappe.throw("No file uploaded.")

    file = frappe.request.files["file"]
    file_content = file.stream.read()

    workbook = openpyxl.load_workbook(filename=BytesIO(file_content))
    sheet = workbook.active

    headers = [cell.value for cell in sheet[1]]

    preview_data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not any(row):
            continue

        data = dict(zip(headers, row))
        preview_data.append({
            "foodname": data.get("FoodName"),
            "foodtype": data.get("FoodType")
        })

    return {
        "preview": preview_data
    }