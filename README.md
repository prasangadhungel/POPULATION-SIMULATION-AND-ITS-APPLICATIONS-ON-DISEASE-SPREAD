# POPULATION-SIMULATION-AND-ITS-APPLICATIONS-ON-DISEASE-SPREAD
Simulates the social interaction between humans at various places (home, schools, offices, hospitals, market, vehicles etc.) to predict and visualize the spread of a disease. 
Population related data are extracted from [CBS](https://cbs.gov.np/wp-content/upLoads/2018/12/25-Lalitpur_VDCLevelReport.pdf). Map related data (location of buildings, schools, hospitals ,roads) are obtained from [Open-Street-Map](www.openstreetmap.org). We allocate different parameters like age, sex, education status, schools, office destination to individual population based on statistical central measures.

### Requirements
1. pandas (python)
2. GL/GLUT (c++)

### How to run?
#### For simulation:
`python world.py`

#### For visualization:
`g++ visualize.cpp -o visualize -lglut -lGLU -lGL ; ./visualize`

### Demo
![](https://github.com/PrasangaDhungel/POPULATION-SIMULATION-AND-ITS-APPLICATIONS-ON-DISEASE-SPREAD/blob/master/demo.gif)

### Authors
[Prasanga Dhungel](https://github.com/PrasangaDhungel)<br/>
[Paridhi Parajuli](https://github.com/paridhi-parajuli)<br/>
[Sandesh Bhusal](https://github.com/sandeshbhusal)<br/>
[Sobit Neupane](https://github.com/sobitneupane)<br/>
