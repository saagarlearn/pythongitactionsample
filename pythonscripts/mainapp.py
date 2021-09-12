import requests
from requests.auth import HTTPBasicAuth
import json

class CustomValidationError(Exception):
    pass
#print("Welcome to fun")
class SemarchyClient:
  def __init__(self, host, port, username,password):
    self.host = host
    self.port = port
    self.username = username
    self.password = password

#getbaseAPIUrl
  def getbaseAPIUrl(self):
       apibaseURL=""
       if len(str(self.port).strip())!=0:
           apibaseURL="http://" + self.host + ":" + str(self.port)
       else:
           apibaseURL="http://" + self.host
       return apibaseURL

#list all the model editions for and return the latest close model key
  def getLatestCloseModelKey(self, model_name):
      latestClosedModelKey=0.0
      isCloseModelFound = False
      print("get latest closed model version")
      apiUrl=self.getbaseAPIUrl() +"/semarchy/api/rest/app-builder/models/" + model_name + "/editions"
      print(apiUrl)
      response = requests.get(apiUrl, auth=HTTPBasicAuth(self.username, self.password))
      if response.status_code != 200:
           raise CustomValidationError("API call to get model editions failed")
      modelEditionListAll = json.loads(response.text)
      for modelEditionListEach in modelEditionListAll:
          if modelEditionListEach['status'] == 'CLOSED':
              if float(modelEditionListEach['key']) >= latestClosedModelKey:
                  latestClosedModelKey = float(modelEditionListEach['key'])
                  isCloseModelFound = True
      if isCloseModelFound == False:
           raise CustomValidationError("No close model found")
      return latestClosedModelKey

#Export the latest close model
  def exportModelEdition(self, model_name, model_version):
       print("export latest closed model version")
       apiUrl=self.getbaseAPIUrl() +"/semarchy/api/rest/app-builder/models/" + model_name + "/editions/" +model_version+ "/content"
       print(apiUrl)
       response = requests.get(apiUrl, auth=HTTPBasicAuth(self.username, self.password))
       return response

  def importModelEdition(self, xml):
      print("import latest closed model version to target")
      #http://prodsemarchy.eastus.cloudapp.azure.com/semarchy/api/rest/app-builder/model-imports
      apiUrl=self.getbaseAPIUrl() +"/semarchy/api/rest/app-builder/model-imports"
      print (apiUrl)
      response = requests.post(apiUrl, auth=HTTPBasicAuth(self.username, self.password), data=xml,headers={'Content-Type': 'application/octet-stream'})
     # print(response.text)
      return response
