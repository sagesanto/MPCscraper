import os


def expandPath(workingDir, returner):
    if not os.path.isdir(workingDir):  # we're a file. append ourselves and return!
        returner.append(workingDir)
        print("appended " + workingDir)
        return returner
    else: #call our nodes
        for item in os.listdir(workingDir):
            returner = expandPath(workingDir + "/" + item, returner)
        return returner

dir = "../src/bulletins2/"
path = list(filter(lambda p: ".txt" in p, expandPath(dir, [])))
print(path)