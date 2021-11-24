import argparse
from time import sleep
from os import listdir, rename
from src.data.mcl_interface import MCL_Interface
from src.pipelines.pipelines import WeeklyDataPipeline

# CLI Argument settings.
# parser = argparse.ArgumentParser()

# parser.add_argument(
#     "--filename",
#     default="mcl_raw_data.csv",
#     type=str,
#     help="Name of the CSV file from Medtronic's CareLink portal.",
# )
# args = parser.parse_args()

# if args.filename:
#     print("Output file set to: " + str(args.filename))


def main(user, token):
    """
    Downloads the appropriate datasets from Medtronic CareLink
    """
    dl_agent = MCL_Interface(user, token)
    dl_agent.login()
    dl_agent.pullCSVReports()

    # This sleep command adds a buffer of time to allow for data to be written to disk
    sleep(5)

    try:
        external_path = "data/raw/"
        for _ in listdir(external_path):
            if _.endswith(".csv"):
                # rename(external_path + _, external_path + args.filename)
                rename(external_path + _, external_path + "raw_data.csv")
    except:
        raise
    finally:
        """
        TODO:
        1. Run data pipeline
        2. Calculate statistics
        """
        # cleaned_dict = WeeklyDataPipeline.pipe()
        pass


if __name__ == "__main__":
    """
    Execute main method.
    """
    main()
