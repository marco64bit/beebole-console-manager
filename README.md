# beebole-console-manager <b>V1.0.0</b>
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
<li><b>set-token (token) (account_name)</b> 
	'set beebole token to authentication'

<li><b>add (alias_name) (project id) (task_id) (comment_optional)</b> 
  	'add alias to set with alias_name the current project'</li>

<li><b>set (project_alias)</b> 
	'set your current work to a project'</li>

<li><b>set-date (start-date) (finish-date)</b> 
	'set your work date range hh:mm'</li>
	
<li><b>current </b> 
  'get current project'</li>

<li><b>list _aliases</b> 
  	'all aliases set with beebole add'</li>

<li><b>list     </b> 
    'return list of all companies'</li>

<li><b>list -s (string)  </b> 
    'search in all companies'</li>

<li><b>? </b> 
    'help'</li>
</ul>

