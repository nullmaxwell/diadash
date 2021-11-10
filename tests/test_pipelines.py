import pytest
from src.pipelines.pipelines import WeeklyDataPipeline


# class WeeklyDataPipelineTests:
"""
The following tests verify the WeeklyDataPipeline and its components.
"""


@pytest.fixture
@pytest.mark.order(1)
def test_readData_success():
    """
    Verifies that the source CSV can be read in as a DataFrame
    """
    try:
        df = WeeklyDataPipeline.readData()
    except:
        print(">>> readData failed. Raising Exception")
        raise
    finally:
        return df


@pytest.fixture
@pytest.mark.order(2)
def test_sectionalizeData_success(test_readData_success):
    """
    Verifies that the sectionalizeData method functions correctly.
    """
    try:
        test_dict = WeeklyDataPipeline.sectionalizeData(test_readData_success)
    except:
        print(">>> sectionalizeData failed. Raising exception.")
        raise
    finally:
        assert len(test_dict) == 3, "test_dict length post-sectionalizing is incorrect."
        return test_dict


@pytest.mark.order(3)
def test_sectionalizeData_lengths(test_sectionalizeData_success):
    """
    Verifies the length of the testing data after sectionalizing.
    """
    for key in test_sectionalizeData_success.keys():
        assert len(test_sectionalizeData_success[key]) > 100, (
            str(key)
            + " does not meet length requirement: "
            + str(len(test_sectionalizeData_success[key]))
        )


@pytest.mark.order(4)
@pytest.mark.skip(reason="Unverified. Will check in future")
def test_sectionalizeData_headerCheck(test_sectionalizeData_success):
    """
    Verifies that the headers for each chunk after sectionalizing are correct.
    """
    temp_dict = test_sectionalizeData_success
    for key in temp_dict.keys():
        assert (
            list(temp_dict[key].columns.values)
            == [
                "Index",
                "Date",
                "Time",
                "New Device Time",
                "BG Source",
                "BG Reading (mg/dL)",
                "Linked BG Meter ID",
                "Basal Rate (U/h)",
                "Temp Basal Amount",
                "Temp Basal Type",
                "Temp Basal Duration (h:mm:ss)",
                "Bolus Type",
                "Bolus Volume Selected (U)",
                "Bolus Volume Delivered (U)",
                "Bolus Duration (h:mm:ss)",
                "Prime Type",
                "Prime Volume Delivered (U)",
                "Alarm",
                "Suspend",
                "Rewind",
                "BWZ Estimate (U)",
                "BWZ Target High BG (mg/dL)",
                "BWZ Target Low BG (mg/dL)",
                "BWZ Carb Ratio (g/U)",
                "BWZ Insulin Sensitivity (mg/dL/U)",
                "BWZ Carb Input (grams)",
                "BWZ BG Input (mg/dL)",
                "BWZ Correction Estimate (U)",
                "BWZ Food Estimate (U)",
                "BWZ Active Insulin (U)",
                "BWZ Status",
                "Sensor Calibration BG (mg/dL)",
                "Sensor Glucose (mg/dL)",
                "ISIG Value",
                "Event Marker",
                "Bolus Number",
                "Bolus Cancellation Reason",
                "BWZ Unabsorbed Insulin Total (U)",
                "Final Bolus Estimate",
                "Scroll Step Size",
                "Insulin Action Curve Time",
                "Sensor Calibration Rejected Reason",
                "Preset Bolus",
                "Bolus Source",
                "BLE Network Device",
                "Network Device Associated Reason",
                "Network Device Disassociated Reason",
                "Network Device Disconnected Reason",
                "Sensor Exception",
                "Preset Temp Basal Name",
            ]
        ).all(), (
            str(key) + " header issue detected. Is there a problem with indexxing?"
        )


@pytest.fixture
@pytest.mark.order(5)
def test_scrubFeatures_success(test_sectionalizeData_success):
    """
    Verifies that the scrubFeatures method functions correctly
    and only the necessary features for each chunk are present.
    """
    try:
        temp_dict = WeeklyDataPipeline.scrubFeatures(test_sectionalizeData_success)
    except:
        print(">>> Error scrubbing features. Rasing exception.")
        raise
    finally:
        assert (
            test_sectionalizeData_success["chunk1"]
            == [
                "Index",
                "Date",
                "Time",
                "Bolus Volume Delivered (U)",
                "Basal Rate (U/h)",
            ]
        ).all(), "Chunk1 contains unwanted indexes."

        assert "chunk2" not in list(
            test_sectionalizeData_success.keys()
        ), "Chunk2 has not been deleted."

        assert (
            test_sectionalizeData_success["chunk3"]
            == ["Index", "Date", "Time", "Sensor Glucose (mg/dL)"]
        ).all(), "Chunk3 contains unwanted indexes."
        return temp_dict


@pytest.fixture
@pytest.mark.order(6)
def test_castFeatures_success(test_scrubFeatures_success):
    """
    Verifies that the castFeatures method functions correctly.
    """
    try:
        temp_dict = WeeklyDataPipeline.castFeatures(test_scrubFeatures_success)
    except:
        print(">>> castFeatures failed. Rasing exception.")
        raise
    finally:
        return temp_dict


@pytest.mark.order(7)
@pytest.mark.skip(reason="Unverified. Will check in future")
def test_castFeatures_types(test_castFeatures_success):
    """
    Verifies that each of the features within the frames post-casting are correct.
    """
    temp_dict = test_castFeatures_success

    # Generic Checks for each df
    for key in temp_dict.keys():
        indexType = str(temp_dict[key]["Index"].dtypes)
        assert indexType == "float32", "Index type is incorrect: " + indexType

        dateType = str(temp_dict[key]["Date"].dtypes)
        assert dateType == "datetime64[ns]", "Date type is incorrect: " + dateType

        timeType = str(temp_dict[key]["Time"].dtypes)
        assert timeType == "object", "Time type is incorrect: " + timeType

    # Chunk1 Specific checks
    for _ in ["Bolus Volume Delivered (U)", "Basal Rate (U/h)"]:
        temp_type = str(temp_dict["chunk1"][_].dytpes)
        assert temp_type == "float32", _ + " type is incorrect: " + temp_type

    # Chunk3 Specific checks
    temp_type = str(temp_dict["chunk3"]["Sensor Glucose (mg/dL)"].dytpes)
    assert temp_type == "float32", (
        "Sensor Glucose (mg/dL) type is incorrect: " + temp_type
    )
    pass


@pytest.mark.order(8)
def test_pipeline_success():
    """
    Verifies that the pipeline runs successfully.
    """
    try:
        temp_dict = WeeklyDataPipeline.pipe()
    except:
        print(">>> WeeklyData Pipeline failed. Raising exception.")
        raise
    finally:
        return 0
