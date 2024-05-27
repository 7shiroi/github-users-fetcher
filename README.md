# GitHub Users Fetcher

This script fetches GitHub user details based on a specified location and saves the data to a CSV file.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library

## Installation

First, make sure you have Python 3 installed. Then, install the required libraries using `pip`:

```sh
pip install requests pandas
```

# Usage

To run the script, use the following command:
```sh
python3 github_users_fetcher.py --location='some location' --token='your_github_token' --per_page=100
```

## Command-Line Arguments

- `--location`: (Required) The location to search for GitHub users.
- `--token`: (Required) Your GitHub token for authentication.
- `--per_page`: (Optional) The number of users to fetch per page (default: 100).

## Example

```sh
python3 github_users_fetcher.py --location='Selangor' --token='your_github_token' --per_page=50
```

# Output

The script will create a CSV file named github_users_<location>.csv containing the fetched user details.

## Sample Output

| username   | name         | email            | location |
|------------|--------------|------------------|----------|
| johndoe    | John Doe     | johndoe@gmail.com| Selangor |
| janedoe    | Jane Doe     | janedoe@gmail.com| Selangor |
| ...        | ...          | ...              | ...      |