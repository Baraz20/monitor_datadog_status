import argparse
import requests
import time


def monitor_datadog_status(freq: int) -> None:
    """
    this function prints DataDog's non-operational components status at a regular frequency.
    :param freq: the frequency (in seconds) in which to check the status
    """

    # defining helper function
    def process_datadog_status(data: dict) -> None:
        """
        helper function to process/filter the json respond from the API,
        and print the non-operational components.
        :param data: the json respond from the API.
        """
        for component in data["components"]:
            if "operational" not in component["status"]:
                now = time.strftime("%d/%m/%Y %H:%M:%S")
                print(f'{now} Component {component["name"]} is in status: {component["status"]}')

    # The API's URL
    URL = "https://status.datadoghq.com/api/v2/components.json"
    start_time = int(time.time())
    # making a request every @freq seconds
    while 1:
        process_datadog_status(requests.get(URL).json())
        time.sleep(freq - (time.time() - start_time) % freq)


if __name__ == '__main__':
    # creating parser for CLI and it's arguments
    parser = argparse.ArgumentParser(
        description="checks DataDog's component status at a regular frequency.")

    parser.add_argument('--frequency', required=True, type=int,
                        help="Enter the frequency at which you want to check DataDog's component status.")

    args = parser.parse_args()
    monitor_datadog_status(args.frequency)
