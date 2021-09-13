import sys
from datetime import datetime
import mainapp
from mainapp import SemarchyClient

#Main calling mechanism start below
#Initialize the class ClassName(object):
#python script takes the command line arguments as below
#to export e.g py WrapperSemarchyadmin.py deploy <modelname> <SourceServer> <Sourceport> <DestinationServer> <Destinationport>
modelName="CustomerB2CDemo"
outputfilename="CustomerB2CDemo_0.1.xml"
print(len(sys.argv))

if len(sys.argv) != 7:
    print("Insufficient arguments")
    quit()

print("Args len " +str(len(sys.argv)))
print("4th argument " +sys.argv[4])


if sys.argv[1]=="deploy":
    if sys.argv[4] == "NA":
        print("Without port")
        sourceClient = SemarchyClient(sys.argv[3],"","semadmin","semadmin")
    else:
        print("With port")
        sourceClient = SemarchyClient(sys.argv[3],sys.argv[4],"semadmin","semadmin")   
    try:
        latestModelVersion = sourceClient.getLatestCloseModelKey(sys.argv[2])
    except CustomValidationError as exception:
        print (exception.message)
    print("Latest key for model  is " + str(latestModelVersion))
    modelExport = sourceClient.exportModelEdition(modelName, str(latestModelVersion))
    todaydtfolder = datetime.today().strftime('%d-%m-%Y')

    outputfilename=todaydtfolder+"/"+sys.argv[2]+"-" +str(latestModelVersion)+ ".xml"
    with open(outputfilename, "wb") as f:
        f.write(modelExport.content)
    print("Model Exported completed and saved to file "+outputfilename)
else:
    print("Bye!")
    quit()

'''
if importval.upper()=="import":
    openFile = open(outputfilename,"rb")
    xmldata = openFile.read()
    targetClient = SemarchyClient("prodsemarchy.eastus.cloudapp.azure.com","8088","semadmin","semadmin")
    r=targetClient.importModelEdition(xmldata)
    if r.status_code == 200:
        print("Model imported successfully to the target")
    else:
        print("Model import failed to the target "+r.text)
else:
    print("Bye!")
    quit()
'''
