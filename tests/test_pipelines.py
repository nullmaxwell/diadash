import pytest
from src.pipelines.pipelines import WeeklyReportPipeline


@pytest.fixture
@pytest.mark.order(1)
def test_readData():
    """
    Verifies that the source CSV can be read in as a DataFrame
    """
    try:
        df = WeeklyReportPipeline.readData()
        return df
    except:
        print(">>> readData failed. Raising Exception")
        raise


@pytest.fixture
@pytest.mark.order(2)
def test_sliceWeeklyReport(test_readData):
    """
    Verifies that the weekly report is split correctly.
    """
    test_dict = WeeklyReportPipeline.sliceWeeklyReport(test_readData)
    assert len(test_dict) == 3, "test_dict length is incorrect."
    return test_dict


def test_sliceWeeklyReportLengths(test_sliceWeeklyReport):
    """
    Verifies the length of the testing data.
    """
    assert (
        len(test_sliceWeeklyReport["chunk1"]) > 100
    ), "chunk1 does not meet length requirement."
    assert (
        len(test_sliceWeeklyReport["chunk2"]) > 100
    ), "chunk2 does not meet length requirement."
    assert (
        len(test_sliceWeeklyReport["chunk3"]) > 100
    ), "chunk3 does not meet length requirement."
