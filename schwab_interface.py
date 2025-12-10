import schwabdev
import logging
import os
import time
import json
import threading
import copy

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from accurate_time import get_ntp_time
from file_writer import update_file

from templates import COMPANY_INFO_TEMPLATE

load_dotenv()

message_received = []

# Constant variables for each day (11 per day)
DAY_ONE_COMPANIES = 'FUBO,ROKU,AFRM,ABNB,ELF,NFLX,SPOT,ARM,GTLB,VEEV,XYZ'
DAY_TWO_COMPANIES = 'TSLA,CART,COIN,GBX,DASH,SNAP,APP,IONQ,TOST,HIMS,CMG'
DAY_THREE_COMPANIES = 'SBUX,CVNA,META,PLTR,FFIV,INTC,IBM,SAP,IBKR,NKE,ADBE'

def establish_client() -> schwabdev.Client:
    """
    Establish a connection with the Charles Schwab API and store it within a client.
    The client will be used to access all Charles Schwab API funcntionality.

    @return a schwabdev.Client that will serve as our Charles Schwab API interface.
    """

    logging.basicConfig(level=logging.INFO)

    client = schwabdev.Client(
        os.getenv('CLIENT_ID'),
        os.getenv('CLIENT_SECRET'),
        os.getenv('CALLBACK_URL'),
        timeout=500
    )

    return client

def start_stream(companies: str, client: schwabdev.Client) -> None:
    """
    Creates a connection with a Charles Schwab API Data Stream and begins the flow of information
    by specifying exactly what we wish to receive per the companies provided as a parameter. The
    stream values we are concerned with are the following: 
    - 0: The company tickers we wish to observe
    - 1: The current bid price of the tickers we are observing
    - 2: The current ask price of the tickers we are observing
    - 4: The current bid size of the tickers we are observing
    - 5: The current ask size of the tickers we are observing
    - 10: The high price of the tickers we are observing
    - 11: The low price of the tickers we are observing
    - 29: The regular market last price of the tickers we are observing (to observe after hours
    movement)

    @param companies a string containing all companies we are observing separated by commas.
    @param client the Charles Schwab client enabling us to create the data stream.
    """

    streamer = client.stream

    def my_handler(message):
        global message_received

        stream_message = json.loads(message)

        if 'notify' in stream_message:
            if 'heartbeat' not in stream_message['notify'][0]:
                message_received = stream_message
        else:
            message_received = stream_message

    # Start Charles Schwab Api Stream of Level One Equities Information
    try:
        streamer.start(my_handler)
        streamer.send(streamer.level_one_equities(companies, "0,1,2,4,5,10,11,29"))
    except Exception as e:
        print(f"Stream encountered an error: {e}. Reconnecting in 5 seconds...")
        time.sleep(5)

    return None

def populate_company_dict(companies: str) -> dict:
    """
    Populate each company in the company_info dictionary with the imported template.

    @param companies a string containing each company ticker separated by commas.
    """

    company_list = companies.split(',')
    company_info = {}

    for company in company_list:
        company_info[company] = copy.deepcopy(COMPANY_INFO_TEMPLATE)
    
    company_info['Update Flag'] = bool

    return company_info

def extract_content(content: list, company_info: dict) -> None:
    """
    Extract all of the numbers provided by the data stream and update the dictionary values if values have
    changed.

    @param content a list containing the content provided by the data stream.
    @param company_info a dictionary containing all information related to each company we are observing.
    """

    for item in content:
        try:
            if item['1'] == company_info[item['key']]['Bid Price']:
                continue

            company_info[item['key']]['Bid Price'] = item['1']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )
                
        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH BID {e}')

        try:
            if item['2'] == company_info[item['key']]['Ask Price']:
                continue

            company_info[item['key']]['Ask Price'] = item['2']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )

        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH ASK {e}')
        
        try:
            if item['4'] == company_info[item['key']]['Bid Size']:
                continue

            company_info[item['key']]['Bid Size'] = item['4']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )
                
        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH BID SIZE {e}')
            
        try:
            if item['5'] == company_info[item['key']]['Ask Size']:
                continue

            company_info[item['key']]['Ask Size'] = item['5']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )

        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH ASK SIZE {e}')

        try:
            if item['10'] == company_info[item['key']]['High Price']:
                continue

            company_info[item['key']]['High Price'] = item['1']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )

        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH HIGH PRICE {e}')
            
        try:
            if item['11'] == company_info[item['key']]['Low Price']:
                continue

            company_info[item['key']]['Low Price'] = item['11']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )

        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH LOW PRICE {e}')
        
        try:
            if item['29'] == company_info[item['key']]['Close Price']:
                continue

            company_info[item['key']]['Close Price'] = item['29']
            company_info['Update Flag'] = (
                True if company_info['Update Flag'] is False 
                else True
            )

        except KeyError:
            pass
        except Exception as e:
            print(f'UNKNOWN ERROR WITH CLOSE PRICE {e}')

    return None

def main() -> None:
    """
    The main function which will serve as the central point of the script. Here all functionality
    will be called.
    """

    client = establish_client()
    
    # Stream For Day 1 Companies
    # stream_thread = threading.Thread(target=start_stream, args=(DAY_ONE_COMPANIES,client,), daemon=True)
    
    # Stream For Day 2 Companies
    # stream_thread = threading.Thread(target=start_stream, args=(DAY_TWO_COMPANIES,client,), daemon=True)
    
    # Stream For Day 3 Companies
    stream_thread = threading.Thread(target=start_stream, args=(DAY_THREE_COMPANIES,client,), daemon=True)

    stream_thread.start()

    reference_utc = get_ntp_time()
    local_reference = datetime.now(timezone.utc)

    time_format = "%I:%M:%S.%f %p"

    # Company Info For Day 1 Companies
    # company_info = populate_company_dict(DAY_ONE_COMPANIES)
    
    # Company Info For Day 2 Companies
    # company_info = populate_company_dict(DAY_TWO_COMPANIES)
    
    # Company Info For Day 3 Companies
    company_info = populate_company_dict(DAY_THREE_COMPANIES)

    while True:
        content = []

        if len(message_received) > 0:
            if 'data' in message_received:
                content = message_received['data'][0]['content']

        # Adjust the returned time from our utc reference to accurately reflect EST
        elapsed = datetime.now(timezone.utc) - local_reference
        adjusted_utc = reference_utc + elapsed
        adjusted_est = adjusted_utc.replace(tzinfo=ZoneInfo("UTC"))
        current_time = adjusted_est.strftime(time_format)

        ## Might need time below incase we need to re-establish NTP connection 
        # hour = int(current_time.split(':')[0])
        # minute = int(current_time.split(':')[1])
        # second = int(current_time.split(':')[2].split('.')[0])
        # millisecond = float(current_time.split(':')[2].split('.')[1].split(' ')[0]) / 1000000

        if len(content) > 0:
            extract_content(content, company_info)

        if company_info['Update Flag'] is True:
            # Update File For Day 1 Companies
            # update_file('Day1', DAY_ONE_COMPANIES, company_info, current_time)
            
            # Update File For Dday 2 Companies
            # update_file('Day2', DAY_TWO_COMPANIES, company_info, current_time)
            
            # Update File For Day 3 Companies
            update_file('Day3', DAY_THREE_COMPANIES, company_info, current_time)


        # print(f'CURRENT TIME: {current_time}')
        

if __name__ == '__main__':
    main()
