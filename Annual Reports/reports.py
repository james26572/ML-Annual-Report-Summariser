# Download 10ks to local machine 

from sandp500_tickers import save_sp500_tickers
from sec_api import QueryApi
from sec_api import ExtractorApi

api_key = "b8113d497aa775cb50186f7f03c97c7e8b3158734705787264d31e7f627dc6db"

tickers = save_sp500_tickers()

# Creating a new instance of the queryapi 

queryapi = QueryApi(api_key)
extractorApi = ExtractorApi(api_key)

base_query = {
  "query": { 
      "query_string": { 
          "query": "PLACEHOLDER", # this will be set during runtime 
          "time_zone": "America/New_York"
      } 
  },
  "from": "0",
  "size": "10", # dont change this
  # sort returned filings by the filedAt key/value
  "sort": [{ "filedAt": { "order": "desc" } }]
}

# This function writes 10k filing urls   for ticker = ticker to ticker.txt from start_year to end_year

def get_urls_for_ticker(base_query, ticker, start_year, end_year):
  log_file = open('{ticker}.txt'.format(ticker = ticker), 'a')
  for year in range(end_year, start_year, -1):
    print('Starting {year}'.format(year = year))
    universe_query = "ticker:{ticker} AND ".format(ticker = ticker) + \
      "filedAt:[{year}-01-01 TO {year}-12-31] AND ".format(year = year) + \
      "formType:\"10-K\""  
    base_query["query"]["query_string"]["query"] = universe_query
    response = queryapi.get_filings(base_query)
    urls_list = list(map(lambda x: x["linkToFilingDetails"], response["filings"]))
    print(urls_list)
    if (len(urls_list) == 0):
      print("No annual report for {year}! Breaking out of function -> assuming IPO was in {year}".format(year = year))
      break
    log_file.write(urls_list[-1] + "\n")
    print("Filing URLs downloaded for {year}-01".format(year=year))
  log_file.close()



''' 
1 - Business
1A - Risk Factors
1B - Unresolved Staff Comments
2 - Properties
3 - Legal Proceedings
4 - Mine Safety Disclosures
5 - Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities
6 - Selected Financial Data (prior to February 2021)
7 - Management’s Discussion and Analysis of Financial Condition and Results of Operations
7A - Quantitative and Qualitative Disclosures about Market Risk
8 - Financial Statements and Supplementary Data
9 - Changes in and Disagreements with Accountants on Accounting and Financial Disclosure
9A - Controls and Procedures
9B - Other Information
10 - Directors, Executive Officers and Corporate Governance
11 - Executive Compensation
12 - Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters
13 - Certain Relationships and Related Transactions, and Director Independence
14 - Principal Accountant Fees and Services
'''
# Getting the clean-text of an item (see above) for the list of urls in a .txt file located at path

def get_section(path, item): 
    file = open(path, 'r')
    lines = file.readlines()
    output_file = open(path[:-3] + "_{item}.txt".format(item = item), 'a')
    for url in lines:
      print(url)
      section_text = extractorApi.get_section(url, item, "text")
      output_file.write(section_text + "\n\n\n")
    output_file.close()

# Testing above function 

# Getting just the 10ks for TSLA from the year 2022 to 2000

# get_urls_for_ticker(base_query, 'TSLA', 2000, 2022)

get_section('./TSLA.txt', '7')
