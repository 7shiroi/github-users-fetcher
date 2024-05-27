import requests
import pandas as pd
import argparse
import time

def get_github_users(location, token, per_page=100, max_retries=5, retry_delay=5):
    headers = {'Authorization': f'token {token}'}
    users = []
    page = 1

    while True:
        url = f'https://api.github.com/search/users?q=location:{location}&per_page={per_page}&page={page}'
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    break
                else:
                    print(f"Failed to retrieve data: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            print(f"Failed to retrieve data after {max_retries} attempts.")
            break

        data = response.json()
        users.extend(data.get('items', []))
        
        if len(data.get('items', [])) < per_page:
            break
        
        page += 1

    return users

def get_user_details(username, token, max_retries=5, retry_delay=5):
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/users/{username}'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to retrieve user details: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else:
        print(f"Failed to retrieve user details for {username} after {max_retries} attempts.")
        return None

def main(location, token, per_page):
    print(f'Getting users from {location}')
    users = get_github_users(location, token, per_page)
    user_data = []

    count = 0
    for user in users:
        count += 1
        print(f"Getting user details ({count}/{len(users)})")
        details = get_user_details(user['login'], token)
        
        if details and 'email' in details and details['email']:
            user_data.append({
                'username': details['login'],
                'name': details['name'],
                'email': details['email'],
                'location': details.get('location', location)
            })

    df = pd.DataFrame(user_data)
    filename = f'github_users_{location}.csv' 
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch GitHub users by location.')
    parser.add_argument('--location', required=True, help='Location to search for GitHub users')
    parser.add_argument('--token', required=True, help='GitHub token for authentication')
    parser.add_argument('--per_page', type=int, default=100, help='Number of users to fetch per page (default: 100)')

    args = parser.parse_args()
    main(args.location, args.token, args.per_page)
