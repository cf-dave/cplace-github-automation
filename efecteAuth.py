import requests
import json
import logging
import github
import os
import enum

dc_url = 'https://cplace.efectecloud-test.com/itsm/EfecteFrameset.do#/workspace/datacard/view/'


class EfecteApi:
    BASE_API_URL = 'https://cplace.efectecloud-test.com/rest-api/itsm/v1'

    def __init__(self, login: str, password: str):
        self.jwt_token = self._generate_jwt_token(login, password)
        self.headers = {
            'accept': 'application/json',
            'Authorization': self.jwt_token
        }

    def _generate_jwt_token(self, login: str, password: str) -> str:
        response = requests.post(self.BASE_API_URL + '/users/login', data={"login": login, "password": password})
        if response.status_code == 200:
            logging.info(f"Acquired token starting with")
            return response.headers['Authorization']
        else:
            logging.error(f"Can't acquire jwt token. Status code {response.status_code}.")
            return ""

    def get_datacards(self, template_code: str, selected_attributes, limit: int = 50, data_cards=True):
        params = {
            "limit": limit,
            "filterId": 100000000,
            'selectedAttributes': ",".join(selected_attributes),
            'dataCards': data_cards if len(selected_attributes) != 0 else False
        }
        response = requests.get(self.BASE_API_URL + f'/dc/{template_code}/data', headers=self.headers, params=params)

        # TODO check meta for count < limit and request recursely

        try:
            return response.json()["data"]
        except KeyError:
            # TODo error handling
            return dict()

    def get_datacard(self, template_code: str, datacard_id: int, selected_attributes):
        params = {
            'selectedAttributes': ",".join(selected_attributes),
        }
        response = requests.get(self.BASE_API_URL + f'/dc/{template_code}/data/{datacard_id}', headers=self.headers,
                                params=params)
        return response.json()

    def get_all_datacards(self):
        response = requests.get(self.BASE_API_URL + f'/dc/', headers=self.headers)
        return response.json()


class GithubTicketStatus(enum.Enum):
    NOT_STARTED = 1
    WAITING_FOR_APPROVAL = 2
    APPROVED = 3
    IN_IMPLEMENTATION = 5
    WAITING_FOR_DELIVERY = 6
    CLOSED = 10


class GithubApi:

    def __init__(self, token):
        self.cplace_github = github.Github(token)

    def add_user_ticket(self, ticket):
        # https://docs.github.com/en/rest/collaborators/collaborators#add-a-repository-collaborator
        self.cplace_github.get_repo(ticket.repo_name).add_to_collaborators(ticket.github_user, ticket.permission)


class GithubTicket:

    def __init__(self, status: str, github_user: str, repo_name: str, permission: str, justification: str):
        self.status = status
        self.github_user = github_user
        self.repo_name = repo_name
        self.permission = permission
        self.justification = justification


class GithubAccessTicket(GithubTicket):

    def __init__(self, status: str, github_user: str, repo_name: str, permission: str, justification: str):
        super().__init__(status, github_user, repo_name, permission, justification)


class GithubCreateRepoTicket(GithubTicket):

    def __init__(self, status: str, github_user: str, repo_name: str, permission: str, justification: str):
        super().__init__(status, github_user, repo_name, permission, justification)


def parse_github_tickets(github_tickets: list):

    def extract_val(attribute: dict):
        if "values" in attribute.keys() and len(attribute["values"]) > 0:
            return attribute["values"][0]["value"]

    relevant_tickets = list()
    for ticket in github_tickets:
        data = ticket["data"]

        # TODO this is bullshit, this should be changed in Efecte not worked around in code
        try:
            html_info = extract_val(data["AdditionalInformation"])[3:-4].split("<br>")
            user, repo, permission, justification = [line.split(":", maxsplit=1)[-1] for line in html_info]
            relevant_tickets.append(GithubTicket(extract_val(data["status"]), user, repo, permission, justification))

        except Exception:
            pass

    return relevant_tickets


def filter_github_tickets(tickets: list):
    github_tickets = list()
    for ticket in tickets:
        # tickets of GitHub Managment
        service_offerings = ticket["data"]["ServiceOffering"]["values"]
        if len(service_offerings) > 0 and "GitHub Management" in [service["value"] for service in service_offerings]:
            github_tickets.append(ticket)

    return github_tickets


def main():
    # TODO move credentials to github secrets
    # github_api = GithubApi(os.environ["github_token"])

    efecte_api = EfecteApi('restp-api-test', 'Cplace123!')

    service_request_tickets = efecte_api.get_datacards("ServiceRequest", ('ServiceOffering', 'status', 'AdditionalInformation'), limit=100)
    service_request_tickets = filter_github_tickets(service_request_tickets)
    github_tickets = parse_github_tickets(service_request_tickets)


if __name__ == "__main__":
    main()
