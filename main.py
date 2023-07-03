import pandas as pd
import os
from login_payerpath import payerpath_login
from get_credential_frm_pgtble import get_conn,SelectQueryToGetDataframe
from checking_eligibility import checking_eligibility, extract_patient_copay,extracting_insudata,checking_eligibility_1,checking_eligibility_2
import glob
import shutil
from GetDataFromQonductor import getapicall
from GetDataFromQonductor import Errorlines, logintoken,get_api_credential
from datetime import date,timezone
import datetime
# today = date.today()
# print(today)
# today = datetime.now(timezone.utc)
# print(today.strftime("%d-%m-%Y"))
# current_time = datetime.now(timezone.utc)
# print(current_time)
# print("Today date is: ", today)
folder_path = os.getcwd() + str('\\') + 'Payer Data'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
else:
    files = glob.glob(folder_path)
    for f in files:
        shutil.rmtree(f)
    os.makedirs(folder_path)

pgdatabase = 'QAutomation'
pgusername = 'postgres'
pgpassword = 'scroll!1234'
pghost = '34.28.196.43'
pgport = '5432'
# create postgres connection
conn = get_conn(pgdatabase, pgusername, pgpassword, pghost, pgport)
dataFrame = SelectQueryToGetDataframe(conn, 'miu_evbv.payerpth_details')
customer_name = ""
payer_pswd = ""
url = ""
# passing payer path credential to login method
for i, rows in dataFrame.iterrows():
    customer_name = rows['cust_name']
    username = rows['username']
    payer_pswd = rows['payer_password']
    url = rows['url']
# reading data from excels file and create dataframe
# df = pd.read_excel(r"C:\Users\roshan.pandav\Documents\test_payerfile.xlsx")
# df = pd.read_excel(r"C:\Users\roshan.pandav\Documents\ev_test.xlsx")
# df = pd.read_excel(r"C:\Users\roshan.pandav\Downloads\test_evbv.xlsx",dtype=str)
# "C:\Users\roshan.pandav\Downloads\testing excel_100-150(06-07-2023).xlsx"
# df = pd.read_excel(r"C:\Users\roshan.pandav\Documents\testfile.xlsx")
# df = pd.read_excel(r"C:\Users\roshan.pandav\Documents\rmp01.xlsx")
df2 = pd.read_excel(r"testfile27.xlsx", dtype=str)
conn = get_conn(pgdatabase, pgusername, pgpassword, pghost, pgport)
apidf = get_api_credential(conn)
print(apidf)
for i, rows in apidf.iterrows():
    myqoneloginurl = rows['myqone_url']
    myqone_UN = rows['myqone_username']
    myqone_PW = rows['myqone_password']
    get_api_url = rows['pp_qonductor_get_url']
headers = logintoken(myqoneloginurl, myqone_UN, myqone_PW)['message']
print('headers',headers)
# cursor = conn.cursor()
df = getapicall(headers, get_api_url)
# checking datafranme is empty
print(df)
driver = payerpath_login(folder_path, customer_name, username, payer_pswd, url)
# checking_eligibility(driver, df)
# result_df = checking_eligibility_1(driver, df)
result_df = checking_eligibility_2(driver, df2)
# print(len(result_df))
# patient_data = extract_patient_copay(driver, df)
# extracting_insudata(driver, df)
print("copay Calculated Successfully....")



