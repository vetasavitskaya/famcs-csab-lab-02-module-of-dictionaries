# famcs-csab-lab-01-reporting-module
## Lab 1. Модуль отчетности.
 - шаблон документа в Microsoft Word - [template.docx](https://github.com/vetasavitskaya/famcs-csab-lab-01-reporting-module/blob/main/template.docx)
 - desktop приложение на Python и PyQt5 - [famcs_csab_lab_01_reporting_module.py](https://github.com/vetasavitskaya/famcs-csab-lab-01-reporting-module/blob/main/famcs_csab_lab_01_reporting_module.py)
#### To run on Linux
replace
`os.system('start ' + result_file_name)`
with
`opener = "open" if sys.platform == "darwin" else "xdg-open"
subprocess.call([opener, result_file_name])`
