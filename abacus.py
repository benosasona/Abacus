############################################################
# $Date: 2020-04-14 19:42:52 EST (Tue, 14 April 2020) $
# $Author: Ben Osasona $ <ben.osasona@consultant.com>
# $Version: 1.0.0 $
#############################################################

"""
Description
===========

Abacus is a mental math training program. It is a GUI based program built on the kivy framework.

The program helps train on an arithmetic method based on abacus calculation principles.

I developed this program, in the middle of the covid pandemic, to help young children/adults train for
mental math during, and after, the lockdown.

This program is my way of helping kids out of school, in my own little way.


Features
========

This version of Abacus has a number of features. I will continue to add more feature; however, contributions
are welcome from the development community. The current features of the app are:

* Possibility to choose from 3 difficulty levels
* Possibility to set time limit
* Possiblity to set the number of questions to generate
* Allow users to operate in 2 modes. The app's abacus can be removed for mental math training, or the abacus can
  be used for calculations
* Ability to review and fix incorrect answers. The incorrect answers can only be viewed at the end of a set of questions.
  This is in a bid to reduce learned helplessness
"""


from kivy.app import App
from kivy.atlas import CoreImage
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.clock import Clock
import datetime
import math
import random
import threading
from kivy.core.window import Window
from json_settings import json_settings

Window.clearcolor = (1,1,1,1)
nodes = []
sumTotal = 0
#numq = 5
choice = ''
tm = 28800
level = 10

class Bead(Scatter):
    def __init__(self, id, value, x, y, **kwargs):
        super().__init__(**kwargs)
        self.position = [x, y]
        self.orig_pos = [x,y]
        self.value = value
        self.active = False
        self.uniqueID = id
        self.beadSep = 1
        self.beadHeight = 40
        self.beadPerLine = 5
        self.width = 33
        self.height = 14
        self.beadLines = 17
        self.beadPerLine = 5
        self.beadSep = 3
        with self.canvas:
            if self.uniqueID != 25 and self.uniqueID != 19 and self.uniqueID != 22 and self.uniqueID != 28 and self.uniqueID != 31:
                self.player = Rectangle(source='bead3.png', size=(self.width, self.height), pos=(self.position[0], self.position[1]))
            else:
                self.player = Rectangle(source='middle_bead2.png', size=(self.width, self.height),
                                        pos=(self.position[0], self.position[1]))


    def reset_position(self):
        self.player.pos = (self.orig_pos[0], self.orig_pos[1])

    def setActive(self,active):
        global sumTotal
        self.active = active
        if active:
            sumTotal += self.value
        else:
            sumTotal -= self.value
        print('ID: ', str(self.uniqueID), 'Total : ',str(sumTotal), 'Position: (',self.position[0],',', self.position[1],')')

    def getBeadPositionX(self, nodeID):
        return nodes[nodeID].position[0]

    def getBeadPositionY(self, nodeID):
        return nodes[nodeID].position[1]



    def on_touch_down(self, touch):
        #super().on_touch_down(touch)
        if self.collide_point(*touch.pos):
            if self.active:
                #total -= self.value
                self.setActive(False)
                self.reset_position()
                if 17 <= self.uniqueID <= 33:  # The second row
                    self.reset_position()
                    if nodes[self.uniqueID + 51].active:
                        nodes[self.uniqueID + 51].reset_position()
                        nodes[self.uniqueID + 51].setActive(False)
                    if nodes[self.uniqueID + 34].active:
                        nodes[self.uniqueID + 34].reset_position()
                        nodes[self.uniqueID + 34].setActive(False)
                    if nodes[self.uniqueID + 17].active:
                        nodes[self.uniqueID + 17].reset_position()
                        nodes[self.uniqueID + 17].setActive(False)
                if 34 <= self.uniqueID <= 50: #The third row
                    if nodes[self.uniqueID + 34].active:
                        nodes[self.uniqueID + 34].reset_position()
                        nodes[self.uniqueID + 34].setActive(False)
                    if nodes[self.uniqueID + 17].active:
                        nodes[self.uniqueID + 17].reset_position()
                        nodes[self.uniqueID + 17].setActive(False)
                if 51 <= self.uniqueID <= 67: #The fourth row
                    if nodes[self.uniqueID + 17].active:
                        nodes[self.uniqueID + 17].reset_position()
                        nodes[self.uniqueID + 17].setActive(False)
            else:
                #total += self.value
                self.setActive(True)
                if 0 <= self.uniqueID <= 16:  #This is the first row
                    self.player.pos = (10,0)
                if 17 <= self.uniqueID <= 33: #The second row
                    self.player.pos = (10,25)
                if 34 <= self.uniqueID <= 50: #The third row
                    if not nodes[self.uniqueID - 17].active:
                        nodes[self.uniqueID - 17].player.pos = (10,25)
                        nodes[self.uniqueID - 17].setActive(True)
                    self.player.pos = (10, 25)
                if 51 <= self.uniqueID <= 67: #The fourth row
                    if not nodes[self.uniqueID - 34].active:
                        nodes[self.uniqueID - 34].player.pos = (10, 25)
                        nodes[self.uniqueID - 34].setActive(True)
                    if not nodes[self.uniqueID - 17].active:
                        nodes[self.uniqueID - 17].player.pos = (10, 25)
                        nodes[self.uniqueID - 17].setActive(True)
                    self.player.pos = (10, 25)
                if 68 <= self.uniqueID <= 84: #The last row
                    if not nodes[self.uniqueID - 51].active:
                        nodes[self.uniqueID - 51].player.pos = (10, 25)
                        nodes[self.uniqueID - 51].setActive(True)
                    if not nodes[self.uniqueID - 34].active:
                        nodes[self.uniqueID - 34].player.pos = (10, 25)
                        nodes[self.uniqueID - 34].setActive(True)
                    if not nodes[self.uniqueID - 17].active:
                        nodes[self.uniqueID - 17].player.pos = (10, 25)
                        nodes[self.uniqueID - 17].setActive(True)
                    self.player.pos = (10, 25)
            return True

class Seperator(Widget):
    def __init__(self,x,y, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Rectangle(source = 'sep_3d2.png', pos=(x,y), size=(self.width,6))

class Questions(BoxLayout):
    def __init__(self,problems,**kwargs):
        super().__init__(**kwargs)
        self.index = 0
        self.num = 0
        self.wrong = []
        self.problems = problems
        self.orientation = 'vertical'
        self.qnum = Label(text='Questions', font_size=18, font_name='comic.ttf', bold=True, color=(0,0,1,1),halign='left')

        self.label1 = Label(text='', font_size=24, font_name='comic.ttf',color=(1,0,0,1),halign='center')
        self.label2 = Label(text='', font_size=24, font_name='comic.ttf', color=(1,0,0,1), halign='center')
        self.label3 = Label(text='', font_size=24, font_name='comic.ttf', color=(1,0,0,1), halign='center')
        self.label4 = Label(text='', font_size=24, font_name='comic.ttf', color=(1, 0, 0, 1), halign='center')

        self.add_widget(self.qnum)
        lbox = BoxLayout(orientation='vertical')
        lbox.size_hint=(1, 4.5)
        lbox.add_widget(self.label1)
        lbox.add_widget(self.label2)
        lbox.add_widget(self.label3)
        lbox.add_widget(self.label4)
        self.add_widget(lbox)
        self.bind(size=self.do_resize)
        with self.canvas.before:
            self.rect = Rectangle(pos=self.pos, size=self.size,source='whiteboard5.png')

    def do_resize(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start(self):
        print(self.problems)
        self.index = 0
        key_list = list(self.problems[self.index])
        print(key_list)
        print('Index: ',self.index)
        print('Question:',self.problems[self.index][key_list[0]])
        self.label1.text = self.problems[self.index][key_list[0]][0]
        self.label2.text = self.problems[self.index][key_list[0]][1]
        self.label3.text = self.problems[self.index][key_list[0]][2]
        print(self.label1,self.label2,self.label3)

        self.qnum.text = 'Question ' + key_list[0] + ':'
        #self.index += 1

    def next_question(self):
        self.index += 1
        key_list = list(self.problems[self.index])
        self.label1.text = self.problems[self.index][key_list[0]][0]
        self.label2.text = self.problems[self.index][key_list[0]][1]
        self.label3.text = self.problems[self.index][key_list[0]][2]

        self.qnum.text = 'Question ' + key_list[0] + ':'

    def prev_question(self):
        if self.index > 0:
            self.index -= 1
            key_list = list(self.problems[self.index])
            self.label1.text = self.problems[self.index][key_list[0]][0]
            self.label2.text = self.problems[self.index][key_list[0]][1]
            self.label3.text = self.problems[self.index][key_list[0]][2]

            self.qnum.text = 'Question ' + key_list[0] + ':'

    def check(self):
        global subTotal
        q = self.key_list(self.index)
        l = len(q)
        l += 1
        ans = q[l:]
        if subTotal != str(ans):
            self.wrong.append(self.index)
        self.next_question()

class Timer(BoxLayout):
    def __init__(self, set_time, **kwargs):
        super().__init__(**kwargs)
        self.modes = (
            '%I:%m:%S',
            '%H:%m:%S %P',
            '%S:',
        )
        self.time = set_time
        self.mode = 0
        self.orientation = 'vertical'
        self.button = Button(text='00:00', font_size=36, font_name='comic.ttf')
        self.add_widget(self.button)


        self.button.bind(on_press=self.tap)

    def tap(self):
        Clock.schedule_interval(self.timer, 0.01)

    def stop(self):
        Clock.unschedule(self.timer, 0.01)

    def timer(self,dt):
        self.time -= 1
        l_time = self.time
        mins = l_time // 3600
        l_time %= 3600
        secs = l_time // 60
        if secs < 10:
            secs = '0' + str(mins)
        else:
            secs = str(secs)
        lst = (str(mins),secs)
        self.button.text = ':'.join(lst)

class AbacusCtrl(GridLayout):
    def __init__(self, **kwargs):
        super(AbacusCtrl, self).__init__(**kwargs)
        self.cols = 17
        self.beadColor = "(133, 178, 255)"
        self.hooveredBeadColor = "(170, 215, 255)"
        self.hooveredElement = -1
        self.hooveredBead = -1
        self.id = 'My_Abacus'
        self.beadLines = 17
        self.beadPerLine = 5
        self.beadSep = 3
        self.beadHeight = 14
        self.beadSpacing = 0
        self.beadWidth = 33
        self.col_default_width = 33
        self.row_default_height = 35
        self.col_force_default = True
        self.row_force_default = True
        self.total_width = 0
        self.total_height = 0

        id = 0
        i = 1
        level = 1
        s = 0
        while i < self.beadPerLine + 1:
            lvalue_btm = 100000000
            j = 0
            while j < self.beadLines:
                if i == 1:
                    x = 10
                    y = 15
                    value = lvalue_btm * 5
                else:
                    x = 10
                    y = 10
                    value = lvalue_btm * 1
                bead = Bead(id, value, x, y)
                id += 1
                j += 1
                level += 1
                nodes.append(bead)
                lvalue_btm /= 10
            i += 1

        self.drawBeads()

    def getBeadsCount(self):
        return len(nodes)

    def getBeadPositionX(self, nodeID):
        return nodes[nodeID].position[0]

    def getBeadPositionY(self, nodeID):
        return nodes[nodeID].position[1]


    def drawBead(self, nodeID):
        print(nodeID, nodes[nodeID].position, 'Value: ',nodes[nodeID].value)
        self.add_widget(nodes[nodeID])

    def drawBeads(self):
        cnt = self.getBeadsCount()
        i = 0
        s = 0
        x = 10
        y = 160
        while i < cnt:
            if i == self.beadLines:
                self.total_width = self.beadLines * ((self.beadSep - 2) + self.beadWidth + self.beadSpacing)
                while s < self.beadLines:
                    sep = Seperator(x+self.beadSep, y)
                    self.add_widget(sep)
                    s += 1
                    x += 28
            self.drawBead(i)
            i += 1
        self.total_height = (self.beadPerLine + 2) * (y + self.beadHeight)
        self.total_height /= 3
        self.total_height -= (self.beadHeight + self.beadPerLine + (2 * self.beadSep))

class MainLayout(GridLayout):
    def __init__(self,defw,defh,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.col_default_width = defw
        self.row_default_height = defh
        self.col_force_default = True

class Abacus(BoxLayout):
    def __init__(self, w, h, **kwargs):
        super().__init__(**kwargs)
        '''
        with self.canvas.before:
            Rectangle(pos=self.pos, size=self.size)
            BorderImage(border=(1, 1, 1, 1),
                        source='frame.png')
        '''

class Ctrls():
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.startBtn = Button(background_normal='start.png',background_disabled_normal='start_disabled.png')
        self.startBtn.bind(on_press=self.start_test)
        self.pauseBtn = Button(background_normal='pause.png', background_disabled_normal='pause_disabled.png')
        self.pauseBtn.bind(on_press=self.stop_test)
        self.pauseBtn.disabled = True
        self.settingsBtn = (Button(text='Settings', font_size=24, font_name='comic.ttf', on_press=self.open_config))
        self.prevBtn = Button(background_normal='previous.png',background_disabled_normal='previous_disabled.png')
        self.prevBtn.bind(on_press=self.Previous)
        self.prevBtn.disabled = True
        self.nextBtn = Button(background_normal='next.png',background_disabled_normal='next_disabled.png')
        self.nextBtn.bind(on_press=self.Next)
        self.nextBtn.disabled = True
        self.timer = Timer(tm)
        self.numq = 20
        self.ans = TextInput(font_size=36, font_name='comic.ttf')
        self.stime = Label(text='')
        self.slider = Slider(min=1,max=108000)

        self.ans.input_type = 'number'
        self.ans.multiline = False

        i = 0
        x = 10
        y = 160
        s = 0

        # create the questions:
        self.createQuestions()

        #Create confirmation pop-up:
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='Are you done?', size_hint=(1, .5)))
        yesBtn = Button(text='Yes', size_hint=(1, .5), on_press=self.on_yes)
        noBtn = Button(text='No', size_hint=(1, .5), on_press=self.on_no)
        cancelBtn = Button(text='Cancel', size_hint=(1, .5), on_pressed=self.on_cancel)
        panel = BoxLayout(orientation='horizontal')
        panel.add_widget(yesBtn)
        panel.add_widget(noBtn)
        panel.add_widget(cancelBtn)
        content.add_widget(panel)

        self.confirm = Popup(
            title='Finish',
            content=content,
            size_hint=(None, None),
            size=(Window.width / 3, Window.height / 3),
            auto_dismiss=False,
        )

        self.result = Popup(
            title='Result',
            size_hint=(None, None),
            size=(Window.width / 3, Window.height / 3),
            auto_dismiss=False,
        )

    def set_focus(self,event):
        self.ans.focus = True

    def open_config(self,event):
        self.stop()
        App.get_running_app().open_settings()

    def on_review(self,event):
        self.result.dismiss()
        self.quiz.problems = self.quiz.wrong
        self.quiz.wrong = []
        self.start()

    def on_new(self,event):
        newq = self.newQuestions()
        print('New Questions: ',newq)
        self.quiz.problems = newq
        self.quiz.wrong = []
        self.start()
        self.result.dismiss()

    def on_close(self,event):
        quit()

    def newQuestions(self):
        quest = {}
        probs = []
        prob = []
        temp = ''
        oper = ['+', '-']
        ans = 0
        temp_ans = 0
        i = 0

        while i < self.numq:
            number_1 = random.randrange(1, level)
            number_2 = random.randrange(1, level)
            number_3 = random.randrange(1, level)
            operator = random.choice(oper)
            if operator == '-':
                temp_ans = number_1 - number_2
                if temp_ans < 0:
                    ans = number_1 + number_2
                    prob = [str(number_1), str(number_2)]
                else:
                    ans = number_1 - number_2
                    temp = '-' + str(number_2)
                    prob = [str(number_1), temp]
            else:
                ans = number_1 + number_2
                prob = [str(number_1), str(number_2)]
            operator = random.choice(oper)
            if operator == '-':
                temp_ans -= number_3
                if temp_ans < 0:
                    ans += number_3
                    prob.append(str(number_3))
                else:
                    ans -= number_3
                    temp = '-' + str(number_3)
                    prob.append(temp)
            else:
                ans += number_3
                prob.append(str(number_3))
            key = str(i + 1)
            quest[key] = prob
            quest['ans'] = ans
            quest['given_ans'] = None
            probs.append(quest)
            quest = {}
            i += 1
        return probs

    def createQuestions(self):
        quest = {}
        probs = []
        prob = []
        temp = ''
        oper = ['+', '-']
        ans = 0
        temp_ans = 0
        i = 0
        while i < self.numq:
            number_1 = random.randrange(1, level)
            number_2 = random.randrange(1, level)
            number_3 = random.randrange(1, level)
            operator = random.choice(oper)
            if operator == '-':
                temp_ans = number_1 - number_2
                if temp_ans < 0:
                    ans = number_1 + number_2
                    prob = [str(number_1), str(number_2)]
                else:
                    ans = number_1 - number_2
                    temp = '-' + str(number_2)
                    prob = [str(number_1), temp]
            else:
                ans = number_1 + number_2
                prob = [str(number_1), str(number_2)]
            operator = random.choice(oper)
            if operator == '-':
                temp_ans -= number_3
                if temp_ans < 0:
                    ans += number_3
                    prob.append(str(number_3))
                else:
                    ans -= number_3
                    temp = '-' + str(number_3)
                    prob.append(temp)
            else:
                ans += number_3
                prob.append(str(number_3))
            key = str(i + 1)
            quest[key] = prob
            quest['ans'] = ans
            quest['given_ans'] = None
            probs.append(quest)
            quest = {}
            i += 1
        print(probs)

        self.quiz = Questions(probs)


    def start_test(self,event):
        self.start()

    def start(self):
        self.startBtn.disabled = True
        if len(self.quiz.problems) == 1:
            #self.nextBtn.text = 'Finish'
            self.nextBtn.background_normal = 'finish.png'
        else:
            #self.nextBtn.text = 'Next'
            self.nextBtn.background_normal = 'next.png'
        self.pauseBtn.disabled = False
        self.nextBtn.disabled = False
        if self.quiz.index > 0:
            self.prevBtn.disabled = False
        self.timer.button.text = '00:00'
        self.quiz.start()
        self.ans.text = ''
        if self.quiz.problems[0]['given_ans'] != None:
            self.ans.text = str(self.quiz.problems[0]['given_ans'])
        self.timer.tap()
        Clock.schedule_once(self.set_focus, 0.2)

    def stop_test(self,event):
        self.stop()

    def stop(self):
        self.timer.stop()
        self.pauseBtn.disabled = True
        self.prevBtn.disabled = True
        self.nextBtn.disabled = True
        self.startBtn.disabled = False
        self.ResetAbacus()


    def finish(self):
        self.timer.stop()
        self.pauseBtn.disabled = True
        self.prevBtn.disabled = True
        self.nextBtn.disabled = True
        self.startBtn.disabled = False
        self.ResetAbacus()

    def on_value(self,instance,value):
        val = int(value)
        l_time = 0
        mins = val // 3600
        l_time %= 3600
        secs = l_time // 60
        #l_time %= 60
        #seconds = l_time

        '''
        val = int(value)
        mins = val // 60
        val %= 60
        secs = val
        value = ''
        '''
        if mins > 0:
            if secs == 0:
                value = str(mins) + ' minutes '
            else:
                value = str(mins) + ' minutes, ' + str(secs) + ' seconds'
        else:
            if secs > 1:
                value = str(secs) + ' seconds'
            else:
                value = str(secs) + ' second'
        self.stime.text = str(value)

    def on_scancel(self,event):
        self.settings.dismiss()

    def Previous(self,event):
        self.nextBtn.disabled = False
        self.nextBtn.background_normal = 'next.png'
        self.ResetAbacus()
        if self.quiz.index-1 == 0:
            self.prevBtn.disabled = True
            if self.quiz.problems[0]['given_ans'] != None:
                self.ans.text = str(self.quiz.problems[0]['given_ans'])
            else:
                self.quiz.problems[0]['given_ans'] = None
        else:
            if self.quiz.problems[self.quiz.index -1]['given_ans'] != None:
                self.ans.text = str(self.quiz.problems[self.quiz.index -1]['given_ans'])
            else:
                self.quiz.problems[0]['given_ans'] = None
        self.quiz.prev_question()
        Clock.schedule_once(self.set_focus, 0.2)

    def Next(self,event):
        global choice
        if self.nextBtn.background_normal != 'finish.png':
            self.prevBtn.disabled = False
            if self.quiz.index+1 >= len(self.quiz.problems)-1:
                self.nextBtn.background_normal = 'finish.png'
            else:
                self.nextBtn.background_normal = 'next.png'
            if self.ans.text != None and self.ans.text != '':
                self.quiz.problems[self.quiz.index]['given_ans'] = int(self.ans.text)
            if str(self.quiz.problems[self.quiz.index]['ans']) != self.ans.text:  #The given answer is wrong
                self.quiz.wrong.append(self.quiz.problems[self.quiz.index])
            else:
                if self.quiz.problems[self.quiz.index] in self.quiz.wrong:
                    self.quiz.wrong.remove(self.quiz.problems[self.quiz.index])
            self.ResetAbacus()
            self.quiz.next_question()
            if self.quiz.problems[self.quiz.index]['given_ans'] != None:
                self.ans.text = str(self.quiz.problems[self.quiz.index]['given_ans'])
            else:
                self.ans.text = ''
        else:  #End
            if self.ans.text != None and self.ans.text != '':
                self.quiz.problems[self.quiz.index]['given_ans'] = int(self.ans.text)
            if str(self.quiz.problems[self.quiz.index]['ans']) != self.ans.text:  #The given answer is wrong
                self.quiz.wrong.append(self.quiz.problems[self.quiz.index])
            else:
                if self.quiz.problems[self.quiz.index] in self.quiz.wrong:
                    self.quiz.wrong.remove(self.quiz.problems[self.quiz.index])

            self.confirm.open()
        Clock.schedule_once(self.set_focus,0.2)

    def on_yes(self,event):
        self.confirm.dismiss()
        self.finish()
        self.dispayResult()

    def on_no(self,event):
        self.confirm.dismiss()

    def on_cancel(self,event):
        self.confirm.dismiss()

    def ResetAbacus(self):
        i = 0
        while i < len(nodes):
            nodes[i].reset_position()
            i += 1

    def dispayResult(self):
        # Create pop up to display result:

        content = BoxLayout(orientation='vertical')
        w = len(self.quiz.wrong)
        c = len(self.quiz.problems) - w
        tcorrect = BoxLayout(orientation='horizontal')
        tcorrect.add_widget(Label(text='Number of Correct Answers: ', size_hint=(3.5, 1)))
        tcorrect.add_widget(Label(text=str(c), size_hint=(1, 1)))
        content.add_widget(tcorrect)


        twrong = BoxLayout(orientation='horizontal')
        twrong.add_widget(Label(text='Number of Wrong Answers: ', size_hint=(3.5, 1)))
        twrong.add_widget(Label(text=str(w), size_hint=(1, 1)))
        content.add_widget(twrong)
        reviewBtn = Button(text='Fix Mistakes', size_hint=(4, 1), on_press=self.on_review)
        if w == 0:
            reviewBtn.disabled = True
        newBtn = Button(text='New', size_hint=(2, 1), on_press=self.on_new)
        closeBtn = Button(text='Close App', size_hint=(4, 1), on_press=self.on_close)
        panel = BoxLayout(orientation='horizontal')
        panel.add_widget(reviewBtn)
        panel.add_widget(newBtn)
        panel.add_widget(closeBtn)
        content.add_widget(panel)

        self.result.content = content
        self.result.open()


class AbacusDisplay(App):
    icon = 'icon.png'
    title = 'Abacus'

    abcCtrl = AbacusCtrl()

    abcCtrl.padding = [0, 0, 0, 0]
    abcCtrl.width = abcCtrl.total_width
    abcCtrl.size_hint_x = None
    abcCtrl.bind(minimum_height=abcCtrl.setter('height'), minimum_width=abcCtrl.setter('width'))
    abacus = Abacus(abcCtrl.total_width,abcCtrl.total_height)
    abacus.add_widget(abcCtrl)

    main_layout = MainLayout(abcCtrl.total_width,abcCtrl.total_height)

    ctrl = Ctrls()
    ctrl.quiz.size_hint_x = None
    ctrl.quiz.width = abcCtrl.total_width / 2

    btns = GridLayout()
    btns.size_hint_x = None
    btns.width = abcCtrl.total_width / 2
    btns.size_hint_y = None
    btns.height = abcCtrl.total_height / 2
    btns.orientation = 'horizontal'
    btns.cols = 2
    btns.add_widget(ctrl.startBtn)
    btns.add_widget(ctrl.pauseBtn)
    btns.add_widget(ctrl.prevBtn)
    btns.add_widget(ctrl.nextBtn)
    btns.add_widget(Label(text='Answer:',color=(0,128/255,0,1),font_size=36, font_name='comic.ttf',halign='right' ))
    btns.add_widget(ctrl.ans)

    settings = BoxLayout()
    settings.orientation = 'horizontal'
    settings.size_hint_x = None
    settings.bind(minimum_height=settings.setter('height'), minimum_width=settings.setter('width'))
    settings.width = abcCtrl.total_width / 2

    settings.add_widget(ctrl.settingsBtn)

    ctrl.timer.size_hint_x = None
    ctrl.timer.width = abcCtrl.total_width / 2

    panel = GridLayout()
    panel.size_hint_x = None
    panel.width = abcCtrl.total_width / 2
    panel.cols = 1
    panel.add_widget(ctrl.timer)
    panel.add_widget(btns)
    panel.add_widget(settings)

    top = GridLayout()
    top.cols = 2
    top.add_widget(ctrl.quiz)
    top.add_widget(panel)

    main_layout.add_widget(top)

    main_layout.add_widget(abacus)

    ratio = abcCtrl.total_height / abcCtrl.total_width
    wh = abcCtrl.total_height // ratio

    Window.size = (abcCtrl.total_width,wh + 20)


    def build_config(self, config):
        config.setdefaults("General", {'time_limit':8,'level':1,'num_questions':20,'mode':1})

    def on_start(self):
        global tm, numq, level
        mode = self.config.get('General','mode')
        if int(mode) == 2:
            self.main_layout.remove_widget(self.abacus)
            self.abacus.parent = None
        tm = int(self.config.get('General','time_limit')) * 3600
        self.ctrl.timer.time = tm
        lv = int(self.config.get('General','level'))
        if lv < 1 or lv > 3:
            level = 10
        if lv == 1:
            level = 10
        if lv == 2:
            level = 15
        if lv == 3:
            level = 20
        numq = int(self.config.get('General','num_questions'))
        self.ctrl.numq = numq
        newq = self.ctrl.newQuestions()
        self.ctrl.quiz.problems = newq
    def build_settings(self, settings):
        settings.add_json_panel('Abacus',self.config,data=json_settings)

    def on_config_change(self, config, section, key, value):
        global tm, numq,level
        if key == 'mode':
            print(value)
            if int(value) == 2:
                self.main_layout.remove_widget(self.abacus)
                self.abacus.parent = None
            elif int(value) == 1:
                self.abacus.parent = None
                self.main_layout.add_widget(self.abacus)
        if key == 'time_limit':
            tm = int(value) * 3600
            print(tm)
            self.ctrl.timer.time = tm
        if key == 'level':
            lv = int(value)
            if lv < 1 or lv > 3:
                level = 10
            if lv == 1:
                level = 10
            if lv == 2:
                level = 15
            if lv == 3:
                level = 20

            newq = self.ctrl.newQuestions()
            self.ctrl.quiz.problems = newq
            self.ctrl.quiz.wrong = []
        if key == 'num_questions':
            self.ctrl.numq = int(value)
            numq = self.ctrl.numq
            newq = self.ctrl.newQuestions()
            self.ctrl.quiz.problems = newq
            self.ctrl.quiz.wrong = []

    def build(self):
        config = self.config
        return self.main_layout

if __name__ == '__main__':
    AbacusDisplay().run()
