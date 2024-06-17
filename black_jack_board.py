import tkinter as tk
import numpy as np
import os
from PIL import ImageTk, Image
import pandas as pd
from tensorflow import keras
import blackjack_AI


class BlackJack:
    def __init__(self):
        self.AI = keras.models.load_model('BlackJack_Model.h')
        self.dealer_scores = 0
        self.player_scores = 0
        self.number_of_episodes = 20000
        self.root = tk.Tk()
        self.stats = tk.Frame(self.root, bg="white", border=10)
        self.dealer = tk.Frame(self.root, bg="white", border=2)
        self.player = tk.Frame(self.root, bg="white",border=2)
        self.buttons = tk.Frame(self.root, bg="white",border=2)
        self.dealer_canvas = tk.Canvas(self.dealer, width=420, height=250, bg="white")
        self.player_canvas = tk.Canvas(self.player, width=620, height=250, bg="white")
        self.dealers_total = tk.Label(self.dealer, font=('', 14), justify='center', pady=10, padx=10)
        self.players_total = tk.Label(self.player, font=('', 14), justify='center', pady=10, padx=10)
        self.dealer_status_value = tk.Label(self.dealer,text="", font=('', 12), justify='center', pady=3, bg="white")
        self.player_status_value = tk.Label(self.player,text="", font=('', 12), justify='center', pady=3, bg="white")
        self.dealer_score = tk.Label(self.stats, font=('', 14), justify='center', pady=10, padx=10)
        self.player_score = tk.Label(self.stats, font=('', 14), justify='center', pady=10, padx=10)

        self.images_array()
        self.play_status = False
       # self.dealer_stats_value = ""
       # self.player_stats_value = ""
        self.game_train_data = list()
        
        
        
    def images_array(self):
        # os.chdir(r"C:\Users\Ero\Desktop\PersonalWorks\AIProjects\ErosAIPortfolio\QLearning")
        images = ["card_2","card_3","card_4", "card_5","card_6","card_7","card_8","card_9",
                 "card_10","card_A", "card_king", "card_prince", "card_queen", "card_joker"]
        self.images_number = [2,3,4,5,6,7,8,9,10,11,10,10,10,20]
        rand_previous = list()
        self.images_list=list()
        self.observations = list()
        for i in range(0, 5):
            random_gen =np.random.randint(0, len(images))
            while(random_gen in rand_previous):
                random_gen =np.random.randint(0, len(images))
            rand_previous.append(random_gen)
            image  = ImageTk.PhotoImage(Image.open("black_images/" + images[random_gen]+".JPG" ).resize((200,250)), master=self.root)
            self.images_list.append(image)
            
            
        self.dealer_total = self.images_number[rand_previous[0]]
        self.player_total = self.images_number[rand_previous[2]] + self.images_number[rand_previous[3]]
        self.dealer_image1 = self.images_list[0]
        self.dealer_image2 = ImageTk.PhotoImage(Image.open("black_images/card_back.JPG").resize((200,250)), master=self.root)
        self.player_image1 = self.images_list[2]
        self.player_image2 = self.images_list[3]
        self.player_image3 = ImageTk.PhotoImage(Image.open("black_images/card_back.JPG").resize((200,250)), master=self.root)
        self.dealer_canvas.create_image(5,5,anchor="nw", image=self.dealer_image1)
        self.dealer_canvas.create_image(210,5,anchor="nw", image=self.dealer_image2)
        self.player_canvas.create_image(5,5,anchor="nw", image=self.player_image1)
        self.player_canvas.create_image(210,5,anchor="nw", image=self.player_image2)
        self.player_canvas.create_image(420,5,anchor="nw", image=self.player_image3)
        self.players_total.configure(text=str(self.player_total))
        self.dealers_total.configure(text=str(self.dealer_total))
        
        
        self.root.update()
        for i in rand_previous:
            self.observations.append(self.images_number[i])
            
        
        return self.observations
        
         
    def playGame(self):
        self.newButton.configure(state ="disabled")
        self.playButton.configure(state ="disabled")
        self.trainButton.configure(state ="disabled")
        observations = np.array([self.observations[0], self.observations[2], self.observations[3]])
        observations_ = np.array(observations).reshape(1,3)
        action = np.argmax(blackjack_AI.predict_game(observations_))
        self.dealer_total = np.sum(self.observations[:2])
        if(action==0):
            self.player_total = np.sum(self.observations[2:])
            move = "hit"
        else:
            self.player_total = np.sum(self.observations[2:4])
            move = "stand"
        if( self.player_total > self.dealer_total and self.player_total <= 21 ):
            self.player_status_value.configure(text="win" + ", "+ move)
            self.dealer_status_value.configure(text="lose")
            self.player_scores += 1
       
        elif(self.dealer_total > self.player_total and self.dealer_total <= 21): 
            self.player_status_value.configure(text="lose" + ", "+ move)
            self.dealer_status_value.configure(text="win")
            self.dealer_scores += 1
            
        elif(self.player_total <= 21 and self.dealer_total > 21): 
            self.player_status_value.configure(text="win" + ", "+ move)
            self.dealer_status_value.configure(text="lose")
            self.player_scores += 1
        
        elif(self.dealer_total <= 21 and self.player_total > 21): 
            self.player_status_value.configure(text="lose" + ", "+ move)
            self.dealer_status_value.configure(text="win")
            self.dealer_scores += 1
        
        else:
            self.player_status_value.configure(text="draw" + ", "+ move)
            self.dealer_status_value.configure(text="draw")
            
        self.players_total.configure(text=str(self.player_total))
        self.dealers_total.configure(text=str(self.dealer_total))
        self.player_score.configure(text=str(self.player_scores))
        self.dealer_score.configure(text=str(self.dealer_scores))
        self.player_image3 = self.images_list[4]
        self.dealer_image2 = self.images_list[1]
        self.player_canvas.create_image(420,5,anchor="nw", image=self.player_image3)
        self.dealer_canvas.create_image(210,5,anchor="nw", image=self.dealer_image2)
        self.root.update()
        self.newButton.configure(state ="normal")
        self.trainButton.configure(state ="normal")
            
            
            
        
    
    def newGame(self):
        self.playButton.configure(state ="normal")
        self.images_array()
        
        
        
    
    def train(self):
        self.newButton.configure(state ="disabled")
        self.playButton.configure(state ="disabled")
        self.trainButton.configure(state ="disabled")
        
        #0 - hit actions
        #1 - stand actions
        #2 - blackjack
        for i  in range(0, self.number_of_episodes):
            observations = np.array(self.images_array())
            
            if(self.player_total==21 and (self.dealer_total < 21 or self.dealer_total > 21)):
                action=1
                reward = 1
                self.player_status_value.configure(text="win")
                self.dealer_status_value.configure(text="lose")
            elif(self.player_total==21 and self.dealer_total==21 ):
                action=1
                reward = 0
                self.player_status_value.configure(text="draw")
                self.dealer_status_value.configure(text="draw")
            else:
                action = np.random.randint(0,2)
                if(action == 0):
                    player_score = np.sum(observations[2:])
                    dealer_score = np.sum(observations[:2])
                    if(player_score > dealer_score and player_score <= 21 ):
                        reward = 1
                        self.player_status_value.configure(text="win")
                        self.dealer_status_value.configure(text="lose")
                    elif(dealer_score > player_score and dealer_score <= 21):
                        reward = -1
                        self.player_status_value.configure(text="lose")
                        self.dealer_status_value.configure(text="win")
                        
                    elif(player_score <= 21 and dealer_score > 21): 
                        reward = 1
                        self.player_status_value.configure(text="win")
                        self.dealer_status_value.configure(text="lose")
        
                    elif(dealer_score <= 21 and player_score > 21): 
                        self.player_status_value.configure(text="lose")
                        self.dealer_status_value.configure(text="win")
                        reward = -1
                    else:
                        reward = 0
                        self.player_status_value.configure(text="draw")
                        self.dealer_status_value.configure(text="draw")
                elif(action == 1):
                    player_score = np.sum(observations[2:4])
                    dealer_score = np.sum(observations[:2])
                    if(player_score > dealer_score and player_score <= 21 ):
                        reward = 1
                        self.player_status_value.configure(text="win")
                        self.dealer_status_value.configure(text="lose")
                    elif(dealer_score > player_score and dealer_score <= 21):
                        reward = -1
                        self.player_status_value.configure(text="lose")
                        self.dealer_status_value.configure(text="win")
                    elif(player_score <= 21 and dealer_score > 21): 
                        reward = 1
                        self.player_status_value.configure(text="win")
                        self.dealer_status_value.configure(text="lose")
        
                    elif(dealer_score <= 21 and player_score > 21): 
                        self.player_status_value.configure(text="lose")
                        self.dealer_status_value.configure(text="win")
                        reward = -1
                    else:
                        reward = 0
                        self.player_status_value.configure(text="draw")
                        self.dealer_status_value.configure(text="draw")
            observations = np.append(arr = observations, values=[reward,action])
            self.game_train_data.append(observations)
        pd_data = pd.DataFrame(self.game_train_data, columns = ["dealer_card1","delear_card2","player_card1", "player_card2", "unused_card","reward", "action"])
        pd_data.to_csv("BlackJack_training_data.csv")
        #blackjack_AI.train_game()
        #print(self.game_train_data)
                    
        self.player_status_value.configure(text="")
        self.dealer_status_value.configure(text="")  
            
        self.newButton.configure(state ="normal")
        self.playButton.configure(state ="normal")
        self.trainButton.configure(state ="normal")
            
        
    def create_board(self):
       
        dealer_score_label = tk.Label(self.stats,text="Dealer_score:", font=('', 14), justify='center', pady=10, padx=10, bg="#111111", fg="white")
        dealer_score_label.grid(row=0, column=0,pady=10)
        
        self.dealer_score.grid(row=0, column=1,pady=10, ipadx = 10)
        
        player_score_label = tk.Label(self.stats,text="Player_score:", font=('', 14), justify='center', pady=10, padx=10, bg="red", fg="white")
        player_score_label.grid(row=0, column=2,pady=10)
        self.player_score.grid(row=0, column=3,pady=10, ipadx = 10)
        
        
        self.dealer_canvas.grid(row=1, column=0,pady=5)
       
        
        
        dealer_total_label = tk.Label(self.dealer,text="Dealer_total:", font=('', 14), justify='center', pady=10, padx=10, fg="white", bg="black")
        dealer_total_label.grid(row=1, column = 1, pady=10)
       
        self.dealers_total.grid(row=1, column = 2, pady=10, ipadx = 10)
        
        dealer_status = tk.Label(self.dealer,text="Dealer_status:", font=('', 12), justify='center', pady=3, padx=3, bg="white")
        dealer_status.grid(row=0, column = 0, ipadx = 5)
        
        
        self.dealer_status_value.grid(row=0, columnspan = 3, ipadx = 5)
        
        
        
        
        self.player_canvas.grid(row=1, column=0,pady=5)
       
        
        
        
        player_total_label = tk.Label(self.player,text="player_total:", font=('', 14), justify='center', pady=10, padx=10, fg="white", bg="black")
        player_total_label.grid(row=1, column = 1, pady=10)
       
        
        self.players_total.grid(row=1, column = 2, pady=10, ipadx = 10)
        
        player_status = tk.Label(self.player,text="Player_status:", font=('', 12), justify='center', pady=3, padx=3, bg="white")
        player_status.grid(row=0, column = 0, ipadx = 5)
        
        
        self.player_status_value.grid(row=0, columnspan = 3, ipadx = 5)
       
        
        self.playButton = tk.Button(self.buttons, text="PLAY", font=('', 14), justify='center', pady=5, bg="#7FDBFF", command=self.playGame)
        self.playButton.grid(row=0, column=1, ipadx=10,pady=5)
       
        self.newButton = tk.Button(self.buttons, text="NEW GAME", font=('', 14), justify='center', pady=5, bg="orange", command=self.newGame)
        self.newButton.grid(row=0, column=2, ipadx=7,pady=5)
        
        self.trainButton = tk.Button(self.buttons, text="TRAIN", font=('', 14), justify='center', pady=5, bg="green", fg="white", command=self.train)
        self.trainButton.grid(row=0, column=3, ipadx=7,pady=5)
        
        
        
        self.stats.pack()
        self.dealer.pack()
        self.player.pack()
        self.buttons.pack()
        self.root.title("BlackJack")
        self.root.config(bg="black")
        w,h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        #self.root.attributes('-fullscreen', True)
        self.root.geometry("%dx%d+0+0"%(w,h))
        self.root.mainloop()
        
        
        
        
blackjack = BlackJack()
blackjack.create_board()
        