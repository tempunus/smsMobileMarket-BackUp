from encodings import utf_8
coding:utf_8

from xml.dom.minidom import parse

doc = parse('Minidon_Create.xml')
xml = doc.documentElement
 
 if xml.hasAttribute('content'):
     