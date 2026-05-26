import csv
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def transformar_csv_a_xml():
    # 1. OBJETIVO: Saber dónde está este script físicamente.
    # Como está en 'scripts/', script_dir representará la ruta absoluta a la carpeta 'scripts'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. OBJETIVO: Localizar la carpeta 'data_raw' subiendo un nivel ('..') y entrando a 'data_raw'
    data_raw_dir = os.path.abspath(os.path.join(script_dir, '..', 'data_raw'))
    
    # Mapeo exacto de los archivos de entrada (CSV) en 'data_raw'
    csv_departments = os.path.join(data_raw_dir, 'departments.csv')
    csv_employees = os.path.join(data_raw_dir, 'employees.csv')
    csv_job_history = os.path.join(data_raw_dir, 'job_history.csv')
    
    # Mapeo del archivo de salida (XML) en la misma carpeta 'scripts'
    output_xml = os.path.join(script_dir, 'hrscheme.xml')
    
    print(f"Ruta del script / Salida XML: {script_dir}")
    print(f"Buscando los CSV en: {data_raw_dir}")
    
    # Validar que los archivos existan antes de abrirlos para evitar caídas
    if not os.path.exists(csv_departments):
        print(f"Error crítico: No se encontró el archivo {csv_departments}. Verifica el nombre.")
        return

    print("Leyendo archivos CSV...")
    
    # Cargar Departamentos
    departments = []
    with open(csv_departments, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            departments.append(row)
            
    # Cargar Empleados agrupándolos por su DEPARTMENT_ID
    employees_by_dept = {}
    with open(csv_employees, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dept_id = row.get('DEPARTMENT_ID', '').strip()
            if not dept_id:
                dept_id = "None"
            if dept_id not in employees_by_dept:
                employees_by_dept[dept_id] = []
            employees_by_dept[dept_id].append(row)
            
    # Cargar Historial Laboral agrupándolo por EMPLOYEE_ID
    history_by_emp = {}
    with open(csv_job_history, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            emp_id = row.get('EMPLOYEE_ID', '').strip()
            if emp_id not in history_by_emp:
                history_by_emp[emp_id] = []
            history_by_emp[emp_id].append(row)

    print("Construyendo la estructura jerárquica XML...")
    root = ET.Element('departments')
    
    for dept in departments:
        dept_id = dept.get('DEPARTMENT_ID', '').strip()
        dept_el = ET.SubElement(root, 'department', {'department_id': dept_id})
        
        ET.SubElement(dept_el, 'department_name').text = dept.get('DEPARTMENT_NAME', '')
        
        manager_id = dept.get('MANAGER_ID', '').strip()
        if manager_id:
            ET.SubElement(dept_el, 'manager_id').text = manager_id
            
        ET.SubElement(dept_el, 'location_id').text = dept.get('LOCATION_ID', '')
        
        # Integrar empleados
        dept_emps = employees_by_dept.get(dept_id, [])
        if dept_emps:
            employees_el = ET.SubElement(dept_el, 'employees')
            for emp in dept_emps:
                emp_id = emp.get('EMPLOYEE_ID', '').strip()
                emp_el = ET.SubElement(employees_el, 'employee', {'employee_id': emp_id})
                
                ET.SubElement(emp_el, 'first_name').text = emp.get('FIRST_NAME', '')
                ET.SubElement(emp_el, 'last_name').text = emp.get('LAST_NAME', '')
                ET.SubElement(emp_el, 'email').text = emp.get('EMAIL', '')
                ET.SubElement(emp_el, 'phone_number').text = emp.get('PHONE_NUMBER', '')
                ET.SubElement(emp_el, 'hire_date').text = emp.get('HIRE_DATE', '')
                ET.SubElement(emp_el, 'job_id').text = emp.get('JOB_ID', '')
                
                salary = emp.get('SALARY', '').strip()
                if salary:
                    ET.SubElement(emp_el, 'salary').text = salary
                    
                comm = emp.get('COMMISSION_PCT', '').strip()
                if comm:
                    ET.SubElement(emp_el, 'commission_pct').text = comm
                    
                emp_m_id = emp.get('MANAGER_ID', '').strip()
                if emp_m_id:
                    ET.SubElement(emp_el, 'manager_id').text = emp_m_id
                    
                # Integrar el historial laboral
                emp_hist = history_by_emp.get(emp_id, [])
                for hist in emp_hist:
                    hist_el = ET.SubElement(emp_el, 'job_history')
                    ET.SubElement(hist_el, 'start_date').text = hist.get('START_DATE', '')
                    ET.SubElement(hist_el, 'end_date').text = hist.get('END_DATE', '')
                    ET.SubElement(hist_el, 'job_id').text = hist.get('JOB_ID', '')
                    ET.SubElement(hist_el, 'department_id').text = hist.get('DEPARTMENT_ID', '')

    print("Formateando el XML (Pretty Print)...")
    xml_raw = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_raw)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    
    # Eliminar líneas vacías duplicadas por minidom
    clean_xml = "\n".join([line for line in pretty_xml.split('\n') if line.strip()])
    
    # Guardar en la carpeta 'scripts/'
    with open(output_xml, 'w', encoding='utf-8') as f:
        f.write(clean_xml)
        
    print(f"¡Hecho! Archivo XML generado exitosamente en: {output_xml}")

if __name__ == '__main__':
    transformar_csv_a_xml()