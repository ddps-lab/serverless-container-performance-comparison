import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def open_sheet(spreadsheet_key):
  scope = [
      'https://spreadsheets.google.com/feeds'
  ]
  cred_json_file_name = get_file_path('sheet_credential.json')
  credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_json_file_name,scope)
  gc = gspread.authorize(credentials)
  doc = gc.open_by_key(spreadsheet_key)
  return doc