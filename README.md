Crypto Trading Bot
Collaborators: Trevor McGlaflin and Qin Quan Lin

The Goal 
The goal of this project is to create a crypto trading bot that places
automatic buy and sell orders through coinbase API. It will be a very short
term trading strategy that uses candlesticks and volumes, as well as trend
indicators like 20MA and RSI to signal good times to place orders. 

To run:
1. create a coinbase api sandbox account (https://public.sandbox.pro.coinbase.com/)
2. generate API keys by clicking your name in upper right corner -> API -> add new API key
3. create a constants.py file that will store the public key, secret key and passphrase
4. use these credentials to create an authenticated client
5. run the script `python3 trading_bot.py`


We will utilize a python library called TA-lib which can only be run inside of 
a jupyter notebook unfortunately. This is a huge pain in the ass, but if you follow
these instructions you should be good to go.


How to get the jupyter lab going with TA-lib:
1. install anaconda through this link https://www.anaconda.com/products/individual
2. once anaconda is installed you can get to the anaconda prompt by searching
"anaconda prompt" in the search bar. It will look something like this (base) `C:\Users\tmcgl>`
   
3. run `python update python` in anaconda prompt
4. look up how many bits your operating system is by going to your files -> right clicking
this pc -> click properties -> look at system type. (mine is 64 bit)
   
5. figure out which python version you have installed by running `python --version`
6. navigate to this link https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
7. find the proper ta-lib link to install based on your python version and operating system.
For instance, I have python version 3.8 and a windows 64 bit OS so i click on 
   TA_Lib‑0.4.20‑cp38‑cp38‑win_amd64.whl
   
8. you will see that this file has been saved so downloads
9. Create a new folder in your `C:Users` directory called `hp`
10. copy the file you downloaded from Downloads into the new hp folder
11. now, navigate to the hp folder in anaconda prompt. `cd ../` then `cd hp`
12. once in the hp folder run the following command `pip install TA_Lib‑0.4.20‑cp38‑cp38‑win_amd64.whl`
note: if you don't have same python version or OS as me this will be whatever the link
    of the file you downloaded is
    
13. click `y` if you are prompted
14. nice, you have successfully configured TA-lib, now lets get jupyter notebook going
15. get out of the hp folder and go back to whatever folder you were in before
mine is C:Users/tmcgl
    
16. run this `conda install -c conda-forge notebook`
17. run this `conda install -c conda-forge nb_conda_kernels`
    
18. run this `jupyter notebook` to open your jupyter notebook
19. now to test that TA-lib is installed properly create a blank notebook
by clicking `new` -> `python3` then run import talib. If no errors popup you are good.
    





