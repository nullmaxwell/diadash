# Basic Selenium Imports
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# All below necessary for waitForPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Necessary for credentials
from src.credentials.credentials import CredentialHandler


class MCL_Interface:
    """
    Handlles all of the web navigation necessary to donwload the reports.
    """

    DATA_OUT_PATH = str(pathlib.Path("data/external").resolve())

    # Class Attributes
    TIMEOUT = 40  # in seconds
    OPTIONS = FirefoxOptions()
    # OPTIONS.headless = True # Makes the process run headless.
    OPTIONS.set_preference("browser.download.folderList", 2)
    OPTIONS.set_preference("browser.download.manager.showWhenStarting", False)
    OPTIONS.set_preference("browser.download.dir", DATA_OUT_PATH)
    OPTIONS.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/csv, text/csv, text/plain,application/octet-stream doc xls pdf txt",
    )

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.creds = CredentialHandler()
        self.user = self.creds.getUser()
        self.token = self.creds.getToken()
        # self.driver = webdriver.Firefox(firefox_profile=MCL_Interface.PROFILE)
        self.driver = webdriver.Firefox(options=MCL_Interface.OPTIONS)
        pass

    def login(self) -> None:
        """
        Logs into the Medtronic CareLink portal
        """
        self.driver.get(
            "https://carelink.minimed.com/patient/sso/login?country=us&lang=en"
        )

        # Filling the username
        u_box = self.driver.find_element(By.ID, "username")
        u_box.clear()
        u_box.send_keys(self.user)

        # Filling password
        p_box = self.driver.find_element(By.ID, "password")
        p_box.clear()
        p_box.send_keys(self.token)

        # Clicking Login
        self.driver.find_element(
            By.XPATH, "/html/body/div/div/div[3]/form/div[3]/input"
        ).click()
        pass

    def pullCSVReports(self) -> None:
        """
        Navigates to the reports page and downloads the appropriate data.
        """
        # Navigating to the reports page.
        # self.driver.get(
        #     "https://carelink.minimed.com/app/reports"
        # )  # old call --> this raises compat error

        self.driver.implicitly_wait(5)
        # self.driver.find_element(By.LINK_TEXT, "Reports").click()

        report_element = self.driver.find_element(By.ID, "h-reports")
        self.driver.execute_script("arguments[0].click();", report_element)

        # Selecting 7 Days of reporting.
        self.driver.find_element(
            By.XPATH,
            "/html/body/app-root/app-dashboard-wrapper/div/mat-sidenav-container/mat-sidenav-content/div/app-reports/div/div[2]/div/div[2]/div/div[2]/app-period-selector-horizontal/app-period-selector-option[1]/button",
        ).click()

        # Selecting the weekly review report.
        self.driver.find_element(
            By.XPATH,
            "/html/body/app-root/app-dashboard-wrapper/div/mat-sidenav-container/mat-sidenav-content/div/app-reports/div/div[3]/div[2]/app-report-type[3]/div/div[1]/div[1]",
        ).click()

        # Click to export
        self.driver.find_element(By.ID, "p-button-export-reports").click()

        # Ensuring the report is generated before passing
        WebDriverWait(self.driver, MCL_Interface.TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "p-button-export-reports"))
        )
        pass

    def clickableWaitAndClick(self, element_type: any, element: str) -> None:
        """
        Waits until a given element is clickable before clicking it.
        """
        try:
            WebDriverWait(self.driver, MCL_Interface.TIMEOUT).until(
                EC.element_to_be_clickable((element_type, element))
            )
        finally:
            self.driver.find_element(By.ID, element).click()
        pass

    def presenceWaitAndClick(self, element_type: any, element: str) -> None:
        """
        Waits until a given element is present before clicking it.
        """
        try:
            WebDriverWait(self.driver, MCL_Interface.TIMEOUT).until(
                EC.element_to_be_clickable((element_type, element))
            )
        finally:
            self.driver.find_element(By.ID, element).click()
        pass
