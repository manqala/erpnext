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
    elif component.accrual_basis=="Overtime Days":
        query1="Select count(*) employee from `tabOvertime Application` where status='Confirmed' and employee_name='%s' and date<='%s' and date>='%s'"%(emp.employee_name,end_date,start_date)
        result2=frappe.db.sql(query1,as_dict=1)
        result2=int(result2[0].employee)
        return(result2)
    else:
        return None

def frequency_calculator(component,basis):
    while component.accrual_frequency==True:
        if component.accrual_frequency=="Based On Payment Schedule":
            component.default_amoount=component.amount
            component.amount=component.default_amoount*1
            return(component.amount)
        elif component.accrual_frequency=="Daily":
            component.default_amoount=component.amount
            component.amount=component.default_amoount*basis
            return(component.amount)
        elif component.accrual_frequency=="Hourly":
            component.default_amoount=component.amount
            component.amount=component.default_amoount*basis
            return(component.amount)



def get_frequency_and_basis(struc,component_name):
    structure_=frappe.get_doc("Salary Structure",struc)
    for each in structure_.earnings:
        if each.salary_component==component_name:
            return{"accrual_basis":each.accrual_basis,"accrual_frequency":each.accrual_frequency}



@frappe.whitelist()
def comp_calc(duration,employee,structure,rate,start_date,end_date,twd,cur_form):
    return(cur_form)
    # res_li=[]
    # check=verify_employee(structure,employee)
    # if check:
    #     sal_struc=frappe.get_doc("Salary Structure",structure)
    #     emp=frappe.get_doc("Employee",employee)
    #     for each in sal_struc.earnings:
    #         accruals=get_frequency_and_basis(structure,each.salary_component)
    #         res_li.append(accruals)
            # each.update(accurals)
            # result=basis_calculator(each,structure,emp,start_date,end_date,twd,duration)
            # amount_=frequency_calculator(each,result)
        # return(res_li)
            # if each.accrual_basis=="Holidays":
            #     str_comp=emp.company
            #     comp=frappe.get_doc("Company",str_comp)
            #     holiday_list=comp.default_holiday_list
            #     query1="select count(*) holiday_date from `tabHoliday` where holiday_date>='%s' and holiday_date<='%s' and parent='%s'"%(start_date,end_date,holiday_list)
            #     result=frappe.db.sql(query1, as_dict=1)
            #     result=int(result[0].holiday_date)
            #     return(result)
