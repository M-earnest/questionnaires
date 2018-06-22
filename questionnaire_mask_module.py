from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                            STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
               sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
reload(sys)
# provides utf8 support for user input
sys.setdefaultencoding('utf8')


''' module to create self updating questionaire which repeats ans marks uanswered questions deemed necessary'''




def update(list_,list_1,firsttrial,check):
    ''' function to prompt questions on the first run, input and store already answered values on repeating runs and repeat and mark questions if necessary'''
    # function to display Dialogue
    # assign gui to variable and define title

    if check ==0:
        # title of gui
        myDlg = gui.Dlg(title="Screening-Fragebogen")
        # fixed text e.g. headline
        myDlg.addText('\nSubject info')
        # questions with fixed answer format
        myDlg.addField(u'Example one:',choices=['Y','N'],initial=list_[0])
        myDlg.addField('gender:',choices=['male','female','other'],initial=list_[1])

        # check if questions are unanswered - or define other condition
        if not list_[2] == '' or firsttrial==0:
            # when string not empty or first run - assign answer to question, if already provided
            myDlg.addField('Age:',initial=list_[2])
            # mark question red, if second run and question unanswered
        else:
            myDlg.addField('Age:',initial=list_[2], color='red')

        if not list_[3] == ''or firsttrial==0:
            myDlg.addField('Date of Birth:',initial=list_[3])
        else:
            myDlg.addField('Date of Birth:',initial=list_[3],color='red')

        if not list_[4] == ''or firsttrial==0:
            myDlg.addField('Degree:',initial=list_[4])
        else:
            myDlg.addField('Degree:',initial=list_[4],color='red')


        # show dialogue, save in variable and return to main func
        myDlg.show()
        myDlg = myDlg.data
        return myDlg,list_1,


    # only true when gui one is complete
    elif check ==1:
        print(firsttrial)
        myDlg1 = gui.Dlg(title="Screening-Fragebogen")
        myDlg1.addText(u'\n cardiovascualr diseases')
        myDlg1.addField('Diabetus:', choices=['Y','N'],initial=list_1[0])
        myDlg1.addField(u'high blood pressure:', choices=['Y','N'],initial=list_1[1])

        # more complex example
        myDlg1.addField('coronary:',choices= ['Y','N'],initial=list_1[2])
        # if firsttrial empty display question : age at coronary
        if firsttrial==0:
            myDlg1.addField(u'age at coronary?:',initial=list_1[3])
        # if coronary = Y and no age given - rerun gui and underline question for age red
        elif list_1[2] == 'Y' and list_1[3] == '' and firsttrial==1:
            myDlg1.addField('age at coronary:',initial=list_1[3], color='red')
        # if coronary = N and gui is repeated add already provided answers, necessary if other questions are responsible for repetition
        elif list_1[2] == 'N'  and firsttrial==1:
            myDlg1.addField('age at coronary?:',initial=list_1[3])
        # if coronary = Y and question for age answered add alraedy provided answer on repetition
        elif list_1[2] == 'Y' and not list_1[3]=='' and firsttrial==1:
            myDlg1.addField('age at coronary?:',initial=list_1[3])

        # show dialogue, save in variable and return to main func
        myDlg1.show()
        myDlg1 = myDlg1.data
        return list_,myDlg1



def check_values(list_,list_1,check):
    # function to check status of question
    # remains zero if empty stings remain after firt run and input was necssary
    if check ==0:
        if list_[2] == '' or list_[2] == 'Y':
            return 0
        elif list_[3] == ''or list_[3] == 'Y':
            return 0
        elif list_[4] == ''or list_[4] == 'Y':
            return 0
    # return 1 when run was complete
        else:
            return 1

    # check for second window
    elif check==1:
        # if question 3 is answered with yes and question 4 is empty return 1
        if list_1[2] == 'Y' and  list_1[3] == '':
            return 1
    #    elif list_1[x] == 'Y' and list_1[x] == '':
    #        return 1
        else:
            return 2

def savecsv(list_,list_1,filename,num_items,num_items_1):
    ''' function to add data to experiment handler and save as csv'''
    # specify number of column names, e.g questions
    keys = [''] * num_items
    keys1 = ['']*num_items_1

    # specify column name for each question
    keys[0] = 'exampe one '
    keys[1] = 'sex'
    keys[2] = 'age'
    keys[3] = 'date of birth'
    keys[4] = 'degree'

    keys1[0] = 'diabetus'
    keys1[1] = 'high blodd pressure'
    keys1[2] = 'coronary'
    keys1[3] = 'age at coronary'


    #add column names to csv
    # open new csv with filename as name and write access
    file_open = open(filename + '.csv','w')
    # write column names to csv for number of column names
    # column names gui 1
    for i in range(num_items):
        file_open.write(keys[i]+',')

    # column names gui 2
    for i in range(num_items_1):
        if i == num_items_1-1:
            file_open.write(keys1[i])
        else:
            file_open.write(keys1[i]+',')
    # line break
    file_open.write('\n')

    #add data to csv - same procedure
    for i in range(len(list_)):
            # replace commata provided by participant with ':', breaks format otherwise
            list_[i] = list_[i].replace(',',':')
            file_open.write(list_[i]+',')

    for i in range(len(list_1)):
            list_1[i] = list_1[i].replace(',',':')
            file_open.write(list_1[i]+',')


def questionaire_func():
    ''' main function - creates exp handler and info and contains while loop to check over questionaire'''
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
    os.chdir(_thisDir)
    expName = u'Screening' # provide experiment name
    # create dictionary that takes necessary info, eg. participant, session, where to save to etc.
    expInfo = {'participant':'', 'session':'001','directory':''}
    dlg = gui.DlgFromDict(dictionary=expInfo, title='questionaire')
    if dlg.OK == False:
        core.quit()
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    save_path = expInfo['directory']
    print(save_path)

    filename =save_path + os.sep + u'%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])


# An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=None,
        savePickle=True, saveWideText=True,
        dataFileName=filename)
# save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file


    # create list  of empty strings to store data and help determine status of question - defined by number of questions
    num_items = 5
    list_ = [''] * num_items
    print list_

    num_items_1 = 4
    list_1 = [''] * num_items_1
    print list_1
    # create variable which ensures that the first run of the test has no questions marked as unanswered
    firsttrial=0
    # create variable to check if question has been answered
    check = 0

    # displays inital questions, checks for incomplete answers and repeats questions if necessary
    while check <2:
        # display questions
        temp_Dlg = update (list_,list_1,firsttrial,check)
        # provide temp check variable to compare to
        temp_check = check
        # print temp check to output e.g. 0 for gui and 1 for gui 2 etc.
        print(temp_check)
        # calls check function and returns check value
        check = check_values(temp_Dlg[0],temp_Dlg[1],check)
        # print check - allows comparision with temp check directly in psychopy output
        print(check)
        # compare check values before and after check function and assign either 1 or 0 tp trial number
        if temp_check == check:
            firsttrial=1
        else:
            firsttrial=0
        # write temporary answers to actual lists and return
        list_ = temp_Dlg[0]
        list_1= temp_Dlg[1]



    # save values in csv
    savecsv(list_,list_1,filename, num_items, num_items_1)


    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit

questionaire_func()
