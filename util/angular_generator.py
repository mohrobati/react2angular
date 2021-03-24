import esprima
import glob
import os


class AngularGenerator:

    def __init__(self):
        self.appModuleHeader = """import { NgModule } from '@angular/core';\nimport { BrowserModule } from '@angular/platform-browser';\n"""
        self.appModuleFooter = """
    ],
    imports: [
        BrowserModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
        """
        self.allReactComponents = []
        self.variables = {}

    def generateAppModule(self, allFiles):
        components = [c.replace('angular', '.') for c in list(filter(self.isComponent, allFiles))]
        componentNames = self.getComponentNames(components)
        string = ""
        for i in range(len(components)):
            string += "import { " + componentNames[i] + " } from '" + components[i] + "';\n"
        string += """@NgModule({\n\tdeclarations: [\n\t\t"""
        string += ",\n\t\t".join(componentNames)
        f = open('angular/app.module.ts', "w")
        f.write(self.appModuleHeader + string + self.appModuleFooter)

    def getComponentNames(self, components):
        componentNames = []
        for component in components:
            parts = component.split("/")
            componentName = parts[len(parts) - 1].split(".")[0]
            self.allReactComponents.append(componentName)
            componentNames.append(componentName + "Component")
        return componentNames

    def isComponent(self, string):
        return string.find('component.ts') > 0


    def generateAngularComponent(self, parsedReactComponent):
        for element in parsedReactComponent.body:
            if element.type == "VariableDeclaration":
                self.variables[element.declarations[0].id.name] = element.declarations[0].init.value
            elif element.type == "FunctionDeclaration" and element.id.name in self.allReactComponents:
                self.generateAngularComponent(element.body)
            elif element.type == "ReturnStatement" and element.argument.type == "JSXElement":
                pass
        # print(parsedReactComponent)


