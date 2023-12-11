class SheetsUtils:
    def __init__(self, creds_path=""):
        self.creds_path = creds_path

    def gs_to_dict(self, tab_name, spreadsheet_id):
        gc = gspread.service_account(filename=self.creds_path)
        sh = gc.open_by_key(spreadsheet_id)
        wks = sh.worksheet(tab_name)
        results_json = wks.get_all_records()
        return results_json

    def gs_to_df(self, tab_name, spreadsheet_id):
        json_data = self.gs_to_dict(tab_name, spreadsheet_id)
        gspread_result = sc.parallelize(json_data).toDF()
        return gspread_result

    def gs_to_list(self, tab_name, spreadsheet_id, relevant_key):
        json_data = self.gs_to_dict(tab_name, spreadsheet_id)
        results_list = [result[relevant_key] for result in json_data]
        return results_list
