# get_spot_dataset

This script fetches spot instance price information for all AWS regions and saves the data as CSV files.

## Features
- Retrieves AWS Spot Instance pricing using the `spotinfo` command.
- Supports fetching data for all available AWS regions.
- Saves the output in CSV format for easy analysis.
- Handles errors and missing credentials gracefully.

## Requirements
- Python 3.x
- AWS CLI configured with proper credentials
- `boto3` library
- `sps` module (used for retrieving AWS region list)

## Installation
Ensure you have the required dependencies installed:
```bash
pip install boto3 sps
```

## Usage
Run the script to fetch spot instance price information and save it to CSV files:
```bash
python spotinfo_csv.py
```

## Output
The script saves CSV files in the `spot_prices_by_region_csv` directory, named by region.

## Error Handling
- If the `spotinfo` command fails, an error message is logged.
- If AWS credentials are missing or incomplete, the script catches and reports the error.

## License
This project is open-source. Modify and distribute it as needed.

