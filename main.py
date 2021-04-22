import json
import os
from base64 import b64decode
from os.path import dirname, join

import github3
from dotenv import load_dotenv

load_dotenv()

ORG = os.getenv("organization")
GH_TOKEN = os.getenv("gh_token")
TOPIC = os.getenv("topic")
OUTPUTFILENAME = os.getenv("outputFileName") or "repositories.json"
ARCHIVED = os.getenv("archived") or "false"

gh = github3.login(token=GH_TOKEN)

query = "org:{} topic:{} archived:{}".format(ORG, TOPIC, ARCHIVED)
all_repos = gh.search_repositories(query)
repo_list = []

for repo in all_repos:
    if repo is not None:
        print("{0}".format(repo.repository))
        full_repository = repo.repository.refresh()

        innersource_repo = repo.as_dict()
        innersource_repo["_InnerSourceMetadata"] = {}

        # fetch repository participation
        participation = repo.repository.weekly_commit_count()
        innersource_repo["_InnerSourceMetadata"]["participation"] = participation["all"]

        # fetch contributing guidelines
        try:
            # if CONTRIBUTING.md exists in the repository, link to that instead of repo root
            content = repo.repository.file_contents("/CONTRIBUTING.md").content
            innersource_repo["_InnerSourceMetadata"]["guidelines"] = "CONTRIBUTING.md"
        except github3.exceptions.NotFoundError:
            # CONTRIBUTING.md not found in repository, but it's not required
            pass

        # fetch repository topics
        topics = repo.repository.topics()
        innersource_repo["_InnerSourceMetadata"]["topics"] = topics.names

        repo_list.append(innersource_repo)

# Write each repository to a repos.json file
with open(OUTPUTFILENAME, "w") as f:
    json.dump(repo_list, f, indent=4)
    print("::set-output name=repositories::" + OUTPUTFILENAME)
