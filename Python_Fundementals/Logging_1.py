import logging

// Part 1 : logging levels

"""
notset 0
debug 10
info 20
warning 30
error 40
critical 50
default : 30 // so it willl ebcnahged to 20 thansk to setlevel 

"""

#changing the level of filtering of the default 
logging.getLogger().setLevel(logging.INFO)

logging.info('this is a info')
logging.warning('this is a warninng')

//part 2 : chaneg the typical format of a logger 


logging.basicConfig(format='')




