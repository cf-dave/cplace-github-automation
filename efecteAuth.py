import requests
import json
import logging
import github
import os

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

    def get_datacards(self, template_code: str, selected_attributes, limit: int = 50):
        params = {
            "limit": limit,
            "filterId": 100000000,
            'dataCards': True
        }
        response = requests.get(self.BASE_API_URL + f'/dc/{template_code}/data', headers=self.headers, params=params)
        return response.json()

    def get_datacard(self, template_code: str, datacard_id: int, selected_attributes):
        params = {
            'selectedAttributes': ",".join(selected_attributes),
        }
        response = requests.get(self.BASE_API_URL + f'/dc/{template_code}/data/{datacard_id}', headers=self.headers, params=params)
        return response.json()


def main():
    # cplace_github = github.Github(os.environ["github_token"])
    # https://docs.github.com/en/rest/collaborators/collaborators#add-a-repository-collaborator
    # cplace_github.get_repo("cfactory").add_to_collaborators("Timon33", "push")

    # TODO move credentials to github secrets
    api = EfecteApi('restp-api-test', 'Cplace123!')
    r = api.get_datacards('ServiceRequest', ('subject, request_service, status, ServiceItem, direktLink, AdditionalInformation'))
    pass


if __name__ == "__main__":
    main()

"""
api = EfecteApi('restp-api-test', 'Cplace123!')

params = (
    # ('filter', '$Self-Service Item$ = \'IT Repository | New\''),
    ('selectedAttributes', 'subject, request_service, status, ServiceItem, direktLink, AdditionalInformation'),
    ('limit', '50'),
    ('filterId', '1000000000'),
)


notStarted = []
approved = []
for datacard in dataCards:  # Go through and filter the git hub ones out

    if len(datacard['data']['request_service']['values']) > 0:
        if datacard['data']['request_service']['values'][0]['name'] == 'GitHub Management':
            service = datacard['data']['ServiceItem']['values'][0]['name']
            status = datacard['data']['status']['values'][0]['value']
            id = datacard['dataCardId']
            if status == '01 - Not started':
                print(status)
                notStarted.append([id, service])
            elif status == '03 - Approved':
                print(status)
                approved.append([id, service])
            else:
                continue
ghRequests = [notStarted, approved]

print(len(notStarted))

for ticket in notStarted:
    response = requests.get(url + str(ticket[0]), headers=headers, params=params)
    text = json.loads(response.text)
    print(text)
    serviceOffering = text['data']['ServiceOffering']['values'][0]['value']
    serviceItem = text['data']['ServiceItem']['values'][0]['name']
    # link = text['data']['direktLink']['values'][0]['value']
    additionalInformation = (text['data']['AdditionalInformation']['values'][0]['value']).split(" ")
    # print(additionalInformation)
    user = "cf-dave"
    repo, level, justification = additionalInformation[1].split(':')[1], additionalInformation[3].split(':')[1], \
                                 additionalInformation[4].split(':')[1]  # ,additionalInformation[3].split(':')[1]
    if level == "Read":
        level = "pull"
    elif level == "Write":
        level = "push"
    link = dc_url + ticket[0]

    service = -1  ## Entscheidung welche Aktion ausgeführt wird

    if serviceItem == "IT Repository | New":
        service = 1
    elif serviceItem == "IT Repository | Access Request":
        service = 2
    else:
        service = 0

    if service == 1:
        with open("todo.txt", 'w') as fd:
            print(repo)
            if (repo.startswith('cplace')):
                fd.write("repoName:" + repo)
                p = check_output(['node', 'createRepo.js'])
                if p == "Script ran through":
                    print("Script ran through")
            else:
                # reject for naming scheme
                print("Illegal name")
    elif service == 2:
        with open("todo.txt", 'w') as fd:
            # print(repo)
            fd.write("user:" + user + "\n")
            # if(repo.startswith('cplace')):
            fd.write("repoName:" + repo + "\n")
            fd.write("level:" + level + "\n")
            fd.write("justification:" + justification + "\n")
    sendEmail(link)

if (status == "03 - Approved"):
    # add user to repo
else:
    ("Illegal status")
"""
