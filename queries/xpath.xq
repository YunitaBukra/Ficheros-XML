(: Consulta XPath para filtrar empleados con salarios altos en el departamento 90 :)
doc("/home/yen/Documentos/lab1_hr-scheme/data/hrscheme.xml")
  /hr_system
  /departments
  /department[@department_id = "90"]
  /employees
  /employee[xs:decimal(salary) > 10000]

