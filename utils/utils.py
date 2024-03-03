from datetime import datetime
import pytz

def convert_unix_to_datetime(unix_timestamp):
    # Convert the UNIX timestamp to a datetime object
    dt_object = datetime.fromtimestamp(unix_timestamp, pytz.UTC)
    # Format the datetime object to match the desired format
    return dt_object.strftime('%Y-%m-%d %H:%M:%S%z')

if __name__ == '__main__':
    # Example usage of the function
    example_timestamp = 1709393673
    print(convert_unix_to_datetime(example_timestamp))