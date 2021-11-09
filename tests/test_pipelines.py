import pytest
from src.pipelines.pipelines import WeeklyDataPipeline

# The following tests verify the WeeklyDataPipeline and its components.
@pytest.mark.order(1)
def test_readData():
    """
    Verifies that the source CSV can be read in as a DataFrame
    """
    try:
        df = WeeklyDataPipeline.readData()
        return df
    except:
        print(">>> readData failed. Raising Exception")
        raise


@pytest.mark.order(2)
def test_sectionalizeData(test_readData):
    """
    Verifies that the weekly report is split correctly.
    """
    test_dict = WeeklyDataPipeline.sectionalizeData(test_readData)
    assert len(test_dict) == 3, "test_dict length post-sectionalizing is incorrect."
    return test_dict


@pytest.mark.order(3)
def test_sectionalizeDataLengths(test_sectionalizeData):
    """
    Verifies the length of the testing data.
    """
    assert (
        len(test_sectionalizeData["chunk1"]) > 100
    ), "chunk1 does not meet length requirement."
    assert (
        len(test_sectionalizeData["chunk2"]) > 100
    ), "chunk2 does not meet length requirement."
    assert (
        len(test_sectionalizeData["chunk3"]) > 100
    ), "chunk3 does not meet length requirement."


@pytest.mark.order(4)
def test_scrubFeatures(test_sectionalizeData):
    """
    Verifies that only the necessary features for each chunk are present.
    """
    try:
        WeeklyDataPipeline.scrubFeatures(test_sectionalizeData)
    except:
        print(">>> Error scrubbing features. Rasing exception.")
        raise
    finally:
        assert (
            test_sectionalizeData["chunk1"]
            == ["Index", "Date", "Time", "Bolus Volume Delivered (U)"]
        ).all(), "Chunk1 contains unwanted indexes."

        assert (
            type(test_sectionalizeData["chunk1"]) == None
        ), "Chunk2 incorrectly deleted."

        assert (
            test_sectionalizeData["chunk3"]
            == ["Index", "Date", "Time", "Sensor Glucose (mg/dL)"]
        ).all(), "Chunk3 contains unwanted indexes."
    pass
