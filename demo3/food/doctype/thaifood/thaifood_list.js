frappe.listview_settings['ThaiFood'] = {
    onload: function (listview) {
        console.log("✅ ThaiFood ListView loaded");

        listview.page.add_inner_button('Import Excel', () => {
            const dialog = new frappe.ui.Dialog({
                title: 'Import ThaiFood from Excel',
                fields: [
                    {
                        label: 'Excel File',
                        fieldname: 'excel_file',
                        fieldtype: 'Attach',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Import',
                primary_action(values) {
                    frappe.call({
                        method: 'demo3.food.doctype.thaifood.thaifood.import_thaifood_excel',
                        args: {
                            file_url: values.excel_file
                        },
                        callback: function (r) {
                            frappe.msgprint(__('Imported: ') + r.message.imported + ' rows');
                            dialog.hide();
                            frappe.set_route('List', 'ThaiFood');
                        },
                        error: function () {
                            frappe.msgprint(__('Import failed'));
                        }
                    });
                }
            });

            dialog.show();
        });
    }
};
