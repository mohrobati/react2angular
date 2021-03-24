from util.react_parser import ReactParser

rp = ReactParser("./react/")
rp.generateAngularStructure()
rp.parseReactComponent('react/Components/EntryBox/EntryBox.js')


