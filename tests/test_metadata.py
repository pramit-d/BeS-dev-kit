from typer.testing import CliRunner
import os, json

from besecure_developer_toolkit.cli import app

runner = CliRunner()

def test_metadata():
    id = "136"
    name = "fastjson"
    version = "version"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=id+"\n"+name+"\n")
    assert result.exit_code == 0
    version_file = os.path.exists(f'{osspoi}/version_details/{id}-{name}-Versiondetails.json')
    ossp_master_file = os.path.exists(f'{osspoi}/OSSP-Master.json')
    print(ossp_master_file)
    f = open(f'{osspoi}/OSSP-Master.json')
    ossp_master_data = json.load(f)
    for i in range(len(ossp_master_data["items"])):
        if ossp_master_data["items"][i]["id"] == int(id) and ossp_master_data["items"][i]["name"] == name:
            found = True
            break
        else:
            found = False
    assert ossp_master_file == True
    assert version_file == True
    assert found == True

def test_version_file_not_empty():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=id+"\n"+name+"\n")
    assert result.exit_code == 0
    size = os.path.getsize(f'{osspoi}/version_details/{id}-{name}-Versiondetails.json')
    assert size > 0

def test_overwrite():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    test_version_file = [{
        "version": "1.2.24",
        "release_date": "19-Jan-2017",
        "criticality_score": "Not Available",
        "scorecard": "Not Available",
        "cve_details": "Not Available"
    }]
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata", "--overwrite"], input=id+"\n"+name+"\n")
    assert result.exit_code == 0
    f = open(f'{osspoi}/version_details/{id}-{name}-Versiondetails.json')
    fastjson_version_file = json.load(f)
    assert sorted(test_version_file[0]) == sorted(fastjson_version_file[0])

def test_without_overwrite():
    id = "136"
    name = "fastjson"
    version = "1.2.24"
    osspoi = os.environ['OSSPOI_DIR']
    f = open(f"{osspoi}/version_details/{id}-{name}-Versiondetails.json")
    original_version_data = json.load(f)
    for i in range(len(original_version_data)):
        if original_version_data[i]["version"] == version:
            test_data_original = original_version_data[i]
            break
    f.close()
    result = runner.invoke(app, ["generate", "metadata"], input=id+"\n"+name+"\n")
    f = open(f"{osspoi}/version_details/{id}-{name}-Versiondetails.json")
    original_version_data = json.load(f)
    for i in range(len(original_version_data)):
        if original_version_data[i]["version"] == version:
            test_data_new = original_version_data[i]
            break
    f.close()
    assert result.exit_code == 0
    assert sorted(test_data_original) == sorted(test_data_new)
    assert f'Alert! Entry for {id}-{name} already present' in result.stdout
    assert f'Alert! Version {version} exists' in result.stdout

def test_issue_project_mismatch():
    id = 137
    name = "fastjson"
    osspoi = os.environ['OSSPOI_DIR']
    result = runner.invoke(app, ["generate", "metadata"], input=str(id)+"\n"+name+"\n")
    assert result.exit_code == 0
    f = open(f'{osspoi}/OSSP-Master.json')
    ossp_master_json = json.load(f)
    for i in range(len(ossp_master_json["items"])): 
        if ossp_master_json["items"][i]["id"] == id and ossp_master_json["items"][i]["name"] == name:
            new_id = ossp_master_json["items"][i]["id"]
            new_name = ossp_master_json["items"][i]["name"]
            print(new_id, new_name)
            raise AssertionError
        else:
            pass