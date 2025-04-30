import os
import sys
from github import Github
from github import Auth
import urllib.request
import zipfile
import io
import json


def get_report(artifact, filename="ctrf-report.json"):
    status, headers, response = artifact._requester.requestJson(
        "GET", artifact.archive_download_url
    )
    assert status == 302
    zipobj = urllib.request.urlopen(headers["location"])
    assert zipobj.status == 200
    data_zip = zipfile.ZipFile(io.BytesIO(zipobj.read()))
    data_b = data_zip.read("ctrf-report.json")
    data = json.loads(data_b.decode("utf-8"))
    return data
    

auth = Auth.Token(os.environ.get("GITHUB_TOKEN"))
g = Github(auth=auth)

repo = g.get_repo("mkerrinrapid/testgithub")

# One run per patchset
current_run = repo.get_workflow_run(int(os.environ["GITHUB_RUN_ID"]))

artifacts = current_run.get_artifacts()
print(list(artifacts))
reports = list(filter(lambda a: a.name == "ctrf-report", artifacts))
if not reports:
    print("No reports")
    sys.exit(0)

old_report_data = get_report(reports[0])
old_tests = {test["name"]: test for test in old_report_data["results"]["tests"]}

report_data = json.load(open("ctrf/report.json"))



for test in report_data["results"]["tests"]:
    old_test = old_tests[test["name"]]
    if old_test["status"] != test["status"]:
        test["flaky"] = True

print(json.dumps(report_data, indent=4))

with open("ctrf/report.json", "w") as fp:
    json.dump(report_data, fp, indent=4)
