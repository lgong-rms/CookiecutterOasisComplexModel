cookiecutter-OasisModel
=======================

A cookiecutter project structure for Oasis models that can be replicated
using the \ ``cookiecutter`` Python tool.

Cloning the repository
----------------------

You can clone this repository from GitHub if you are a member of the
Oasis development team on GitHub or have write access to the GitHub
repository via another OasisLMF organizational team. You can clone over
HTTPS or SSH, but it is recommended that that you use SSH: first ensure
that you have generated an SSH key pair on your local machine and add
the public key of that pair to your GitHub account (use the GitHub guide
at https://help.github.com/articles/connecting-to-github-with-ssh/).
Then run

::

    git clone git+ssh://git@github.com/OasisLMF/cookiecutter-OasisModel

To clone over HTTPS use

::

    git clone https://github.com/OasisLMF/cookiecutter-OasisModel

You may receive a password prompt - to bypass the password prompt use

::

    git clone https://<GitHub user name:GitHub password>@github.com/OasisLMF/cookiecutter-OasisModel

First steps
-----------

Install cookiecutter (if not present):

::

    /home/foo$ pip install cookiecutter

Run cookiecutter on the source repo (the URI can be specified using
either ``https`` or ``git`` or ``git+ssh``):

::

    /home/foo$ cookiecutter git+ssh://git@github.com/OasisLMF/cookiecutter-OasisModel

You should see the following prompts for project and model settings in
sequence (press ENTER to use default values):

::

    project_name [OM]: 
    project_slug [OM]: 
    project_short_description [Oasis Model]: 
    project_maintainer [<full name of primary project maintainer>]: 
    project_maintainer_email [<primary GitHub account email of primary project maintainer>]: 
    version [0.0.1]: 
    primary_language [Python]: 
    organization [OasisLMF]: 
    model_identifier [OM]: 
    model_version [0.0.0.1]: 

These prompts are self-explanatory, but ``project_name``,
``project_slug``, ``organization``, ``model_identifier`` and
``model_version`` are mandatory, while the others are optional. Here are
some guidelines to follow for the mandatory prompts.

-  ``project_name`` should be a concise title for the project (title
   words should be capitalised)
-  ``project_slug`` is the folder name for the project and by default
   cookiecutter will set this to a camel casing of the ``project_name``
   value, but you may enter a specific value yourself, provided it does
   not contain spaces or any special characters not normally present in
   folder names
-  ``organization`` should either be a camel case of the organization
   name or an acronym
-  ``model_identifier`` should be a short ID for the full model name,
   e.g. an acronym of the full model name
-  ``model_version`` this can be any meaningful string that indicates a
   version for the model (by default it is set to ``0.0.0.1``)

The project structure is contained in the repo folder named
\ ``{{cookiecutter.project_slug}}``\  and project-related settings such
as the project descriptive name, model name and version etc., which are
set during runtime via the prompts, are configurable in the repo file
\ ``cookiecutter.json``\ .

For the current state of the \ ``{{cookiecutter.project_slug}}``\ 
directory you should see the following project structure in the place
where you ran the command (assuming you used default boilerplate values
for the project name, organization and model name):

::

    OM/
    ├── Dockerfile.oasislmf_om_keys_server
    ├── Dockerfile.oasislmf_om_model_execution_worker
    ├── LICENSE
    ├── README.md
    ├── flamingo/
    │   └── generic_model/
    │       ├── Files/
    │       │   ├── MappingFiles/
    │       │   │   ├── Generic_Earthquake_CanLoc_BToModelLoc.mfd
    │       │   │   ├── Generic_Earthquake_SourceLocToCanLoc_A.mfd
    │       │   │   ├── Generic_Flood_CanLoc_BToModelLoc.mfd
    │       │   │   ├── Generic_Flood_SourceLocToCanLoc_A.mfd
    │       │   │   ├── Generic_SourceAccToCanAcc_A.mfd
    │       │   │   ├── Generic_Windstorm_CanLoc_BToModelLoc.mfd
    │       │   │   └── Generic_Windstorm_SourceLocToCanLoc_A.mfd
    │       │   ├── TransformationFiles/
    │       │   │   ├── MappingMapToGeneric_CanAcc_A.xslt
    │       │   │   ├── MappingMapToGeneric_Earthquake_CanLoc_A.xslt
    │       │   │   ├── MappingMapToGeneric_Earthquake_ModelLoc.xslt
    │       │   │   ├── MappingMapToGeneric_Flood_CanLoc_A.xslt
    │       │   │   ├── MappingMapToGeneric_Flood_ModelLoc.xslt
    │       │   │   ├── MappingMapToGeneric_Windstorm_CanLoc_A.xslt
    │       │   │   └── MappingMapToGeneric_Windstorm_ModelLoc.xslt
    │       │   └── ValidationFiles/
    │       │       ├── Generic_CanAcc_A.xsd
    │       │       ├── Generic_CanAcc_B.xsd
    │       │       ├── Generic_Earthquake_CanLoc_A.xsd
    │       │       ├── Generic_Earthquake_CanLoc_B.xsd
    │       │       ├── Generic_Earthquake_ModelLoc.xsd
    │       │       ├── Generic_Earthquake_SourceLoc.xsd
    │       │       ├── Generic_Flood_CanLoc_A.xsd
    │       │       ├── Generic_Flood_CanLoc_B.xsd
    │       │       ├── Generic_Flood_ModelLoc.xsd
    │       │       ├── Generic_Flood_SourceLoc.xsd
    │       │       ├── Generic_SourceAcc.xsd
    │       │       ├── Generic_Windstorm_CanLoc_A.xsd
    │       │       ├── Generic_Windstorm_CanLoc_B.xsd
    │       │       ├── Generic_Windstorm_ModelLoc.xsd
    │       │       └── Generic_Windstorm_SourceLoc.xsd
    │       └── SQLFiles/
    ├── keys_data/
    │   └── OM/
    │       └── ModelVersion.csv
    ├── keys_server_config/
    │   ├── apache2.conf
    │   ├── oasis.conf
    │   └── oasis.wsgi
    ├── model_data/
    │   └── OM/
    │       ├── ModelVersion.csv
    │       ├── damage_bin_dict.bin
    │       ├── damage_bin_dict.csv
    │       ├── data.csv
    │       ├── events.bin
    │       ├── events.csv
    │       ├── footprint.bin
    │       ├── footprint.csv
    │       ├── footprint.idx
    │       ├── occurrence.bin
    │       ├── occurrence.csv
    │       ├── random.bin
    │       ├── random.csv
    │       ├── returnperiods.bin
    │       ├── returnperiods.csv
    │       ├── vulnerability.bin
    │       └── vulnerability.csv
    ├── oasis_build_utils/
    │   └── keys_server_build_utils.sh
    ├── oasislmf_om_keys_server_build_config
    ├── src/
    │   ├── keys_server/
    │   │   ├── OM/
    │   │   │   ├── KeysServer.ini
    │   │   │   ├── OMKeysLookup.py
    │   │   │   ├── __init__.py
    │   │   │   ├── requirements.txt
    │   │   │   └── utils.py
    │   │   ├── __init__.py
    │   │   ├── __init__.py.base
    │   │   ├── requirements.txt
    │   │   └── utils.py
    │   ├── model_execution_worker/
    │   │   └── OM/
    │   │       ├── __init__.py
    │   │       └── supplier_model_runner.py
    │   └── oasis_keys_server/
    │       ├── KeysServer.ini
    │       ├── LICENSE
    │       ├── README.md
    │       ├── __init__.py
    │       ├── app.py
    │       ├── docs/
    │       ├── requirements.txt
    │       ├── startup.sh
    │       ├── tests/
    │       │   ├── KeysServerTests.ini
    │       │   ├── KeysServerTests.py
    │       │   ├── __init__.py
    │       │   └── requirements.txt
    │       └── utils.py
    └── tests/
        └── keys_server_tests/
            └── data/
                └── OM/
                    ├── KeysServerTests.ini
                    └── ModelVersion.csv
