"""Module to get data from Security Scorecard"""

from collections import OrderedDict

from .formatters import format_date_string
from .scorecard_exceptions import NoDataError
from .utils import connect_to_ss, get_value_from_dict_list


class ScoreCard(object):
    """Represents a scorecard object"""
    default_server_url = 'https://api.securityscorecard.io'

    def __init__(self, access_key, base_url=None):
        self.__access_key = access_key
        self.__base_url = base_url or self.default_server_url

    def get_overall_score_url(self, company):
        return '{}/companies/{}/history/score'.format(self.__base_url, company)

    def get_factors_meta_url(self):
        return '{}/metadata/factors'.format(self.__base_url)

    def get_factor_score_url(self, company):
        return '{}/companies/{}/history/factors/score'.format(self.__base_url, company)

    def get_issue_types_meta_url(self):
        return '{}/metadata/issue-types'.format(self.__base_url)

    def get_issue_levels_url(self, company):
        return '{}/companies/{}/history/events'.format(self.__base_url, company)

    def get_portfolios_url(self):
        return '{}/portfolios'.format(self.__base_url)

    def get_portfolio_data_url(self, portfolio_id):
        return "{}/portfolios/{}/companies".format(self.__base_url, portfolio_id)

    @staticmethod
    def generate_overall_score(company, today_values, yesterday_values):
        diff = today_values['score'] - yesterday_values['score']

        return OrderedDict([
            ('body', 'OverAll'),
            ('type', "'scoreChange'"),
            ('src', 'OverallScore'),
            ('subject', company),
            ('dateYesterday', format_date_string(yesterday_values.get('date', ''))),
            ('dateToday', format_date_string(today_values.get('date', ''))),
            ('scoreYesterday', yesterday_values.get('score', '')),
            ('scoreToday', today_values.get('score', '')),
            ('scoreChange', diff),
            ('diff', diff),
        ])

    def get_overall_score(self, company, **config):
        from_date, to_date = config.get('from_date'), config.get('to_date')
        params = {'date_from': from_date, 'date_to': to_date} if from_date and to_date else {}
        scores = connect_to_ss(
            self.get_overall_score_url(company),
            token=self.__access_key,
            params=params,
            proxy=config.get('proxy'),
        )

        if not scores['entries']:
            raise NoDataError
        rv = []

        try:
            # Python 2.7
            range_ = xrange
        except Exception:
            # Python 3
            range_ = range

        for l in range_(len(scores['entries']) - 1):
            yesterday_values = scores['entries'][l]
            today_values = scores['entries'][l+1]
            rv.append(self.generate_overall_score(company, today_values, yesterday_values))
        return rv

    @staticmethod
    def generate_factors(company, today_values, yesterday_values, factors_meta):
        rv = []
        for factor in today_values.get('factors', []):
            name = factor['name']
            other = get_value_from_dict_list(today_values['factors'], 'name', name)
            diff = factor['score'] - other['score'] if other else 0
            matched_factor = get_value_from_dict_list(factors_meta, 'key', name)
            try:
                factor_description = matched_factor.get('description', '')
            except KeyError:
                factor_description = 'data is not there'
            except AttributeError:
                factor_description = 'data is not there'

            rv.append(OrderedDict([
                ('body', 'Factor'),
                ('type', "'scoreChange'"),
                ('src', name),
                ('subject', company),
                ('dateYesterday', format_date_string(yesterday_values.get('date', ''))),
                ('dateToday', format_date_string(today_values.get('date', ''))),
                ('scoreYesterday', other['score']),
                ('scoreToday', factor['score']),
                ('scoreChange', diff),
                ('diff', diff),
                ('factorDescription', "'{}'".format(factor_description))
            ]))

        return rv

    def get_factors(self, company, **config):
        factors_meta = connect_to_ss(
            self.get_factors_meta_url(),
            token=self.__access_key,
            proxy=config.get('proxy'),
        )['entries']
        from_date, to_date = config.get('from_date'), config.get('to_date')
        params = {'date_from': from_date, 'date_to': to_date, 'timing': 'daily'} if from_date and to_date else {}
        url = self.get_factor_score_url(company)

        factors = connect_to_ss(
            url,
            token=self.__access_key,
            params=params,
            proxy=config.get('proxy'),
        )

        if not factors['entries']:
            raise NoDataError
        rv = []

        try:
            # Python 2.7
            range_ = xrange
        except Exception:
            # Python 3
            range_ = range

        for l in range_(len(factors['entries']) - 1):
            yesterday_values = factors['entries'][l]
            today_values = factors['entries'][l + 1]
            rv.extend(self.generate_factors(company, today_values, yesterday_values, factors_meta))
        return rv

    def get_issue_levels(self, company, **config):
        """Finds all the issue levels for a company

        :param company: str
        :return: list of dicts
        """

        issue_types = connect_to_ss(
            self.get_issue_types_meta_url(),
            self.__access_key,
            proxy=config.get('proxy'),
        )['entries']

        url = self.get_issue_levels_url(company)
        # date = config.get('from_date')
        from_date = config.get('from_date')
        to_date = config.get('to_date')

        if from_date:
            # For issue levels from date and to date are the same.
            from_date = '{}T00:00:00Z'.format(from_date)
            to_date = '{}T00:00:00Z'.format(to_date)
            params = {'date_from': from_date, 'date_to': to_date}
        else:
            params = {}

        levels = connect_to_ss(
            url,
            self.__access_key,
            params=params,
            proxy=config.get('proxy'),
        )

        if not levels['entries']:
            raise NoDataError

        issue_detail_list = []
        if config.get('fetch_issue_level_data'):
            error_list = []
            # issue_level_entries(levels['entries'])
            for issue in levels['entries']:
                try:
                    issue_details = connect_to_ss(issue['detail_url'],
                                                  self.__access_key,
                                                  params=params,
                                                  proxy=config.get('proxy')
                                                  )
                    for issue_detail in issue_details['entries']:
                        issue_detail['eventId'] = issue.get('id', 'Not found any id corresponding to this issue')
                        issue_detail['issueType'] = issue.get('issue_type',
                                                              'Not found any issue type corresponding to this issue')
                        issue_detail['factor'] = issue.get('factor', 'Not found any factor corresponding to this issue')
                        issue_detail['ssc_domain'] = company

                        issue_detail_list.append(issue_detail)
                except Exception:
                    error_list.append(issue['detail_url'])
            if error_list:
                issue_detail_list.append({'error': error_list})
        group_status_mapping = {
            'active': 'Issues Observed',
            'departed': 'Issues UnObserved',
            'resolved': 'Issues Refuted',
        }

        return map(
            lambda entry: OrderedDict([
                ('body', 'Issue'),
                ('type', "'{}'".format(group_status_mapping.get(entry['group_status'], 'Unknown'))),
                ('src', entry['factor']),
                ('eventID', entry['id']),
                ('subject', company),
                ('date', format_date_string(entry['date'])),
                ('issueType', entry['issue_type']),
                ('findingsCount', entry['issue_count']),
                ('groupStatus', entry['group_status']),
                ('issueName', "'{}'".format(
                    get_value_from_dict_list(issue_types, 'key', entry['issue_type'])['title'])),
                ('totalScoreImpact', entry.get('total_score_impact')),
                ('severity_value', entry.get('severity')),
                # ('IssueTypeDescription', get_value_from_dict_list(issue_types, 'key', entry['issue_type'])['title']),
                # ('factor', entry['factor']),
            ]),
            filter(lambda each: each['issue_type'] != 'breach', levels['entries'])
        ), issue_detail_list

    def get_portfolios(self, **config):
        portfolio = connect_to_ss(
            self.get_portfolios_url(),
            self.__access_key,
            proxy=config.get('proxy'),
        )
        return portfolio['entries']

    def get_portfolio_data(self, portfolio_id, **config):
        companies = connect_to_ss(
            self.get_portfolio_data_url(portfolio_id),
            self.__access_key,
            proxy=config.get('proxy'),
        )
        return companies['entries']


class Company(object):
    """Represents a company object."""

    def __init__(self, access_key, domain, portfolio_id=None, portfolio_name=None):
        self.score_card = ScoreCard(access_key)
        self.domain = domain
        self.portfolio_id = portfolio_id
        self.portfolio_name = portfolio_name

    def get_overall_score(self, **config):
        return self.score_card.get_overall_score(self.domain, **config)

    def get_factors(self, **config):
        return self.score_card.get_factors(self.domain, **config)

    def get_issue_levels(self, **config):
        return self.score_card.get_issue_levels(self.domain, **config)


class Portfolio(object):
    """Represents a portfolio object."""

    def __init__(self, access_key, ids=None, **config):
        self.score_card = ScoreCard(access_key)
        self.companies = []
        self.invalid_ids = []
        self.valid_ids = []

        portfolios = self.score_card.get_portfolios(**config)

        if ids:
            portfolios = list(filter(lambda val: val['id'] in ids, portfolios))
            self.valid_ids = [val['id'] for val in portfolios]
            self.invalid_ids = list(filter(lambda val: val not in self.valid_ids, ids))
        else:
            self.valid_ids = [val['id'] for val in portfolios]

        for portfolio in portfolios:
            portfolio_data = self.score_card.get_portfolio_data(portfolio['id'])
            self.companies.extend(map(
                lambda val: Company(
                    access_key=access_key,
                    domain=val['domain'],
                    portfolio_id=portfolio['id'],
                    portfolio_name=portfolio['name'],
                ),
                portfolio_data,
            ))
