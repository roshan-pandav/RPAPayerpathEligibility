import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
import json

def waits(el, driver):
    """
    This function waits robotscraper until element given in the argument loads
    :param el: element of interest
    :return: None
    """
    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, el)))

def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = False
    while dl_wait != True and seconds < 60:
        time.sleep(1)
        files_in_directory = os.listdir(path_to_downloads)
        filtered_files = [file for file in files_in_directory if (file.startswith("export"))]
        print(len(filtered_files) == 1)
        if len(filtered_files) == 1:
            dl_wait = True
        seconds += 1
    return dl_wait

def checking_eligibility(driver, df):
    try:
        for i, rows in df.iterrows():
            try:
                f_name = str(rows['Patient First Name'])
                l_name = str(rows['Patient Last Name'])
                policy_id=str(rows['Policy_id'])

                dob = str(rows['Patient DOB'])
                dob1 = dob.split(" ")[0]
                dob2 = dob1.split("-")
                dd = dob2[1]
                dd=str(int(dd)+1)

                mm = dob2[2]
                yy = dob2[0]
                patient_dob = f"{mm}/{dd}/{yy}"
                print(patient_dob)

                insu_name=str(rows['Patient Primary Insur'])

                # p_name = str(rows['Patient Name']).split(" ")
                # p_firstname = p_name[1]
                # p_lastname = p_name[0]
                # insu_id = str(rows['Policy Id'])
                # insu_name = str(rows['Insurance '])
                # dob = (rows['DOB'])
                # gender = rows['Gender']
                # date_time = dob.strftime("%m/%d/%Y")
                # dob = str(date_time).replace("-", "/")
                # print(dob)
                waits("//iframe[@src='/EligibilityUI/Transaction']", driver)
                time.sleep(2)
                frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
                driver.switch_to.frame(frm)
                time.sleep(3)
                waits("(//label[@class='tool-bar-dropbtn'])[1]", driver)
                loc = driver.find_element(by=By.XPATH, value="(//label[@class='tool-bar-dropbtn'])[1]")
                print("Loc", loc)
                time.sleep(1)
                hover = ActionChains(driver).move_to_element(loc)
                hover.perform()
                driver.find_element(by=By.XPATH, value="//li[@id='ActionId_0']").click()
                waits("//img[@id='PayerNameImgId']",driver)
                driver.find_element(by=By.XPATH, value="//img[@id='PayerNameImgId']").click()
                time.sleep(3)
                # driver.find_element(by=By.XPATH, value='//*[@id="quickFilter"]').click()
                # driver.find_element(by=By.XPATH, value='//*[@id="quickFilter"]').send_keys(insu_name)
                driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input").click()
                driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input").send_keys(insu_name)
                time.sleep(2)
                driver.find_element(by=By.XPATH, value="/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[3]/div[2]/div/div/div/div[1]/div/div/div/div[2]/input").click()
                time.sleep(3)
                # click on OK button for selecting insurance name
                element = driver.find_element(by=By.XPATH,value="//div[@class='benefit-payment']//div[@class='border-top center']//button[1]")
                try:
                    if element.is_enabled():
                        time.sleep(5)
                        element.click()
                    else:
                        pass
                except Exception as Error:
                    print(Error)
                    print("Submit button not clickable")
                time.sleep(5)
                driver.find_element(by=By.XPATH, value="//input[@id='DependentFirstNameId']").send_keys(l_name)
                driver.find_element(by=By.XPATH, value="//input[@id='DependentLastNameId']").send_keys(f_name)
                driver.find_element(by=By.XPATH, value="//input[@id='DependentDOBInputId']").send_keys(patient_dob)

                # select gender from excel
                # Gender=Select(driver.find_element(by=By.XPATH,value="//select[@id='DependentGenderId']"))
                # Gender.select_by_visible_text(gender)
                driver.find_element(by=By.XPATH, value="//input[@id='PolicyIdId']").send_keys(policy_id)
                time.sleep(1)
                waits("//*[@id='Last Name/OrgId']", driver)
                driver.find_element(by=By.XPATH, value="//*[@id='Last Name/OrgId']").send_keys("MICHIGAN INSTITUTE OF UROLOGY PC")
                driver.find_element(by=By.XPATH, value="//input[@id='ProviderNPIId']").click()
                driver.find_element(by=By.XPATH, value="//input[@id='ProviderNPIId']").send_keys("1427027416")
                time.sleep(1)
                driver.find_element(by=By.XPATH, value='//*[@id="PolicyGroupId"]').click()
                # click on Submit the eligibility request
                driver.find_element(by=By.XPATH, value='//*[@id="submitRequest"]').click()
                time.sleep(8)
                driver.switch_to.default_content()
            except:
                continue
    except Exception as error:
        print(error)

# optional functionality if needed
def downloadfile(driver, folder_path):
    try:
        frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
        driver.switch_to.frame(frm)
        time.sleep(5)
        sel = Select(driver.find_element(by=By.XPATH, value='// *[ @ id = "date-range-select"]'))
        sel.select_by_index(0)
        time.sleep(5)
        driver.find_element(by=By.XPATH, value='//img[@title="Export to CSV file."]').click()
        time.sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@id="okMessage"]').click()
        file_download_status = download_wait(folder_path)
        print(file_download_status)
        return file_download_status
    except Exception as error:
        print(error)

def extract_patient_copay(driver, df):
    """
    :param driver: chrome driver
    :param df: dataframe iterate to find active coverage
    :return: return Copay value
    """
    try:
        time.sleep(5)
        frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
        driver.switch_to.frame(frm)
        # time.sleep(2)
        sel = Select(driver.find_element(by=By.XPATH, value='// *[ @ id = "date-range-select"]'))
        sel.select_by_index(4)
        # lst = ['R58710106']
        for i,row in df.iterrows():
            try:
                policy_id = str(row['Policy_id'])
                network_list = []
                benefit_list = []
                amount_list = []
                details_list = []
                email_dict = {}
                # insu_id = str(row['Policy Id'])
                try:
                    # need to find alterate Xpath
                    print("Clear Search Window")
                    waits("//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']",driver)
                    driver.find_element(by=By.XPATH, value= "//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']").clear()
                    time.sleep(1)
                    print("Search Patient by ID")
                    driver.find_element(by=By.XPATH, value= "//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']").send_keys(policy_id)
                    time.sleep(5)
                except:
                    print("No record found")
                    continue
                try:
                    # element = driver.find_element(by=By.XPATH, value="//img[@alt='Active Coverage']")
                    element = driver.find_element(by=By.XPATH, value="/html/body/app-root/transaction/div[2]/div[2]/transaction-list/ag-grid-angular[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div[7]/result-cell-renderer/a/div/img")
                    status = element.get_attribute("alt")
                    print(status)
                except:
                    continue
                if status != 'Active Coverage':
                    status=status.split('\n')[0]
                    df.loc[i, 'pp_coverage']=status
                    df.loc[i,'pp_current_plan_name'] = ""
                    df.loc[i,'pp_copayment'] = ""
                    # df['pp_coverage'] = status
                    continue
                else:
                    df.loc[i, 'pp_coverage'] = status
                    time.sleep(2)
                    # driver.find_element(by=By.XPATH, value="//img[@alt='Active Coverage']").click()
                    driver.find_element(by=By.XPATH,
                                        value="/html/body/app-root/transaction/div[2]/div[2]/transaction-list/ag-grid-angular[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div[7]/result-cell-renderer/a/div/img").click()

                    driver.find_element(by=By.XPATH, value="//*[@id='details-header']").click()
                    driver.find_element(by=By.XPATH, value="//button[@id='expand-all-header']").click()
                    driver.find_element(by=By.XPATH, value="//*[@id='collapse-all-header']").click()
                    # Extracting Plan name
                    time.sleep(5)
                    print(".......Extracting Insurance Information.......")
                    insurance_info = driver.find_element(by=By.XPATH,
                                                         value="//span[normalize-space()='Insurance Information']").text
                    if insurance_info == 'Insurance Information':
                        driver.find_element(by=By.XPATH,
                                            value="//span[normalize-space()='Insurance Information']").click()
                        try:
                            current_plan_name = driver.find_element(by=By.XPATH,
                                                                    value="//*[@id='insuranceinformation-currenthealthplan-value']").text
                            # current_plan.append(current_plan_name)
                            df.loc[i, 'pp_current_plan_name'] = current_plan_name
                            # df['pp_current_plan_name'] = current_plan_name
                            # print(current_plan)
                        except:
                            current_plan_name = ""
                            # current_plan.append(current_plan_name)
                            df.loc[i, 'pp_current_plan_name'] = current_plan_name
                            # print(current_plan)
                    # Extracting Copayment Information
                    try:
                        waits("//span[normalize-space()='Professional (Physician) Visit - Office']", driver)
                        driver.find_element(by=By.XPATH, value="//span[normalize-space()='Professional (Physician) Visit - Office']").click()
                    except:
                        continue
                    time.sleep(3)
                    # length = driver.find_elements(by=By.XPATH, value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
                    # change xpath for testing
                    # waits("//div[@class='table benefit-detail-table']//following-sibling::div[@class='benefits row']",driver)
                    length = driver.find_elements(by=By.XPATH,
                                                  value="//div[@class='table benefit-detail-table']//following-sibling::div[@class='benefits row']")
                    container = len(length)
                    print("Length of DataFrame",container)
                    for j in range(1, container + 1):
                        print("loop1")
                        # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
                        time.sleep(2)
                        # driver.find_element(by=By.XPATH,value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{j}]").click()
                        driver.find_element(by=By.XPATH,
                                            value=f"//div[@class='table benefit-detail-table']//following-sibling::div[@class='benefits row'][{j}]").click()
                        print("loop2")
                        time.sleep(0.5)
                        benefit = driver.find_element(by=By.XPATH, value=f'//div[@class="benefits row"][{j}]/child::div[@class="benefit-b"]')
                        if benefit.text != 'Co-Payment':
                            continue
                        print("loop3")
                        time.sleep(0.5)
                        detail = driver.find_element(by=By.XPATH, value=f'//div[@class="benefits row"][{j}]/child::div[@class="benefit-d"]')
                        print("loop4")
                        time.sleep(0.5)
                        network = driver.find_element(by=By.XPATH, value=f'//div[@class="benefits row"][{j}]/child::div[@class="benefit-n"]')
                        time.sleep(0.5)
                        print("loop5")
                        amount = driver.find_element(by=By.XPATH, value=f'//div[@class="benefits row"][{j}]/child::div[@class="benefit-q"]')
                        copay = benefit.text
                        if copay == "Co-Payment":
                            benefit_list.append(benefit.text)
                            details_list.append(detail.text)
                            network_list.append(network.text)
                            amount_list.append(amount.text)

                    email_dict['Network'] = network_list
                    email_dict['Benefits'] = benefit_list
                    email_dict['Amounts'] = amount_list
                    email_dict['Details'] = details_list
                    data = pd.DataFrame(email_dict)
                    copay = calculate_co_pay(data)
                    if copay == '$0.0':
                        df.loc[i, 'pp_copayment'] = copay
                    else:
                        df.loc[i, 'pp_copayment'] = copay
                    print(copay)
                    print(df)
                    # Extracting Subscriber Patient Information
                    # time.sleep(3)
                    # # waits("//span[normalize-space()='Subscriber']",driver)
                    # driver.find_element(by=By.XPATH, value="//span[normalize-space()='Subscriber']").click()
                    #
                    # # driver.find_element(by=By.XPATH,value='/html/body/app-root/transaction-details/div/div[2]/div[1]/div[3]/div[3]/div/key-value/div/span').click()
                    # time.sleep(1)
                    # size = driver.find_elements(by=By.XPATH,
                    #                             value="//legend[@id='subscriber-section']/following-sibling::div/div[@class='key-value-row']")
                    # print("Length of Size", len(size))
                    # length1 = len(size)
                    # print(type(size))
                    #
                    # for i in range(1):
                    #     # Retriving Patient name
                    #
                    #     key_name = driver.find_element(by=By.XPATH,value="//*[@id='subscriber-name-key']").text
                    #     print(key_name)
                    #     # driver.find_element(by=By.XPATH,
                    #     #                     value=f"//legend[@id='subscriber-section']/following-sibling::div/div[@class='key-value-row'][{i}]").click()
                    #
                    #     patient_name = driver.find_element(by=By.XPATH, value='//*[@id="subscriber-name-value"]')
                    #     print(patient_name.text)
                    #
                    #     # retriving Patient Date of Birth
                    #     dob = driver.find_element(by=By.XPATH,value="//*[@id='subscriber-dateofbirth-key']").text
                    #     print(dob)
                    #     patient_date = driver.find_element(by=By.XPATH,value="//*[@id='subscriber-dateofbirth-value']").text
                    #     print(patient_date)
                    #     print(dob, patient_date)
                    #
                    #     # Getting Patient address
                    #     address_1 = driver.find_element(by=By.XPATH, value="//div[@id='subscriber-address-value']")
                    #     address_1 = address_1.text
                    #     address_2 = driver.find_element(by=By.XPATH, value="//div[@id='subscriber--value']")
                    #     address_2 = address_2.text
                    #     full_address = address_1 + "\n" + address_2
                    #     print(full_address)
                    #     #extracting the gender data
                    #     gen=driver.find_element(by=By.XPATH,value="//*[@id='subscriber-gender-key']").text
                    #     gen2=driver.find_element(by=By.XPATH,value="// *[@id='subscriber-gender-value']").text
                    #     print(gen,gen2)
                    # Back to list and search another patient
                    var = driver.find_element(by=By.XPATH, value="//button[@id='list-header']")
                    var.click()
                    time.sleep(2)
            except:
                print("Skip patient")
                continue
        df.to_csv("test7.csv")
    except Exception as error:
        print("There was exception while calculating copay")
        print(error)
        return "error"

def calculate_co_pay(df):
    print(df)
    sp_list = []
    for i, row in df.iterrows():
        if 'Specialist' in row['Details'] or 'SPECIALIST' in row['Details']:
            if 'In Network' in row['Network']:
                sp_list.append(row['Amounts'])
            elif 'Not Applicable' in row['Network']:
                sp_list.append(row['Amounts'])
    if sp_list:
        copay = max(sp_list)
    else:
        copay = '$0.0'
    return copay

def extracting_insudata(driver, df):

    time.sleep(5)
    frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
    driver.switch_to.frame(frm)
    time.sleep(2)
    sel = Select(driver.find_element(by=By.XPATH, value='// *[ @ id = "date-range-select"]'))
    sel.select_by_index(4)

    patient_name=""
    revieved_date=""
    # payer_list
    payer_name = []
    payer_id_no = []

    # Alert/Notification
    patient_info_change_status_list=[]
    group_no_in_alert_list = []
    deductible_value_list = []
    provider_npi_in_transaction_list =[]

    # trasaction Information
    tansaction_date_list=[]
    provider_name_list1=[]
    Payerpath_TRN_list=[]
    payer_TRN_list=[]
    # provider organization
    provider_name_list=[]
    provider_address_list=[]
    provider_npi_list=[]
    provider_TRN_list=[]

    # Insurance list
    subscriber_id = []
    current_plan = []
    coverage_list=[]
    plan_date_list1 = []

    # Subscriber List
    S_name = []
    S_DOB = []
    S_gender=[]
    S_address=[]
    S_group_no=[]
    plan_number_list=[]
    plan_date_list=[]
    service_date_list=[]
    S_Plan_Dates=[]
    # copayment List
    copay=[]

    benefit_list=[]
    details_list=[]
    network_list=[]
    amount_list=[]

    # benefit_list_1=[]
    # details_list_1=[]
    # network_list_1=[]
    # amount_list_1=[]

    benefit_list_c = []
    details_list_c = []
    network_list_c = []
    amount_list_c = []

    benefit_list_o=[]
    details_list_o=[]
    network_list_o=[]
    amount_list_o=[]

    benefit_list_w=[]
    details_list_w=[]
    network_list_w=[]
    amount_list_w=[]

    benefit_list_u=[]
    details_list_u=[]
    network_list_u=[]
    amount_list_u=[]

    lst = ['JXP894049784']
    for item in lst:
        print(item)
        try:
            # need to find alterate Xpath
            print("Clear Search Window")
            waits(
                "//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']",
                driver)
            driver.find_element(by=By.XPATH,
                                value="//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']").clear()
            time.sleep(1)
            print("Search Patient by ID")
            driver.find_element(by=By.XPATH,
                                value="//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']").send_keys(
                item)
            time.sleep(5)
        except:
            print("No record found")
            continue
        try:
            element = driver.find_element(by=By.XPATH, value="//img[@alt='Active Coverage']")
            status = element.get_attribute("alt")
            print(status)
        except:
            continue
        if status != 'Active Coverage':
            continue
        else:
            time.sleep(2)
            driver.find_element(by=By.XPATH, value="//img[@alt='Active Coverage']").click()
            driver.find_element(by=By.XPATH, value="//*[@id='details-header']").click()
            driver.find_element(by=By.XPATH, value="//button[@id='expand-all-header']").click()
            driver.find_element(by=By.XPATH, value="//*[@id='collapse-all-header']").click()

            # getting patient name
            patient_name=driver.find_element(by=By.XPATH,value="//span[contains(@class,'text')]//b").text
            print(patient_name)
            revieved_date=driver.find_element(by=By.XPATH,value="//div[@class='border-btm header-div'][3]").text
            revieved_date=revieved_date.split(":")[1]
            print(revieved_date)

            waits("//span[normalize-space()='Subscriber']", driver)
            # patient_name=driver.find_element(by=By.XPATH,value="//body[1]/app-root[1]/transaction-summary[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]").text
            # print(patient_name)
            # getting payer information
            print("........Extracting Payer Information......")
            # tab_name = ["Payer"]
            driver.find_element(by=By.XPATH, value="//span[normalize-space()='Payer']").click()
            time.sleep(2)
            driver.find_element(by=By.XPATH,value="//div[@class='key-value-table']").click()
            table=driver.find_elements(by=By.XPATH,value="//div[@class='key-value-table']//div[@class='key-value-row']")
            size=len(table)
            print(size)

            # for i in size:
            #     pass

            payer = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Payer']").text


            if payer == 'Payer':
                try:
                    driver.find_element(by=By.XPATH,value="//span[normalize-space()='Payer']").click()
                    p_name = driver.find_element(by=By.XPATH,value="//div[@id='payer-payer-value']").text
                    print(payer_name)
                    payer_name.append(p_name)
                    print(payer_name)
                    p_identitification = driver.find_element(by=By.XPATH,
                                                             value="//div[@id='payer-payoridentification-value']").text
                    payer_id_no.append(p_identitification)
                    print(payer_id_no)
                except:
                    p_name = " "
                    payer_name.append(p_name)
                    p_identitification=" "
                    payer_id_no.append(p_identitification)
                    print(payer_name)
                    print(payer_id_no)
            else:
                p_name = " "
                payer_name.append(p_name)
                p_identitification = " "
                payer_id_no.append(p_identitification)
                print(payer_name)
                print(payer_id_no)

            # Extracting Alert Notification tab
            AlertNotification = driver.find_element(by=By.XPATH,value="//span[@class='legend']").text
            if AlertNotification == 'Alerts/Notifications':
               driver.find_element(by=By.XPATH,value="//span[@class='legend']").click()
               try:
                   patient_info_change_status1=driver.find_element(by=By.XPATH,value="//*[@id='alertsnotifications-patientinformationchange-value']").text
                   print(patient_info_change_status1)
                   patient_info_change_status = str(patient_info_change_status1.split('\n')[0])
                   patient_info_change_status = patient_info_change_status.replace("'","")
                   print(patient_info_change_status)
                   patient_info_change_status_list.append(patient_info_change_status)
                   print(patient_info_change_status)
               except:
                   patient_info_change_status=""
                   patient_info_change_status_list.append(patient_info_change_status)

               try:
                   group_no=driver.find_element(by=By.XPATH,value="//div[@id='alertsnotifications-groupnumber-msg-3']").text
                   group_no_in_alert_list.append(group_no)
                   print(group_no)
               except:
                   group_no = ""
                   group_no_in_alert_list.append(group_no)
               try:
                   deductible_value=driver.find_element(by=By.XPATH,value="//*[@id='alertsnotifications-deductiblealert-value']").text
                   deductible_value_list.append(deductible_value)
               except:
                   deductible_value=""
                   deductible_value_list.append(deductible_value)
            # Extracting Transation Information
            transation_information = driver.find_element(by=By.XPATH,value="//span[normalize-space()='Transaction Information']").text
            if transation_information == "Transaction Information":
                driver.find_element(by=By.XPATH, value="//span[normalize-space()='Transaction Information']").click()
                try:
                    transaction_date=driver.find_element(by=By.XPATH,value="//div[@id='transactioninformation-transactiondate-value']").text
                    tansaction_date_list.append(transaction_date)
                    print(transaction_date)
                except:
                    transaction_date=""
                    tansaction_date_list.append(transaction_date)

                try:
                    provider_name=driver.find_element(by=By.XPATH,value="//*[@id='transactioninformation-providername-value']").text
                    provider_name_list1.append(provider_name)
                except:
                    provider_name=""
                    provider_name_list1.append(provider_name)

                try:
                    npi1=driver.find_element(by=By.XPATH,value="//*[@id='transactioninformation-npi-value']").text
                    provider_npi_in_transaction_list.append(npi1)
                    print(npi1)
                except:
                    npi1=""
                    provider_npi_in_transaction_list.append(npi1)
                try:
                    Payerpath_TRN = driver.find_element(by=By.XPATH,value="//*[@id='transactioninformation-payerpathtrn-value']").text
                    Payerpath_TRN_list.append(Payerpath_TRN)
                    print(Payerpath_TRN)
                except:
                    Payerpath_TRN = ""
                    Payerpath_TRN_list.append(Payerpath_TRN)
                try:
                    Provider_TRN = driver.find_element(by=By.XPATH,value="//*[@id='transactioninformation-providertrn-value']").text
                    provider_TRN_list.append(Provider_TRN)
                    print(Provider_TRN)
                except:
                    Provider_TRN = ""
                    provider_TRN_list.append(Provider_TRN)
                try:
                    payer_TRN = driver.find_element(by=By.XPATH,value="//*[@id='transactioninformation-payertrn-value']").text
                    payer_TRN_list.append(payer_TRN)
                    print(payer_TRN)
                except:
                    payer_TRN = ""
                    payer_TRN_list.append(payer_TRN)

            # getting provider Organization/Organization
            provider_info=driver.find_element(by=By.XPATH,value="//span[normalize-space()='Provider/Organization']").text
            if provider_info == 'Provider/Organization':
                driver.find_element(by=By.XPATH, value="//span[normalize-space()='Provider/Organization']").click()
                try:
                    name=driver.find_element(by=By.XPATH,value="//*[@id='providerorganization-name-value']").text
                    provider_name_list.append(name)
                except:
                    name=""
                    provider_name_list.append(name)
                try:
                    address1=driver.find_element(by=By.XPATH, value="//*[@id='providerorganization-address-value']").text
                    address2=driver.find_element(by=By.XPATH, value="//*[@id='providerorganization--value']").text
                    full_address = address1 + "\n" + address2
                    provider_address_list.append(full_address)
                except:
                    full_address=""
                    provider_address_list.append(full_address)
                try:
                    provider_npi=driver.find_element(by=By.XPATH, value="//*[@id='providerorganization-cmsnpi-value']").text
                    provider_npi_list.append(provider_npi)
                except:
                    provider_npi=""
                    provider_npi_list.append(provider_npi)

            # getting information information
            print(".......Extracting Insurance Information.......")
            insurance_info = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Insurance Information']").text
            if insurance_info == 'Insurance Information':
                driver.find_element(by=By.XPATH,value="//span[normalize-space()='Insurance Information']").click()
                try:
                    subsciber_id1 = driver.find_element(by=By.XPATH,value="//div[@id='insuranceinformation-subscriberid-value']").text
                    subscriber_id.append(subsciber_id1)
                    print(subscriber_id)
                except:
                    subsciber_id1=" "
                    subscriber_id.append(subsciber_id1)
                    print(subscriber_id)
                try:
                    current_plan_name=driver.find_element(by=By.XPATH,value="//*[@id='insuranceinformation-currenthealthplan-value']").text
                    current_plan.append(current_plan_name)
                    print(current_plan)
                except:
                    current_plan_name = ""
                    current_plan.append(current_plan_name)
                    print(current_plan)
                try:
                    plan_date=driver.find_element(by=By.XPATH,value="//*[@id='insuranceinformation-plandate-value']").text
                    plan_date_list1.append(plan_date)
                except:
                    plan_date=""
                    plan_date_list1.append(plan_date)
            #  Adding Coverage
                try:
                 coverage_type=driver.find_element(by=By.XPATH,value="//*[@id='insuranceinformation-coverage-value']").text
                 coverage_list.append(coverage_type)
                except:
                    coverage_type=""
                    coverage_list.append(coverage_type)

            # Getting the Subcriber information
            print(".....Extracting Subscriber Information......")
            Subcriber = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Subscriber']").text
            if Subcriber == 'Subscriber':
                driver.find_element(by=By.XPATH, value="//span[normalize-space()='Subscriber']").click()
                try:
                    patient_name = driver.find_element(by=By.XPATH, value='//*[@id="subscriber-name-value"]').text
                    # print(patient_name.text)
                    S_name.append(patient_name)
                except:
                    patient_name = ""
                    S_name.append(patient_name)
                try:
                    address_1 = driver.find_element(by=By.XPATH,value="//div[@id='subscriber-address-value']")
                    address_1 = address_1.text
                    address_2 = driver.find_element(by=By.XPATH,value="//div[@id='subscriber--value']")
                    address_2 = address_2.text
                    full_address = address_1 + " " + address_2
                    print(full_address)
                    S_address.append(full_address)
                except:
                    full_address=" "
                    S_address.append(full_address)
                # retriving Patient Date of Birth
                try:
                    dob = driver.find_element(by=By.XPATH, value="//*[@id='subscriber-dateofbirth-key']").text
                    print(dob)
                    patient_date = driver.find_element(by=By.XPATH,value="//*[@id='subscriber-dateofbirth-value']").text
                    S_DOB.append(patient_date)
                    # print(dob, patient_date)
                except:
                    patient_date=""
                    S_DOB.append(patient_date)
                try:
                    gen = driver.find_element(by=By.XPATH, value="//*[@id='subscriber-gender-key']").text
                    gen2 = driver.find_element(by=By.XPATH, value="// *[@id='subscriber-gender-value']").text
                    print(gen, gen2)
                    S_gender.append(gen2)
                except:
                    gen2=""
                    S_gender.append(gen2)
                try:
                    plan_number=driver.find_element(by=By.XPATH,value="//*[@id='subscriber-plannumber-value']").text
                    plan_number_list.append(plan_number)
                except:
                    plan_number = ""
                    plan_number_list.append(plan_number)
                try:
                    grp = driver.find_element(by=By.XPATH, value="//*[@id='subscriber-groupnumber-key']").text
                    grp_no = driver.find_element(by=By.XPATH, value="//*[@id='subscriber-groupnumber-value']").text
                    S_group_no.append(grp_no)
                    print(grp, grp_no)
                except:
                    grp_no = ""
                    S_group_no.append(grp_no)
                try:
                    plan_date = driver.find_element(by=By.XPATH,value="//*[@id='subscriber-plandates-value']").text
                    plan_date_list.append(plan_date)
                except:
                    plan_date = ""
                    plan_date_list.append(plan_date)
                try:
                    service_date=driver.find_element(by=By.XPATH,value="//*[@id='subscriber-servicedate-value']").text
                    service_date_list.append(service_date)
                    print(service_date)
                except:
                    service_date = ""
                    service_date_list.append(service_date)

            # testing code for code redundancy
            out_patient = "//span[normalize-space()='Hospital - Outpatient']"
            close_out_patient = "//span[normalize-space()='Physician Visit - Office: Well']"
            office_well = "//span[normalize-space()='Physician Visit - Office: Well']"
            close_office_well = "//*[contains(text(),'Physician Visit - Office: Well')]"

            tab_list= ["Hospital - Outpatient","Physician Visit - Office: Well"]
            for j in tab_list:
                tab_name = driver.find_element(by=By.XPATH,value=f"//span[normalize-space()='{j}']").text
                if j == tab_name:
                    driver.find_element(by=By.XPATH,value=f"//span[normalize-space()='{j}']").click()
                    time.sleep(1)
                    length = driver.find_elements(by=By.XPATH,value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
                    container = len(length)
                    print("Length of DataFrame", container)
                    for i in range(1, container + 1):
                        print("loop1")
                        # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
                        time.sleep(2)
                        driver.find_element(by=By.XPATH,
                                            value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
                        print("loop2")
                        time.sleep(0.5)
                        benefit = driver.find_element(by=By.XPATH,
                                                      value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-b"]')
                        print(benefit.text)

                        print("loop3")
                        time.sleep(0.5)
                        detail = driver.find_element(by=By.XPATH,
                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-d"]')
                        print(detail.text)
                        details = detail.text
                        details = details.replace('\n', " ")

                        print("loop4")
                        time.sleep(0.5)
                        network = driver.find_element(by=By.XPATH,
                                                      value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-n"]')
                        time.sleep(0.5)
                        print("loop5")
                        amount = driver.find_element(by=By.XPATH,
                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-q"]')
                        # copay = benefit.text
                        # if copay == "Co-Payment":
                        benefit_list_o.append(benefit.text)
                        details_list_o.append(details)
                        network_list_o.append(network.text)
                        amount_list_o.append(amount.text)

                    print("Click on close tab")
                    time.sleep(2)
                    driver.find_element(by=By.XPATH, value=f"//*[contains(text(),'{j}')]").click()

            # if tab_name == 'Hospital - Outpatient':
            #     driver.find_element(by=By.XPATH,
            #                         value="//span[normalize-space()='Hospital - Outpatient']").click()
            #     time.sleep(1)
            #     length = driver.find_elements(by=By.XPATH,
            #                                   value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
            #     container = len(length)
            #     print("Length of DataFrame", container)
            #     for i in range(1, container + 1):
            #         print("loop1")
            #         # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
            #         time.sleep(2)
            #         driver.find_element(by=By.XPATH,
            #                             value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
            #         print("loop2")
            #         time.sleep(0.5)
            #         benefit = driver.find_element(by=By.XPATH,
            #                                       value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-b"]')
            #         print(benefit.text)
            #         # if benefit.text != 'Co-Payment':
            #         #     continue
            #         print("loop3")
            #         time.sleep(0.5)
            #         detail = driver.find_element(by=By.XPATH,
            #                                      value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-d"]')
            #         print(detail.text)
            #         details=detail.text
            #         details=details.replace('\n'," ")
            #
            #         print("loop4")
            #         time.sleep(0.5)
            #         network = driver.find_element(by=By.XPATH,
            #                                       value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-n"]')
            #         time.sleep(0.5)
            #         print("loop5")
            #         amount = driver.find_element(by=By.XPATH,
            #                                      value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-q"]')
            #         # copay = benefit.text
            #         # if copay == "Co-Payment":
            #         benefit_list_o.append(benefit.text)
            #         details_list_o.append(details)
            #         network_list_o.append(network.text)
            #         amount_list_o.append(amount.text)
            # print("Click on Text path")
            # driver.find_element(by=By.XPATH, value="//*[contains(text(), 'Hospital - Outpatient')]").click()


            # Extracting Profesional physician  office - well
            # print("Extract Profesional Physician office Well")
            # profesional = driver.find_element(by=By.XPATH,
            #                                   value="//span[normalize-space()='Physician Visit - Office: Well']").text






    #             print("Break code")
    #             if profesional == 'Physician Visit - Office: Well':
    #                 driver.find_element(by=By.XPATH,
    #                                     value="//span[normalize-space()='Physician Visit - Office: Well']").click()
    #                 time.sleep(1)
    #                 length = driver.find_elements(by=By.XPATH,
    #                                               value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
    #                 container = len(length)
    #                 print("Length of DataFrame", container)
    #                 for i in range(1, container + 1):
    #                     print("loop1")
    #                     # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     time.sleep(2)
    #                     driver.find_element(by=By.XPATH,
    #                                         value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     print("loop2")
    #                     time.sleep(0.5)
    #                     benefit_1 = driver.find_element(by=By.XPATH,
    #                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-b"]')
    #                     print(benefit_1.text)
    #                     # if benefit.text != 'Co-Payment':
    #                     #     continue
    #                     print("loop3")
    #                     time.sleep(0.5)
    #                     detail_1 = driver.find_element(by=By.XPATH,
    #                                                    value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-d"]')
    #                     print(detail_1.text)
    #                     details_1=detail_1.text
    #                     details_1=details_1.replace('\n'," ")
    #                     print("loop4")
    #                     time.sleep(1)
    #                     network_1 = driver.find_element(by=By.XPATH,
    #                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-n"]')
    #                     print(network_1.text)
    #                     time.sleep(0.5)
    #                     print("loop5")
    #                     amount_1 = driver.find_element(by=By.XPATH,
    #                                                    value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-q"]')
    #                     print(amount_1.text)
    #                     # copay = benefit.text
    #                     # if copay == "Co-Payment":
    #                     network_list_w.append(network_1.text)
    #                     details_list_w.append(details_1)
    #                     amount_list_w.append(amount_1.text)
    #                     benefit_list_w.append(benefit_1.text)
    #             print("Click on office well")
    #             driver.find_element(by=By.XPATH,
    #                                 value="//*[contains(text(),'Physician Visit - Office: Well')]").click()
    #
    #         #   Extracting Profesional physician visit code
    #             print("Profesional Physician visit office")
    #             profesional = driver.find_element(by=By.XPATH,
    #                                 value="//span[normalize-space()='Professional (Physician) Visit - Office']").text
    #             if profesional == 'Professional (Physician) Visit - Office':
    #                 driver.find_element(by=By.XPATH,value="//span[normalize-space()='Professional (Physician) Visit - Office']").click()
    #                 time.sleep(1)
    #                 length = driver.find_elements(by=By.XPATH,value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
    #                 container = len(length)
    #                 print("Length of DataFrame", container)
    #                 for i in range(1, container + 1):
    #                     print("loop1")
    #                     # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     time.sleep(2)
    #                     driver.find_element(by=By.XPATH,
    #                                         value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     print("loop2")
    #                     time.sleep(0.5)
    #                     benefit = driver.find_element(by=By.XPATH,
    #                                                   value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-b"]')
    #                     print(benefit.text)
    #                     # if benefit.text != 'Co-Payment':
    #                     #     continue
    #                     print("loop3")
    #                     time.sleep(0.5)
    #                     detail = driver.find_element(by=By.XPATH,
    #                                                  value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-d"]')
    #                     print(detail.text)
    #                     details_1 = detail.text
    #                     detail=details_1.replace('\n', " ")
    #                     print("loop4")
    #                     time.sleep(0.5)
    #                     network = driver.find_element(by=By.XPATH,
    #                                                   value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-n"]')
    #                     time.sleep(0.5)
    #                     print("loop5")
    #                     amount = driver.find_element(by=By.XPATH,
    #                                                  value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-q"]')
    #
    #                     # if copay == "Co-Payment":
    #                     benefit_list.append(benefit.text)
    #                     details_list.append(detail)
    #                     network_list.append(network.text)
    #                     amount_list.append(amount.text)
    #             print("Click on Office")
    #             driver.find_element(by=By.XPATH,value="//*[contains(text(),'Professional (Physician) Visit - Office')]").click()
    #
    #             print("Urgent care")
    #             urgentcare = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Urgent Care']").text
    #             if urgentcare == 'Urgent Care':
    #                 driver.find_element(by=By.XPATH,
    #                                     value="//span[normalize-space()='Urgent Care']").click()
    #                 time.sleep(1)
    #                 length = driver.find_elements(by=By.XPATH,
    #                                               value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
    #                 container = len(length)
    #                 print("Length of DataFrame", container)
    #                 for i in range(1, container + 1):
    #                     print("loop1")
    #                     # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     time.sleep(2)
    #                     driver.find_element(by=By.XPATH,
    #                                         value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     print("loop2")
    #                     time.sleep(0.5)
    #                     benefit_1 = driver.find_element(by=By.XPATH,
    #                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-b"]')
    #                     print(benefit_1.text)
    #                     # if benefit.text != 'Co-Payment':
    #                     #     continue
    #                     print("loop3")
    #                     time.sleep(0.5)
    #                     detail_1 = driver.find_element(by=By.XPATH,
    #                                                    value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-d"]')
    #                     print(detail_1.text)
    #                     details_1 = detail_1.text
    #                     details_1=details_1.replace('\n', " ")
    #                     print("loop4")
    #                     time.sleep(0.5)
    #                     network_1 = driver.find_element(by=By.XPATH,
    #                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-n"]')
    #                     print(network_1.text)
    #                     time.sleep(0.5)
    #                     print("loop5")
    #                     amount_1 = driver.find_element(by=By.XPATH,
    #                                                    value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-q"]')
    #                     print(amount_1.text)
    #                     # copay = benefit.text
    #                     # if copay == "Co-Payment":
    #                     benefit_list_c.append(benefit_1.text)
    #                     details_list_c.append(details_1)
    #                     network_list_c.append(network_1.text)
    #                     amount_list_c.append(amount_1.text)
    #             print("Click on Urgent Care")
    #             driver.find_element(by=By.XPATH,
    #                                 value="//*[contains(text(),'Urgent Care')]").click()
    #
    #             print("Unspecified ")
    #             urgentcare = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Unspecified']").text
    #             if urgentcare == 'Unspecified':
    #                 driver.find_element(by=By.XPATH,
    #                                     value="//span[normalize-space()='Unspecified']").click()
    #                 time.sleep(1)
    #                 length = driver.find_elements(by=By.XPATH,
    #                                               value="//div[@class='table benefit-detail-table']//div[@class='benefits row']")
    #                 container = len(length)
    #                 print("Length of DataFrame", container)
    #                 for i in range(1, container + 1):
    #                     print("loop1")
    #                     # driver.find_element(by=By.XPATH, value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     time.sleep(2)
    #                     driver.find_element(by=By.XPATH,
    #                                         value=f"//div[@class='table benefit-detail-table']//div[@class='benefits row'][{i}]").click()
    #                     print("loop2")
    #                     time.sleep(0.5)
    #                     benefit_1 = driver.find_element(by=By.XPATH,
    #                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-b"]')
    #                     print(benefit_1.text)
    #                     # if benefit.text != 'Co-Payment':
    #                     #     continue
    #                     print("loop3")
    #                     time.sleep(0.5)
    #                     detail_1 = driver.find_element(by=By.XPATH,
    #                                                    value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-d"]')
    #                     print(detail_1.text)
    #                     details_1=details_1.replace('\n'," ")
    #                     print("loop4")
    #                     time.sleep(0.5)
    #                     network_1 = driver.find_element(by=By.XPATH,
    #                                                     value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-n"]')
    #                     print(network_1.text)
    #                     time.sleep(0.5)
    #                     print("loop5")
    #                     amount_1 = driver.find_element(by=By.XPATH,
    #                                                    value=f'//div[@class="benefits row"][{i}]/child::div[@class="benefit-q"]')
    #                     print(amount_1.text)
    #                     # copay = benefit.text
    #                     # if copay == "Co-Payment":
    #                     benefit_list_u.append(benefit_1.text)
    #                     details_list_u.append(details_1)
    #                     network_list_u.append(network_1.text)
    #                     amount_list_u.append(amount_1.text)
    #             print("Click on Unspecified ")
    #             driver.find_element(by=By.XPATH,
    #                                 value="//*[contains(text(),'Unspecified')]").click()
    #
    #     except:
    #         continue
    # info_dict ={}
    # info_dict['Payer Name'] = payer_name
    # info_dict['Payer Identification Number'] = payer_id_no
    #
    # info_dict["Alert Notification Status"] = patient_info_change_status_list
    # info_dict["group Number in Alert"] = group_no_in_alert_list
    # info_dict["Deductible in alert"] = deductible_value_list
    #
    # info_dict['Transaction Date']=tansaction_date_list
    # info_dict['Provider Name'] = provider_name_list1
    # info_dict['NPI']=provider_npi_in_transaction_list
    # info_dict['Payerpath TRN']=Payerpath_TRN_list
    # info_dict['Provider TRN']=provider_TRN_list
    # info_dict['Payer TRN']=payer_TRN_list
    #
    # info_dict['Insurance_id'] = subscriber_id
    # info_dict['Current Plan Name'] = current_plan
    # info_dict['Plan Date1'] = plan_date_list1
    #
    # info_dict['Subsciber Name'] = S_name
    # info_dict['Subscriber DOB'] = S_DOB
    # info_dict['Subscriber Gender'] = S_gender
    # info_dict['Subscriber Address'] = S_address
    # info_dict['Group Number'] = S_group_no
    # info_dict['Plan Number'] = plan_number_list
    # info_dict['Plan Date'] = plan_date_list
    # info_dict['Service Date']=service_date_list
    # info_dict['coverage'] = coverage_list
    # info_dict["provider_name"] = provider_name_list
    # info_dict['Address'] = provider_address_list
    # info_dict['Provider NPI'] = provider_npi_list
    #
    # # info_dict['Network']=network_list
    # # info_dict['Benefit']=benefit_list
    # # info_dict['Amount']=amount_list
    # # info_dict['Details'] =details_list
    #
    # # abc=[]
    # # abc.append(info_dict)
    # # with open("API_JSON3.json", "w") as outfile:
    # #     json.dump(abc,outfile)
    # #     print("data dumped")
    #
    # data = pd.DataFrame(info_dict)
    # print(data)
    #
    # for i,rows in data.iterrows():
    #     payer_name = rows['Payer Name']
    #     insurance_identification_number = rows['Payer Identification Number']
    #
    #     alert_notification_status = rows['Alert Notification Status']
    #     group_no = rows['group Number in Alert']
    #     deductible_value1 = rows['Deductible in alert']
    #
    #     transaction_date = rows['Transaction Date']
    #     providername = rows['Provider Name']
    #     npi1 = rows['NPI']
    #     payer_path_trn = rows['Payerpath TRN']
    #     provider_trn = rows['Provider TRN']
    #     payer_trn = rows['Payer TRN']
    #
    #     Subscriber_id = rows['Insurance_id']
    #     current_plan_name = rows['Current Plan Name']
    #     plan_date1 = rows['Plan Date1']
    #     Subsciber_Name = rows['Subsciber Name']
    #     Subscriber_DOB = rows['Subscriber DOB']
    #     Subscriber_Gender = rows['Subscriber Gender']
    #     Subscriber_Address = rows['Subscriber Address']
    #     Group_Number = rows['Group Number']
    #
    #     plan_number=rows['Plan Number']
    #     # plan_date=rows['Plan Date']
    #     coverage = rows['coverage']
    #     provider_name = rows['provider_name']
    #     address = rows['Address']
    #     npi = rows['Provider NPI']
    #     plan_date = rows['Plan Date']
    #     plan_date_S = rows['Service Date']
    #
    #     api_json = {
    #         "Patient_Name":patient_name,
    #         "Received_Date": revieved_date,
    #         "Coverage":"Active Coverage",
    #         "Payer":{
    #              "payer_name":payer_name,
    #              "payer_identification_number":insurance_identification_number
    #         },
    #         "Alerts/Notifications":{
    #             "Patient_Information_Change":alert_notification_status,
    #             "Group_Number":group_no,
    #             "Deductible_Alert":deductible_value1
    #
    #         },
    #         "Insurance_Information": {
    #             "Subscriber_id": Subscriber_id,
    #             "current_plan_name": current_plan_name,
    #             "coverage": coverage,
    #             "Plan_date": plan_date1
    #         },
    #          "Provider/Organization":{
    #              "Name": provider_name,
    #              "Address": address,
    #              "CMS NPI": npi
    #         },
    #         "Transaction Information":{
    #             "Transaction_Date":transaction_date,
    #             "Provider_Name":providername,
    #             "NPI":npi1,
    #             "Payerpath_TRN":payer_path_trn,
    #             "Provider_TRN":provider_trn,
    #             "Payer_TRN":payer_trn
    #         },
    #         "Subscriber":{
    #               "Subsciber_Name": Subsciber_Name,
    #               "Subscriber_DOB": Subscriber_DOB,
    #               "Subscriber_Gender": Subscriber_Gender,
    #               "Subscriber_Address": Subscriber_Address,
    #               "Group_Number": Group_Number,
    #               "plan_number": plan_number,
    #               "Plan_date": plan_date,
    #               "Service Date":plan_date_S
    #         },
    #         "Hospital - Outpatient": {
    #             "Network": network_list_o,
    #             "Benefit": benefit_list_o,
    #             "Amount": amount_list_o,
    #             "Details": details_list_o
    #         },
    #
    #         "Professional (Physician) Visit - Office":{
    #             "Network":network_list,
    #             "Benefit":benefit_list,
    #             "Amount": amount_list,
    #             "Details":details_list
    #         },
    #         "Urgent Care":
    #             {
    #                 "Network": network_list_c,
    #                 "Benefit": benefit_list_c,
    #                 "Amount": amount_list_c,
    #                 "Details": details_list_c
    #
    #             },
    #         "Physician Visit - Office: Well":
    #             {
    #                 "Network": network_list_w,
    #                 "Benefit": benefit_list_w,
    #                 "Amount": amount_list_w,
    #                 "Details": details_list_w
    #             },
    #         "Unspecified":
    #             {
    #                 "Network": network_list_u,
    #                 "Benefit": benefit_list_u,
    #                 "Amount": amount_list_u,
    #                 "Details": details_list_u
    #             },
    #
    #     }
    #
    #     json_object = json.dumps(api_json, indent=4)
    #     print(json_object)
    #     with open("sample6.json", "w") as outfile:
    #         outfile.write(json_object)





