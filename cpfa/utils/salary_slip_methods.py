import frappe

def verify_employee(salary_structure,employee):
    struc=frappe.get_doc("Salary Structure",salary_structure)
    employee_=frappe.get_doc("Employee",employee)
    box=[]
    if struc.is_active=="Yes":
        for i in struc.employees:
            if i.employee==employee_.name:
                box.append(True)
            else:
                box.append(False)
        if True in box:
            return(True)
        else:
            return(False)
    frappe.throw("The salary structure is not active")

@frappe.whitelist()
def comp_based_on_timesheet(duration,employee,structure,rate):
checker=verify_employee(structure,employee)
if checker:
    sal_struc=frappe.get_doc("Salary Structure",structure)
    emp=frappe.get_doc("salary_structure",employee)
    for each in sal_struc.earnings:
        if each.depends_on_timesheet_:
            
