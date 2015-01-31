# beebole-console-manager <b>V0.0.1</b>
a command line beebole api interface to update your beebole account!

<h3>Install</h3>

clone this repo<br>
install python 2.7<br>
run "pip install -r requirements.txt" in repo folder<br>
run "python main.py"in console<br>
<br>
OPTIONAL: set beebole as linux bash alias<br>
<br>
create or open ~/.bash_aliases<br>
add this row<br>
<pre>
#!/usr/bin/env bash

#beebole shortcut 
alias beebole='python ~/(path_to_your_repo_folder)/main.py "$@"'

shopt -s expand_aliases
beebole
</pre>
<br>
run "source ~/.bash_aliases<br>


<h3>Usage</h3>

if you set beebole as alias type "beebole ?" to view beebole help<br>
else run "python (path_to_folder)/main.py ?" to view beebole help<br><br>

<ul>
<li><b>?: </b> view beebole help</li>
<li><b>set_token: </b> set your api token and account name to authorize the application</li>
<li><b>List: </b> list all of your company in beebole</li>
<li><b>List -s (search string): </b> filter your beebole company</li>
</ul>
