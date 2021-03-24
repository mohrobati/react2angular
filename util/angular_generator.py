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
        self.angularHTML = ""

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

    def generateAngularComponent(self, parsedReactComponent, component):
        currReactComponent = ""
        angularComponent = "import { Component } from '@angular/core';\n\n"
        for element in parsedReactComponent.body:
            if element.type == "VariableDeclaration":
                self.variables[element.declarations[0].id.name] = element.declarations[0].init.value
            elif element.type == "FunctionDeclaration" and element.id.name in self.allReactComponents:
                currReactComponent = element.id.name
                self.generateAngularComponent(element.body, False)
            elif element.type == "ReturnStatement" and element.argument.type == "JSXElement":
                print(element)
                self.parseJSX(element.argument)
        if component:
            angularComponent += self.getComponentArgs(currReactComponent)
            angularComponent += self.generateAngularComponentSyntax(currReactComponent)
            return angularComponent, self.angularHTML

    def getComponentArgs(self, currReactComponent):
        componentArgs = {}
        componentArgs['templateUrl'] = './' + currReactComponent + '.component.html'
        componentArgs['styleUrls'] = "['./" + currReactComponent + ".component.css']"
        if currReactComponent == 'App':
            componentArgs['selector'] = 'app-root'
        else:
            componentArgs['selector'] = 'app-' + currReactComponent
        return "@Component(" + str(componentArgs) + ")\n"

    def generateAngularComponentSyntax(self, currReactComponent):
        angularComponentSyntax = "export class " + currReactComponent + "Component {\n"
        for var in self.variables:
            angularComponentSyntax += var + " = '" + self.variables[var] + "';\n"
        return angularComponentSyntax + "}"

    def parseJSX(self, jsxElement):
        if not jsxElement.type == "JSXExpressionContainer":
            elementName = jsxElement.openingElement.name.name
            if elementName in self.allReactComponents:
                self.angularHTML += '<app-' + elementName
            else:
                self.angularHTML += '<' + elementName
            for attribute in jsxElement.openingElement.attributes:
                if attribute.value.expression:
                    self.angularHTML += ' [' + attribute.name.name.replace("style", "ngStyle") + ']="'
                    if attribute.value.expression.properties:
                        self.angularHTML += "{"
                        for p in attribute.value.expression.properties:
                            self.angularHTML += "'" + p.key.name + "'" + ": " + p.value.property.name + ';'
                        self.angularHTML += "}"
                    elif attribute.value.expression.object:
                        self.angularHTML += attribute.value.expression.property.name + '"'
                else:
                    self.angularHTML += ' ' + attribute.name.name.replace("className",
                                                                          "class") + '="' + attribute.value.value + '"'
            if jsxElement.openingElement.selfClosing:
                self.angularHTML += '/>\n'
            else:
                self.angularHTML += '>\n'
            for child in jsxElement.children:
                if child.type == "JSXElement" or child.type == "JSXExpressionContainer":
                    self.parseJSX(child)
            if jsxElement.closingElement:
                self.angularHTML += "</" + jsxElement.closingElement.name.name + ">\n"
        else:
            self.angularHTML += "{{" + jsxElement.expression.property.name + "}}"
