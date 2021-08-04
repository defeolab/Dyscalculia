# CE601 Dsycalculia Project

In this project I have created a small mini game that could be used inside of the bigger game that will be created to help diagnose and train children with dyscalculia.

## Technology used

Python version 3.6 server located here: https://gitlab.com/dyscalculia-project/server

Unity Version 2020.1.9f1

MySQL server version 5.7.32

Uses C# JSON libary: https://www.newtonsoft.com/json

Use with any other versions may lead to issues.


## Instructions to load and start the client

1. Download or clone the git repository onto your local machine wherever you would like
2. Open up the unity hub (or download this if you haven't already) on the left hand side you should see "Installs" in here make sure you have 2020.1.9f1 if you don't press the add button and find this version you should be able to download it. 
3. Once you have the version go back to the "Projects" on the left hand side of the unity hub and press the add button, find where you downloaded the code and click all the way through the folders until you see one called "Chicken Mini-Game" and the select this folder and press the "Select Folder" button. 
4. Once that is done you should see a project in your unity hub called "Chicken Mini-Game" then click this to open.
5. This should open the unity editor and you may get some errors the first time you open it if this does happen close unity and reopen the project. If you get an error about failure to load the window layout please try to load the default layout this will have no effect over the game.
6. Once the project opens with no errors you will probably still see nothing on screen. To add everything to the screen click file in the top left -> open scene -> Scenes then click the one scene that should be there. 
7. Then last but not least press the play button and the game should play locally without hitting the server. Please go to step 8 if you wish for it to hit the local Python server.
8. Click on the game object called "GameManager" Then on the right hand side you should see some options one is called "Demo Mode" and then just untick the box next to it for the game to hit the server rather than play locally.

## Mini-Game Client

Developed inside Unity.

All art for the chicken is attributed to Daniel Eddeland at https://opengameart.org/content/lpc-style-farm-animals

Tutorials used for movement in unity: 
 - https://www.youtube.com/watch?v=whzomFgjT50&ab_channel=Brackeys
 - https://www.youtube.com/watch?v=ExRQAEm4jPg&ab_channel=AlexanderZotov
 
The aim of the game is to select the correct area which contains the highest number of chickens.

The number of chickens in each area and which area will have the larger sized chickens is random so that the test can be repeated as often as neceassary and the answer changes.

Initially the buttons are disbaled but once the chickens reach their starting positions they will then be enabled.

Once a choice has been made the text will change to display to the player if they are correct or not. This result will also be added to the players scores and shown at the top of the screen.

After a few seconds pause the game is then reset and the player can play again with the scores carrying over from the previous game.

There is also a import and export button which will either export all current upcoming trails to json or it will import all trials from a file to be the upcoming trials.

The import file should be called [trials.json](https://cseegit.essex.ac.uk/2020_ce601/ce601_hurn_fletcher_c/-/blob/master/Unity/CE601%20Project/Chicken%20Mini-Game/trails.json).

## Python Server

Located here: https://gitlab.com/dyscalculia-project/server

The Python server starts up a server socket and listens for connections on localhost port 65432.

For each new connection an instance of ClientHandler is created on a new thread to handle the connection.

Pythons own random class is used to create the parameters for the trials which are currently uncorrolated. 

All imports used are from within Python 3.6 so no third party packages are currently required to run.

## Communication Protocol

### Cleint To Server

> #### Requesting one Trial 
>
> Request of type string - "TRIAL"
>
> #### Requesting a batch of Trials
> 
> Request of type string - "TRAILS:{Number Of Trials}"  
>
> **Number Of Trials** should be a whole integer greater than 1
>
> #### Sending Results Back To Server
>
> Request of type string - "COMPLETE:{Results}"  
>
> **Results** should be a json string of the following format  
>
> {"results": [{"DecisionTime": 5, "Correct": "false"}, {"DecisionTime": 2, "Correct": "true"}]}  
>
> DecisionTime should be of type double and Correct should be a string of either true or false.  

### Server To Client

On connection there is no extra message between client and server until the client requests something.

> #### Response To Client Requesting One Trial 
> 
> Response of type string in the following json format:  
>  
> {"circleRadius": 5.1, "sizeOfChicken": 1.2, "averageSpaceBetween": 2.2, "ratio": 1.4}  
>  
> All values should be of type double
>
> #### Response To Client Requesting A Batch Of Trials
> 
> Response of type string in the following json format:  
>  
> [{"circleRadius": 5.1, "sizeOfChicken": 1.2, "averageSpaceBetween": 2.2, "ratio": 1.4}, {"circleRadius": 4.5, "sizeOfChicken": 0.9, "averageSpaceBetween": 1.8, "ratio": 1.1}, ...] 
>  
> All values should be of type double
>
> #### Response to Client Sending Results Back To Server
>
> If Results can be processed by the server correctly then it will return the below, if not it will return nothing.
>
> Request of type string - "SUCCESS"  
> 


