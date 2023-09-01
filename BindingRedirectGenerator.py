# author: Kerry Cao
# date: 2023-08-21
# description: This script will generate a list of binding redirects from an app.config file
# usage: python BindingRedirectGenerator.py
# input: absolute file path for app.config
# output: GeneratedBindingRedirects.txt

import xml.etree.ElementTree as ET


def getXMLTreeRoot(filename):
    return ET.parse(filename).getroot()


def getBindingRedirects(filename):
    redirects = []
    root = getXMLTreeRoot(filename)
    for dependentAssembly in root.find('.//runtime//{*}assemblyBinding'):
        name = dependentAssembly.find('{*}assemblyIdentity').attrib['name']
        token = dependentAssembly.find('{*}assemblyIdentity').attrib['publicKeyToken']
        version = dependentAssembly.find('{*}bindingRedirect').attrib['newVersion']

        redirect_str = f'{{\"ShortName\":\"{name}\",\"RedirectToVersion\":\"{version}\",\"PublicKeyToken\":\"{token}\"}}'
        redirects.append(redirect_str)
    return redirects


if __name__ == '__main__':
    # get file path from input
    filenameInput = input('Enter absolute file path for app.config: ')

    # validate file exists
    try:
        with open(filenameInput, "r") as f:
            pass
    except IOError:
        print('File not found')
        print('Check your input or contact Kerry Cao')
        exit()

    # get binding binding_redirects
    binding_redirects = getBindingRedirects(filenameInput)

    # ask user if they want to ecape the output
    escape = input('Escape output? (y/n): ')
    if escape == 'y':
        binding_redirects = [redirect.replace('"', '\\"') for redirect in binding_redirects]

    # write to file
    with open('GeneratedBindingRedirects.txt', 'w') as f:
        f.write('Individual Redirects:\n')
        for redirect in binding_redirects:
            f.write(redirect + '\n')
        f.write('\nArray:\n')
        f.write(f'[{",".join(binding_redirects)}]')

    print(f'[{",".join(binding_redirects)}]')
    print('Done')
