{{cookiecutter.organization.replace(' ', '')}} Keys Server ({{cookiecutter.model_identifier.replace(' ', '').upper()}})
======================================================================================================

## Cloning the repository

You can clone this repository from <a href="https://github.com/OasisLMF/Catrisks" target="_blank">GitHub</a> using HTTPS or SSH. Before doing this you must generate an SSH key pair on your local machine and add the public key of that pair to your GitHub account (use the GitHub guide at <a href="https://help.github.com/articles/connecting-to-github-with-ssh/" target="_blank">https://help.github.com/articles/connecting-to-github-with-ssh/</a>). To clone over SSH use

    git clone --recursive git+ssh://git@github.com/OasisLMF/{{cookiecutter.organization.replace(' ', '')}}

To clone over HTTPS use

    git clone --recursive https://<GitHub user name:GitHub password>@github.com/OasisLMF/{{cookiecutter.organization.replace(' ', '')}}

The `--recursive` option ensures the cloned repository contains the <a href="https://github.com/OasisLMF/oasis_keys_server" target="_blank">`oasis_keys_server`</a> submodule. You have read only access to this submodule.

## Managing the submodules

Run the command

    git submodule

to list the submodules (latest commit IDs, paths and branches). If any are missing then you can add them using

    git submodule add <submodule GitHub repo URL> <local path/destination>

to ensure that the Oasis submodules are checked out on the `master` branches.

If you've already cloned the repository and wish to update the submodules (all at once) in your working directory from their GitHub repositories then run

    git submodule foreach 'git pull origin'

You can also update the submodules individually by pulling from within them.

You should not make any local changes to these submodules because you have read-only access to their GitHub repositories. So submodule changes can only propagate from GitHub to your local repository. To detect these changes you can run `git status -uno` and to commit them you can add the paths and commit them in the normal way.

## Building and running a keys server

First, ensure that you have Docker installed on your system and that your Unix user has been added to the `docker` user group (run `sudo usermod -a -G docker $USER`).

To build a keys server run the command

    sudo docker build -f <docker file name> -t <image name/tag> .

Run `docker images` to list all images and check the one you've built exists. To run the image in a container you can use the command

    docker run -dp 5000:80 --name=<container name/tag> <image name/tag>

To check the container is running use the command `docker ps`. If you want to run the healthcheck on the keys server then use the command

    curl -s http://<server or localhost>:5000/{{cookiecutter.organization.replace(' ', '')}}/<model ID>/<model version>/healthcheck

You should get a response of `OK` if the keys server has initialised and is running normally, otherwise you should get the HTML error response from Apache. To enter the running container you can use the command

    docker exec -it <container name> bash

The log files to check are `/var/log/apache/error.log` (Apache error log), `/var/log/apache/access.log` (Apache request log), and `/var/log/oasis/keys_server.log` (the keys server Python log). In case of request timeout issues you can edit the `Timeout` option value (in seconds) in the file `/etc/apache2/sites-available/oasis.conf` and restart Apache (`service apache2 restart`).

## Testing the keys server

The `./src/oasis_keys_server` submodule contains a set of Python test cases which you can run against a running keys server for a defined model. The tests require configuration information which can be found in an INI file `KeysServerTests.ini` located in `./tests/keys_server_tests/data/<model ID>`. If this subfolder and file does not exist then you will have to create it. The file should define some files and keys server properties needed to run the tests.

    [Default]

    MODEL_VERSION_FILE_PATH=/path/to/your/{{cookiecutter.organization.replace(' ', '')}}/tests/keys_server_tests/data/<model ID>/ModelVersion.csv

    KEYS_DATA_PATH=/path/to/model/lookup/keys/data

    SAMPLE_CSV_MODEL_EXPOSURES_FILE_PATH=/path/to/your/{{cookiecutter.organization.replace(' ', '')}}/tests/keys_server_tests/data/<model ID>/<model loc. test CSV file>

    SAMPLE_JSON_MODEL_EXPOSURES_FILE_PATH=/path/to/your/{{cookiecutter.organization.replace(' ', '')}}/tests/keys_server_tests/data/<model ID>/<model loc. test JSON file>

    KEYS_SERVER_HOSTNAME_OR_IP=localhost

    KEYS_SERVER_PORT=5000

Make sure the paths exist and the server hostname/IP and port are correct. Then copy the INI file for the model (`./tests/keys_server_tests/data/<model ID>/KeysServerTests.ini`) to `./src/oasis_keys_server/tests` and then run

    python -m unittest -v KeysServerTests

You should see the tests passing

    test_healthcheck (KeysServerTests.KeysServerTests) ... ok
    test_keys_request_csv (KeysServerTests.KeysServerTests) ... ok
    test_keys_request_csv__invalid_content_type (KeysServerTests.KeysServerTests) ... ok
    test_keys_request_json (KeysServerTests.KeysServerTests) ... ok
    test_keys_request_json__invalid_content_type (KeysServerTests.KeysServerTests) ... ok

    ----------------------------------------------------------------------
    Ran 5 tests in 0.250s

    OK

To run individual test cases you can use

    python -m unittest -v KeysServerTests.KeysServerTests.<test case name>
