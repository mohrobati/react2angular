import esprima
import glob
import os
from .angular_generator import AngularGenerator


class ReactParser:

    def __init__(self, directory):
        self.directory = directory
        self.allAngularFiles = []
        self.angularGenerator = AngularGenerator()

    def parseStructure(self):
        files = [f[len(self.directory):] for f in glob.glob(self.directory + "**/*.js", recursive=True)]
        return files

    def makeNewFile(self, dir):
        self.allAngularFiles.append(dir)
        try:
            open(dir, "w")
        except OSError as error:
            pass
        if dir.endswith(".css"):
            self.moveCSS(dir)

    def makeNewFolder(self, dir):
        try:
            os.makedirs(dir)
        except OSError as error:
            pass

    def moveCSS(self, dir):
        f_react = open(dir.replace('angular', 'react').replace('.component', ""), "r")
        f_ng = open(dir, "w+")
        css = f_react.read()
        f_ng.write(css)

    def generateAngularStructure(self):
        self.makeNewFolder('angular')
        files = self.parseStructure()
        for f in files:
            parts = f.split("/")
            if len(parts) == 1:
                self.makeNewFile('angular/' + parts[0].split(".")[0] + ".component.ts")
                self.makeNewFile('angular/' + parts[0].split(".")[0] + ".component.html")
                self.makeNewFile('angular/' + parts[0].split(".")[0] + ".component.css")
            else:
                newDir = 'angular/' + "/".join(parts[0:len(parts) - 1]) + "/"
                self.makeNewFolder(newDir)
                self.makeNewFile(newDir + parts[len(parts) - 1].split(".")[0] + ".component.ts")
                self.makeNewFile(newDir + parts[len(parts) - 1].split(".")[0] + ".component.html")
                self.makeNewFile(newDir + parts[len(parts) - 1].split(".")[0] + ".component.css")
        self.makeNewFile('angular/app.module.ts')
        self.angularGenerator.generateAppModule(self.allAngularFiles)

    def parseReactComponent(self, dir):
        reactCode = ""
        f = open(dir, "r")
        for line in f:
            if line.startswith("import") or line.startswith("export"):
                reactCode += "// " + line
            else:
                reactCode += line
        parsedReactCode = esprima.parseScript(reactCode, jsx=True)
        print('Parsing React Component...')
        angularComponent, angularHTML = self.angularGenerator.generateAngularComponent(parsedReactCode, True)
        f_ts = open(dir.replace("react", "angular").replace(".js", ".component.ts"), "w")
        f_html = open(dir.replace("react", "angular").replace(".js", ".component.html"), "w")
        print('Generating Angular Component...')
        f_ts.write(angularComponent)
        f_html.write(angularHTML)

    def transformReactFiles(self):
        self.generateAngularStructure()
        for file in self.parseStructure():
            self.parseReactComponent(self.directory + file)
        print("\n*** Files are ready at ./angular ***")



