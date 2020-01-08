#include<bits/stdc++.h>
#include <GL/glut.h>
using namespace std;

float screenwidth = 1300.0;
float screenheight = 700.0;
float mapwidth = 800;
float mapheight = 550;
float graphwidth = 300.0;
float graphheight = 200.0;
int numOfIteration = 5;
int iteration = 1; 
int steps = 1;
int pause = 0;
int numOfTimeSteps = 160;
map<unsigned int, pair<double, double> > mapNodes;
map<unsigned int, pair<double, double> > roadNodes;
map<unsigned int, vector<unsigned int> > maps;
map<unsigned int, vector<unsigned int> > roads;

void putPixel(float a, float b){
    glVertex2i(a+30,b+30);
}

void loadMapNodes(){
    ifstream fp("real_input/MapNodesKoniyosom.csv");
    string str, token;
    getline(fp, str);
    
    while(getline(fp, str)){
        std::stringstream ss(str);
        vector<string> strList;
        while (std::getline(ss, token, ',')){
            strList.push_back(token);
        }
        mapNodes[atoi(strList[0].c_str())] = make_pair(atof(strList[1].c_str()) * mapwidth/1000.0,atof(strList[2].c_str())* mapheight/1000.0);
    }
}

void loadRoadNodes(){
    ifstream fp("real_input/RoadNodes.csv");
    string str, token;
    getline(fp, str);
    
    while(getline(fp, str)){
        std::stringstream ss(str);
        vector<string> strList;
        while (std::getline(ss, token, ',')){
            strList.push_back(token);
        }
        roadNodes[atoi(strList[0].c_str())] = make_pair(atof(strList[1].c_str()) * mapwidth/1000.0,atof(strList[2].c_str()) * mapheight/1000.0);
    }
}


void loadMap(){
    ifstream fp("real_input/MapsKoniyosom.csv");
    string str, token;
    getline(fp, str);
    while(getline(fp, str)){
        while(1){
            auto it = find(str.begin(), str.end(), '"');
            if(it != str.end()){
                str.erase(it);
            }
            else break;
        }
        auto it1 = find(str.begin(), str.end(), '[');
        if(it1 != str.end())
            str.erase(it1);
        
        it1 = find(str.begin(), str.end(), ']');
        if(it1 != str.end())
            str.erase(it1);
        
        stringstream ss(str);
        vector<unsigned int> ids;
        std::getline(ss, token, ',');
        unsigned int id = atoi(token.c_str());
        while (std::getline(ss, token, ',')){
            ids.push_back(atoi(token.c_str()));
        }
        maps[id] = ids;
    }
}

void loadRoad(){
    ifstream fp("real_input/Roads.csv");
    string str, token;
    getline(fp, str);
    while(getline(fp, str)){
        while(1){
            auto it = find(str.begin(), str.end(), '"');
            if(it != str.end()){
                str.erase(it);
            }
            else break;
        }
        auto it1 = find(str.begin(), str.end(), '[');
        if(it1 != str.end())
            str.erase(it1);
        
        it1 = find(str.begin(), str.end(), ']');
        if(it1 != str.end())
            str.erase(it1);
        
        stringstream ss(str);
        vector<unsigned int> ids;
        std::getline(ss, token, ',');
        unsigned int id = atoi(token.c_str());
        while (std::getline(ss, token, ',')){
            ids.push_back(atoi(token.c_str()));
        }
        roads[id] = ids;
    }
}
void parseVehicleJson(){
    ifstream fp("logs/iteration_count"+to_string(iteration) +"/time_steps" + to_string(steps)+".json");
    string str, token;
    getline(fp, str);
    str.replace(0, str.find(']') + 1, "");
    glBegin(GL_POINTS);
    auto first = str.find('[');
    string HumanStr = str.substr(first, str.find(']') - first);
    while(1){
        auto it = HumanStr.find('{');
        if(it <= HumanStr.end() - HumanStr.begin()){
            auto last = HumanStr.find('}');
            string dictionary = HumanStr.substr(it + 1, last - it - 1);
            HumanStr.replace(0, last + 1, "");
            std::stringstream ss(dictionary);
            vector<string> strList;
            while (std::getline(ss, token, ' ')){
                strList.push_back(token);
            }
            glColor3f(0.5, 0.0, 1.0);
            glPointSize(5);
            putPixel(atof(strList[1].c_str())  * mapwidth/1000.0, atof(strList[3].c_str()) * mapheight/1000.0);
        }
        else{
            break;        
        }
    }
    glEnd();
}

void parseUninfectedJson(){
    ifstream fp("logs/iteration_count"+to_string(iteration) +"/time_steps" + to_string(steps)+".json");
    string str, token;
    getline(fp, str);
    glBegin(GL_POINTS);
    auto first = str.find('[');
    string HumanStr = str.substr(first, str.find(']') - first);
    while(1){
        auto it = HumanStr.find('{');
        if(it <= HumanStr.end() - HumanStr.begin()){
            auto last = HumanStr.find('}');
            string dictionary = HumanStr.substr(it + 1, last - it - 1);
            HumanStr.replace(0, last + 1, "");
            std::stringstream ss(dictionary);
            vector<string> strList;
            while (std::getline(ss, token, ' ')){
                strList.push_back(token);
            }
            if(strList[1] == "false,"){
                glColor3f(0.0, 1.0, 0.0);
                glPointSize(5);
                putPixel(atof(strList[3].c_str())  * mapwidth/1000.0, atof(strList[5].c_str()) * mapheight/1000.0);
            }
        }
        else{
            break;        
        }
    }
    glEnd();
}

void parseInfectedJson(){
    ifstream fp("logs/iteration_count"+to_string(iteration) +"/time_steps" + to_string(steps)+".json");
    string str, token;
    getline(fp, str);
    glBegin(GL_POINTS);
    auto first = str.find('[');
    string HumanStr = str.substr(first, str.find(']') - first);
    while(1){
        auto it = HumanStr.find('{');
        if(it <= HumanStr.end() - HumanStr.begin()){
            auto last = HumanStr.find('}');
            string dictionary = HumanStr.substr(it + 1, last - it - 1);
            HumanStr.replace(0, last + 1, "");
            std::stringstream ss(dictionary);
            vector<string> strList;
            while (std::getline(ss, token, ' ')){
                strList.push_back(token);
            }
            if(strList[1] != "false,"){
                glColor3f(1.0, 0.0, 0);
                glPointSize(5);
                putPixel(atof(strList[3].c_str())  * mapwidth/1000.0, atof(strList[5].c_str()) * mapheight/1000.0);
            }
        }
        else{
            break;        
        }
    }
    glEnd();
}

void InitializeMap(){
    loadMapNodes();
    loadRoadNodes();
    loadMap();
    loadRoad();
}



void drawMap(){
    glLineWidth(4);
    glColor3f(0.0, 0.0, 1.0);
    for(auto x:maps){
        glBegin(GL_LINE_STRIP);
        for(auto y: x.second){
            putPixel(mapNodes[y].first, mapNodes[y].second);
        }
        glEnd();
    }
    glLineWidth(2);
    glColor3f(0.0, 0, 0);
    for(auto x:roads){
        glBegin(GL_LINE_STRIP);
        for(auto y: x.second){
            putPixel(roadNodes[y].first, roadNodes[y].second);
        }
        glEnd();
    }
}

int initWindow(int *argc, char **argv, int x, int y, int xsize, int ysize, const std::string &s){
    glutInit(argc, argv);
    glutInitDisplayMode(GLUT_RGB);
    glutInitWindowPosition(x,y);
    glutInitWindowSize(xsize,ysize);
    return glutCreateWindow(s.c_str());
}

void putpixel(int x, int y, float r, float g, float b){
    glColor3f(r, g, b);
    putPixel(x, y);
}

void exitWindow(){
    glEnd();
    glFlush();
    glutMainLoop();
}

void changeSize(int w, int h) {
    if (h == 0)
        h = 1;
    float ratio =  w * 1.0f / h;
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glViewport(0, 0, w, h);
    gluPerspective(45.0f, ratio, 0.1f, 100.0f);
    glMatrixMode(GL_MODELVIEW);
}

void processNormalKeys(unsigned char key, int x, int y) {
    if (key == 27)
        exit(0);
    if(key == ' '){
        pause = 1 - pause;
    }
}

void specialKeyFunction(int key, int x, int y) {
    if (key == GLUT_KEY_LEFT && steps > 1){
        steps -= 1;
    }
    else if ( key == GLUT_KEY_RIGHT && steps < numOfTimeSteps - 1) {
        steps += 1;
    }
    glutPostRedisplay();
}



void render(void){
    glClearColor(1.0, 1.0, 1.0, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0,screenwidth, 0,screenheight);
    drawMap();
    glPointSize(10);
    parseVehicleJson();
    glPointSize(4);
    parseUninfectedJson();
    glPointSize(6);
    parseInfectedJson();
    if (steps < numOfTimeSteps && !pause){
        steps += 1;
    }
    glFlush();
    glutSwapBuffers();
}

int main(int argc, char** argv) {
    InitializeMap();
    int mainWindow = initWindow(&argc, argv, 0,0,screenwidth,screenheight, "Simulation");
    // int subWindow = glutCreateSubWindow(mainWindow, 900,0, 100,100);
    glutReshapeFunc(changeSize);
    glutDisplayFunc(render);
    glutIdleFunc(render);
    glutKeyboardFunc(processNormalKeys);
    glutSpecialFunc(specialKeyFunction);
    int subWindow = glutCreateSubWindow(mainWindow, screenwidth - graphwidth + 20,0, graphwidth, graphheight);
    glutDisplayFunc(render);    
    // glutIdleFunc(render);
    glutMainLoop();
    return 0;
}