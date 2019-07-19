{{cookiecutter.organization.replace(' ', '')}} model repository ({{cookiecutter.model_identifier.replace(' ', '').upper()}})
============================================================================================================================

## Cloning the repository

You can clone this repository from <a href="https://github.com/OasisLMF/{{cookiecutter.organization.replace(' ', '')}}" target="_blank">GitHub</a> using HTTPS or SSH. Before doing this you must generate an SSH key pair on your local machine and add the public key of that pair to your GitHub account (use the GitHub guide at <a href="https://help.github.com/articles/connecting-to-github-with-ssh/" target="_blank">https://help.github.com/articles/connecting-to-github-with-ssh/</a>). You can clone using the following command.

    git clone git+{https, ssh}://git@github.com/OasisLMF/{{cookiecutter.organization.replace(' ', '')}}
