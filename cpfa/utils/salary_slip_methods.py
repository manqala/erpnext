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


def basis_calculator(component,structure,emp,start_date,end_date,twd,duration):
    if component.accrual_basis=="Holidays":
        str_comp=emp.company
        comp=frappe.get_doc("Company",str_comp)
        holiday_list=comp.default_holiday_list
        query="select count(*) holiday_date from `tabHoliday` where holiday_date>='%s' and holiday_date<='%s' and parent='%s'"%(start_date,end_date,holiday_list)
        result=frappe.db.sql(query,as_dict=1)
        result=int(result[0].holiday_date)
        return(result)
    elif component.accrual_basis=="Working Days":
        return(int(twd))
    elif component.accrual_basis=="Timesheet":
        return(int(duration))



@frappe.whitelist()
def comp_calc(duration,employee,structure,rate,start_date,end_date,twd):
    check=verify_employee(structure,employee)
    if check:
        sal_struc=frappe.get_doc("Salary Structure",structure)
        emp=frappe.get_doc("Employee",employee)
        res_li=[]
        for each in sal_struc.earnings:
            # if each.accrual_basis=="Holidays":
            #     str_comp=emp.company
            #     comp=frappe.get_doc("Company",str_comp)
            #     holiday_list=comp.default_holiday_list
            #     query1="select count(*) holiday_date from `tabHoliday` where holiday_date>='%s' and holiday_date<='%s' and parent='%s'"%(start_date,end_date,holiday_list)
            #     result=frappe.db.sql(query1, as_dict=1)
            #     result=int(result[0].holiday_date)
            #     return(result)
            res_li.append(basis_calculator(each,structure,emp,start_date,end_date,twd,duration))
        return(res_li)
