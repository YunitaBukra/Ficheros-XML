xquery version "3.1";

(: Reporte de departamentos y volumen de empleados :)
let $doc := doc("/home/yen/Documentos/lab1_hr-scheme/data/hrscheme.xml")
return
  <hr_reporte_personal>
    {
      for $dept in $doc/hr_system/departments/department
      let $nombre_dept := $dept/department_name/text()
      let $total_empleados := count($dept/employees/employee)
      
      (: Solo mostramos departamentos que tengan empleados contratados :)
      where $total_empleados > 0
      order by $total_empleados descending
      
      return
        <departamento id="{$dept/@department_id}">
          <nombre>{$nombre_dept}</nombre>
          <total_nominas>{$total_empleados}</total_nominas>
        </departamento>
    }
  </hr_reporte_personal>