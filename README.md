# SpaceBulletins
A script to scrape your spacehey bulletins and save them before they expire.

## What it does?
Well the bio says almost it all, when you open the "main.py" it will save yours (or a friend's) currently posted bulletins into your machine. 

## How it works?
### Configurating The App.
The first thing you'll need to do is put your login information into the .env file. This is necesseary because only your friends can see your bulletins, so the program will login into your account and save the bulletins from the desired target. Also, I need to say that **I absolutely don't have access to that information**, and you can check the code to confirm that. <br> <br>

After you put your login info, you'll need to put the target id, i.e. who you'll save the bulleints from, and you can change that value before opening the main.py if you want to save bulletins from a different person. <br>
To get that value just go to the person's bulletins page and copy the id on the url, like the image below <br>
![url of the spacehey site, with a red line under the number after "id="](https://github.com/CaioEmPessoa/SpaceBulletins/assets/127911795/768fdbe9-1365-4a55-a468-d52b229fbc96)


### Viewing the Bulletins
After you ran the program without errors, the bulletins should be on the "bulletins" foulder of the app, but you can easily access them on the "index.html" page on the root of the app too. They will appear like this:
|Index Page|Bulletin Opened|
| - | - |
| ![image](https://github.com/CaioEmPessoa/SpaceBulletins/assets/127911795/47855006-ea26-4df2-96b1-2d50a85060f2) | ![image](https://github.com/CaioEmPessoa/SpaceBulletins/assets/127911795/f119151e-5881-4fcb-8d3f-be2e12244fdb) |

### Tip:
If you don't want to open the program all the time after you post a bulletins, you could make that it runs every time you start the computer, so it checks if you have new bulletins posted or not. Its not a heavy app so it shouldn't affect your performance.
