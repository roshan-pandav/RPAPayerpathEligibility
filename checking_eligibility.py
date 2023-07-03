import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from SaveData_inQonductor import save_data_in_qonductor
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from pytz import timezone
from datetime import datetime

def waits(el, driver):
    """
    This function waits robotscraper until element given in the argument loads
    :param el: element of interest
    :return: None
    """
    WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.XPATH, el)))
def checking_eligibility_2(driver, df,save_api_url,headers):

    try:
        waits("//iframe[@src='/EligibilityUI/Transaction']", driver)
        frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
        driver.switch_to.frame(frm)

        df["pp_primary_coverage"] = ""
        df["pp_primary_transaction_date"] = ""
        df["pp_primary_current_plan"] = ""
        df["pp_primary_plan_date"] = ""
        df["pp_primary_subscriber_id"] = ""
        df["pp_primary_group_no"] = ""
        df["pp_primary_network_id"] = ""
        df["pp_primary_copay"] = ""
        df["pp_primary_check_medicare_advantage"] = ""

        df["pp_secondary_coverage"] = ""
        df["pp_secondary_transaction_date"] = ""
        df["pp_secondary_network_id"] = ""
        df["pp_secondary_check_medicare_advantage"] = ""
        df["pp_secondary_current_plan"] = ""
        df["pp_secondary_subscriber_id"] = ""
        df["pp_secondary_group_no"] = ""
        df["pp_secondary_plan_date"] = ""

        df["pp_tertiary_coverage"] = ""
        df["pp_tertiary_plan_date"] = ""
        df["pp_tertiary_transaction_date"] = ""
        df["pp_tertiary_network_id"] = ""
        df["pp_tertiary_check_medicare_advantage"] = ""
        df["pp_tertiary_current_plan"] = ""

        df.loc["Automation_status"] = ""
        df.loc["cancel_reason"] = ""

        for i, rows in df.iterrows():
            try:
                if i == 4:
                    break
                pp_primary_coverage = ""
                pp_primary_transaction_date = ""
                pp_primary_current_plan = ""
                pp_primary_plan_date = ""
                pp_primary_subscriber_id = ""
                pp_primary_group_no = ""
                pp_primary_network_id = ""
                pp_primary_copay = ""
                pp_primary_check_medicare_advantage = ""

                pp_secondary_coverage = ""
                pp_secondary_transaction_date = ""
                pp_secondary_current_plan = ""
                pp_secondary_subscriber_id = ""
                pp_secondary_group_no = ""
                pp_secondary_plan_date = ""
                pp_secondary_network_id = ""
                pp_secondary_check_medicare_advantage = ""

                pp_tertiary_network_id = ""
                pp_tertiary_plan_date = ""
                pp_tertiary_coverage = ""
                pp_tertiary_transaction_date = ""
                pp_tertiary_check_medicare_advantage = ""
                pp_tertiary_current_plan = ""

                # Taking patient first name last name from columns
                projectclaimid = str(rows['projectclaimid'])
                patientmrn = str(rows['patientmrn'])
                appointmentdate = str(rows['appointmentdate'])
                createdon=str(rows['createdon'])

                f_name = str(rows['Patient First Name'])
                l_name = str(rows['Patient Last Name'])

                # need to handle DOB
                patient_dob = str(rows['Patient DOB'])
                patient_dob1 = patient_dob.split("-")
                mm = str(patient_dob1[1])
                dd = str(patient_dob1[2])
                yy = str(patient_dob1[0])
                patient_dob = f"{mm}/{dd}/{yy}"


                # taking Primary insurance name and primary policy id
                primaryinsu_name = str(rows['Patient Primary Insur'])
                primarypolicy_id = str(rows['pri_Policy_id'])

                # secondary insurance name and secondary policy id
                secondaryinsu_name = str(rows['Patient Secondary  Insur'])
                secondarypolicy_id = str(rows['Sec_policy_id'])

                # taking tertiary insurance name and tertiary policy id
                tertiaryinsu_name = str(rows['Patient Tertiary insur'])
                tertiarypolicy_id = str(rows['Ter_policy_id'])

                if primaryinsu_name != "":
                    primary_dict = {
                        "f_name": f_name,
                        "l_name": l_name,
                        "insurance_name": primaryinsu_name,
                        "policy_id": primarypolicy_id,
                        "dob": patient_dob,
                        "insurance_sequence": "Primary"
                    }
                    ev_status = insu_eligibility_verification(driver, primary_dict)
                    if ev_status == 'success':
                        status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1, check_medicare_advantage = data_extraction(
                            driver, primarypolicy_id, primary_dict["insurance_sequence"])
                        print("Primary information:",status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id,
                              subsciber_id1)
                        pp_primary_coverage = status
                        pp_primary_transaction_date = transaction_date
                        pp_primary_current_plan = current_plan_name
                        pp_primary_plan_date = plan_date
                        pp_primary_subscriber_id = subsciber_id1
                        pp_primary_group_no = grp_no
                        pp_primary_network_id = network_id
                        pp_primary_copay = copay
                        pp_primary_check_medicare_advantage = check_medicare_advantage

                        df.loc[i, "pp_primary_coverage"] = status
                        df.loc[i, "pp_primary_transaction_date"] = transaction_date
                        df.loc[i, "pp_primary_current_plan"] = current_plan_name
                        df.loc[i, "pp_primary_subscriber_id"] = subsciber_id1
                        df.loc[i, "pp_primary_group_no"] = grp_no
                        df.loc[i, "pp_primary_plan_date"] = plan_date
                        df.loc[i, "pp_primary_network_id"] = network_id
                        df.loc[i, "pp_primary_copay"] = copay
                        df.loc[i, "pp_primary_check_medicare_advantage"] = check_medicare_advantage
                        df.loc[i, "Automation_status"] = "Completed"
                    else:
                        df.loc[i, "Automation_status"] = "Skipped"
                        # df.loc[i,"cancel_reason"] = "Patient basic EV info not present"
                        continue
                #  Check Secondary insurance info
                else:
                    df.loc[i, "Automation_status"] = "Skipped"
                    df.loc[i, "cancel_reason"] = "Patient basic EV info not present"
                    continue
                if secondaryinsu_name != "":
                    secondary_dict = {
                        "f_name": f_name,
                        "l_name": l_name,
                        "insurance_name": secondaryinsu_name,
                        "policy_id": secondarypolicy_id,
                        "dob": patient_dob,
                        "insurance_sequence": "Secondary"
                    }
                    ev_status = insu_eligibility_verification(driver, secondary_dict)
                    if ev_status == 'success':
                        status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1, check_medicare_advantage = data_extraction(
                            driver, secondarypolicy_id, secondary_dict["insurance_sequence"])
                        print("secondary information",status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1)

                        pp_secondary_coverage = status
                        pp_secondary_transaction_date = transaction_date
                        pp_secondary_current_plan = current_plan_name
                        pp_secondary_subscriber_id = subsciber_id1
                        pp_secondary_group_no = grp_no
                        pp_secondary_plan_date = plan_date
                        pp_secondary_network_id = network_id
                        pp_secondary_check_medicare_advantage = check_medicare_advantage

                        df.loc[i, "pp_secondary_coverage"] = status
                        df.loc[i, "pp_secondary_transaction_date"] = transaction_date
                        df.loc[i, "pp_secondary_subscriber_id"] = subsciber_id1
                        df.loc[i, "pp_secondary_group_no"] = grp_no
                        df.loc[i, "pp_secondary_plan_date"] = plan_date
                        df.loc[i, "pp_secondary_network_id"] = network_id
                        df.loc[i, "pp_secondary_current_plan"] = current_plan_name
                        df.loc[i, "pp_secondary_check_medicare_advantage"] = check_medicare_advantage

                        df.loc[i, "Automation_status"] = "Completed"
                    else:
                        # df.loc[i, "Automation_status"] = "Skip-[Need to review manually]"
                        continue
                        #  Check Secondary insurance info
                else:
                    # df.loc[i, "Automation_status"] = "Skip-[Need to review manually]"
                    # df.loc[i, "cancel_reason"] = "Patient basic EV info not present"
                    pass
                if tertiaryinsu_name != "":
                    tertiary_dict = {
                        "f_name": f_name,
                        "l_name": l_name,
                        "insurance_name": tertiaryinsu_name,
                        "policy_id": tertiarypolicy_id,
                        "dob": patient_dob,
                        "insurance_sequence": "Tertiary"
                    }
                    ev_status = insu_eligibility_verification(driver, tertiary_dict)
                    if ev_status == 'success':
                        status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1, check_medicare_advantage = data_extraction(
                            driver, tertiarypolicy_id, tertiary_dict["insurance_sequence"])
                        print("tertiary information",status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id,subsciber_id1)

                        pp_tertiary_coverage = status
                        pp_tertiary_transaction_date = transaction_date
                        pp_tertiary_plan_date = plan_date
                        pp_tertiary_network_id = network_id
                        pp_tertiary_check_medicare_advantage = check_medicare_advantage
                        pp_tertiary_current_plan = current_plan_name

                        df.loc[i, "pp_tertiary_coverage"] = status
                        df.loc[i, "pp_tertiary_transaction_date"] = transaction_date
                        df.loc[i, "pp_tertiary_plan_date"] = plan_date
                        df.loc[i, "pp_tertiary_network_id"] = network_id
                        df.loc[i, "pp_tertiary_check_medicare_advantage"] = check_medicare_advantage
                        df.loc[i, "pp_tertiary_current_plan"] = current_plan_name
                        df.loc[i, "Automation_status"] = "Completed"
                    else:
                        # df.loc[i, "Automation_status"] = "Skip-[Need to review manually]"
                        # df.loc[i, "cancel_reason"] = "Patient basic EV info not present"
                        continue
                else:
                    # df.loc[i, "Automation_status"] = "Skip-[Need to review manually]"
                    # df.loc[i, "cancel_reason"] = "Patient basic EV info not present"
                    createdon = str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f'))
                    # print(createdon)
                    # new code is added for saving
                    # create json
                    try:
                        jsn = [
                                {
                                    "projectclaimid": projectclaimid,
                                    "patientmrn": patientmrn,
                                    "appointmentdate": appointmentdate,
                                    "payerpathinfo": {
                                        "pp_primary_coverage": pp_primary_coverage,
                                        "pp_primary_transaction_date": pp_primary_transaction_date,
                                        "pp_primary_current_plan": pp_primary_current_plan,
                                        "pp_primary_plan_date": pp_primary_plan_date,
                                        "pp_primary_subscriber_id": pp_primary_subscriber_id,
                                        "pp_primary_group_no": pp_primary_group_no,
                                        "pp_primary_network_id": pp_primary_network_id,
                                        "pp_primary_copay": pp_primary_copay,
                                        "pp_primary_check_medicare_advantage": pp_primary_check_medicare_advantage,

                                        "pp_secondary_coverage": pp_secondary_coverage,
                                        "pp_secondary_transaction_date": pp_secondary_transaction_date,
                                        "pp_secondary_current_plan": pp_secondary_current_plan,
                                        "pp_secondary_subscriber_id": pp_secondary_subscriber_id,
                                        "pp_secondary_group_no": pp_secondary_group_no,
                                        "pp_secondary_plan_date": pp_secondary_plan_date,
                                        "pp_secondary_network_id": pp_secondary_network_id,
                                        "pp_secondary_check_medicare_advantage": pp_secondary_check_medicare_advantage,

                                        "pp_tertiary_coverage": pp_tertiary_coverage,
                                        "pp_tertiary_transaction_date": pp_tertiary_transaction_date,
                                        "pp_tertiary_plan_date": pp_tertiary_plan_date,
                                        "pp_tertiary_network_id": pp_tertiary_network_id,
                                        "pp_tertiary_check_medicare_advantage": pp_tertiary_check_medicare_advantage,
                                        "pp_tertiary_current_plan": pp_tertiary_current_plan
                                    },
                                    "pp_automationstatus": 'Complited',
                                    "modifiedon": createdon
                                }
                              ]
                        savejson = jsn
                        save_data_in_qonductor(save_api_url, headers, savejson)
                        continue

                    except Exception as e:
                        print("Error while saving in qonductor")
                    continue
            except:
                df.loc[i, "Automation_status"] = "Exception"
                df.loc[i, "cancel_reason"] = "Exception occure while EV checking"
                continue
        # finaljson = df.to_json(orient='records')
        # print(finaljson)
        # return finaljson, df
        return df
    except Exception as error:
        print(error)
def data_extraction(driver, policy_id, insurance_sequence):
    """
    :param driver: chrome driver
    :param df: dataframe iterate to find active coverage
    :return: return Copay value
    """
    status = ""
    transaction_date = ""
    current_plan_name = ""
    copay = ""
    subsciber_id1 = ""
    grp_no = ""
    plan_date = ""
    network_id = ""
    check_medicare_advantage = ""
    try:
        time.sleep(2)
        frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
        driver.switch_to.frame(frm)
        time.sleep(1)
        # sel = Select(driver.find_element(by=By.XPATH, value='// *[ @ id = "date-range-select"]'))
        # sel.select_by_index(1)
        try:
            network_list = []
            benefit_list = []
            amount_list = []
            details_list = []
            email_dict = {}
            waits("//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']",
                  driver)
            driver.find_element(by=By.XPATH,
                                value="//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']").clear()
            time.sleep(1)
            print("Search Patient by ID",policy_id)
            driver.find_element(by=By.XPATH,
                                value="//input[@class='ag-input-field-input ag-text-field-input'][@aria-label='Policy Id Filter Input']").send_keys(policy_id)
            # time.sleep(6)
            waits(
                "/html/body/app-root/transaction/div[2]/div[2]/transaction-list/ag-grid-angular[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div[7]/result-cell-renderer/a/div/img",
                driver)
            element = driver.find_element(by=By.XPATH,
                                          value="/html/body/app-root/transaction/div[2]/div[2]/transaction-list/ag-grid-angular[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div[7]/result-cell-renderer/a/div/img")
            status = element.get_attribute("alt")
            print(status)
            if status != 'Active Coverage':
                status = status.split('\n')[0]
                # handling Can not Process, inactive and Unknown coverage
                if status == 'Cannot Process' or status == "Inactive" or status == "Unknown":
                    driver.find_element(by=By.XPATH,
                                        value="/html/body/app-root/transaction/div[2]/div[2]/transaction-list/ag-grid-angular[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div[7]/result-cell-renderer/a/div/img").click()
                    driver.find_element(by=By.XPATH, value="//*[@id='details-header']").click()
                    driver.find_element(by=By.XPATH, value="//button[@id='expand-all-header']").click()
                    driver.find_element(by=By.XPATH, value="//*[@id='collapse-all-header']").click()
                    transation_information = driver.find_element(by=By.XPATH,
                                                                 value="//span[normalize-space()='Transaction Information']").text
                    if transation_information == "Transaction Information":
                        driver.find_element(by=By.XPATH,
                                            value="//span[normalize-space()='Transaction Information']").click()
                        try:
                            time.sleep(2)
                            transaction_date = driver.find_element(by=By.XPATH,
                                                                   value="//div[@id='transactioninformation-transactiondate-value']").text
                            print(transaction_date)
                            driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
                            time.sleep(1)
                        except:
                            transaction_date = ""
                            driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
                            time.sleep(1)
                return status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1, check_medicare_advantage
            else:
                time.sleep(5)
                driver.find_element(by=By.XPATH,
                                    value="/html/body/app-root/transaction/div[2]/div[2]/transaction-list/ag-grid-angular[1]/div/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div[7]/result-cell-renderer/a/div/img").click()

                driver.find_element(by=By.XPATH, value="//*[@id='details-header']").click()
                driver.find_element(by=By.XPATH, value="//button[@id='expand-all-header']").click()
                driver.find_element(by=By.XPATH, value="//*[@id='collapse-all-header']").click()

                # handling medicare advantage plan
                print("Checking Advantage Plan")
                AlertNotification = driver.find_element(by=By.XPATH,
                                                        value="//span[normalize-space()='Alerts/Notifications']").text
                if AlertNotification == 'Alerts/Notifications':
                    driver.find_element(by=By.XPATH, value="//span[normalize-space()='Alerts/Notifications']").click()
                    try:
                        check_medicare_advantage = driver.find_element(by=By.XPATH,
                                                                       value="//*[@id='alertsnotifications-medicareadvantage-key']").text
                        check_medicare_advantage = "YES"
                        print(check_medicare_advantage)
                    except:
                        check_medicare_advantage = "NO"
                        print(check_medicare_advantage)

                print("Transaction information")
                time.sleep(2)
                transation_information = driver.find_element(by=By.XPATH,
                                                             value="//span[normalize-space()='Transaction Information']").text
                if transation_information == "Transaction Information":
                    time.sleep(2)
                    driver.find_element(by=By.XPATH, value="//span[normalize-space()='Transaction Information']").click()
                    if status == 'Active Coverage':
                        try:
                            time.sleep(2)
                            transaction_date = driver.find_element(by=By.XPATH, value="//div[@id='transactioninformation-transactiondate-value']").text
                            print(transaction_date)
                        except:
                            transaction_date = ""
                            print(transaction_date)
                    else:
                        pass
                print("Extracting Insurance Information")
                insurance_info = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Insurance Information']").text
                if insurance_info == 'Insurance Information':
                    driver.find_element(by=By.XPATH, value="//span[normalize-space()='Insurance Information']").click()
                    try:
                        time.sleep(2)
                        current_plan_name = driver.find_element(by=By.XPATH,
                                                                value="//*[@id='insuranceinformation-currenthealthplan-value']").text
                        print(current_plan_name)
                    except:
                        current_plan_name = ""
                        print(current_plan_name)
                    try:
                        time.sleep(2)
                        subsciber_id1 = driver.find_element(by=By.XPATH,
                                                            value="//div[@id='insuranceinformation-subscriberid-value']").text
                        print(subsciber_id1)
                    except:
                        subsciber_id1 = ""
                        print(subsciber_id1)
                print("Subscriber Information")
                Subcriber = driver.find_element(by=By.XPATH, value="//span[normalize-space()='Subscriber']").text
                if Subcriber == 'Subscriber':
                    time.sleep(2)
                    driver.find_element(by=By.XPATH, value="//span[normalize-space()='Subscriber']").click()
                    try:
                        time.sleep(2)
                        grp_no = driver.find_element(by=By.XPATH, value="//*[@id='subscriber-groupnumber-value']").text
                        print(grp_no)
                    except:
                        grp_no = ""
                        print(grp_no)
                    try:
                        time.sleep(2)
                        plan_date = driver.find_element(by=By.XPATH, value="//*[@id='subscriber-plandates-value']").text
                        print(plan_date)
                    except:
                        plan_date = ""
                    try:
                        time.sleep(2)
                        network_id = driver.find_element(by=By.XPATH,
                                                         value="//div[@id='subscriber-plannetworkidentificationnumber-value']").text
                        print(network_id)
                    except:
                        network_id = ""
                        print(network_id)
                print("Extract Copay Information")
                if insurance_sequence == "Primary":
                    try:
                        # waits("//span[normalize-space()='Professional (Physician) Visit - Office']", driver)
                        time.sleep(2)
                        driver.find_element(by=By.XPATH,
                                            value="//span[normalize-space()='Professional (Physician) Visit - Office']").click()
                    except:
                        copay = '$0.0'
                        driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
                    if copay != '$0.0':
                        time.sleep(3)
                        length = driver.find_elements(by=By.XPATH, value="//*[@class='table benefit-detail-table']/div")
                        container = len(length)
                        print("Length of DataFrame", container)
                        for j in range(2, container + 1):
                            network = driver.find_element(by=By.XPATH,
                                                          value=f"//*[@class='table benefit-detail-table']/div[{j}]/div[1]").text
                            if network == 'Out of Network':
                                continue
                            benefit = driver.find_element(by=By.XPATH,
                                                          value=f"//*[@class='table benefit-detail-table']/div[{j}]/div[3]").text
                            if benefit != 'Co-Payment':
                                continue
                            amount = driver.find_element(by=By.XPATH,
                                                         value=f"//*[@class='table benefit-detail-table']/div[{j}]/div[5]").text
                            detail = driver.find_elements(by=By.XPATH,
                                                          value=f"//*[@class='table benefit-detail-table']/div[{j}]/div[8]/div/div")
                            detail_len = len(detail)
                            print(detail_len)
                            detail_str = ""
                            for cnt in range(1, detail_len + 1):
                                detail = driver.find_element(by=By.XPATH,
                                                             value=f"//*[@class='table benefit-detail-table']/div[{j}]/div[8]/div[{cnt}]/div[1]").text
                                detail_str = f'{detail_str} {detail}'

                            details_list.append(detail_str)
                            amount_list.append(amount)
                            network_list.append(network)
                            benefit_list.append(benefit)

                        email_dict['Network'] = network_list
                        email_dict['Benefits'] = benefit_list
                        email_dict['Amounts'] = amount_list
                        email_dict['Details'] = details_list
                        print(email_dict)
                        data = pd.DataFrame(email_dict)
                        # print(data)
                        copay = calculate_co_pay(data)
                        print(copay)
                        time.sleep(2)
                        driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
                        time.sleep(2)
                else:
                    driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
                time.sleep(2)
                return status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1, check_medicare_advantage
        except:
            print("Skip patient[Need to Review Manually]")
            time.sleep(2)
            driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
            return status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id, subsciber_id1, check_medicare_advantage
        # driver.find_element(by=By.XPATH,value ="//div[@class='profile']//a[1]").click()
        # driver.find_element(by=By.XPATH,value ="//a[@name='Logout']").click()
    except Exception as error:
        print(error)
        print("Error during data extraction..")
        time.sleep(2)
        driver.find_element(by=By.XPATH, value="//button[@id='list-header']").click()
        return status, transaction_date, current_plan_name, copay, grp_no, plan_date, network_id
def insu_eligibility_verification(driver, dict):
    """
    :param driver: "Chrome Driver"
    :param dict: "Dictionary containing demographic information required for EC checking"
    :return: "success if successufully EC check else return error
    """
    try:
        f_name = dict["f_name"]
        l_name = dict["l_name"]
        patient_dob = dict["dob"]
        insu_name = dict["insurance_name"]
        policy_id = dict["policy_id"]
        # time.sleep(5)
        # frm = driver.find_element(By.XPATH, "//iframe[@src='/EligibilityUI/Transaction']")
        # driver.switch_to.frame(frm)
        # time.sleep(3)
        waits("(//label[@class='tool-bar-dropbtn'])[1]", driver)
        loc = driver.find_element(by=By.XPATH, value="(//label[@class='tool-bar-dropbtn'])[1]")
        # print("Loc", loc)
        time.sleep(1)
        hover = ActionChains(driver).move_to_element(loc)
        hover.perform()
        driver.find_element(by=By.XPATH, value="//li[@id='ActionId_0']").click()
        time.sleep(2)
        #  handled Service date
        # driver.find_element(by=By.XPATH,value="/html[1]/body[1]/app-root[1]/eligibility-request[1]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/input-tag[1]/fieldset[1]/div[1]/div[1]/div[2]/div[1]/input[1]").clear()
        # time.sleep(1)
        # driver.find_element(by=By.XPATH,value="//*[@id='ServiceDateInputId']").send_keys("06/21/2024")
        waits("//img[@id='PayerNameImgId']", driver)
        driver.find_element(by=By.XPATH, value="//img[@id='PayerNameImgId']").click()
        time.sleep(1)
        waits(
            "/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input",
            driver)
        driver.find_element(by=By.XPATH,
                            value="/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input").click()
        time.sleep(3)
        driver.find_element(by=By.XPATH,
                            value="/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input").send_keys(
            insu_name)
        time.sleep(1)
        driver.find_element(by=By.XPATH,
                            value="/html/body/div/div[2]/div/mat-dialog-container/app-payermodal/div/div[2]/ag-grid-angular/div/div[2]/div[2]/div[3]/div[2]/div/div/div/div[1]/div/div/div/div[2]/input").click()
        time.sleep(1)
        # click on OK button for selecting insurance name
        element = driver.find_element(by=By.XPATH,
                                      value="//div[@class='benefit-payment']//div[@class='border-top center']//button[1]")
        try:
            if element.is_enabled():
                element.click()
        except Exception as Error:
            print(Error)
            print("Submit button not clickable")
        time.sleep(2)
        driver.find_element(by=By.XPATH, value="//input[@id='DependentFirstNameId']").send_keys(f_name)
        driver.find_element(by=By.XPATH, value="//input[@id='DependentLastNameId']").send_keys(l_name)
        driver.find_element(by=By.XPATH, value="//input[@id='DependentDOBInputId']").send_keys(patient_dob)
        # select gender from excel
        # Gender=Select(driver.find_element(by=By.XPATH,value="//select[@id='DependentGenderId']"))
        # Gender.select_by_visible_text(gender)
        driver.find_element(by=By.XPATH, value="//input[@id='PolicyIdId']").send_keys(policy_id)
        time.sleep(1)
        waits("//*[@id='Last Name/OrgId']", driver)
        driver.find_element(by=By.XPATH, value="//*[@id='Last Name/OrgId']").send_keys(
            "MICHIGAN INSTITUTE OF UROLOGY PC")
        driver.find_element(by=By.XPATH, value="//input[@id='ProviderNPIId']").click()
        driver.find_element(by=By.XPATH, value="//input[@id='ProviderNPIId']").send_keys("1427027416")
        time.sleep(1)
        driver.find_element(by=By.XPATH, value='//*[@id="PolicyGroupId"]').click()
        time.sleep(1)
        # click on Submit the eligibility request
        driver.find_element(by=By.XPATH, value='//*[@id="submitRequest"]').click()
        time.sleep(3)
        driver.switch_to.default_content()
        return 'success'
    except Exception as error:
        print(error)
        driver.find_element(by=By.XPATH,value="//button[@id='cancelRequest']").click()
        # driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/div[1]/div/div[1]/div[3]/div/a[1]/span').click()
        return error
def calculate_co_pay(df):
    # function defination for calculating co-payment for primary insurance
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
