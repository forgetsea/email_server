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
	py -m venv pubpro
	cd pubpro
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
cd C:\Documents\project\pubpro
Scripts\activate
python medpro.py
```

