import datetime
import time

# from config import CHECKPOINT_NAME
from .scorecard_exceptions import InvalidAPIKeyError, InvalidJSONError, NoDataError, ServerError

MAX_RETRY = 3
OVERALL_CNT = 0
FACTOR_CNT = 0
ISSUE_CNT = 0
new_from_date = ''


class CompanyWriter(object):

    def __init__(self, company):
        self.__company = company
        
    def write_overall(self, **config):
        global OVERALL_CNT
        try:
            scores = self.__company.get_overall_score(**config)
        except KeyError:
            print("Getting overall score for {} to {} returned only "
                                    "1 entry for getting difference it needed  at least "
                                    "two entry".format(config['from_date'],
                                                       config['to_date']))
        except InvalidAPIKeyError as e:
            print("API key is invalid or expired. "
                                    "Please validate that your token is entered correctly")
            print(str(e))
            return
        except NoDataError as e:
            print("No Overall data found in between {} to {}".format(config['from_date'],
                                                                                       config['to_date']))
            print(str(e))
        except InvalidJSONError as e:
            print("Data received from API is not in JSON format")
            print(str(e))
        except ServerError as e:
            print("Sever error occurred while calling the Overall API")
            print(str(e))
            while OVERALL_CNT <= MAX_RETRY:
                OVERALL_CNT += 1
                print("Halt for 5 sec due to server error.")
                time.sleep(5)
                print("Resuming for {} time.")
                self.write_overall(**config)
            print("Retry limit exhausted for ServerError.")
        except Exception as e:
            print("Error in fetching company overall")
            print(str(e))
            raise
        else:
            score_list = []
            global new_from_date
            # Write overall score for company
            print("Total Overall received = {} ".format(len(scores)))
            if not config.get('portfolioId') and (len(scores) >1):
                try:
                    from_date = scores[-1]['dateToday'][:10]
                    new_from_date = str(datetime.datetime.strptime(from_date, '%Y-%m-%d') + datetime.timedelta(days=1))[:10]
                    print("New date for fetching data will be saved as {}".format(new_from_date))
                except Exception as err:
                    print('Error {} occurred while fetching from date'.format(err))
            override = config.get('diff_override_portfolio_overall') \
                if config.get('portfolioId') and config.get('portfolioName') \
                else config.get('diff_override_own_overall')
            for score in scores:

                if score.get('diff') != 0 or override:
                    score.pop('diff', None)
                    score.update({'severity': config['level_overall_change']})

                    # Insert portfolio id and name if present
                    if config.get('portfolioId') and config.get('portfolioName'):
                        score.update({
                            'portfolioId': config['portfolioId'],
                            'portfolioName': config['portfolioName'],
                        })
                    score_list.append(score)
            return score_list

    def write_factors(self, **config):
        global FACTOR_CNT
        try:
            factors = self.__company.get_factors(**config)
        except IndexError:
            print("Getting factor score from {} to {} returned only "
                                    "1 entry for getting difference it needed  at least "
                                    "two entry".format(config['from_date'], config['to_date']))
        except NoDataError as e:
            print("No factor data found in between {} to {}.".format(config['from_date'],
                                                                                      config['to_date']))
            print(str(e))
        except InvalidJSONError as e:
            print("Data received from API is not in JSON format")
            print(str(e))
        except ServerError as e:
            print("Server error occurred while calling the factors API")
            print(str(e))
            while FACTOR_CNT <= MAX_RETRY:
                FACTOR_CNT += 1
                print("Halt for 5 sec due to server error.")
                time.sleep(5)
                print("Resuming for {} time.")
                self.write_factors(**config)
        except Exception as e:
            print("Error in fetching company factors")
            print(str(e))
            raise
        else:
            factor_list = []
            print("Total Factors received = {} ".format(len(factors)))
            override = config.get('diff_override_portfolio_factor') \
                if config.get('portfolioId') and config.get('portfolioName') \
                else config.get('diff_override_own_factor')

            for factor in factors:
                if factor.get('diff') != 0 or override:
                    factor.pop('diff', None)
                    factor.update({'severity': config['level_factor_change']})

                    # Insert portfolio id and name if present
                    if config.get('portfolioId') and config.get('portfolioName'):
                        factor.update({
                            'portfolioId': config['portfolioId'],
                            'portfolioName': config['portfolioName'],
                        })
                    factor_list.append(factor)

            return factor_list

    def write_issues(self, **config):
        global ISSUE_CNT
        try:
            issues, issue_detail_list = self.__company.get_issue_levels(**config)
        except NoDataError as e:
            print("No issue data found in between {} to {}".format(config['from_date'],
                                                                                     config['to_date']))
            print(str(e))
        except InvalidJSONError as e:
            print("Data received from API is not in JSON format.")
            print(str(e))
        except ServerError as e:
            print("Server error occurred while calling the ISSUE API.")
            print(str(e))
            while ISSUE_CNT <= MAX_RETRY:
                ISSUE_CNT += 1
                print("Halt for 5 sec due to server error.")
                time.sleep(5)
                print("Resuming for {} time.")
                self.write_issues(**config)
        except Exception as e:
            print("Error in fetching company issues")
            print(str(e))
            raise
        else:
            result = []
            issues_list = []
            print('Total Issues received = {} '.format(len(issues)))
            for issue in issues:
                issue.update({'severity': config['level_new_issue_change']})

                # Insert portfolio id and name if present
                if config.get('portfolioId') and config.get('portfolioName'):
                    issue.update({
                        'portfolioId': config['portfolioId'],
                        'portfolioName': config['portfolioName'],
                    })
                issues_list.append(issue)
            result.append(issues_list)

            if config['fetch_issue_level_data']:
                result.append(issue_detail_list)

            return result
