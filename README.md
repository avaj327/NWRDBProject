# NWRDBProject
Database project made by NWR students, for NWR

Using Flask Python Microframework

<h2>Downloading</h2>
To download and run (external computer):
<ol>
  <li>Download master branch as zip</li>
  <li>Extract zip file</li>
  <li>Navigate to the NWRDBProject-master folder in a command line</li>
  <li>Run the command: export FLASK_APP=test.py</li>
  <li>Run the command: flask run</li>
</ol>
<br>
To download and run (NWR network server):
<ol>
  <li>Connect to the NWR server (see below)</li>
  <li>Enter the command 'updategit [-b (branch)]'</li>
  <li>Enter the command 'setflask'</li>
  <li>Enter the command 'runflask'</li>
</ol>
<h2>Running on the network</h2>
In the command terminal:
<ol>
  <li>Type "ssh student@10.1.10.88 -p 22"</li>
  <li>Upon being prompted for a password, type "student"</li>
  <li>To update repository, type "updategit -b " + branch name</li>
  <li>To run the server, first type "setflask"</li>
  <li>Then type "runflask"</li>
</ol>
To connect to the server through a browser, enter the address "10.1.10.88:5000"
