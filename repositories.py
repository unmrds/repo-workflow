import config
import requests
import dateutil.parser
from datetime import datetime
import repositories
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import json
from base64 import b64encode


# DataCite  object
class DataCite:
    """
    Based on V2 API documentation from DataCite
    https://support.datacite.org/reference/introduction

    process = "preflight" or "production" depending on if a test run or a final production run
    """
    def __init__(self, process = "preflight"):
        if process == "production":
            self.endpoint_base= config.datacite_production_host
            self.username = config.datacite_production_user
            self.password = config.datacite_production_pw
            self.prefix = config.datacite_production_prefix
        else:
            self.endpoint_base= config.datacite_test_host
            self.username = config.datacite_test_user
            self.password = config.datacite_test_pw
            self.prefix = config.datacite_test_prefix
        self.publisher = config.publisher
        self.headers = {
            "Content-Type": "application/vnd.api+json"
        }
        self.result = {
            "request":"",
            "results":"",
        }

    def get_metadata(self):
        return self.metadata

    def get_request(self):
        return self.result["request"]

    def get_result(self):
        return self.result["results"]

    def test(self):
        print(self.headers)
        print("endpoint base: " + self.endpoint_base)

    def register_doi(
            self,
            doi_metadata
        ):
        r_url = self.endpoint_base + "/dois"
        #print("Submitting DOI registration metadata to: " + r_url)
        #print("Request headers:")
        #print(self.headers)
        r = requests.post(r_url, data=json.dumps(doi_metadata), headers=self.headers, auth=(self.username,self.password))
        #print(r.headers)
        #response = r.json()
        return r

    def get_dois(
            self,
            query = "",
            page_size = "25",
            page_number = "1",
        ):
        endpoint = self.endpoint_base + "/dois?"
        parameters = ""
        if query != "":
            if parameters == "":
                parameters = parameters + "query=" + query
            else:
                parameters = parameters + "&query=" + query
        if page_size != "":
            if parameters == "":
                parameters = parameters + "page[size]=" + page_size
            else:
                parameters = parameters + "&page[size]=" + page_size
        if page_number != "":
            if parameters == "":
                parameters = parameters + "page[number]=" + page_number
            else:
                parameters = parameters + "&page[number]=" + page_number
        print("request: " + endpoint + parameters)
        r = requests.get(endpoint + parameters, headers=self.headers, auth=self.auth_info)
        print(r.headers)
        response = r.json()
        self.result["request"] = endpoint + parameters
        self.result["results"] = response
        #self.result["query_meta"] = response["query_meta"]
        #print(result_data)


###############################################################################
# Digital Commons respository object
class DigitalCommons:
    """
    Based on V2 API documentation from Digital Commons/BePress
    """
    def __init__(self, publication, process = "preflight"):
        self.publication = publication
        self.process = process
        self.endpoint_base = config.dc_endpoint
        self.host = config.dc_host
        self.token = config.dc_api_token
        self.headers = {
            "Authorization": self.token,
        }
        self.result = {
            "request":"",
            "query_meta":"",
            "results":"",
        }


    def get_request(self):
        return self.result["request"]

    def get_query_meta(self):
        return self.result["query_meta"]

    def get_result(self):
        return self.result["results"]

    def test(self):
        print(self.headers)
        print("endpoint base: " + self.endpoint_base)
        print("repository hostname: " + self.host)

    def query(
            self,
            query = "",
            metadata_field = ("",""),
            fields = "",
            select_fields = "all",
            limit = 100,
            start = 1,
        ):
        endpoint = self.endpoint_base + "/" + self.host + "/query?"
        parameters = ""
        if query != "":
            if parameters == "":
                parameters = parameters + "q=" + query
            else:
                parameters = parameters + "&q=" + query
        if metadata_field[0] != "":
            if parameters == "":
                parameters = parameters + metadata_field[0] + "=" + metadata_field[1]
            else:
                parameters = parameters + "&" + metadata_field[0] + "=" + metadata_field[1]
        if fields != "":
            if parameters == "":
                parameters = parameters + "fields=" + fields
            else:
                parameters = parameters + "&fields=" + fields
        if select_fields != "":
            if parameters == "":
                parameters = parameters + "select_fields=" + select_fields
            else:
                parameters = parameters + "&select_fields=" + select_fields
        if parameters == "":
            parameters = parameters + "limit=" + str(limit) + "&start=" + str(start)
        else:
            parameters = parameters + "&limit=" + str(limit) + "&start=" + str(start)
        print("request: " + endpoint + parameters)
        r = requests.get(endpoint + parameters, headers=self.headers)
        print(r.headers)
        print()
        response = r.json()
        self.result["request"] = endpoint + parameters
        self.result["results"] = response["results"]
        self.result["query_meta"] = response["query_meta"]
        #print(result_data)

    def create_dois(
            self,
            resource_type = "Text"
        ):
        if self.process == "production":
            prefix = config.datacite_production_prefix
        else:
            prefix = config.datacite_test_prefix
        publisher = config.publisher
        # map digital commons metadata fields to corresponding datacite fields
        # for each digital commons metadata entry in the current result set
        start_time = datetime.now().isoformat()
        print()
        print("===============================================================")
        print(start_time)
        registration_result = []
        for result in self.result["results"]:
            # process name list into DataCite creators block
            datacite_creators = []
            i = 0
            for author in result["author"]:
                try:
                    author_name = result["author_display_lname"][i] + ", " + author.replace(result["author_display_lname"][i], "")
                except:
                    author_name = ""

                author_affiliation = []
                try:
                    author_affiliation = author_affiliation.append(result["institution"][i])
                except:
                    author_affiliation = author_affiliation.append("")

                try:
                    author_givenName = author.replace(result["author_display_lname"][i], "")
                except:
                    author_givenName = ""

                try:
                    author_familyName = result["author_display_lname"][i]
                except:
                    author_familyName = ""

                author_object = {
                    "name": author_name,
                    "nameType": "Personal",
                    #"affiliation": author_affiliation,
                    "givenName": author_givenName,
                    "familyName": author_familyName
                }
                datacite_creators.append(author_object)
                i += 1
            try:
                abstract = result["abstract"]
            except:
                abstract = "missing"
            try:
                title = result["title"]
            except:
                title = "missing"
            try:
                pubYear = dateutil.parser.isoparse(result["publication_date"]).year
            except:
                pubYear = 9999
            try:
                url = result["url"]
            except:
                url = "missing"
            draft_doi_object = {
                "data":{
                    "type":"dois",
                    "attributes": {
                        "prefix": prefix,   # this triggers the automatic generation of a DOI
                        "event": "register", # create the generated DOI in a registered state
                        "creators": datacite_creators,
                        "titles": [{
                            "title": title
                        }],
                        "descriptions": [{
                            "description": abstract,
                            "descriptionType": "Abstract"
                        }],
                        "publisher": publisher,
                        # todo: update publication year to reflect embargo date if after publication date
                        "publicationYear": pubYear,
                        "types": {
                            "resourceTypeGeneral": resource_type
                        },
                        "url": url,
                        "schemaVersion": "http://datacite.org/schema/kernel-4"
                    }
                }
            }
            print("Article: " + url)
            #print(result)
            #print(draft_doi_object)

            # register the documented resource in DataCite and get back the DOI
            print("Now starting DOI generation for: " + result["url"])
            doi_endpoint = repositories.DataCite(process = self.process)
            registration_return = doi_endpoint.register_doi(draft_doi_object)
            print("Registration Return: " + registration_return.headers["Status"])
            #print(registration_return.text)
            registration_result.append({
                "headers":dict(registration_return.headers),
                "metadata":registration_return.text
            })
            print()
        #print("Registration results:")
        #print(registration_result)
        registration_result_dict = {
            "start_time": start_time,
            "query_info": self.result,
            "results": registration_result,
        }
        filename = "run_output/" + "doiregistration_" + start_time + "_" + self.process + "_" + self.publication + ".json"

        print("Writing " + str(len(registration_result_dict["results"])) + " items into: " + filename)
        print()
        with open(filename, "w") as outfile:
            json.dump(registration_result_dict, outfile)


    def update_dois(
            self,
            endpoint_base,
            username,
            password,
            prefix,
            publisher
        ):
        """Update existing DOI metadata based on submitted metadata info"""










    # based on V1 of the API
    # def get_filelink(self, endpoint):
    #     r = requests.get(endpoint, headers=self.headers)
    #     result_data = r.json()
    #     file_url = result_data["results"][0]
    #     return file_url
    #
    # def get_snapshot(self):
    #     endpoint = self.endpoint_base + "/results/latest/" + self.host
    #     return self.get_filelink(endpoint)
    #
    # def get_monthly(self, yyyy_mm):
    #     endpoint = self.endpoint_base + "/results/monthly/" + self.host + "/" + yyyy_mm
    #     return self.get_filelink(endpoint)


