import csv
import requests
import requests.auth

#Custom libraries
import json

#API_Endpoint = "https://bsdd-prototype.azure-api.net/api/" 
API_EndPoint = 'https://test.bsdd.buildingsmart.org/api/';

# API ressources
Resource_Domains = "Domain/v2"
Resource_Classification = "Classification/v3"
Resource_Country = "Country/v1"
Resource_Search_Open = 'SearchListOpen/v2' #Unsecured
Resource_Search_Secured = 'SearchList/v2' #secured

# Custom made Resources
Resource_ExportFile = "RequestExportFile/preview"
Resource_Languages = "Language/v1"
Resource_ReferenceDocument =  "ReferenceDocument/v1"
Resource_Unit = "Unit/v1"
Resource_DomainClassificationTree = "Domain/v2/Classifications"
Resource_TextSearch_Open = 'TextSearchListOpen/v5'
Resource_Material_Details = 'Material/v1'
Resource_List_Material_Domain = 'Material/SearchOpen/preview'
Resource_Property_Details = 'Property/v2'
Resource_PropertyValue_Details = 'PropertyValue/v1'

class TObject():
    name = ''
    namespaceUri = ''

    #----------------------------------------------------------------------------------------------------
    # Read a JSON value 
    def ReadVal(self, _JObj, _key):
        
        res = ''
        
        if _key in _JObj:
          try :
            res = _JObj[_key]
          except: 
            res ='error'
        
        return res
    #----------------------------------------------------------------------------------------------------
        
#----------------------#        
#  Country             #   
#----------------------#        
class TCountry(TObject):
    code = ''
    
    def FillValuesFromJSON(self, _content):
        self.name = self.ReadVal(_content, 'name')
        self.code = self.ReadVal(_content, 'code')

#----------------------#        
#  Classification      #   
#----------------------#        
class TClassification(TObject):    
    def __init__(self): #Added constructor to expand available properties for this object
      self.definition = ''
      self.IFCLinks = []
      self.Properties = []
      self.namespaceUri = []
      self.uid = []

    # Read the values from the JSON response    
    def FillValuesFromJSON(self, _content):
        self.name = self.ReadVal(_content, 'name')
        self.namespaceUri = self.ReadVal(_content, 'namespaceUri') 
        self.definition = self.ReadVal(_content, 'definition') 

    # Ask the API for the classification details
    def Load_Details(self, _content):
          if "relatedIfcEntityNames" in _content:
                for item in _content["relatedIfcEntityNames"]:
                      self.IFCLinks.append(item)
                      
          # Properties attached to the classification
          if "classificationProperties" in _content:
                    for item in _content["classificationProperties"]:                                  
                      NewProperty = TProperty()
                      NewProperty.FillValuesFromJSON(item)                      
                      self.Properties.append(NewProperty)

          # Properties attached to the classification
          if "namespaceUri" in _content:
            for item in _content["namespaceUri"]:                                  
              NewProperty = TProperty()
              NewProperty.FillValuesFromJSON(item)                      
              self.Properties.append(NewProperty)

    # Save properties list  values  of the class into a csv file
    def SaveToCSV(self, _Name):
        with open(_Name + '_Properties.csv' , 'w+') as csvfile:
            MyFields = ['Name' , 'Domain', 'URI', 'Definition', 'dataType']
            writer = csv.DictWriter(csvfile, delimiter=';' , fieldnames=MyFields)
            writer.writeheader()
            for item in self.Properties:
                writer.writerow({'Name' : item.name, 'Domain': item.domain , 'URI' : item.namespaceUri, 'Definition' : item.definition, 'dataType' : item.dataType})

#----------------------#        
#  Property            #   
#----------------------#        
class TProperty(TObject):    
    def __init__(self):  #Added constructor for future expansion of available properties for this object
      self.definition = ""
      self.domain = ""
      self.dataType = ""

    # Read the values from the JSON response    
    def FillValuesFromJSON(self, _content):
        self.name = self.ReadVal(_content, 'name')
        self.domain = self.ReadVal(_content, 'propertyDomainName') 
        self.namespaceUri = self.ReadVal(_content, 'propertyNamespaceUri') 
        self.definition = self.ReadVal(_content, 'description') 
        self.dataType = self.ReadVal(_content, "dataType")
     
#----------------------#        
#  Domain              #   
#----------------------#        
class TDomain(TObject):
    def __init__(self): #Added constructor for future expansion of available properties for this object
      self.version = ''
      self.organizationNameOwner = ''
      self.defaultLanguageCode = ''
      self.license = ''
      self.licenseUrl = ''
      self.qualityAssuranceProcedure = ''
      self.qualityAssuranceProcedureUrl = ''
      self.Classes = []

    # Read the values from the JSON response
    def FillValuesFromJSON(self, _content):
      self.namespaceUri = self.ReadVal(_content, 'namespaceUri')
      self.name = self.ReadVal(_content, 'name')
      self.version = self.ReadVal(_content, 'version')
      self.organizationNameOwner = self.ReadVal(_content, 'organizationNameOwner')
      self.defaultLanguageCode = self.ReadVal(_content, 'defaultLanguageCode')
      self.license = self.ReadVal(_content, 'license')
      self.licenseUrl = self.ReadVal(_content, 'licenseUrl')
      self.qualityAssuranceProcedure = self.ReadVal(_content, 'qualityAssuranceProcedure')
      self.qualityAssuranceProcedureUrl = self.ReadVal(_content, 'qualityAssuranceProcedureUrl')

    # Save classifications list  values  of the domain into a csv file
    def SaveToCSV(self):
        with open(self.name + '_Classes.csv' , 'w+') as csvfile:
            MyFields = ['Name' , 'URI', 'Definition']
            writer = csv.DictWriter(csvfile, delimiter=';' , fieldnames=MyFields)
            writer.writeheader()
            for item in self.Classes:
                writer.writerow({'Name' : item.name, 'URI' : item.namespaceUri, 'Definition' : item.definition})
    
    # Dump data into json format, for visualization and saving in a GUI or file
    def toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=1)

#CUSTOM MADE CLASSES: These classes were created to accomodate all the available requests from the RESTful API
#----------------------#        
#  Language            #   
#----------------------#        
class TLanguage(TObject):
  def __init__(self):   
    self.isoCode = ''
    
  def FillValuesFromJSON(self, _content):
      self.name = self.ReadVal(_content, 'name')
      self.namespaceUri = self.ReadVal(_content, 'namespaceUri')
      self.isoCode = self.ReadVal(_content, 'isoCode')

#----------------------#        
#  ReferenceDocuments  #   
#----------------------#        
class TReferenceDocument(TObject):
  def __init__(self):   
    self.title = ''
    self.date = ''

  def FillValuesFromJSON(self, _content):
    self.name = self.ReadVal(_content, 'name')
    self.namespaceUri = self.ReadVal(_content, 'namespaceUri')
    self.title = self.ReadVal(_content, 'title')
    self.date = self.ReadVal(_content, 'date')        

#----------------------#        
#  Unit                #   
#----------------------#        
class TUnit(TObject):
  def __init__(self):   
    self.code = ''
    self.symbol = ''

  def FillValuesFromJSON(self, _content):
    self.name = self.ReadVal(_content, 'name')
    self.namespaceUri = self.ReadVal(_content, 'namespaceUri')
    self.code = self.ReadVal(_content, 'code')
    self.symbol = self.ReadVal(_content, 'symbol') 


#------------------------------------------------------------------------#
#        This class contains                                             # 
#           - authorization                                              #
#           - Header formatting of a request (with & without token)      #
#           - Send of a Get request for a specific ressource             #
#           - Calls to the API Ressources                                #
#------------------------------------------------------------------------#

class TPostman():
    def __init__(self): #Added constructor for future expansion of available properties for this object
      self.Domains = [] # Used to store domains received from an API call
      self.Countries = [] # used to store the list of countries received from an API call
      self.Token = None # used to store the token received from an authorization call

      #CUSTOM MADE HOLDERS
      self.Languages = [] # Used to store list of languages available in bSDD received from an API call
      self.ReferenceDocuments = [] # Used to store list of reference documents available in bSDD received from an API call
      self.Units = [] # Used to store list of units available in bSDD received from an API call
      #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    # get an authorization token - will open a web browser for the credentials
    #----------------------------------------------------------------------------------------------------

    def Authorize(self):

      bSDD_ClientID = '4aba821f-d4ff-498b-a462-c2837dbbba70'                             
      bSDD_Scope = "https://buildingsmartservices.onmicrosoft.com/api/read"
      
      from msal import PublicClientApplication

      bSDD_authority = 'https://buildingsmartservices.b2clogin.com/tfp/buildingsmartservices.onmicrosoft.com/b2c_1_signupsignin'
      
      app = PublicClientApplication( bSDD_ClientID, authority = bSDD_authority) #need localhost redirection on azure portal for the client ID
      flow = app.initiate_auth_code_flow(scopes=[bSDD_Scope])
      
      #First try to see if there are accounts in cache. If not or an error is received, get token interactively through browser
      #By standard, cache is only maintaned during a given Python session (runtime session of the code), since it is store in-memory (not persistent). In order to build a persistent version, the app instance constructor PublicClientApplication must receive a cache, that may be created manually with the SerializableTokenCache() class. See https://msal-python.readthedocs.io/en/latest/#msal.SerializableTokenCache and https://msal-python.readthedocs.io/en/latest/ for more information on that.
      result = None
      accounts = app.get_accounts()
      if accounts:
        result = app.acquire_token_silent(scopes=[bSDD_Scope], account=accounts[0])
      if not result:
        self.Token = app.acquire_token_interactive(scopes=[bSDD_Scope])

        print('logged in')
     
    #----------------------------------------------------------------------------------------------------
    # Format the header of a query 
    #----------------------------------------------------------------------------------------------------

    def setHeader(self):                 

        if self.Token:
         myheader = {
          'content-type': 'application/json',
          'Accept' :'application/json', # We want JSON
          'Authorization' : 'Bearer ' + (self.Token['access_token']) #if logged in, here is the received token to send for secured API call
         }
        else : 
         myheader = {
          'content-type': 'application/json',
          'Accept' :'application/json', 
         }

        return myheader    

    #----------------------------------------------------------------------------------------------------
    # Send a GET API Call
    #----------------------------------------------------------------------------------------------------

    def get(self, _resource, _params):
      
      #print (_params)#Uncomment to check the parameters sent  
      mResponse = requests.get(API_EndPoint + _resource, headers=self.setHeader(), params=_params)
      #print (mResponse.url) #uncomment to see the URL sent
      #print(mResponse.text) #uncomment to see the result of the call in the console
      #sometimes it is needed to be able to access the header of the response
      self.header = mResponse.headers
      
      #Status code is also passed secondarily for optional error handling or visualization on the GUI
      return mResponse.json(), mResponse.status_code

    #----------------------------------------------------------------------------------------------------
    # Get available countries - /api/Country/v1: 
    #----------------------------------------------------------------------------------------------------

    def get_Countries(self, _SaveResult):

      Response, request_status = self.get(Resource_Country, "")
      #Browse the results
      NbRes = 0

      for item in Response:
        Country = TCountry()
        Country.FillValuesFromJSON(item)
        self.Countries.append(Country)

      if _SaveResult:
        True
        #TODO: Implement and test saving this information in a CSV file
        #Save domain list to a csv file
        #self.Save_Domains_To_CSV()

    #----------------------------------------------------------------------------------------------------
    # Get available domains - /api/Domain/v2: 
    #----------------------------------------------------------------------------------------------------
    
    def get_Domains(self, _SaveResult):
      
      Response, request_status = self.get(Resource_Domains, "")
      #Browse the results
      NbRes = 0
      
      for item in Response:
        Domain = TDomain()
        Domain.FillValuesFromJSON(item)
        self.Domains.append(Domain)
        NbRes = NbRes + 1
      
      if _SaveResult:
        #Save domain list to a csv file
        self.Save_Domains_To_CSV()

      return NbRes

    #----------------------------------------------------------------------------------------------------
    # Get Classes of domains - /api/SearchList/v2
    #----------------------------------------------------------------------------------------------------

    def get_Domain_Classes(self, _DomainURI, _LanguageCode, _SaveResult, _Get_Details):
      
      # params of the request
      payload = dict()
      payload["DomainNamespaceUri"] = _DomainURI
      #Language code for the request ; EN for Internation English
      payload["LanguageCode"] = _LanguageCode
      
      Response, request_status = self.get(Resource_Search_Secured, payload)

      NbRes = Response["numberOfClassificationsFound"]
      
      for item in Response['domains']: #in this case we should have just 1 ! (Since we informed a URI from a specific domain)
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)

          #If details are required, a request is launched for each class
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)

        if _SaveResult:
          #Save the classes informations to a csv    
          ReadDomain.SaveToCSV();

      return NbRes

    #----------------------------------------------------------------------------------------------------
    # Retrieve the properties of a classification (i.e. retrieve all properties of a given definition) - /api/Classification/v3
    #----------------------------------------------------------------------------------------------------

    def Get_Classification_Properties(self, _ClassificationURI, _LanguageCode, _SaveResult, _ClassificationName = None): #Classification name, optional, just to nicely name the excel export
       payloadClass = dict()
       payloadClass["namespaceUri"] = _ClassificationURI
       payloadClass["languageCode"] = _LanguageCode
       payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
       mResponse, request_status = self.get(Resource_Classification, payloadClass)

       mClassification = TClassification()

       NbRes = 0

       if "relatedIfcEntityNames" in mResponse:
              for item in mResponse["relatedIfcEntityNames"]:
                  mClassification.IFCLinks.append(item)
                      
        # Get the properties attached to the classification
       if "classificationProperties" in mResponse:
            for item in mResponse["classificationProperties"]:                                  
              mProperty = TProperty()
              mProperty.FillValuesFromJSON(item)                      
              mClassification.Properties.append(mProperty)
              NbRes += 1

       #Save the properties informations to a csv    
       if _SaveResult:          
          mClassification.SaveToCSV(_ClassificationName)       

       return NbRes, mResponse, request_status #Expanded to return more inputs than originally returned
          
    #----------------------------------------------------------------------------------------------------
    # Retrieve a the classes of a domain linked to an IFC Entity - /api/SearchListOpen/v2
    #----------------------------------------------------------------------------------------------------

    def get_Linked_Classes(self, _DomainURI, _LanguageCode, _IFCEntity, _SaveResult, _Get_Details):
      # params of the request
      payload = dict()
      payload["DomainNamespaceUri"] = _DomainURI
      #Language code for the request ; EN for Internation English
      payload["LanguageCode"] = _LanguageCode
      payload["RelatedIfcEntity"] = _IFCEntity
      
      Response, request_status = self.get(Resource_Search_Open, payload)
      
      NbRes = Response["numberOfClassificationsFound"]

      for item in Response['domains']: #in this case we should have just 1 !
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)

          #If details are required, a request is launched for each one
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)

        if _SaveResult:
          #Save the classes informations to a csv    
          ReadDomain.SaveToCSV();

      return NbRes

    #----------------------------------------------------------------------------------------------------
    # Retrieve a domain from its URI, in the list of domains got from the API ressource "Domain"
    #----------------------------------------------------------------------------------------------------

    def GetDomainFromURI(self, _URI):

      i = 0;

      for item in self.Domains:
            if item.namespaceUri == _URI:
                  return item
                  break

    #----------------------------------------------------------------------------------------------------
    # Save domains list into a csv file
    #----------------------------------------------------------------------------------------------------

    def Save_Domains_To_CSV(self):

      with  open('bSDD_Domains.csv' , 'w+') as csvfile:

        MyFields = ['Name' , 'URI']
        writer = csv.DictWriter(csvfile, delimiter=';' , fieldnames=MyFields)
        writer.writeheader()
        for item in self.Domains:
          writer.writerow({'Name' : item.name, 'URI' : item.namespaceUri})

    #----------------------------------------------------------------------------------------------------
    # Get available Languages (CUSTOM MADE) - /api/Language/v1: 
    #----------------------------------------------------------------------------------------------------
    
    def get_Languages(self, _SaveResult):
      
      Response, request_status = self.get(Resource_Languages, "")
      #Browse the results
      NbRes = 0
      
      for item in Response:
        Language = TLanguage()
        Language.FillValuesFromJSON(item)
        self.Languages.append(Language)
        NbRes = NbRes + 1
      
      if _SaveResult:
        True
        #TODO: Implement a way to save this information in a CSV file
        #Save domain list to a csv file
        #self.Save_Domains_To_CSV()

      return NbRes  

    #----------------------------------------------------------------------------------------------------
    # Get available Reference Documents (CUSTOM MADE) - /api/ReferenceDocument/v1: 
    #----------------------------------------------------------------------------------------------------
    
    def get_ReferenceDocuments(self, _SaveResult):
      
      Response, request_status = self.get(Resource_ReferenceDocument, "")
      #Browse the results
      NbRes = 0
      
      for item in Response:
        ReferenceDocument = TReferenceDocument()
        ReferenceDocument.FillValuesFromJSON(item)
        self.ReferenceDocuments.append(ReferenceDocument)
        NbRes = NbRes + 1
      
      if _SaveResult:
        True
        #TODO: Implement a way to save this information in a CSV file
        #Save domain list to a csv file
        #self.Save_Domains_To_CSV()

      #Return number of results, i.e., number of Reference Documents available in bSDD
      return NbRes  

    #----------------------------------------------------------------------------------------------------
    # Get available Units (CUSTOM MADE) - /api/Unit/v1
    #----------------------------------------------------------------------------------------------------
    
    def get_Units(self, _SaveResult):
      
      Response, request_status = self.get(Resource_Unit, "")
      #Browse the results
      NbRes = 0
      
      for item in Response:
        Unit = TUnit()
        Unit.FillValuesFromJSON(item)
        self.Units.append(Unit)
        NbRes = NbRes + 1
      
      if _SaveResult:
        True
        #TODO: Implement a way to save this information in a CSV file
        #Save domain list to a csv file
        #self.Save_Domains_To_CSV()

      #Return number of results, i.e., number of Units available in bSDD
      return NbRes  

    #----------------------------------------------------------------------------------------------------
    # Get Domain with a classification tree (CUSTOM MADE) - /api/Domain/v2/Classifications: 
    #----------------------------------------------------------------------------------------------------

    def get_Domain_Classes_Tree(self, _DomainURI, _useNestedClassifications, _SaveResult):
      #This is the GET "/api/Domain/v2/Classifications - Get Domain with the classification tree"
      #TODO: Implement verification of response status

      #params of the request
      payload = dict()
      payload["namespaceUri"] = _DomainURI
      payload["useNestedClassifications"] = _useNestedClassifications
      
      # Response = self.get(Resource_Search_Secured, payload)
      Response, request_status = self.get(Resource_DomainClassificationTree, payload)

      #TODO: find a way to compute classification number from the JSON file received
      #NbRes stores the amount of classifications retrieved in the response
      #NbRes = len(Response['classifications'])
      NbRes=1

      #Unwrapping the Response and saving to the global bsdd variable of the script
      #This is useful if we are going to cache information to avoid lots of retrievals
      #TODO: check the method contract and make sure everything in Response is properly unwrapped. As of now, we are just passing Response to the GUI, to show, and will not update bsdd variable.

      #From the list of domains already retrieved when initializing the API with the method "self.get_Domains()", retrieve the general structure of the domain, so we can populate it with data from the classifications retrieved, by having access to the field ".Classes" that is part of the "Domain" data structure.
      ReadDomain = self.GetDomainFromURI(_DomainURI)
      '''
      for item in Response['classifications']: #iterate through each classification found in the domain:
        NewClass = TClassification()
        NewClass.FillValuesFromJSON(item)
        #If details are required, a request is launched for each class
        if  _useNestedClassifications:
          payloadClass = dict()
          payloadClass["namespaceUri"] = NewClass.namespaceUri
          payloadClass["includeChildClassificationReferences"] = True #we don't ask for the hierarchy we just want properties
          mResponse = self.get(Resource_Classification, payloadClass)
          NewClass.Load_Details(mResponse)
        ReadDomain.Classes.append(NewClass)
      '''
      if _SaveResult:
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        #TODO: implement a way to save results here
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    # Make an Open Search on bSDD  (CUSTOM MADE) - /api/TextSearchListOpen/v5: 
    #----------------------------------------------------------------------------------------------------

    def get_TextOpen_Search(self, _SearchText, _TypeFilter, _FilteringDomainUris, _SaveResult):
      # params of the request
      payload = dict()
      payload["SearchText"] = _SearchText #A list of strings
      payload["TypeFilter"] = _TypeFilter #It is a string
      payload["DomainNamespaceUris"] = _FilteringDomainUris #A list of strings
      
      Response, request_status = self.get(Resource_TextSearch_Open, payload)
      
      #TODO: Implement NbRes for this method
      #NbRes = Response["numberOfClassificationsFound"]
      NbRes=1
      '''
      for item in Response['domains']: #in this case we should have just 1 !
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)
          #If details are required, a request is launched for each one
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)
      '''
      if _SaveResult:
        #TODO: Need to implement a way to save the Response data
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    # Make a search about materials details on bSDD  (CUSTOM MADE) - /api/Material/v1: 
    #----------------------------------------------------------------------------------------------------

    def get_Material_Details(self, _namespaceURI, _languageCode, _includeChildMaterialReferences, _SaveResult):
      # params of the request
      payload = dict()
      payload["namespaceUri"] = _namespaceURI #A list of strings
      payload["languageCode"] = _languageCode #It is a string
      payload["includeChildMaterialReferences"] = _includeChildMaterialReferences #A list of strings
      
      Response, request_status = self.get(Resource_Material_Details, payload)
      
      #TODO: Implement NbRes for this method
      #NbRes = Response["numberOfClassificationsFound"]
      NbRes=1
      '''
      for item in Response['domains']: #in this case we should have just 1 !
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)
          #If details are required, a request is launched for each one
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)
      '''
      if _SaveResult:
        #TODO: Need to implement a way to save the Response data
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    # Make a serch to get a list of Materials from a given Domain, without details  (CUSTOM MADE) - /api/Material/SearchOpen/preview: 
    #----------------------------------------------------------------------------------------------------

    def get_List_Material_Domain(self, _DomainNamespaceURI, _SearchText, _LanguageCode, _SaveResult):
      # params of the request
      payload = dict()
      payload["DomainNamespaceUri"] = _DomainNamespaceURI #A list of strings
      payload["SearchText"] = _SearchText #It is a string
      payload["LanguageCode"] = _LanguageCode #A list of strings
      
      Response, request_status = self.get(Resource_List_Material_Domain, payload)
      
      #TODO: Implement NbRes for this method
      #NbRes = Response["numberOfClassificationsFound"]
      NbRes=1
      '''
      for item in Response['domains']: #in this case we should have just 1 !
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)
          #If details are required, a request is launched for each one
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)
      '''
      if _SaveResult:
        #TODO: Need to implement a way to save the Response data
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    # Make a search to get the details of a given Property  (CUSTOM MADE) - /api/Property/v2: 
    #----------------------------------------------------------------------------------------------------

    def get_Property_Details(self, _namespaceURI, _languageCode, _SaveResult):
      # params of the request
      payload = dict()
      payload["namespaceUri"] = _namespaceURI #A list of strings. Namespace URI of the property
      payload["languageCode"] = _languageCode #A list of strings
      
      Response, request_status = self.get(Resource_Property_Details, payload)
      
      #TODO: Implement NbRes for this method
      #NbRes = Response["numberOfClassificationsFound"]
      NbRes=1
      '''
      for item in Response['domains']: #in this case we should have just 1 !
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)
          #If details are required, a request is launched for each one
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)
      '''
      if _SaveResult:
        #TODO: Need to implement a way to save the Response data
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    # Make a search to get the details of a Property value (CUSTOM MADE) - /api/PropertyValue/v1: 
    #----------------------------------------------------------------------------------------------------

    def get_PropertyValue_Details(self, _namespaceURI, _languageCode, _SaveResult):
      # params of the request
      payload = dict()
      payload["namespaceUri"] = _namespaceURI #A list of strings. Namespace URI of the property
      payload["languageCode"] = _languageCode #A list of strings
      
      Response, request_status = self.get(Resource_PropertyValue_Details, payload)
      
      #TODO: Implement NbRes for this method
      #NbRes = Response["numberOfClassificationsFound"]
      NbRes=1
      '''
      for item in Response['domains']: #in this case we should have just 1 !
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)
          #If details are required, a request is launched for each one
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)
      '''
      if _SaveResult:
        #TODO: Need to implement a way to save the Response data
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    # Make open search about classifications - /api/SearchList/v2
    #----------------------------------------------------------------------------------------------------

    def get_Open_Search_Classifications(self, _DomainURI, _SearchText, _LanguageCode, _RelatedIfcEntity, _SaveResult):
      
      # params of the request
      payload = dict()
      payload["DomainNamespaceUri"] = _DomainURI
      payload["SearchText"] = _SearchText
      #Language code for the request ; EN for Internation English
      payload["LanguageCode"] = _LanguageCode
      payload["RelatedIfcEntity"] = _RelatedIfcEntity
      
      Response, request_status = self.get(Resource_Search_Open, payload)

      #TODO: Implement NbRes for this method
      #NbRes = Response["numberOfClassificationsFound"]
      NbRes = 1
      '''
      for item in Response['domains']: #in this case we should have just 1 ! (Since we informed a URI from a specific domain)
        ReadDomain = self.GetDomainFromURI(item['namespaceUri']) 
        for item2 in item["classifications"]:
          NewClass = TClassification()
          NewClass.FillValuesFromJSON(item2)
          ReadDomain.Classes.append(NewClass)

          #If details are required, a request is launched for each class
          if _Get_Details:
                payloadClass = dict()
                payloadClass["namespaceUri"] = NewClass.namespaceUri
                payloadClass["languageCode"] = _LanguageCode
                payloadClass["includeChildClassificationReferences"] = False #we don't ask for the hierarchy we just want properties
                mResponse = self.get(Resource_Classification, payloadClass)
                NewClass.Load_Details(mResponse)
      '''

      if _SaveResult:
        #TODO: Need to implement a way to save the Response data
        #Save the classes informations to a csv    
        #ReadDomain.SaveToCSV();
        True

      return NbRes, Response, request_status

    #----------------------------------------------------------------------------------------------------
    #  Request a file with an export of a domain (CUSTOM MADE) - /api/RequestExportFile/preview: 
    #----------------------------------------------------------------------------------------------------
    
    def RequestExportOfADomain(self, _SaveResult):
      
      Response = self.get(Resource_ExportFile, "")
      #Browse the results
      NbRes = 0
      
      for item in Response:
        Domain = TDomain()
        Domain.FillValuesFromJSON(item)
        self.Domains.append(Domain)
        NbRes = NbRes + 1
      
      if _SaveResult:
        #Save domain list to a csv file
        self.Save_Domains_To_CSV()

      return NbRes