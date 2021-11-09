import pytest
from src.data.mcl_interface import MCL_Interface


@pytest.fixture
def test_instantiation() -> MCL_Interface:
    """Verifies the instantiation of the Selenium MCL_Interface"""
    test_interface = MCL_Interface()
    return test_interface


@pytest.mark.order(1)
@pytest.mark.skip(reason="Verified as working.")
def test_login(test_instantiation):
    """Verifies that Selenium correctly logs into Medtronic CareLink Portal"""
    try:
        test_instantiation.login()
    except:
        print(">>> Login failed. Raising Exception.")
        raise
    pass


@pytest.mark.order(2)
def test_pullCSVReports(test_instantiation):
    """
    Verifies that Selenium can run the reports.
    """
    try:
        test_instantiation.login()
        test_instantiation.pullCSVReports()
    except:
        print(">>> Reporting failed. Raising exception.")
        raise
    pass
