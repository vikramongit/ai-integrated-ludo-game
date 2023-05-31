                                                        # Ludo game Integrated With AI #
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import time
from random import randint, choice
# 6949E8
class Ludo:
    def __init__(self, root,six_side_block,five_side_block,four_side_block,three_side_block,two_side_block,one_side_block):
        self.window = root
        # Make canvas
        self.make_canvas = Canvas(self.window, bg="#f5eded", width=800, height=630)
        self.make_canvas.pack(fill=BOTH,expand=1)

        # Make some containers to store data
        self.made_red_coin = []
        self.made_yellow_coin = []

        self.red_number_label = []
        self.yellow_number_label = []

        self.block_value_predict = []
        self.total_people_play = []

        # Ludo block all side image store
        self.block_number_side = [one_side_block, two_side_block, three_side_block, four_side_block, five_side_block, six_side_block]

        # Use for store specific position of all coins
        self.red_coord_store = [-1, -1, -1, -1]
        self.yellow_coord_store = [-1, -1, -1, -1]

        self.red_coin_position = [0, 1, 2, 3]
        self.yellow_coin_position = [0, 1, 2, 3]

        for index in range(len(self.red_coin_position)):# Specific coin position set to -1 by default
            self.red_coin_position[index] = -1
            self.yellow_coin_position[index] = -1

        # Number to room to be traverse by specific color coin, store in that variable
        self.move_red_counter = 0
        self.move_yellow_counter = 0

        self.take_permission = 0
        self.six_with_overlap = 0

        self.red_store_active = 0
        self.yellow_store_active = 0

        self.six_counter = 0
        self.time_for = -1

        # Some variables initializes with None
        self.right_star = None
        self.down_star = None
        self.left_star = None
        self.up_star = None

        # Robo Control
        self.robo_prem = 0
        self.count_robo_stage_from_start = 0
        self.robo_store = []
        self.red_hit=0
        self.yellow_hit=0

        # By default some function call
        self.board_set_up()

        self.instruction_btn_red()
        self.instruction_btn_yellow()

        self.take_initial_control()


    def board_set_up(self):
        # Cover Box made
        self.make_canvas.create_rectangle(100, 15, 100 + (40 * 15), 15 + (40 * 15), width=6, fill="white")

        # Square box
        
        self.img1= ImageTk.PhotoImage(Image.open("red.jpeg").resize((240, 240), Image.ANTIALIAS))
        self.make_canvas.create_image(100,15,anchor=NW,image=self.img1)
        # self.make_canvas.image= self.img1

        self.img2= ImageTk.PhotoImage(Image.open("blue.jpeg").resize((240, 240), Image.ANTIALIAS))
        self.make_canvas.create_image(100+240, (15+240)+(40*3)+240,anchor=SE,image=self.img2)
        # self.make_canvas.image= self.img2

        self.img3= ImageTk.PhotoImage(Image.open("green.jpeg").resize((240, 240), Image.ANTIALIAS))
        self.make_canvas.create_image(340+(40*3)+240, 15,anchor=NE,image=self.img3)
        self.make_canvas.image= self.img3

        self.img4= ImageTk.PhotoImage(Image.open("yellow.jpeg").resize((240, 240), Image.ANTIALIAS))
        self.make_canvas.create_image(340+(40*3)+240, (15+240)+(40*3)+240,anchor=SE,image=self.img4)
        self.make_canvas.image= self.img4
       
        # red 3 box(In white region)
        self.make_canvas.create_rectangle(100, (15+240), 100+240, (15+240)+40, width=3)
        self.make_canvas.create_rectangle(100+40, (15 + 240)+40, 100 + 240, (15 + 240) + 40+40, width=3, fill="#BA2921")
        self.make_canvas.create_rectangle(100, (15 + 240)+80, 100 + 240, (15 + 240) + 80+40, width=3)

        # green 3 box(In white region)
        self.make_canvas.create_rectangle(100+240, 15, 100 + 240+40, 15 + (40*6), width=3)
        self.make_canvas.create_rectangle(100+240+40, 15+40, 100+240+80, 15 + (40*6), width=3, fill="#41BF4E")
        self.make_canvas.create_rectangle(100+240+80, 15, 100 + 240+80+40, 15 + (40*6), width=3)

        # yellow 3 box(In white region)
        self.make_canvas.create_rectangle(340+(40*3), 15+240, 340+(40*3)+(40*6), 15+240+40, width=3)
        self.make_canvas.create_rectangle(340+(40*3), 15+240+40, 340+(40*3)+(40*6)-40, 15+240+80, width=3, fill="#EAAE2C")
        self.make_canvas.create_rectangle(340+(40*3), 15+240+80, 340+(40*3)+(40*6), 15+240+120, width=3)

        # sky 3 box(In white region)
        self.make_canvas.create_rectangle(100, (15 + 240)+(40*3), 100 + 240+40, (15 + 240)+(40*3)+(40*6), width=3)
        self.make_canvas.create_rectangle(100+240+40, (15 + 240)+(40*3), 100 + 240+40+40, (15 + 240)+(40*3)+(40*6)-40, width=3, fill="#2949E8")
        self.make_canvas.create_rectangle(100 + 240+40+40, (15 + 240)+(40*3), 100 + 240+40+40+40, (15 + 240)+(40*3)+(40*6), width=3)

        # All left separation line
        start_x = 100 + 40
        start_y = 15 + 240
        end_x = 100 + 40
        end_y = 15 + 240 + (40 * 3)
        for _ in range(5):
            self.make_canvas.create_line(start_x, start_y, end_x, end_y, width=3)
            start_x+=40
            end_x+= 40

        # All right separation line
        start_x = 100+240+(40*3)+40
        start_y = 15 + 240
        end_x = 100+240+(40*3)+40
        end_y = 15 + 240 + (40 * 3)
        for _ in range(5):
            self.make_canvas.create_line(start_x, start_y, end_x, end_y, width=3)
            start_x += 40
            end_x += 40

        # All up separation done
        start_x = 100+240
        start_y = 15+40
        end_x = 100+240+(40*3)
        end_y = 15+40
        for _ in range(5):
            self.make_canvas.create_line(start_x, start_y, end_x, end_y, width=3)
            start_y += 40
            end_y += 40

        # All down separation done
        start_x = 100 + 240
        start_y = 15 + (40*6)+(40*3)+40
        end_x = 100 + 240 + (40 * 3)
        end_y = 15 + (40*6)+(40*3)+40
        for _ in range(5):
            self.make_canvas.create_line(start_x, start_y, end_x, end_y, width=3)
            start_y += 40
            end_y += 40

       


        # Left up square inside box made
        self.make_canvas.create_oval(100+40+10, 15+40, 100+40+40+10, 15+40+40, width=0, fill="")
        self.make_canvas.create_rectangle(100+40+60+60, 15 + 40, 100+40+60+40+60, 15 + 40 + 40, width=0, fill="")
        self.make_canvas.create_rectangle(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=0, fill="")
        self.make_canvas.create_rectangle(100 + 40 + 60 + 60, 15 + 40+100, 100 + 40 + 60 + 40 +60, 15 + 40 + 40+100, width=0, fill="")
        
        # Right down square inside box made
        self.make_canvas.create_rectangle(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=0, fill="")
        self.make_canvas.create_rectangle(340 + (40 * 3) + 40 + 60 + 40+20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=0, fill="")
        self.make_canvas.create_rectangle(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=0, fill="")
        self.make_canvas.create_rectangle(340 + (40 * 3) + 40 + 60 + 40+20, 340+80+60+40+15,340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+60+40+40+15, width=0, fill="")

        # sky_blue start position
        self.make_canvas.create_rectangle(100+240,340+(40*5)-5,100+240+40,340+(40*6)-5,fill="#2949E8",width=3)
        # Red start position
        self.make_canvas.create_rectangle(100 + 40, 15+(40*6), 100 +40 + 40, 15+(40*6)+40, fill="#BA2921", width=3)
        # Green start position
        self.make_canvas.create_rectangle(100 + (40*8), 15 + 40, 100 +(40*9), 15 + 40+ 40, fill="#41BF4E", width=3)
        # Yellow start position
        self.make_canvas.create_rectangle(100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8), 100 + (40 * 6)+(40*3)+(40*5), 15 + (40*9), fill="#EAAE2C", width=3)

        # Traingle in middle
        self.make_canvas.create_polygon(100+240, 15+240, 100+240+60, 15+240+60, 100+240, 15+240+(40*3), width=3,fill="#BA2921",outline="black")
        self.make_canvas.create_polygon(100 + 240+(40*3), 15 + 240, 100 + 240 + 60, 15 + 240 + 60, 100 + 240+(40*3), 15 + 240 + (40 * 3), width=3, fill="#EAAE2C",outline="black")
        self.make_canvas.create_polygon(100 + 240, 15 + 240, 100 + 240 + 60, 15 + 240 + 60, 100 + 240 + (40 * 3), 15 + 240, width=3, fill="#41BF4E",outline="black")
        self.make_canvas.create_polygon(100 + 240, 15 + 240+(40*3), 100 + 240 + 60, 15 + 240 + 60, 100 + 240 + (40 * 3), 15 + 240+(40*3), width=3, fill="#2949E8",outline="black")

        # Make coin for red left up block
        red_1_coin = self.make_canvas.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="#BA2921", outline="#FFD0B4")
        red_2_coin = self.make_canvas.create_oval(100+40+60+60, 15 + 40, 100+40+60+60+40, 15 + 40 + 40, width=3, fill="#BA2921", outline="#FFD8B4")
        red_3_coin = self.make_canvas.create_oval(100 + 40 + 60 + 60, 15 + 40 + 100, 100 + 40 + 60 + 60 + 40, 15 + 40 + 40 + 100, width=3, fill="#BA2921", outline="#FFD0B4")
        red_4_coin = self.make_canvas.create_oval(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3,fill="#BA2921", outline="#FFD0B4")
        self.made_red_coin.append(red_1_coin)
        self.made_red_coin.append(red_2_coin)
        self.made_red_coin.append(red_3_coin)
        self.made_red_coin.append(red_4_coin)

        # Make coin under number label for red left up block
        red_1_label = Label(self.make_canvas, text="1", font=("Arial", 15, "bold"), bg="#BA2921", fg="black")
        red_1_label.place(x=100 + 40 + 10, y=15 + 40 + 5)
        red_2_label = Label(self.make_canvas, text="2", font=("Arial", 15, "bold"), bg="#BA2921", fg="black")
        red_2_label.place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 5)
        red_3_label = Label(self.make_canvas, text="3", font=("Arial", 15, "bold"), bg="#BA2921", fg="black")
        red_3_label.place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 100 + 5)
        red_4_label = Label(self.make_canvas, text="4", font=("Arial", 15, "bold"), bg="#BA2921", fg="black")
        red_4_label.place(x=100 + 40 + 10, y=15 + 40 + 100 + 5)
        self.red_number_label.append(red_1_label)
        self.red_number_label.append(red_2_label)
        self.red_number_label.append(red_3_label)
        self.red_number_label.append(red_4_label)

        # Make coin for yellow right down block
        yellow_1_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="#EAAE2C", outline="#F5DF4D")
        yellow_2_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#EAAE2C", outline="#F5DF4D")
        yellow_3_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="#EAAE2C", outline="#F5DF4D")
        yellow_4_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="#EAAE2C", outline="#F5DF4D")
        self.made_yellow_coin.append(yellow_1_coin)
        self.made_yellow_coin.append(yellow_2_coin)
        self.made_yellow_coin.append(yellow_3_coin)
        self.made_yellow_coin.append(yellow_4_coin)

        # Make coin under number label for yellow right down block
        yellow_1_label = Label(self.make_canvas, text="1", font=("Arial", 15, "bold"), bg="#EAAE2C", fg="black")
        yellow_1_label.place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        yellow_2_label = Label(self.make_canvas, text="2", font=("Arial", 15, "bold"), bg="#EAAE2C", fg="black")
        yellow_2_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        yellow_3_label = Label(self.make_canvas, text="3", font=("Arial", 15, "bold"), bg="#EAAE2C", fg="black")
        yellow_3_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
        yellow_4_label = Label(self.make_canvas, text="4", font=("Arial", 15, "bold"), bg="#EAAE2C", fg="black")
        yellow_4_label.place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
        self.yellow_number_label.append(yellow_1_label)
        self.yellow_number_label.append(yellow_2_label)
        self.yellow_number_label.append(yellow_3_label)
        self.yellow_number_label.append(yellow_4_label)


        
        #yellow star
        common_x = 340+(40*6)+20-22
        common_y = 15+240+2-5
        self.points = [common_x+5-2,common_y +20-2,common_x+20-2,common_y +20-2,common_x+25-2,common_y +5-2,common_x+30-2,common_y +20-2,common_x+45-2,common_y +20-2,common_x+32.5-2,common_y +30-2,common_x+37.5-2,common_y +45-2,common_x+25-2,common_y +35-2,common_x+12.5-2,common_y +45-2,common_x+17.7-2,common_y +30-2]
        self.make_canvas.create_polygon(self.points,fill="#EAAE2C",width=4)
        
       # green star
        common_x = 100+240+2+18-22
        common_y = 15 + (40*2) + 2-5
        self.points = [common_x+5-2,common_y +20-2,common_x+20-2,common_y +20-2,common_x+25-2,common_y +5-2,common_x+30-2,common_y +20-2,common_x+45-2,common_y +20-2,common_x+32.5-2,common_y +30-2,common_x+37.5-2,common_y +45-2,common_x+25-2,common_y +35-2,common_x+12.5-2,common_y +45-2,common_x+17.7-2,common_y +30-2]
        self.make_canvas.create_polygon(self.points,fill="#41BF4E",width=4)

        # red star
        common_x = 100 + (40*2) + 2 +18-22
        common_y = 15 + 240+(40*2) + 2-5
        self.points = [common_x+5-2,common_y +20-2,common_x+20-2,common_y +20-2,common_x+25-2,common_y +5-2,common_x+30-2,common_y +20-2,common_x+45-2,common_y +20-2,common_x+32.5-2,common_y +30-2,common_x+37.5-2,common_y +45-2,common_x+25-2,common_y +35-2,common_x+12.5-2,common_y +45-2,common_x+17.7-2,common_y +30-2]
        self.make_canvas.create_polygon(self.points,fill="#BA2921",width=4)

        # blue star
        common_x = 100 + 240 + (40*2) + 2 + 18-22
        common_y = 15 + (40 * 6) + (40*3)+(40*3)+2-5
        self.points = [common_x+5-2,common_y +20-2,common_x+20-2,common_y +20-2,common_x+25-2,common_y +5-2,common_x+30-2,common_y +20-2,common_x+45-2,common_y +20-2,common_x+32.5-2,common_y +30-2,common_x+37.5-2,common_y +45-2,common_x+25-2,common_y +35-2,common_x+12.5-2,common_y +45-2,common_x+17.7-2,common_y +30-2]
        self.make_canvas.create_polygon(self.points,fill="#2949E8",width=4)


    # Total number of players: Control take at first
    def take_initial_control(self):
        for i in range(2):
            self.block_value_predict[i][1]['state'] = DISABLED

        # Make other window to control take
        top = Toplevel()
        top.geometry("530x300")
        top.maxsize(530,300)
        top.minsize(530,300)
        top.config(bg="#FFFFFF")

        head = Label(top,text="           LUDO WITH AI",font=("Arial",25,"bold","italic"),bg="#FFFFFF",fg="black")
        head.place(x=50,y=30)

        def operate(ind):
            if ind:
                self.robo_prem = 1
                for player_index in range(2):
                    self.total_people_play.append(player_index)
                print(self.total_people_play)
               
                top.destroy()
                self.block_value_predict[1][1]['state'] = NORMAL
        
        mvc_btn = Button(top,text="  PLAY  ",bg="#000000",fg="#FFFFFF",font=("Arial",15,"bold"),relief=RAISED,bd=3,command=lambda: operate(1))
        mvc_btn.place(x=220,y=160)
        top.mainloop()

    # Get block value after Z based on probability
    def make_prediction(self,color_indicator):
        try:
            if color_indicator == "red":
                block_value_predict = self.block_value_predict[0]
                if self.robo_prem and self.count_robo_stage_from_start < 3:
                    self.count_robo_stage_from_start += 1
                if self.robo_prem and self.count_robo_stage_from_start == 3 and self.six_counter < 2:
                    permanent_block_number = self.move_red_counter = 6
                    self.count_robo_stage_from_start += 1
                else:    
                    permanent_block_number = self.move_red_counter = randint(1, 6)

            elif color_indicator == "yellow":
                block_value_predict = self.block_value_predict[1]
                permanent_block_number = self.move_yellow_counter = randint(1, 6)
                if self.robo_prem and permanent_block_number == 6:
                    for coin_loc in self.red_coin_position:
                        if coin_loc>=27 and coin_loc<=33:
                            permanent_block_number = self.move_yellow_counter = randint(1, 5)
                            break
                            
            block_value_predict[1]['state'] = DISABLED

            # Illusion of coin floating
            temp_counter = 12
            while temp_counter>0:
                move_temp_counter = randint(1, 6)
                block_value_predict[0]['image'] = self.block_number_side[move_temp_counter - 1]
                self.window.update()
                time.sleep(0.1)
                temp_counter-=1

            print("Prediction result: ", permanent_block_number)

            # Permanent predicted value containing image set
            block_value_predict[0]['image'] = self.block_number_side[permanent_block_number-1]
            if self.robo_prem == 1 and color_indicator == "red":
                self.window.update()
                time.sleep(0.4)
            self.instructional_btn_customization_based_on_current_situation(color_indicator,permanent_block_number,block_value_predict)
        except:
            print("Force Stop Error in Prediction")
        
    def instructional_btn_customization_based_on_current_situation(self,color_indicator,permanent_block_number,block_value_predict):
        robo_operator = None
        if color_indicator == "red":
            temp_coin_position = self.red_coin_position
        elif color_indicator == "yellow":
            temp_coin_position = self.yellow_coin_position

        all_in = 1
        for i in range(4):
            if temp_coin_position[i] == -1:
                all_in = 1
            else:
                all_in = 0
                break

        if  permanent_block_number == 6:
            self.six_counter += 1
        else:
            self.six_counter = 0

        if ((all_in == 1 and permanent_block_number == 6) or (all_in==0)) and self.six_counter<3:
            permission = 1
            if color_indicator == "red":
                temp = self.red_coord_store
            elif color_indicator == "yellow":
                temp = self.yellow_coord_store

            if  permanent_block_number<6:
                if self.six_with_overlap == 1:
                    self.time_for-=1
                    self.six_with_overlap=0
                for i in range(4):
                    if  temp[i] == -1:
                        permission=0
                    elif temp[i]>100:
                        if  temp[i]+permanent_block_number<=106:
                            permission=1
                            break
                        else:
                            permission=0
                    else:
                        permission=1
                        break
            else:
                for i in range(4):
                    if  temp[i]>100:
                        if  temp[i] + permanent_block_number <= 106:
                            permission = 1
                            break
                        else:
                            permission = 0
                    else:
                        permission = 1
                        break
            if permission == 0:
                self.make_command(None)
            else:
                self.num_btns_state_controller(block_value_predict[2])

                if self.robo_prem == 1 and block_value_predict == self.block_value_predict[0]:
                    robo_operator = "give"
                block_value_predict[1]['state'] = DISABLED# Predict btn deactivation

        else:
            block_value_predict[1]['state'] = NORMAL# Predict btn activation
            if self.six_with_overlap == 1:
                self.time_for -= 1
                self.six_with_overlap = 0
            self.make_command()

        if  permanent_block_number == 6 and self.six_counter<3 and block_value_predict[2][0]['state'] == NORMAL:
            self.time_for-=1
        else:
            self.six_counter=0

        if self.robo_prem == 1 and robo_operator:
            self.robo_judge(robo_operator)
            
    # Player Scope controller
    def make_command(self, robo_operator=None):
        if  self.time_for == -1:
            pass
        else:
            self.block_value_predict[self.total_people_play[self.time_for]][1]['state'] = DISABLED
        if  self.time_for == len(self.total_people_play)-1:
            self.time_for = -1

        self.time_for+=1
        self.block_value_predict[self.total_people_play[self.time_for]][1]['state'] = NORMAL
        
        if self.robo_prem==1 and self.time_for == 0:
            robo_operator = "predict"
        if robo_operator:
            self.robo_judge(robo_operator)


    def instruction_btn_red(self):
        self.red_hit_status=Label(self.make_canvas,fg="red",font=("Arial",8,"bold"))
        self.red_hit_status.place(x=15,y=15+140+70)
        block_predict_red = Label(self.make_canvas,image=self.block_number_side[0],relief=FLAT)
        block_predict_red.place(x=34,y=15)
        predict_red = Button(self.make_canvas, bg="#ba2921", fg="#6e82f5", relief=RAISED, bd=5, text="Roll dice", font=("Arial", 9, "bold"), command=lambda: self.make_prediction("red"))
        predict_red.place(x=25, y=15 + 50)
        btn_1 = Button(self.make_canvas,bg="#ba2921",fg="#ffffff",text="1",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("red",'1'), state=DISABLED, disabledforeground="white")
        btn_1.place(x=20,y=15+100)
        btn_2 = Button(self.make_canvas,bg="#ba2921",fg="#ffffff",text="2",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("red",'2'), state=DISABLED, disabledforeground="white")
        btn_2.place(x=60,y=15+100)
        btn_3 = Button(self.make_canvas,bg="#ba2921",fg="#ffffff",text="3",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("red",'3'), state=DISABLED, disabledforeground="white")
        btn_3.place(x=20,y=15+100+40)
        btn_4 = Button(self.make_canvas,bg="#ba2921",fg="#ffffff",text="4",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("red",'4'), state=DISABLED, disabledforeground="white")
        btn_4.place(x=60,y=15+100+40)

        Label(self.make_canvas,text="AI",bg="#f5eded",fg="red",font=("Arial",10,"bold")).place(x=15,y=15+140+50)
        self.store_instructional_btn(block_predict_red,predict_red,[btn_1,btn_2,btn_3,btn_4])

    def instruction_btn_yellow(self):
        self.yellow_hit_status=Label(self.make_canvas,fg="red",font=("Arial",8,"bold"))
        self.yellow_hit_status.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 +7),y=15+(40*6+40*3)+40 + 110+70)
        block_predict_yellow = Label(self.make_canvas, image=self.block_number_side[0])
        block_predict_yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 10)+20, y=15 + (40 * 6 + 40 * 3) + 10)
        predict_yellow = Button(self.make_canvas, bg="#eaae2c", fg="#41BF4E", relief=RAISED, bd=5, text="Roll dice",font=("Arial", 9, "bold"), command=lambda: self.make_prediction("yellow"))
        predict_yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+20, y=15 + (40 * 6 + 40 * 3) + 40 + 20)
        
        btn_1 = Button(self.make_canvas,bg="#eaae2c",fg="#ffffff",text="1",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("yellow",'1'), state=DISABLED, disabledforeground="white")
        btn_1.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15, y=15 + (40 * 6 + 40 * 3) + 40 + 70)
        btn_2 = Button(self.make_canvas,bg="#eaae2c",fg="#ffffff",text="2",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("yellow",'2'), state=DISABLED, disabledforeground="white")
        btn_2.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15 + 40, y=15 + (40 * 6 + 40 * 3) + 40 + 70)
        btn_3 = Button(self.make_canvas,bg="#eaae2c",fg="#ffffff",text="3",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("yellow",'3'), state=DISABLED, disabledforeground="white")
        btn_3.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15, y=15 + (40 * 6 + 40 * 3) + 40 + 70+ 40)
        btn_4 = Button(self.make_canvas,bg="#eaae2c",fg="#ffffff",text="4",font=("Arial",13,"bold","italic"),relief=RAISED,bd=3,command=lambda: self.main_controller("yellow",'4'), state=DISABLED, disabledforeground="white")
        btn_4.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+15 + 40, y=15 + (40 * 6 + 40 * 3) + 40 + 70+ 40)
        
        Label(self.make_canvas, text="YOU", bg="#f5eded", fg="gold", font=("Arial", 10, "bold")).place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 +7),y=15+(40*6+40*3)+40 + 110+50)
        self.store_instructional_btn(block_predict_yellow, predict_yellow, [btn_1,btn_2,btn_3,btn_4])

    def store_instructional_btn(self, block_indicator, predictor, entry_controller):
        temp = []
        temp.append(block_indicator)
        temp.append(predictor)
        temp.append(entry_controller)
        self.block_value_predict.append(temp)

    def red_circle_start_position(self, coin_number):
        self.make_canvas.delete(self.made_red_coin[int(coin_number)-1])
        self.made_red_coin[int(coin_number)-1] = self.make_canvas.create_oval(100 + 40, 15+(40*6), 100 +40 + 40, 15+(40*6)+40, fill="#BA2921", width=3, outline="#FFD0B4")

        self.red_number_label[int(coin_number)-1].place_forget()
        red_start_label_x = 100 + 40 + 10
        red_start_label_y = 15 + (40 * 6) + 5
        self.red_number_label[int(coin_number)-1].place(x=red_start_label_x, y=red_start_label_y)

        self.red_coin_position[int(coin_number)-1] = 1
        self.window.update()
        time.sleep(0.2)

    def yellow_circle_start_position(self,coin_number):
        self.make_canvas.delete(self.made_yellow_coin[int(coin_number)-1])
        self.made_yellow_coin[int(coin_number)-1] = self.make_canvas.create_oval(100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8), 100 + (40 * 6)+(40*3)+(40*5), 15 + (40*9), fill="#EAAE2C", width=3,outline="#F5DF4D")

        self.yellow_number_label[int(coin_number)-1].place_forget()
        yellow_start_label_x = 100 + (40 * 6)+(40*3)+(40*4) + 10
        yellow_start_label_y = 15 + (40*8) + 5
        self.yellow_number_label[int(coin_number) - 1].place(x=yellow_start_label_x, y=yellow_start_label_y)

        self.yellow_coin_position[int(coin_number) - 1] = 27
        self.window.update()
        time.sleep(0.2)

    def num_btns_state_controller(self, take_nums_btns_list, state_control = 1):
        if state_control:
            for num_btn in take_nums_btns_list:
                num_btn['state'] = NORMAL
        else:
            for num_btn in take_nums_btns_list:
                num_btn['state'] = DISABLED

    def main_controller(self, color_coin, coin_number):
        robo_operator = None

        if  color_coin == "red":
            self.num_btns_state_controller(self.block_value_predict[0][2], 0)

            if self.move_red_counter == 106:
                messagebox.showwarning("Destination reached","Reached at the destination")

            elif self.red_coin_position[int(coin_number)-1] == -1 and self.move_red_counter == 6:
                self.red_circle_start_position(coin_number)
                self.red_coord_store[int(coin_number) - 1] = 1

            elif self.red_coin_position[int(coin_number)-1] > -1:
                take_coord = self.make_canvas.coords(self.made_red_coin[int(coin_number)-1])
                red_start_label_x = take_coord[0] + 10
                red_start_label_y = take_coord[1] + 5
                self.red_number_label[int(coin_number) - 1].place(x=red_start_label_x, y=red_start_label_y)

                if self.red_coin_position[int(coin_number)-1]+self.move_red_counter<=106:
                    self.red_coin_position[int(coin_number)-1] = self.motion_of_coin(self.red_coin_position[int(coin_number) - 1],self.made_red_coin[int(coin_number)-1],self.red_number_label[int(coin_number)-1],red_start_label_x,red_start_label_y,"red",self.move_red_counter) 
                    if self.robo_prem and self.red_coin_position[int(coin_number)-1] == 106 and color_coin == "red":
                        self.robo_store.remove(int(coin_number))
                        print("After removing: ", self.robo_store)

                else:
                    if not self.robo_prem: 
                            messagebox.showerror("Not possible","Sorry, not permitted")
                    self.num_btns_state_controller(self.block_value_predict[0][2])

                    if self.robo_prem:
                        robo_operator = "give"
                        self.robo_judge(robo_operator)
                    return

                if  self.red_coin_position[int(coin_number)-1]==22 or self.red_coin_position[int(coin_number)-1]==9 or self.red_coin_position[int(coin_number)-1]==48 or self.red_coin_position[int(coin_number)-1]==35 or self.red_coin_position[int(coin_number)-1]==14 or self.red_coin_position[int(coin_number)-1]==27 or self.red_coin_position[int(coin_number)-1]==40 or self.red_coin_position[int(coin_number)-1]==1:
                    pass
                else:
                    if self.red_coin_position[int(coin_number) - 1] < 100:
                        self.coord_overlap(self.red_coin_position[int(coin_number)-1],color_coin, self.move_red_counter)

                self.red_coord_store[int(coin_number)-1] = self.red_coin_position[int(coin_number)-1]

            else:
                messagebox.showerror("Wrong choice","Sorry, Your coin in not permitted to travel")
                self.num_btns_state_controller(self.block_value_predict[0][2])

                if self.robo_prem == 1:
                    robo_operator = "give"
                    self.robo_judge(robo_operator)
                return

            self.block_value_predict[0][1]['state'] = NORMAL

        elif color_coin == "yellow":
            
            self.num_btns_state_controller(self.block_value_predict[1][2], 0)

            if self.move_yellow_counter == 106:
                messagebox.showwarning("Destination reached","Reached at the destination")

            elif self.yellow_coin_position[int(coin_number) - 1] == -1 and self.move_yellow_counter == 6:
                self.yellow_circle_start_position(coin_number)
                self.yellow_coord_store[int(coin_number) - 1] = 27

            elif self.yellow_coin_position[int(coin_number) - 1] > -1:
                take_coord = self.make_canvas.coords(self.made_yellow_coin[int(coin_number) - 1])
                yellow_start_label_x = take_coord[0] + 10
                yellow_start_label_y = take_coord[1] + 5
                self.yellow_number_label[int(coin_number) - 1].place(x=yellow_start_label_x, y=yellow_start_label_y)

                if  self.yellow_coin_position[int(coin_number) - 1] + self.move_yellow_counter <= 106:
                    if (self.yellow_coin_position[int(coin_number) - 1] + self.move_yellow_counter>=100) and self.yellow_hit==0:
                        messagebox.showerror("Not possible","Make a hit First")                  
                        self.num_btns_state_controller(self.block_value_predict[1][2])
                        return
                    else:
                        self.yellow_coin_position[int(coin_number) - 1] = self.motion_of_coin(self.yellow_coin_position[int(coin_number) - 1], self.made_yellow_coin[int(coin_number) - 1], self.yellow_number_label[int(coin_number) - 1], yellow_start_label_x, yellow_start_label_y, "yellow", self.move_yellow_counter)
                else:
                   messagebox.showerror("Not possible","No path available")
                   
                   self.num_btns_state_controller(self.block_value_predict[1][2])
                   return

                if  self.yellow_coin_position[int(coin_number)-1]==22 or self.yellow_coin_position[int(coin_number)-1]==9 or self.yellow_coin_position[int(coin_number)-1]==48 or self.yellow_coin_position[int(coin_number)-1]==35 or self.yellow_coin_position[int(coin_number)-1]==1 or self.yellow_coin_position[int(coin_number)-1]==14 or self.yellow_coin_position[int(coin_number)-1]==40 or self.yellow_coin_position[int(coin_number)-1]==27:
                    pass
                else:
                    if self.yellow_coin_position[int(coin_number) - 1] < 100:
                        self.coord_overlap(self.yellow_coin_position[int(coin_number) - 1],color_coin, self.move_yellow_counter)

                self.yellow_coord_store[int(coin_number) - 1] = self.yellow_coin_position[int(coin_number) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.num_btns_state_controller(self.block_value_predict[1][2])
                return

            self.block_value_predict[1][1]['state'] = NORMAL

        print(self.red_coord_store)
        print(self.yellow_coord_store)
        if self.robo_prem == 1:
            print("Robo Store is: ", self.robo_store)
        
        permission_granted_to_proceed = True

        if  color_coin == "red" and self.red_coin_position[int(coin_number)-1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner(color_coin)
        elif  color_coin == "yellow" and self.yellow_coin_position[int(coin_number)-1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner(color_coin)

        if permission_granted_to_proceed:# if that is False, Game is over and not proceed more
            self.make_command(robo_operator)

    def motion_of_coin(self,counter_coin,specific_coin,number_label,number_label_x ,number_label_y,color_coin,path_counter):
        try:
            number_label.place(x=number_label_x,y=number_label_y)
            while True:
                if path_counter == 0:
                    break
                elif (counter_coin == 51 and color_coin == "red" and self.red_hit==1)or (counter_coin == 25 and color_coin == "yellow"and self.yellow_hit==1) or counter_coin>=100:
                    if counter_coin<100:
                        counter_coin=100

                    counter_coin = self.under_room_traversal_control(specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin, color_coin)

                    if  counter_coin == 106:
                        
                        if self.robo_prem == 1 and color_coin == "red":
                            messagebox.showinfo("Destination reached","Hey! I am at the destination")
                        else:
                            messagebox.showinfo("Destination reached","Congrats! You now at the destination")
                        if path_counter == 6:
                            self.six_with_overlap = 1
                        else:
                            self.time_for -= 1
                    break

                counter_coin += 1
                path_counter -=1
                number_label.place_forget()

                print(counter_coin)

                if counter_coin<=5:
                    self.make_canvas.move(specific_coin, 40, 0)
                    number_label_x+=40
                elif counter_coin == 6:
                    self.make_canvas.move(specific_coin, 40, -40)
                    number_label_x += 40
                    number_label_y-=40
                elif 6< counter_coin <=11:
                    self.make_canvas.move(specific_coin, 0, -40)
                    number_label_y -= 40
                elif counter_coin <=13:
                    self.make_canvas.move(specific_coin, 40, 0)
                    number_label_x += 40
                elif counter_coin <=18:
                    self.make_canvas.move(specific_coin, 0, 40)
                    number_label_y += 40
                elif counter_coin == 19:
                    self.make_canvas.move(specific_coin, 40, 40)
                    number_label_x += 40
                    number_label_y += 40
                elif counter_coin <=24:
                    self.make_canvas.move(specific_coin, 40, 0)
                    number_label_x += 40
                elif counter_coin <=26:
                    self.make_canvas.move(specific_coin, 0, 40)
                    number_label_y += 40
                elif counter_coin <=31:
                    self.make_canvas.move(specific_coin, -40, 0)
                    number_label_x -= 40
                elif counter_coin == 32:
                    self.make_canvas.move(specific_coin, -40, 40)
                    number_label_x -= 40
                    number_label_y += 40
                elif counter_coin <= 37:
                    self.make_canvas.move(specific_coin, 0, 40)
                    number_label_y += 40
                elif counter_coin <= 39:
                    self.make_canvas.move(specific_coin, -40, 0)
                    number_label_x -= 40
                elif counter_coin <= 44:
                    self.make_canvas.move(specific_coin, 0, -40)
                    number_label_y -= 40
                elif counter_coin == 45:
                    self.make_canvas.move(specific_coin, -40, -40)
                    number_label_x -= 40
                    number_label_y -= 40
                elif counter_coin <= 50:
                    self.make_canvas.move(specific_coin, -40, 0)
                    number_label_x -= 40
                elif 50< counter_coin <=52:
                    self.make_canvas.move(specific_coin, 0, -40)
                    number_label_y -= 40
                elif counter_coin == 53:
                    self.make_canvas.move(specific_coin, 40, 0)
                    number_label_x += 40
                    counter_coin = 1

                number_label.place_forget()
                number_label.place(x=number_label_x, y=number_label_y)

                self.window.update()
                time.sleep(0.2)

            return counter_coin
        except:
            print("Force Stop Error Came in motion of coin")

    # For same position, previous coin deleted and set to the room
    def coord_overlap(self, counter_coin, color_coin, path_to_traverse_before_overlap):
        if  color_coin!="red":
            for take_coin_number in range(len(self.red_coord_store)):
                if  self.red_coord_store[take_coin_number] == counter_coin:
                    if path_to_traverse_before_overlap == 6:
                        self.six_with_overlap=1
                    else:
                        self.time_for-=1

                    self.make_canvas.delete(self.made_red_coin[take_coin_number])
                    self.red_number_label[take_coin_number].place_forget()
                    self.red_coin_position[take_coin_number] = -1
                    self.red_coord_store[take_coin_number] = -1
                    if self.robo_prem == 1:
                        self.robo_store.remove(take_coin_number+1)
                        if self.red_coin_position.count(-1)>=1:
                            self.count_robo_stage_from_start = 2

                    if take_coin_number == 0:
                       remade_coin = self.make_canvas.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="#BA2921", outline="#FFD0B4")
                       self.red_number_label[take_coin_number].place(x=100 + 40 + 10, y=15 + 40 + 5)
                    elif take_coin_number == 1:
                        remade_coin = self.make_canvas.create_oval(100+40+60+60, 15 + 40, 100+40+60+60+40, 15 + 40 + 40, width=3, fill="#BA2921", outline="#FFD0B4")
                        self.red_number_label[take_coin_number].place(x=100 + 40 + 60 +60 + 10, y=15 + 40 + 5)
                    elif take_coin_number == 2:
                        remade_coin = self.make_canvas.create_oval(100 + 40 + 60 + 60, 15 + 40 + 100, 100 + 40 + 60 + 60 + 40, 15 + 40 + 40 + 100, width=3, fill="#BA2921", outline="#FFD0B4")
                        self.red_number_label[take_coin_number].place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 100 + 5)
                    else:
                        remade_coin = self.make_canvas.create_oval(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3,fill="#BA2921", outline="#FFD0B4")
                        self.red_number_label[take_coin_number].place(x=100 + 40 + 10, y=15 + 40 + 100 + 5)
                    
                    self.yellow_hit=1
                    self.yellow_hit_status.config(text="FREE",fg="green",font=("Arial",12))
                    self.made_red_coin[take_coin_number]=remade_coin

        if  color_coin != "yellow":
            for take_coin_number in range(len(self.yellow_coord_store)):
                if  self.yellow_coord_store[take_coin_number] == counter_coin:
                    if path_to_traverse_before_overlap == 6:
                        self.six_with_overlap = 1
                    else:
                        self.time_for -= 1

                    self.make_canvas.delete(self.made_yellow_coin[take_coin_number])
                    self.yellow_number_label[take_coin_number].place_forget()
                    self.yellow_coin_position[take_coin_number] = -1
                    self.yellow_coord_store[take_coin_number] = -1

                    if take_coin_number == 0:
                        remade_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="#EAAE2C", outline="#F5DF4D")
                        self.yellow_number_label[take_coin_number].place(x=340+(40*3) + 40 + 10, y=30 + (40*6)+(40*3)+40+10)
                    elif take_coin_number == 1:
                        remade_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#EAAE2C", outline="#F5DF4D")
                        self.yellow_number_label[take_coin_number].place(x=340+(40*3)+ 40 + 40+ 60 + 30, y=30 + (40*6)+(40*3)+40+10)
                    elif take_coin_number == 2:
                        remade_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="#EAAE2C", outline="#F5DF4D")
                        self.yellow_number_label[take_coin_number].place(x=340+(40*3)+ 40 + 40+ 60 + 30, y=30 + (40*6)+(40*3)+40+100+10)
                    else:
                        remade_coin = self.make_canvas.create_oval(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="#EAAE2C", outline="#F5DF4D")
                        self.yellow_number_label[take_coin_number].place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)

                    self.red_hit=1
                    self.red_hit_status.config(text="FREE",fg="green",font=("Arial",12))
                    self.made_yellow_coin[take_coin_number] = remade_coin

    def under_room_traversal_control(self,specific_coin,number_label,number_label_x,number_label_y,path_counter,counter_coin,color_coin):
        if color_coin == "red" and counter_coin >= 100:
            if int(counter_coin)+int(path_counter)<=106:
               counter_coin = self.room_red_traversal(specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin)

        elif color_coin == "yellow" and counter_coin >= 100:
            if  int(counter_coin) + int(path_counter) <= 106:
                counter_coin = self.room_yellow_traversal(specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin)

        return counter_coin


    def room_red_traversal(self, specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin):
        while path_counter>0:
            counter_coin += 1
            path_counter -= 1
            self.make_canvas.move(specific_coin, 40, 0)
            number_label_x+=40
            number_label.place(x=number_label_x,y=number_label_y)
            self.window.update()
            time.sleep(0.2)
        return counter_coin

    def room_yellow_traversal(self, specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin):
        while path_counter > 0:
            counter_coin += 1
            path_counter -= 1
            self.make_canvas.move(specific_coin, -40, 0)
            number_label_x -= 40
            number_label.place(x=number_label_x, y=number_label_y)
            self.window.update()
            time.sleep(0.2)
        return counter_coin

    def check_winner_and_runner(self,color_coin):
        destination_reached = 0 # Check for all specific color coins
        if color_coin == "red":
            temp_store = self.red_coord_store
            temp_delete = 0# Player index
        elif color_coin == "yellow":
            temp_store = self.yellow_coord_store
            temp_delete = 1 # Player index

        for take in temp_store:
            if take == 106:
                destination_reached = 1
            else:
                destination_reached = 0
                break

        if  destination_reached == 1:# If all coins in block reach to the destination, winner and runner check
            self.take_permission += 1
            if self.take_permission == 1:# Winner check
                if self.robo_prem == 1 and color_coin == "red":
                    messagebox.showinfo("Winner", "Hurrah! I am the winner")
                else:
                    messagebox.showinfo("Winner","Congrats! You are the winner")
                    
            self.block_value_predict[temp_delete][1]['state'] = DISABLED
            self.total_people_play.remove(temp_delete)

            if len(self.total_people_play) == 1:
                messagebox.showinfo("Game Over","Good bye!!!!")
                self.block_value_predict[0][1]['state'] = DISABLED
                return False
            else:
                self.time_for-=1
        else:
            print("Winner not decided")

        return True

    def robo_judge(self, ind="give"):
        if ind == "give":# For give the value
            all_in = 1# Denoting all the coins are present in the room
            for i in range(4):
                if self.red_coin_position[i] == -1:
                    all_in = 1
                else:
                    all_in = 0# Denoting all the coins not present in the room
                    break
            
            if all_in == 1:# All coins are present in room
                if self.move_red_counter == 6:
                    predicted_coin = choice([1,2,3,4])
                    self.robo_store.append(predicted_coin)
                    self.main_controller("red", predicted_coin)
                else:
                    pass
            else:# All coins not present in room
                temp = self.red_coin_position# Take red coin position reference
                take_ref = self.yellow_coin_position# Take yellow coin position reference
                
                if len(self.robo_store) == 1:# When only one coin is outside of the room
                    if self.move_red_counter<6:# When prediction less than 6
                        if (self.count_robo_stage_from_start>3) and (temp[self.robo_store[0]-1] >=33 and temp[self.robo_store[0]-1]<=38):
                            self.count_robo_stage_from_start = 2
                        self.main_controller("red", self.robo_store[0]) 
                    else:# When prediction is 6
                        forward_perm = 0# Controlling process to be forward or not
                        for coin in take_ref:# coin is yellow individual coin distance
                            if coin>-1 and coin<101:
                                if (coin != 40 or coin != 35 or coin != 27 or coin != 22 or coin != 14 or coin != 9 or coin !=1 or coin !=48) and coin-temp[self.robo_store[0]-1] >= 6 and coin-temp[self.robo_store[0]-1] <= 12:
                                    forward_perm = 1
                                    break
                                else:
                                    forward_perm = 0
                            else:
                                forward_perm = 0

                        if forward_perm == 0:# Not forward the process
                            store = [1,2,3,4]
                            store.remove(self.robo_store[0])
                            predicted_coin = choice(store)
                            self.robo_store.append(predicted_coin)
                            self.main_controller("red", predicted_coin)
                        else:# Forward the entire process
                            self.main_controller("red", self.robo_store[0])
                else:
                    def normal_movement_according_condition():
                        # This portion is for checking if current location + predicted value <= 106 or not.....Coin Filtering
                        normal_movement = 1# Normal Movement of the entite coin
                        
                        for coin in self.robo_store:# coin is coin number
                            if temp[coin-1]+self.move_red_counter <= 106:# For all coins having predicted location <=106
                                pass
                            else:
                                normal_movement = 0
                                break

                        if normal_movement:
                            temp_robo_store = [coin for coin in self.robo_store]
                        else:
                            temp_robo_store = [coin for coin in self.robo_store if temp[coin-1]+self.move_red_counter <= 106]

                        # This portion is for coin filtering under some constrains
                        for coin in temp_robo_store:# coin is coin number
                            if len(temp_robo_store)>1 and temp[coin-1]<101:                            
                                if (temp[coin-1] in take_ref) and (temp[coin-1] != 1 or temp[coin-1] != 9 or temp[coin-1] != 14 or temp[coin-1] != 22 or temp[coin-1] != 27 or temp[coin-1] != 35 or temp[coin-1] != 40 or temp[coin-1] != 48):
                                    temp_robo_store.remove(coin)
                                elif temp[coin-1]<=39 and temp[coin-1]+self.move_red_counter>39:                                    
                                    for loc_coin_other in take_ref:
                                        if (loc_coin_other>=40 and loc_coin_other<=46) and (temp[coin-1]+self.move_red_counter>loc_coin_other):
                                            temp_robo_store.remove(coin)
                                            break

                        # Overlapp checking with predicted value to eliminate other coin
                        process_forward = 1
                        for coin in temp_robo_store:
                            if temp[coin-1]+self.move_red_counter in take_ref:
                                process_forward = 0
                                self.main_controller("red", coin)
                                break
                        
                        # Not a single overlapp found so now self rescue or safe forward
                        if process_forward:
                            take_len = len(temp_robo_store)
                            store = {}
                            if take_ref:
                                for robo in temp_robo_store:#  robo is coin number   RED COINS
                                    for coin_other in take_ref:# coin_other Yellow coin location   Yellow Coins
                                        if coin_other>-1 and coin_other<100:
                                            if take_len>1 and (temp[robo-1]>38 and coin_other<=38) or ((temp[robo-1] == 9 or temp[robo-1] == 14 or temp[robo-1] == 27 or temp[robo-1] == 35 or temp[robo-1] == 40 or temp[robo-1] == 48 or temp[robo-1] == 22) and (coin_other<=temp[robo-1] or (coin_other>temp[robo-1] and coin_other<=temp[robo-1]+3))):  # avoid case to store
                                                take_len-=1
                                            else:
                                                store[temp[robo-1]-coin_other] = (robo, take_ref.index(coin_other)+1)# Store coin number
                            
                            # positive_distance = robo front          negative_distance = robo_behind
                            if store:
                                store_positive_dis = {}
                                store_negative_dis = {}
                                take_max = 0
                                take_min = 0
                                
                                try:
                                    store_positive_dis = dict((k,v) for k,v in store.items() if k>0)    # Red is in front of yellow
                                    take_min = min(store_positive_dis.items())
                                except:
                                    pass
                                try:
                                    store_negative_dis = dict((k,v) for k,v in store.items() if k<0)    # yellow is in front of red
                                    take_max = max(store_negative_dis.items())
                                except:
                                    pass
                                
                                # Positive forward checking
                                work_comp_in_pos = 0
                                take_len = len(store_positive_dis)
                                index_from_last = -1

                                while take_len:
                                    if take_min and take_min[0] <= 6:                        
                                        work_comp_in_pos = 1
                                        self.main_controller("red", take_min[1][0])
                                        break
                                    else:
                                        index_from_last -= 1
                                        try:
                                            take_min = min(sorted(store_positive_dis.items())[index_from_last])
                                        except:
                                            break
                                    take_len -= 1


                                # Negative forward checking
                                work_comp_in_neg = 0
                                if not work_comp_in_pos:
                                    take_len = len(store_negative_dis)
                                    index_from_last = len(store_negative_dis)-1
                                    while take_len:
                                        if take_max and temp[take_max[1][0]-1] + self.move_red_counter <= take_ref[take_max[1][1]-1]:
                                            work_comp_in_neg = 1
                                            self.main_controller("red", take_max[1][0])
                                            break
                                        else:
                                            index_from_last -= 1
                                            try:
                                                take_max = max(sorted(store_negative_dis.items())[index_from_last])
                                            except:
                                                break
                                        take_len -= 1
                        
                                # Not operate in positive and negative distance method...So now cover it by closest distance to the destination
                                if not work_comp_in_neg and not work_comp_in_pos:
                                    close_to_dest = temp_robo_store[0]
                                    for coin_index in range(1,len(temp_robo_store)):
                                        if temp[temp_robo_store[coin_index]-1] > temp[close_to_dest-1]:
                                            close_to_dest = temp_robo_store[coin_index]
                        
                                    self.main_controller("red", close_to_dest)
                            else:# If store(Not find the location difference) is empty
                                close_to_dest = temp_robo_store[0]
                                for coin_index in range(1,len(temp_robo_store)):
                                    if temp[temp_robo_store[coin_index]-1] > temp[close_to_dest-1]:
                                        close_to_dest = temp_robo_store[coin_index]
                                self.main_controller("red", close_to_dest)
                        else:
                            pass
                        
                    # For multiple Coin control Giving
                    if self.move_red_counter<6:
                        normal_movement_according_condition()
                    else:
                        coin_proceed = 0
                        
                        for coin in self.robo_store:
                            if temp[coin-1] + self.move_red_counter in self.yellow_coin_position:
                                coin_proceed = coin
                                break

                        if not coin_proceed:
                            if -1 in self.red_coin_position:
                                # Coin out
                                temp_store = [1,2,3,4]
                                for coin in self.robo_store:
                                    temp_store.remove(coin)
                                take_pred = choice(temp_store)
                                self.robo_store.append(take_pred)
                                self.main_controller("red", take_pred)
                            else:
                                # coin proceed
                                normal_movement_according_condition()
                        else:
                            self.main_controller("red", coin_proceed)
        else:
            self.make_prediction("red")# Prediction Function Call


if __name__ == '__main__':
    window = Tk()
    window.geometry("800x630")
    window.maxsize(800,630)
    window.minsize(800,630)
    window.title("Ludo with Computer")
    window.iconbitmap("ludo_icon.ico")
    block_six_side = ImageTk.PhotoImage(Image.open("6.png").resize((33, 33), Image.ANTIALIAS))
    block_five_side = ImageTk.PhotoImage(Image.open("5.png").resize((33, 33), Image.ANTIALIAS))
    block_four_side = ImageTk.PhotoImage(Image.open("4.png").resize((33, 33), Image.ANTIALIAS))
    block_three_side = ImageTk.PhotoImage(Image.open("3.png").resize((33, 33), Image.ANTIALIAS))
    block_two_side = ImageTk.PhotoImage(Image.open("2.png").resize((33, 33), Image.ANTIALIAS))
    block_one_side = ImageTk.PhotoImage(Image.open("1.png").resize((33, 33), Image.ANTIALIAS))
    Ludo(window,block_six_side,block_five_side,block_four_side,block_three_side,block_two_side,block_one_side)
    window.mainloop()