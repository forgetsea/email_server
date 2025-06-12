"# My Project" 
1. Install python
from official websites https://www.python.org/downloads/

2. find a directory
eg: C:\Documents\project

3. open terminal
	a. press `win` + `R` 
	b. type `cmd`
	you will find new terminal open

4. in terminal create python virtual env 
	a. go to directory 
	b. create python virtual environment
	c. go to environment dirctory
	eg: 
	```
	cd C:\Documents\project
	py -m venv email
	cd email
	```

5. start python virtual env
	```
	Scripts\activate
	pip install -r requirements.txt
	```

--------------------------------------------
run scripts

start python virtual env in dictory, execute files

```
cd C:\Documents\project\email
Scripts\activate
python 
```

---------------------------------------------
Image upload

upload to forgetsea/assets
image link(cloudflare cdn): https://assets-42h.pages.dev/


---------------------------------------------
How to send a new topic
1.update email info in src/config.py
2.Create a new template html file in templates/
3.reset files/ , put new excel file in files/