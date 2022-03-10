# CE601 Dsycalculia Project

In this project I have created a small mini game that could be used inside of the bigger game that will be created to help diagnose and train children with dyscalculia.

## Technology used

Python version 3.6 

Unity Version 2020.1.9f1 client located here: https://gitlab.com/dyscalculia-project/client

MySQL server version 5.7.32 port 3306

Use with any other versions may lead to issues.

## Instructions to load and start the server locally

1. Download or clone the git repository onto your local machine wherever you would like
2. Start MySQL server and run schema.sql to add all the needed tables to the database
3. Run server.py and the server should start on port 65432


### All installed python libaries

Pillow	8.1.0

PySimpleGUI	4.34.0

cycler	0.10.0	

kiwisolver	1.3.1

matplotlib	3.3.3

mysql-connector	2.2.9

numpy	1.19.4

pip	21.0.1

pyparsing	2.4.7

python-dateutil	2.8.1

setuptools	50.3.2

six	1.15.0

websockets	8.1

## Database

The server should be MySQL 5.7 and be running on port 3306 but this can be changed in server.py if you wish. To build all the tables you require run schema.sql, if you need to reset your tables run clean.sql.

Once these tables are created data should be inserted as a player completes a batch of trials on the client. This can be viewed using your chosen method of accessing your sql server

## Mini-Game Client

Developed inside Unity found here: https://gitlab.com/dyscalculia-project/client

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

The Python server starts up a server socket and listens for connections on localhost port 65432.

For each new connection an instance of ClientHandler is created on a new thread to handle the connection.

Pythons own random class is used to create the parameters for the trials which are currently uncorrolated. 

All imports used are from within Python 3.6 so no third party packages are currently required to run.

## Communication Protocol

### Client To Server

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


