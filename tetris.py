from msvcrt import kbhit
#from re import I
import sys
from tokenize import single_quoted
import pygame
import time
from pygame.locals import *
import copy
import random
from tkinter import messagebox
#class Tetris_field

def move_check(mino,well,after_fall_minos):#操作ミノが壁や落下済みミノと衝突しているか判定,引数に複数クラスの要素を要求するためクラス外に
    flag = False
    tops=[]
    for i in mino:#動いている4つのミノの衝突確認
        if i.collidelist(well) != -1:#壁衝突
            flag = True
        if i.collidelist(after_fall_minos) != -1:#落下済みブロック衝突
            flag = True
    #print(flag)
    return(flag)

def text_show(screen,text_data,font_size,r,g,b,x,y):
    font = pygame.font.Font("VL-Gothic-Regular.ttf",font_size)#ファイル見つからないければ"VL-Gothic-Regular.ttf"→none置き換える

    text = font.render(str(text_data), True, (r,g,b))
    screen.blit(text, [x,y])

def create_control_mino(next_control_mino):#ランダムで操作ミノのインスタンスを作成
    randam_nam=random.uniform(0,7)
    i=0
    if randam_nam <1:
        i=Tetriminol_I()
        next_control_mino=copy.copy(i)
        return(next_control_mino)
    elif randam_nam <2:
        i=Tetriminol_T()
        next_control_mino=copy.copy(i)
        return(next_control_mino)
    elif randam_nam<3:
        i=Tetriminol_S()
        next_control_mino=copy.copy(i)
        return(next_control_mino)
    elif randam_nam <4:
        i=Tetriminol_S_R()
        next_control_mino=copy.copy(i)
        return(next_control_mino)
    elif randam_nam<5:
        i=Tetriminol_L()
        next_control_mino=copy.copy(i)
        return(next_control_mino)
    elif randam_nam <6:
        i=Tetriminol_L_R()
        next_control_mino=copy.copy(i)
        return(next_control_mino)
    elif randam_nam<7:
        i=Tetriminol_sq()
        next_control_mino=copy.copy(i)
        return(next_control_mino)

class Hold:#ホールド処理
    def __init__(self):
        self.hold_rect="No instance"
        self.hold_rect_back="No instance"

    def swap(self,hold_rect):#ホールド実行
        if self.hold_rect!="No instance":
            self.hold_rect_back=copy.copy(self.hold_rect)
            self.hold_rect=copy.copy(hold_rect)
            if self.hold_rect_back!="No instance":
                self.hold_rect_back.app_x=hold_rect.app_x
                self.hold_rect_back.app_y=hold_rect.app_y
            return(self.hold_rect_back)
        else:
            self.hold_rect=copy.copy(hold_rect)
            return(self.hold_rect_back)
    def swap_check(self,control_mino,well,after_fall_mino):#スワップ後ミノが衝突していたらスワップ処理をとりけす
        control_mino.drow()
        if move_check(control_mino.mino_pass(),well,after_fall_mino)==True:
            self.hold_rect_back=copy.copy(self.hold_rect)
            self.hold_rect=copy.copy(control_mino)
            return(self.hold_rect_back)
        else:
            return(control_mino)
    def drow(self):
        self.hold_rect.hold_drow()

class Tetriminol:#操作ミノに関するクラス
    def __init__(self):
        self.rect_start_x=300
        self.rect_start_y=100
        self.rect_size_x=20
        self.rect_size_y=20
        self.rect_move_x=20
        self.rect_move_y=20
        self.rect_next_x=480
        self.rect_next_y=100
        self.rect_hold_x=70
        self.rect_hold_y=100
        self.screen = pygame.display.set_mode((1200,800))
        self.spin_pattern=0
        self.spin_direction=0#回転方向の命令 -1は左回転、0は回転しない,１は右回転
        self.mino=[]#操作中のミノ4つを格納する
        self.well=[]#4方向の壁を格納する
        self.immediately_after_creation=True #操作ミノ作成直後かどうかの判定
        self.app_y=0
        self.app_x=0
        self.after_fall_minos=[]#落下済みミノの格納
        self.hard_dorp=False
        self.hold=False
        self.key_down_r=False
        self.key_down_l=False
        self.key_down_d=False
        self.key_down_a=False
        self.key_down_q=False
        self.key_down_up=False
        self.key_sensitivity=0
        self.r_move_count=0
        self.l_move_count=0
        self.key_sensitivity=1
        self.key_sensitivity_use=3#キー入力感度の調整、低いほど感度がさがる,上げすぎるとキー入力に反応しにくくなる
        self.deferral_grounded=7 #落下ミノが接地後に動ける猶予
        self.deferral_grounded_use=0
    def rgb_pass(self):
        rect_r=[]
        rect_g=[]
        rect_b=[]
        rect_quantity=4
        for i in range(rect_quantity):
            rect_r.append(self.rect_r)
            rect_g.append(self.rect_g)
            rect_b.append(self.rect_b)
        return(rect_r,rect_g,rect_b)
    def mino_fall(self,fall_flag):
        gameover_text_title="gameover"
        gameover_text="ミノが上限に達しました、終了します"
        if fall_flag  == False:
            self.app_y=self.app_y+20
            self.deferral_grounded_use=0
            self.immediately_after_creation=False
        else:
            self.deferral_grounded_use=self.deferral_grounded_use+1
            if self.deferral_grounded_use>=self.deferral_grounded:
                if self.immediately_after_creation==True:#操作ミノ作成直後に他ブロックと接触していたらゲームオーバ
                       messagebox.showinfo(gameover_text_title, gameover_text)
                       sys.exit()
                for mino in self.mino:
                        self.after_fall_minos.append(mino)
                self.deferral_grounded_use=0
                return(True)
        return(False)

    def mino_fall_check(self,well,after_fall_minos):#ミノ落下可能か判定
        fall=False
        mino_move=20
        for i in range(len(self.mino)):
            self.mino[i].top=self.mino[i].top+mino_move
        if move_check(self.mino,well,after_fall_minos) == False:
            for i in range(len(self.mino)):
                self.mino[i].top=self.mino[i].top-mino_move
            return(False)
        else:
            for i in range(len(self.mino)):
                self.mino[i].top=self.mino[i].top-mino_move
            pygame.display.flip()#画面更新
            return(True)

    def after_fall_minos_pass(self):
        return(self.after_fall_minos)
    def after_fall_minos_clear(self):
        self.after_fall_minos=[]
    def mino_pass(self):
        return(self.mino)

    def move(self,well,after_fall_mino,instance=0):
            """キー入力の監視"""
            key=[]
            for event in  pygame.event.get():#入力されたキーのログがなくなるまでループ
                """event=キー入力などユーザーの操作,elif使うと同時押しに対応できないので使わない"""
                if event.type == pygame.QUIT:#終了
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:#右移動
                        self.key_down_r=True
                    if event.key == pygame.K_LEFT:#左移動
                        self.key_down_l=True
                    if event.key == pygame.K_d:#左回転
                        self.key_down_d=True
                    if event.key == pygame.K_a:#右回転
                        self.key_down_a = True
                    if event.key == pygame.K_q:#ホールド
                        self.key_down_q = True
                    if event.key == pygame.K_UP:#ハードドロップ
                        self.key_down_up=True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.key_down_r= False
                    if event.key == pygame.K_LEFT:
                        self.key_down_l= False
                    if event.key == pygame.K_d:
                        self.key_down_d = False
                    if event.key == pygame.K_a:
                        self.key_down_a = False
                    if event.key == pygame.K_q:
                        self.key_down_q = False
                        self.hold=False
                    if event.key == pygame.K_UP:
                        self.key_down_up = False

            """キー入力に対応した操作ミノの動作"""
            self.key_sensitivity=self.key_sensitivity+1
            if self.key_sensitivity%self.key_sensitivity_use == 0:
                if self.key_down_r == True:
                    self.app_x=self.app_x+20
                    self.drow(well,after_fall_mino,r_move=True)
                    if self.r_move_count > 9:#連続入力対策
                        self.r_move_count=0
                        self.key_down_r=False
                if self.key_down_l == True:
                    self.app_x=self.app_x-20
                    self.drow(well,after_fall_mino,l_move=True)
                    if self.l_move_count > 9:#連続入力対策
                        self.l_move_count=0
                        self.key_down_l=False
                if self.key_down_d == True:
                    self.drow(well,after_fall_mino,-1)#＋1は右回転
                    self.key_down_d == False#連続入力対策
                if self.key_down_a == True:
                    self.drow(well,after_fall_mino,+1)#-1は左回転
                    self.key_down_a == False
                if self.key_down_q == True:#ホールド処理は操作ミノのクラス外なのでholdクラスで処理
                    self.hold=True
                    self.key_down_q= False
                if self.key_down_up == True:#
                    self.hard_dorp=True
            return(self.hard_dorp,self.hold)

class Field_T(Tetriminol):#壁や落下後のテトリミノに関する処理
    def __init__(self):
        super().__init__()
        self.after_fall_mino=[]#落下後のミノを格納する
        self.after_fall_mino_r=[]
        self.after_fall_mino_g=[]
        self.after_fall_mino_b=[]
    def drow(self):#壁を描画
        wall_rgb=50,50,50
        right_wall=0,0,200,800
        left_wall=400,0,200,800
        lower_wall=0,500,400,300
        upper_wall=0,0,400,80
        self.well.append(pygame.draw.rect(self.screen,(wall_rgb[0],wall_rgb[1],wall_rgb[2]),Rect(right_wall[0],right_wall[1],right_wall[2],right_wall[3])))
        self.well.append(pygame.draw.rect(self.screen,(wall_rgb[0],wall_rgb[1],wall_rgb[2]),Rect(left_wall[0],left_wall[1],left_wall[2],left_wall[3])))
        self.well.append(pygame.draw.rect(self.screen,(wall_rgb[0],wall_rgb[1],wall_rgb[2]),Rect(upper_wall[0],upper_wall[1],upper_wall[2],upper_wall[3])))
        self.well.append(pygame.draw.rect(self.screen,(wall_rgb[0],wall_rgb[1],wall_rgb[2]),Rect(lower_wall[0],lower_wall[1],lower_wall[2],lower_wall[3])))
        return(self.well)#衝突判定に使用するため戻り値にする
    def drow_fall_mino(self):#落下済みミノ描写
        for i in range(len(self.after_fall_mino)):

            pygame.draw.rect(self.screen,(self.after_fall_mino_r[i],self.after_fall_mino_g[i],self.after_fall_mino_b[i]),self.after_fall_mino[i])
    def after_fall_mino_add(self,after_fall_mino,control_mino_rgb):#落下済みミノ受け取り用
        rect_quantity=4
        for i in range(rect_quantity):
            self.after_fall_mino_r.append(control_mino_rgb[0][i])
            self.after_fall_mino_g.append(control_mino_rgb[1][i])
            self.after_fall_mino_b.append(control_mino_rgb[2][i])
        for mino in after_fall_mino:
            self.after_fall_mino.append(mino)
        #print(self.after_fall_mino)

    def after_fall_mino_clear(self):#ミノそろったときに消す
        tops=[]
        tops_loop=[]
        tops_index=[]
        clear_top=0
        clear_mino=0
        rect_fall=20
        kazu=0
        #print(len(self.after_fall_mino))
        for i in range (0,len(self.after_fall_mino)):#pygameの四角形(rect)を格納したオブジェクトは個々の値を参照する際メソッドを使用するので、メソッド[.index]を併用できず個々の値から添え字を調べられないので、リストtopsに値を格納してから調べる
            tops.append(self.after_fall_mino[i].top)
        #print(tops.count(420))
        tops_loop=list(dict.fromkeys(tops))#重複要素を削除したループ用リストを作成
        tops_loop.sort()#fromkeyは最小値から順でソートされないのでソートする
        for i in tops_loop:
            if tops.count(i)>=10:#同じ高さのブロックが10列並んだ時
                #print("ミノ数")
                clear_mino=clear_mino+1
                idx=-1
                for j in range(tops.count(i)):#消す予定のミノのインデックスを取得
                    idx = tops.index(i,idx+1)
                    tops_index.append(idx)
                list.sort(tops_index, reverse=True)
                clear_rect_top=[]
                for k in tops_index:#ミノを消す
                    self.after_fall_mino.pop(k)
                    self.after_fall_mino_r.pop(k)
                    self.after_fall_mino_g.pop(k)
                    self.after_fall_mino_b.pop(k)
                    clear_top=tops.pop(k)
                #print(clear_top)
                for j in range(len(self.after_fall_mino)):#消したミノより上のミノを1ブロック分落とす
                    if clear_top>self.after_fall_mino[j].top:
                        self.after_fall_mino[j].top=self.after_fall_mino[j].top+rect_fall
                        tops[j]=tops[j]+rect_fall
                tops_index=[]
        return(clear_mino)
    def after_fall_mino_pass(self):#落下済みミノ渡し用
        return(self.after_fall_mino)
    def well_pass(self):#落下済みミノ渡し用
        return(self.well)

class Score:#スコアの計算と表示
    def __init__(self):
        self.score=0
        self.ren=-1
        self.ren_score=50
    def computation (self,clear_mino):
        single_score=100
        double_score=300
        triple_score=500
        tetris_score=800

        if clear_mino == 1:
            self.ren=self.ren+1
            self.score=self.score+single_score+self.ren*self.ren_score
        elif clear_mino == 2:
            self.ren=self.ren+1
            self.score=self.score+double_score+self.ren*self.ren_score
        elif clear_mino == 3:
            self.ren=self.ren+1
            self.score=self.score+triple_score+self.ren*self.ren_score
        elif clear_mino == 4:
            self.ren=self.ren+1
            self.score=self.score+tetris_score+self.ren*self.ren_score
        else:
            self.ren=-1
    def show(self,screen):
        text_data="Score: "+str(self.score)
        font_size=50
        r=50
        g=50
        b=50
        x=800
        y=100
        text_show(screen,text_data,font_size,r,g,b,x,y)
        x=800
        y=200
        if self.ren>=1:#連続ボーナス表示は2連以上のみ表示
            text_data=self.ren+1
            text_data=str(text_data)+" 連続"
            text_show(screen,text_data,font_size,r,g,b,x,y)
            y=330
            x=800
            text_data="ボーナス+"+str(self.ren*50)
            text_show(screen,text_data,font_size,r,g,b,x,y)
class Tetriminol_I(Tetriminol):#I型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=0
        self.rect_g=255
        self.rect_b=255

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転
        spin_max=1
        spin_min=0
        if self.spin_pattern > spin_max:
            self.spin_pattern=0
        if self.spin_pattern < spin_min:
            self.spin_pattern=1

        if self.spin_pattern == 0:#
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*2,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*3,self.rect_size_x,self.rect_size_y)))

        else:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*2, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*3, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern < spin_min:
                    self.spin_pattern=1
                if self.spin_pattern > spin_max:
                    self.spin_pattern=0
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*2,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*3,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*2,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*3,self.rect_size_x,self.rect_size_y))

class Tetriminol_T(Tetriminol):#T型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=238
        self.rect_g=130
        self.rect_b=238

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転
        spin_max=3
        spin_min=0
        if self.spin_pattern > spin_max:
            self.spin_pattern=spin_min
        if self.spin_pattern < spin_min:
            self.spin_pattern=spin_max
        if self.spin_pattern == 0:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x, self.rect_start_y+self.app_y+self.rect_move_y,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 1:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*2,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 2:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 3:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*2,self.rect_size_x,self.rect_size_y)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern < spin_min:
                    self.spin_pattern=spin_max
                if self.spin_pattern > spin_max:
                    self.spin_pattern=spin_min
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x-self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x-self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))

class Tetriminol_S(Tetriminol):#S型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=0
        self.rect_g=255
        self.rect_b=0

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転
        spin_max=1
        spin_min=0
        if self.spin_pattern > spin_max:
            self.spin_pattern=spin_min
        if self.spin_pattern < spin_min:
            self.spin_pattern=spin_max
        if self.spin_pattern == 0:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        else:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern < spin_min:
                    self.spin_pattern=spin_max
                if self.spin_pattern > spin_max:
                    self.spin_pattern=spin_min
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x-self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x-self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))

class Tetriminol_S_R(Tetriminol):#逆S型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=255
        self.rect_g=0
        self.rect_b=0

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転
        spin_max=1
        spin_min=0
        if self.spin_pattern > spin_max:
            self.spin_pattern=spin_min
        if self.spin_pattern < spin_min:
            self.spin_pattern=spin_max
        if self.spin_pattern == 0:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        else:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*2,self.rect_size_x,self.rect_size_y)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern < spin_min:
                    self.spin_pattern=spin_max
                if self.spin_pattern > spin_max:
                    self.spin_pattern=spin_min
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*2, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*2, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))

class Tetriminol_sq(Tetriminol):#四角型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=255
        self.rect_g=255
        self.rect_b=0

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
        self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
        self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))

class Tetriminol_L(Tetriminol):#L型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=255
        self.rect_g=140
        self.rect_b=5

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転
        spin_max=3
        spin_min=0
        if self.spin_pattern > spin_max:
            self.spin_pattern=spin_min
        if self.spin_pattern < spin_min:
            self.spin_pattern=spin_max
        if self.spin_pattern == 0:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 1:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 2:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 3:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern < spin_min:
                    self.spin_pattern=spin_max
                if self.spin_pattern > spin_max:
                    self.spin_pattern=spin_min
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x-self.rect_move_x*0, self.rect_next_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x-self.rect_move_x*0, self.rect_hold_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))

class Tetriminol_L_R(Tetriminol):#逆L型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=0
        self.rect_g=0
        self.rect_b=150

    def drow(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転
        spin_max=3
        spin_min=0
        if self.spin_pattern > spin_max:
            self.spin_pattern=spin_min
        if self.spin_pattern < spin_min:
            self.spin_pattern=spin_max
        if self.spin_pattern == 0:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 1:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y-self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 2:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))
        elif self.spin_pattern == 3:
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*0, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x+self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern < spin_min:
                    self.spin_pattern=spin_max
                if self.spin_pattern > spin_max:
                    self.spin_pattern=spin_min
            if r_move==True:#右移動指示が出てれば戻す
                self.app_x=self.app_x-self.rect_move_x
            if l_move==True:
                self.app_x=self.app_x+self.rect_move_x
        return()
    def next_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x-self.rect_move_x*0, self.rect_next_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x+self.rect_move_x*0, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_next_x-self.rect_move_x*1, self.rect_next_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
    def hold_drow(self):
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y-self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x-self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x+self.rect_move_x*0, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))
        pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_hold_x-self.rect_move_x*1, self.rect_hold_y+self.rect_move_y*1,self.rect_size_x,self.rect_size_y))


class Pytetris:
    def __init__(self):
        """ゲームを初期化してゲームのリソースを作成する"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Tetris")
        self.bg_color = (150,150,150)

    def run_game(self):
        fall_flag=False
        fall_flag3=False
        control_mino="No instance"#操作ミノのインスタンス用、あとでランダムでミノのインスタンスを決定するので最初はインスタンス化しない
        hold_text="HOLD"
        hold_text_x=50
        hold_text_y=38
        hold_font_size=35
        hold_text_rgb=230,230,230
        next_text="NEXT"
        next_text_x=450
        next_text_y=38
        next_font_size=35
        next_text_rgb=230,230,230
        description_text="―――操作方法―――","→ :右移動","← :左移動","↑ :ハードドロップ","D  :右回転","A  :左回転","Q  :HOLD","","―――スコア表―――","1段揃え : +100","2段揃え : +300","3段揃え : +500","4段揃え : +800","連続揃え: +(連続揃え数*50)"
        description_text_x=30
        description_text_y=360
        description_font_size=15
        description_text_rgb=230,230,230
        description_text_app_y=20
        fall_mino=[]
        fall_flag2=False
        score=Score()
        field=Field_T()
        hold=Hold()
        hold_on=False#hold処理初回実行済みかどうか判定用
        mino_rgb=[]
        sleep_time=0.05
        sleep_fast_time=0
        hard_drop_sleep=0#ハードドロップ時スリープ時間、処理が重くてスリープ0秒でも違和感なく動くので0
        Fall_interval=10
        Fall_interval_use=0
        next_control_mino="No instance"#初期値設定しておかないとcreate_control_mino関数でエラーがでるので初期値を設定
        next_control_mino=create_control_mino(next_control_mino)

        while True:
            if fall_flag == True  or control_mino=="No instance" or fall_flag3==True and Fall_interval_use%Fall_interval == 0:
                control_mino=copy.copy(next_control_mino)
                next_control_mino=create_control_mino(next_control_mino)
                fall_flag=False
                fall_flag2=False
                fall_flag3=False
                time.sleep(sleep_fast_time)

            self.screen.fill(self.bg_color)#画面描画
            well=field.drow()#壁を描画して壁の位置を取得
            for i in range(len(description_text)):#操作説明描画
                text_show(self.screen,description_text[i],description_font_size,description_text_rgb[0],description_text_rgb[1],description_text_rgb[2],description_text_x,description_text_y+description_text_app_y*i)
            control_mino.drow()#操作ミノ描画
            next_control_mino.next_drow()#次の操作ミノ描画
            text_show(self.screen,next_text,next_font_size,next_text_rgb[0],next_text_rgb[1],next_text_rgb[2],next_text_x,next_text_y)
            field.drow_fall_mino()#落下済みミノ描画
            
            if  hold_on== True:
                hold.drow()#ホールド済みミノ描画
                text_show(self.screen,hold_text,hold_font_size,hold_text_rgb[0],hold_text_rgb[1],hold_text_rgb[2],hold_text_x,hold_text_y)

            """ミノの落下処理"""
            print(fall_flag2)
            if Fall_interval_use%Fall_interval == 0:#入力受付に対するミノの落下処理の頻度をきめる
                fall_flag3=control_mino.mino_fall(fall_flag2)#落下処理
                #pygame.display.flip()#画面更新
                """落下処理でミノが衝突したら操作ミノを落下済みミノのリストに移して、ミノの消去判定とスコア計算を行う"""
                if fall_flag3==True:
                    fall_mino=control_mino.after_fall_minos_pass()
                    mino_rgb=control_mino.rgb_pass()
                    field.after_fall_mino_add(fall_mino,mino_rgb)
                    control_mino.after_fall_minos_clear()

                    score.computation(field.after_fall_mino_clear())
                    fall_flag=True

            score.show(self.screen)
            Fall_interval_use=Fall_interval_use+1

            pygame.display.flip()#画面更新
            fall_flag2=control_mino.mino_fall_check(field.well_pass(),field.after_fall_mino_pass())
            flag=control_mino.move(field.well_pass(),field.after_fall_mino_pass(),control_mino)#入力判定、入力に応じて移動したミノがぶつかっていないかの判定など
            if flag[0]==True:#ハードドロップ入力判定
                time.sleep(hard_drop_sleep)
            else:
                time.sleep(sleep_time)

            if flag[1] == True:#ホールド入力判定
                control_mino=hold.swap(control_mino)
                if control_mino != "No instance":
                    control_mino=hold.swap_check(control_mino,field.well_pass(),field.after_fall_mino_pass())
                hold_on=True




if __name__=="__main__":#このプロシャージャがインポートされたものでなく直接呼び出されたときのみ下記を実行
    py = Pytetris()
    py.run_game()

