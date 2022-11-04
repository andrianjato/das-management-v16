from odoo import models


class DasCalculPlanningReport(models.AbstractModel):
    _name = "report.das.calcul_planning_xlsx"
    _description = "Das Calcul Planning Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):
        first_format = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Calcul planning')
        sheet_col = ['Num', 'Appelation', 'Nom', 'Login Jira', 'Post', 'CAT', 'Dep', 'Ref Name', 'Account', 'Project',
                     'Ref BC',
                     'Project category', 'Client', 'Locality', 'Date',  'Planned H', 'Planned J', 'Project type',
                     'FAC', 'PNF',
                     'INT', 'RH', 'AVV', 'MGT', 'PRV', 'REF DATE']

        for i in range(len(sheet_col)):
            sheet.write(0, i, sheet_col[i], first_format)
            i += 1

        i = 1
        for res_id in lines:
            # num
            sheet.write(i, 0, i)
            # appelation
            sheet.write(i, 1, res_id.resource_id.appelation)
            # Nom
            sheet.write(i, 2, res_id.resource_name)
            # Login_jira
            sheet.write(i, 3, res_id.resource_id.login_jira)
            # Post
            sheet.write(i, 4, res_id.resource_id.job_id.display_name)
            # cat
            sheet.write(i, 5, res_id.account_id.category_id.display_name)
            # centre
            sheet.write(i, 6, res_id.resource_id.department_id.name)
            # ref name
            sheet.write(i, 7, res_id.resource_id.ref_name)
            # compte
            sheet.write(i, 8, res_id.account_id.display_name)
            # projet
            sheet.write(i, 9, res_id.project_id.display_name)
            # ref_bc
            sheet.write(i, 10, res_id.account_id.reference_id.display_name)
            # #project_category
            sheet.write(i, 11, res_id.account_id.category_id.display_name)
            # #client
            sheet.write(i, 12, res_id.project_id.partner_id.display_name)
            # #localite
            sheet.write(i, 13, res_id.account_id.locality)
            # #date
            sheet.write(i, 14, str(res_id.date))
            # Semaine

            # ID : num-date-poste
            # Ferié
            # Planned days (daily hours)
            sheet.write(i, 15, res_id.daily_hours)
            # Planned days J
            sheet.write(i, 16, res_id.daily_hours / 8)
            # sequence : yearweek_num
            # week_num
            # month
            # ref date project
            # Project type : ref-date-project
            sheet.write(i, 17, res_id.type)
            # FAC
            sheet.write(i, 18, res_id.fac_hours)
            # PNF
            sheet.write(i, 19, res_id.pnf_hours)
            # int
            sheet.write(i, 20, res_id.int_hours)
            # RH
            sheet.write(i, 21, res_id.rh_hours)
            # AVV
            sheet.write(i, 22, res_id.avv_hours)
            # MGT
            sheet.write(i, 23, res_id.mgt_hours)
            # PRV
            sheet.write(i, 24, res_id.prv_hours)
            # ref date
            ref_date = str(res_id.resource_id.reference) + '-' + str(res_id.date)
            sheet.write(i, 25, ref_date)

            # IC J
            # IC %

            i += 1


class DasResourceReport(models.AbstractModel):
    _name = "report.das.resource_xlsx"
    _description = "Das Resource Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):
        first_format = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Resource ')
        sheet_col = ['Reference', 'Department', 'Jira login', 'Reg Number', 'Name', 'First name', 'Appelation', 'Job',
                     'Gender', 'Previous Dep', 'Jira name', 'CC key', 'REF_NAME']

        for i in range(len(sheet_col)):
            sheet.write(0, i, sheet_col[i], first_format)
            i += 1

        i = 1
        for res_id in lines:
            # reference
            sheet.write(i, 0, res_id.resource_id.reference)
            # Department
            sheet.write(i, 1, res_id.department_id.name)
            # Login_jira
            sheet.write(i, 2, res_id.resource_id.login_jira)
            # Matricule
            sheet.write(i, 3, res_id.resource_id.registration_number)
            # name
            sheet.write(i, 4, res_id.resource_id.name)
            # first name
            sheet.write(i, 5, res_id.resource_id.first_name)
            # appelation
            sheet.write(i, 6, res_id.resource_id.appelation)
            # Job
            sheet.write(i, 7, res_id.resource_id.job_id.display_name)
            # sexe
            sheet.write(i, 8, res_id.resource_id.gender)
            # Previous department
            sheet.write(i, 9, res_id.resource_id.previous_department_id.name)
            # Jira name
            sheet.write(i, 10, res_id.resource_id.name_jira)
            # Code cc
            sheet.write(i, 11, res_id.resource_id.code_cc)
            # ref name
            sheet.write(i, 12, res_id.resource_id.ref_name)
            i += 1

class DasConsolidationPlanningReport(models.AbstractModel):
    _name = "report.das.consolidation_planning_xlsx"
    _description = "Das Consolidation Planning Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):
        first_format = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Consolidation planning')
        sheet_col = ['Num', 'Department', 'Name', 'Account']

        # Add Column name
        for i in range(len(sheet_col)):
            sheet.write(0, i, sheet_col[i], first_format)
            i += 1

        i = 1
        for res_id in lines:
            # num
            sheet.write(i, 0, i)
            # Department
            sheet.write(i, 1, res_id.department_id.name)
            # name
            sheet.write(i, 2, res_id.resource_id.name)
            # Account
            sheet.write(i, 3, res_id.account_id.display_name)

            i += 1
        #
        # list_date = []
        # for res_id in lines:
        #     list_date.append(res_id.date)
        i = 1
        j = 4
        temp_date = lines[0].date
        for planning in lines:
            # Write same date in same column
            if planning.date != temp_date:
                j += 1
                temp_date = planning.date

            sheet.write(0, j, str(planning.date))
            sheet.write(i, j, planning.daily_hours)
            i += 1




class DasProjectPlanningReport(models.AbstractModel):
    _name = "report.das.project_planning_xlsx"
    _description = "DAS Project Planning Report"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, lines):
        first_format = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Project')
        sheet_col = ['Reference', 'Centre', 'Type', 'Key', 'Jira project', 'Client', 'Category', 'Locality',
                     'BC/Account',
                     'Project Description', 'Responsible', 'Techno', 'Payment condition']

        # Add Column name
        for i in range(len(sheet_col)):
            sheet.write(0, i, sheet_col[i], first_format)
            i += 1

        i = 1
        for res_id in lines:
            # reference
            sheet.write(i, 0, res_id.account_id.reference)
            # Department
            sheet.write(i, 1, res_id.department_id.name)
            # Type
            sheet.write(i, 2, res_id.type)
            # Key
            sheet.write(i, 3, res_id.account_id.key)
            # Jira Project
            sheet.write(i, 4, res_id.project_id.display_name)
            # Customer
            sheet.write(i, 5, res_id.project_id.partner_id.display_name)
            # Category
            sheet.write(i, 6, res_id.account_id.category_id.display_name)
            # Locality
            sheet.write(i, 7, res_id.account_id.locality)
            # BC
            sheet.write(i, 8, res_id.account_id.reference_id.display_name)
            # Project Description
            sheet.write(i, 9, res_id.account_id.description)
            # Responsible
            sheet.write(i, 10, res_id.account_id.responsible_id.display_name)
            # Techno
            sheet.write(i, 11, res_id.account_id.techno)
            # Payment condition
            sheet.write(i, 12, res_id.account_id.payment_condition)
            i += 1
