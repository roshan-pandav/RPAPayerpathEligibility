import pandas as pd
import os
from login_payerpath import payerpath_login
from get_credential_frm_pgtble import get_conn,SelectQueryToGetDataframe
from checking_eligibility import checking_eligibility, extract_patient_copay,extracting_insudata
import glob
import shutil
from datetime import date

today = date.today()
print(today.strftime("%d-%m-%Y"))

print("Today date is: ", today)
folder_path = os.getcwd() + str('\\') + 'Payer Data'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
else:
    files = glob.glob(folder_path)
    for f in files:
        shutil.rmtree(f)
    os.makedirs(folder_path)

database = 'QAutomation'
username = 'postgres'
password = 'scroll!1234'
host = '34.28.196.43'
port = '5432'

# create postgres connection
conn = get_conn(database, username, password, host, port)
dataFrame = SelectQueryToGetDataframe(conn, 'payerpath_credential.payerpth_details')
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
df = pd.read_excel(r"C:\Users\roshan.pandav\Documents\testfile.xlsx")
print(df)
# for i, rows in df.iterrows():
#     f_name = str(rows['Patient First Name'])
#     l_name = str(rows['Patient Last Name'])
#     dob = str(rows['Patient DOB'])
#     dob1=dob.split(" ")[0]
#     dob2=dob1.split("-")
#     dd=dob2[2]
#     mm=dob2[1]
#     yy=dob2[0]
#     patient_dob=f"{mm}/{dd}/{yy}"
#     print(patient_dob)
    # dob=dob
    # print(type(dob))
    # print("conver dte")

driver = payerpath_login(folder_path, customer_name, username, payer_pswd, url)
# checking_eligibility(driver, df)
patient_data = extract_patient_copay(driver, df)

# extracting_insudata(driver, df)
print("copay Calculated Successfully....")



