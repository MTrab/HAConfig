def loadHACS():
    with open("/config/.storage/hacs.repositories") as f:
        data = f.read()
    
    return data

def genReadme(integrations, frontends):
    with open("/config/pyscript/scripts/generate_readme/templates/header") as f:
        header = f.read()

    with open("/config/pyscript/scripts/generate_readme/templates/version") as f:
        version = f.read()

    with open("/config/pyscript/scripts/generate_readme/templates/hardware") as f:
        hardware = f.read()

    with open("/config/pyscript/scripts/generate_readme/templates/supervisor") as f:
        supervisor = f.read()

    with open("/config/pyscript/scripts/generate_readme/templates/config") as f:
        config = f.read()
    
    with open("/config/README.md.test", "w") as f:
        f.write(header)