import os
import sys
from datetime import datetime
import mainapp
from mainapp import SemarchyClient

#Main calling mechanism start below
#Initialize the class ClassName(object):
#python script takes the command line arguments as below
#to export e.g py WrapperSemarchyadmin.py deploy <modelname> <SourceServer> <Sourceport> <DestinationServer> <Destinationport>
modelName=""
outputfilename=""
print(len(sys.argv))

if len(sys.argv) != 7:
    print("Insufficient arguments")
    quit()

print("Args len " +str(len(sys.argv)))
print("4th argument " +sys.argv[4])


if sys.argv[1]=="deploy":
    print("export from source")
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
    #import into the target
    print("import to target "+outputfilename)
    print("file size " +str(os.path.getsize(outputfilename)))
    openFile = open(outputfilename,"rb")
    xmldata = openFile.read()
    if sys.argv[5] == "NA":
        print("Target no port")
        targetClient = SemarchyClient(sys.argv[5],"","semadmin","semadmin")
    else:
        print("Target with port")
        targetClient = SemarchyClient(sys.argv[5],sys.argv[6],"semadmin","semadmin")
    r=targetClient.importModelEdition(modelExport.content)
    if r.status_code == 200:
         print("Model imported successfully to the target")
    else:
         print("Model import failed to the target "+r.text)
else:
    print("Bye!")
    quit()


