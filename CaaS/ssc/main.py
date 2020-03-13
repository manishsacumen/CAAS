
# encoding = utf-8

import datetime

from .scorecard import Portfolio
from .scorecard_exceptions import InvalidJSONError, ServerError

# from config import FIELDS, DAYS, CHECKPOINT_NAME
from .scorecard import Company
from .ssc_processor import CompanyWriter

def collect_events(access_key, domain, **options):
    """Implement your data collection logic here
    """

    print("Process started at {}.".format(datetime.datetime.now()))

    # options = extract_input_fields(FIELDS)
    #options = {}

    # access_key = options.get('access_key')
    # domain = options.get('domain')
    #pdb.set_trace()

    level_overall_change = options.get('level_overall_change', 7)
    level_factor_change = options.get('level_factor_change', 7)
    level_new_issue_change = options.get('level_new_issue_change', 7)

    portfolio_ids = options.get('portfolio_ids')
    # proxy = options.get('proxy')
    proxy = {}
    to_date = datetime.datetime.now().date()

    fetch_company_overall = options.get('fetch_company_overall', False)
    fetch_company_factors = options.get('fetch_company_factors', False)
    fetch_company_issues = options.get('fetch_company_issues', False)
    fetch_portfolio_overall = options.get('fetch_portfolio_overall', False)
    fetch_portfolio_factors = options.get('fetch_portfolio_factors', False)
    fetch_portfolio_issues = options.get('fetch_portfolio_issues', False)
    fetch_issue_level_data = options.get('fetch_issue_level_data', False)

    diff_override_own_overall = options.get('diff_override_own_overall', True)
    diff_override_portfolio_overall = options.get('diff_override_portfolio_overall', False)
    diff_override_own_factor = options.get('diff_override_own_factor', False)
    diff_override_portfolio_factor = options.get('diff_override_portfolio_factor', False)

    # check_point_date = helper.get_check_point(CHECKPOINT_NAME)
    check_point_date = '2020-03-04'
    # import pdb
    # pdb.set_trace()

    # If date is there in check point or it will start from 20 days back(for 1st run).
    from_date = check_point_date if check_point_date else str(to_date - datetime.timedelta(days=10))

    print('Started logging records, from {} to {}'.format(from_date, to_date))


    config = {
        'level_overall_change': level_overall_change,
        'level_factor_change': level_factor_change,
        'level_new_issue_change': level_new_issue_change,
        'portfolio_ids': portfolio_ids,
        'to_date': to_date,
        'from_date': from_date,
        'proxy': proxy,
        'diff_override_own_overall': diff_override_own_overall,
        'diff_override_portfolio_overall': diff_override_portfolio_overall,
        'diff_override_own_factor': diff_override_own_factor,
        'diff_override_portfolio_factor': diff_override_portfolio_factor,
        'fetch_issue_level_data': fetch_issue_level_data
    }

    company = Company(access_key=access_key, domain=domain)
    company_writer = CompanyWriter(company)
    result = {}
    # Fetch overall score for company
    if fetch_company_overall:
        overall_resp = company_writer.write_overall(**config)
        result.update({'overall_resp':overall_resp})
        print('Company overall logged.')

    # Fetch factors for company
    if fetch_company_factors:
        factor_resp = company_writer.write_factors(**config)
        result.update({'factor_resp': factor_resp})
        print('Company factors logged.')

    # Fetch issues and issue level details for company
    if fetch_company_issues:
        issue_resp = company_writer.write_issues(**config)
        result.update({'issue_resp': issue_resp})
        print('Company issues logged.')

    print("Start processing portfolio companies.")
    if portfolio_ids:
        ids = None if portfolio_ids == 'all' else portfolio_ids
        portfolio = build_portfolio(access_key, ids, **config)
        print("Total portfolio companies = {}.".format(len(portfolio.companies)))

        for company in portfolio.companies:
            company_writer = CompanyWriter(company)
            print("Processing portfolio company {} ".format(company.domain))
            config.update({
                'portfolioId': company.portfolio_id,
                'portfolioName': "'" + company.portfolio_name + "'",
            })

            # Fetch overall score for company
            if fetch_portfolio_overall:
                port_overall = company_writer.write_overall(**config)
                result.update({'port_overall': port_overall})
                print('Logged portfolio company {} overall'.format(company.domain))

            # Fetch factors for company
            if fetch_portfolio_factors:
                port_factor = company_writer.write_factors(**config)
                result.update({'port_factor': port_factor})
                print('Logged portfolio company {} factor'.format(company.domain))

            # Fetch issues and issue level details for company
            if fetch_portfolio_issues:
                port_issue = company_writer.write_issues(**config)
                result.update({'port_issue': port_issue})
                print('Logged portfolio company {} issue'.format(company.domain))

    print("Process finished at {}.".format(datetime.datetime.now()))
    return result



def build_portfolio(access_key, ids, **config):
    try:
        portfolio = Portfolio(access_key, ids, **config)
    except InvalidJSONError as e:
        print("Data received from API is not in JSON format.")
        print("No portfolios to proceed. Stopping...")
        raise
    except ServerError as e:
        print("Sever error occurred while calling the API")
        print("No portfolios to proceed. Stopping...")
        raise
    except Exception as e:
        print("Error in finding portfolios")
        raise

    for invalid_id in portfolio.invalid_ids:
        print("The Portfolio ID {} invalid. "
                         "Please validate that your portfolio ID is entered correctly".format(invalid_id))

    return portfolio


def extract_input_fields(fields):
    inputs = {}
    for field in fields:
        inputs[field] = helper.get_arg(field)

    inputs['proxy'] = ''
    message = 'Proxy settings found' if inputs['proxy'] else 'No proxy settings found'
    print(message)

    inputs['portfolio_ids'] = format_portfolio_ids(inputs.get('portfolio_ids'))

    if not inputs['portfolio_ids']:
        helper.log_warning('No portfolio ids received. Fetching data from portfolio companies will be skipped')
    elif inputs['portfolio_ids'] == 'all':
        print('Data from all portfolio companies will be fetched')
    else:
        print('Data from following portfolios will be fetched.\n{}'.format(inputs['portfolio_ids']))

    return inputs



def format_portfolio_ids(portfolio_ids):
    try:
        # Python 2.7
        is_string = isinstance(portfolio_ids, unicode)
    except NameError:
        # Python 3
        is_string = isinstance(portfolio_ids, str)

    if is_string and portfolio_ids.strip().strip(',').lower() == 'all':
        portfolio_ids = 'all'
    elif is_string:
        portfolio_ids = portfolio_ids.strip().strip(',')
        portfolio_ids = portfolio_ids.split(',') if portfolio_ids else None

    return portfolio_ids

