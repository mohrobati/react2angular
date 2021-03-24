import esprima
import glob
import os
from copy import deepcopy


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
        self.inputs = []
        self.angularHTML = ""

    def generateAppModule(self, allFiles):
        components = [c.replace('angular', '.') for c in list(filter(self.isComponent, allFiles))]
        componentNames = self.getComponentNames(components)
        string = ""
        for i in range(len(components)):
            string += "import { " + componentNames[i] + " } from '" + components[i].replace(".ts", "") + "';\n"
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
        angularComponent = "import { Component, Input } from '@angular/core';\n\n"
        for element in parsedReactComponent.body:
            if element.type == "VariableDeclaration":
                self.variables[element.declarations[0].id.name] = element.declarations[0].init.value
            elif element.type == "FunctionDeclaration" and element.id.name in self.allReactComponents:
                currReactComponent = element.id.name
                self.generateAngularComponent(element.body, False)
            elif element.type == "ReturnStatement" and element.argument.type == "JSXElement":
                self.parseJSX(element.argument)
        if component:
            angularComponent += self.getComponentArgs(currReactComponent)
            angularComponent += self.generateAngularComponentSyntax(currReactComponent)
            angularHTML = deepcopy(self.angularHTML)
            self.angularHTML = ""
            self.variables = {}
            self.inputs = []
            return angularComponent, angularHTML

    def getComponentArgs(self, currReactComponent):
        componentArgs = {}
        componentArgs['templateUrl'] = './' + currReactComponent + '.component.html'
        componentArgs['styleUrls'] = ['./' + currReactComponent + '.component.css']
        if currReactComponent == 'App':
            componentArgs['selector'] = 'app-root'
        else:
            componentArgs['selector'] = 'app-' + currReactComponent
        return "@Component(" + str(componentArgs) + ")\n"

    def generateAngularComponentSyntax(self, currReactComponent):
        angularComponentSyntax = "export class " + currReactComponent + "Component {\n"
        for input in self.inputs:
            angularComponentSyntax += "@Input() " + input + ": string;\n"
        angularComponentSyntax += "constructor() {\n"
        for input in self.inputs:
            if input in self.variables:
                angularComponentSyntax += "\tthis." + input + "= '" + self.variables[input] + "';\n"
            else:
                angularComponentSyntax += "\tthis." + input + "= '';\n"
        angularComponentSyntax += "}\n"
        return angularComponentSyntax + "}"

    def parseJSX(self, jsxElement):
        if jsxElement.type == "JSXElement":
            elementName = jsxElement.openingElement.name.name
            if elementName in self.allReactComponents:
                self.angularHTML += '<app-' + elementName
            else:
                self.angularHTML += '<' + elementName
            for attribute in jsxElement.openingElement.attributes:
                if attribute.value.expression:
                    if attribute.name.name == "style":
                        self.angularHTML += ' [' + attribute.name.name.replace("style", "ngStyle") + ']="'
                    else:
                        self.angularHTML += ' ' + attribute.name.name + '={{'
                    if attribute.value.expression.properties:
                        self.angularHTML += "{"
                        for p in attribute.value.expression.properties:
                            self.angularHTML += "'" + p.key.name + "'" + ": " + p.value.property.name + ' '
                            self.inputs.append(p.value.property.name)
                        self.angularHTML += '}"'
                    elif attribute.value.expression.object:
                        self.angularHTML += attribute.value.expression.property.name + '}} '
                        self.inputs.append(attribute.value.expression.property.name)
                    else:
                        self.angularHTML += attribute.value.expression.name + '}} '
                        self.inputs.append(attribute.value.expression.name)

                else:
                    self.angularHTML += ' ' + attribute.name.name.replace("className",
                                                                          "class") + '="' + attribute.value.value + '"'
            if elementName in self.allReactComponents:
                self.angularHTML += '></app-' + elementName
            if jsxElement.openingElement.selfClosing and elementName not in self.allReactComponents:
                self.angularHTML += '/>\n'
            else:
                self.angularHTML += '>\n'
            for child in jsxElement.children:
                if child.type == "JSXElement" or child.type == "JSXExpressionContainer" or child.type == "JSXText":
                    self.parseJSX(child)
            if jsxElement.closingElement:
                self.angularHTML += "</" + jsxElement.closingElement.name.name + ">\n"
        elif jsxElement.type == "JSXExpressionContainer":
            self.angularHTML += "{{" + jsxElement.expression.property.name + "}}"
            self.inputs.append(jsxElement.expression.property.name)
        elif jsxElement.type == "JSXText":
            self.angularHTML += jsxElement.value.replace("\n", "").replace(" ", "")
