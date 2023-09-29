import json, urllib, time

class YandexWordstatAPI:
  def __init__(self, login, token, url='https://api-sandbox.direct.yandex.ru/v4/json/'):
    self.login = login
    self.token = token
    self.url = url

  # General methods

  def __GenerateJSONRequestBody(self, method, param):
    request_body = {
      'method': method,
      'token': self.token,
      'locale': 'ru',
      'param': param,
    }

    json_request_body = json.dumps(request_body, ensure_ascii=False)
    return json_request_body.encode('utf8')

  def __DoRequest(self, method, param):
    request_body = self.__GenerateJSONRequestBody(method, param)
    response = urllib.request.urlopen(self.url, request_body)
    return json.loads(response.read().decode('utf8'))

  # Request-specific methods

  def CreateNewWordstatReport(self, phrases, geoid):
    method = "CreateNewWordstatReport"
    param = {
          "Phrases": phrases,
          "GeoID": geoid,
      }
    return self.__DoRequest(method, param)

  def DeleteWordstatReport(self, report_id):
    method = "DeleteWordstatReport"
    return self.__DoRequest(method, report_id)

  def GetWordstatReport(self, report_id):
    method = "GetWordstatReport"
    return self.__DoRequest(method, report_id)

  def GetWordstatReportList(self):
    method = "GetWordstatReportList"
    return self.__DoRequest(method, [])

  def GetKeywordsSuggestion(self, keywords):
    method = "GetKeywordsSuggestion"
    param = {
        "Keywords": keywords,
    }
    return self.__DoRequest(method, param)

class YandexWordstatFetcher:
  report = {}
  yandex_wordstat_api: YandexWordstatAPI

  def __init__(self, login, token):
    self.yandex_wordstat_api = YandexWordstatAPI(login, token)

  def __TryCreateReport(self, phrases, geoid):
    create_report_response = self.yandex_wordstat_api.CreateNewWordstatReport(phrases, geoid)

    if "data" not in create_report_response:
      raise Exception("Failed to create report")

    report_id = create_report_response["data"]
    return report_id

  def __TryGetReportStatus(self, report_id):
    get_report_list_response = self.yandex_wordstat_api.GetWordstatReportList()

    if "data" not in get_report_list_response:
      raise Exception("Failed to get report list")

    for report in get_report_list_response["data"]:
      if report["ReportID"] == report_id:
        return report["StatusReport"]

    return "NoReport"

  def __TryFetchReport(self, report_id):
    return self.yandex_wordstat_api.GetWordstatReport(report_id)

  def __TryDeleteReport(self, report_id):
    delete_report_response = self.yandex_wordstat_api.DeleteWordstatReport(report_id)

    if "data" not in delete_report_response:
      raise Exception("Failed to get delete report")

  def BuildPayload(self, phrases, geoid):
    report_id = self.__TryCreateReport(phrases, geoid)

    while True:
        report_status = self.__TryGetReportStatus(report_id)

        if report_status == "Done":
          break
        elif report_status == "Failed":
          raise Exception("Failed to form report")
        elif report_status == "NoReport":
          raise Exception("No report in report list")
        time.sleep(1)

    self.report = self.__TryFetchReport(report_id)

    self.__TryDeleteReport(report_id)

  def FetchInterest(self):
    assert self.report
    assert self.report['data']

    interest = []
    for keyword_response in self.report['data']:
      interest.append(keyword_response['SearchedWith'][0])

    return interest

  def FetchSearchedWith(self):
    assert self.report
    assert self.report['data']

    searched_with = []
    for keyword_response in self.report['data']:
      searched_with.append(keyword_response['SearchedWith'])

    return searched_with

  def FetchSearchedAlso(self):
    assert self.report
    assert self.report['data']

    searched_also = []
    for keyword_response in self.report['data']:
      searched_also.append(keyword_response['SearchedAlso'])

    return searched_also
