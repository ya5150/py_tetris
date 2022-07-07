from msvcrt import kbhit
#from re import I
import sys
from tokenize import single_quoted
import pygame
import time
from pygame.locals import *
import copy
import random
#class Tetris_field

def move_check(mino,well,after_fall_minos):#ミノと壁が衝突するか判定,引数に複数クラスの要素を要求するためクラス外に
    flag = False
    tops=[]
    for i in mino:#動いている4つのミノの衝突確認
        if i.collidelist(well) != -1:#壁衝突
            flag = True
        if i.collidelist(after_fall_minos) != -1:#おかれたブロック
            flag = True
    #print(flag)
    return(flag)

def text_show(screen,text_data,font_size,r,g,b,x,y):
    font = pygame.font.Font(None,font_size)
    text = font.render(str(text_data), True, (r,g,b))   # 描画する文字列の設定
    screen.blit(text, [x,y])# 文字列の表示位置

def create_control_mino(next_control_mino):#ランダムで操作ミノのインスタンスを作成
    randam_nam=random.uniform(0,7)
    i=0
    if randam_nam <1:#スイッチ文に書き換える
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

class Hold:#ホールド
    def __init__(self):
        self.hold_rect=0
        self.hold_rect_back=0
        #self.hold_rect_r
        #self.hold_rect_g
        #self.hold_rect_b

    def swap(self,hold_rect):
        if self.hold_rect!=0:
            self.hold_rect_back=copy.copy(self.hold_rect)
            self.hold_rect=copy.copy(hold_rect)
            if self.hold_rect_back!=0:
                self.hold_rect_back.app_x=hold_rect.app_x
                self.hold_rect_back.app_y=hold_rect.app_y
            return(self.hold_rect_back)
        else:
            self.hold_rect=copy.copy(hold_rect)
            return(self.hold_rect_back)
    def view(self):
        self.hold_rect.hold_drow()
class Tetriminol:#操作ミノに関するクラス
    def __init__(self):
        self.rect_start_x=300
        self.rect_start_y=100
        self.rect_size_x=20
        self.rect_size_y=21
        self.rect_move_x=20
        self.rect_move_y=20
        self.rect_next_x=700
        self.rect_next_y=100
        self.rect_hold_x=900
        self.rect_hold_y=700
        self.screen = pygame.display.set_mode((1200,800))
        self.spin_pattern=0
        self.spin_direction=0#回転方向の命令 -1は左回転、0は回転しない,１は右回転
        self.mino=[]#操作中のミノ4つを格納する
        self.well=[]#4方向の壁を格納する
        self.immediately_after_creation=True #操作ミノ作成直後かどうかの判定
        self.app_y=0
        self.app_x=0
        self.after_fall_minos=[]
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
        self.key_sensitivity=2
    def mino_fall(self,well,after_fall_minos):
        fall=False
        if move_check(self.mino,well,after_fall_minos) == False:
            self.app_y=self.app_y+20
        else:#操作ミノ着地時、操作ミノを落下済みミノのリストに入れ落下済みフラグをtrueに
            if self.immediately_after_creation==True:#操作ミノ作成直後に他ブロックと接触していたらゲームオーバ
                print("END")
            for mino in self.mino:
                self.after_fall_minos.append(mino)
            fall=True
        self.immediately_after_creation=False
        return(fall)

    def after_fall_minos_pass(self):
        return(self.after_fall_minos)
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
            if self.key_sensitivity%3 == 0:
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
                    #self.key_down_d == False#連続入力対策
                if self.key_down_a == True:
                    self.drow(well,after_fall_mino,+1)#-1は左回転
                    #self.key_down_a == False
                if self.key_down_q == True:#ホールド処理は操作ミノのクラス外なのでholdクラスで処理
                    self.hold=True
                if self.key_down_up == True:#
                    self.hard_dorp=True
            return(self.hard_dorp,self.hold)

class Field_T(Tetriminol):#壁や落下後のテトリミノに関する処理
    def __init__(self):
        super().__init__()
        self.after_fall_mino=[]#落下後のミノを格納する
    def drow(self):#壁を描画
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(0,0,200,800)))#壁
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(400,0,200,800)))#左の壁
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(0,499,400,300)))#下の壁
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(0,0,400,80)))#上の壁
        return(self.well)#衝突判定に使用するため戻り値にする

    def drow_fall_mino(self):#落下済みミノ描写
        for mino in self.after_fall_mino:
            pygame.draw.rect(self.screen,(10,100,10),mino)

    def after_fall_mino_add(self,after_fall_mino):#落下済みミノ受け取り用
        for mino in after_fall_mino:
            self.after_fall_mino.append(mino)

    def after_fall_mino_clear(self):#ミノそろったときに消す
        tops=[]
        tops_loop=[]
        tops_index=[]
        clear_top=0
        clear_mino=0
        for i in range (0,len(self.after_fall_mino)):#pygameの四角形(rect)を格納したオブジェクトは個々の値を参照する際メソッドを使用するので、メソッド[.index]を併用できず個々の値から添え字を調べられないので、リストtopsに値を格納してから調べる
            tops.append(self.after_fall_mino[i].top)
        #print(tops.count(420))
        tops_loop=list(dict.fromkeys(tops))#重複要素を削除したループ用リストを作成
        for i in tops_loop:
            if tops.count(i)>=5:#同じ高さのブロックが10列並んだ時
                clear_mino=clear_mino+1
                idx=-1
                for j in range(tops.count(i)):#消す予定のミノのインデックスを取得
                    idx = tops.index(i,idx+1)
                    tops_index.append(idx)
                list.sort(tops_index, reverse=True)
                clear_rect_top=[]

                for k in tops_index:#ミノを消す
                    self.after_fall_mino.pop(k)
                    #clear_rect_top.append(tops.pop(k))
                    clear_top=tops.pop(k)

                for j in range(len(self.after_fall_mino)):#消したミノより上のミノを1ブロック分落とす
                    if clear_top>self.after_fall_mino[j].top:
                        self.after_fall_mino[j].top=self.after_fall_mino[j].top+20
                        tops[j]=tops[j]+20
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
        if self.ren>=1:
            text_data=self.ren+1
            text_data=str(text_data)+" REN"
            text_show(screen,text_data,font_size,r,g,b,x,y)
            x=900
            text_data="Bonus + "+str(self.ren*50)
            text_show(screen,text_data,font_size,r,g,b,x,y)
class Tetriminol_I(Tetriminol):#I型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_r=100
        self.rect_g=100
        self.rect_b=200

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

        else:#I型テトリミノが横方向の時のミノの配置
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
        self.rect_r=150
        self.rect_g=200
        self.rect_b=150

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
        self.rect_r=150
        self.rect_g=200
        self.rect_b=150

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
            self.mino.append(pygame.draw.rect(self.screen,(self.rect_r,self.rect_g,self.rect_b),Rect(self.rect_start_x+self.app_x-self.rect_move_x*1, self.rect_start_y+self.app_y+self.rect_move_y*0,self.rect_size_x,self.rect_size_y)))
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
        self.rect_r=150
        self.rect_g=200
        self.rect_b=150

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
        self.rect_r=150
        self.rect_g=150
        self.rect_b=150

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
        self.rect_r=150
        self.rect_g=200
        self.rect_b=150

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
        self.rect_r=150
        self.rect_g=200
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


class AlienInvasion:
    def __init__(self):
        """ゲームを初期化してゲームのリソースを作成する"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Tetris")
        self.bg_color = (230,230,100)

    def run_game(self):
        fall_flag=True#操作しているミノが落下済みまたはループ初回時かどうか
        control_mino=0
        fall_mino=[]
        score=Score()
        field=Field_T()
        hold=Hold()
        hold_on=False
        sleep_time=0.05
        sleep_fast_time=0
        hard_drop_sleep=0.001
        Fall_interval=8
        Fall_interval_use=0
        next_control_mino=0
        next_control_mino=create_control_mino(next_control_mino)

        while True:
            if fall_flag==True and Fall_interval_use%Fall_interval == 0 or control_mino==0:
                control_mino=copy.copy(next_control_mino)
                next_control_mino=create_control_mino(next_control_mino)
                #next_control_mino=create_control_mino(next_control_mino)
                #i=Tetriminol_I()
                #control_mino=copy.copy(i)
                fall_flag==False
                time.sleep(sleep_fast_time)
            self.screen.fill(self.bg_color)#画面クリア
            control_mino.drow()
            next_control_mino.next_drow()
            field.drow_fall_mino()
            well=field.drow()
            if  hold_on== True:
                hold.view()


            if Fall_interval_use%Fall_interval == 0:
                fall_flag=control_mino.mino_fall(well,field.after_fall_mino_pass())
                if fall_flag==True:
                    fall_mino=control_mino.after_fall_minos_pass()
                    field.after_fall_mino_add(fall_mino)
                    score.computation(field.after_fall_mino_clear())
                    #fall_flag==False
            score.show(self.screen)
            Fall_interval_use=Fall_interval_use+1

            pygame.display.flip()#画面描画
            flag=control_mino.move(field.well_pass(),field.after_fall_mino_pass(),control_mino)#回転可能かどうかなど試す際に配置するミノを描画したくないので画面クリア直前に配置
            if flag[0]==True:#ハードドロップ入力判定
                time.sleep(hard_drop_sleep)
            else:
                time.sleep(sleep_time)

            if flag[1] == True:#ホールド入力判定
                control_mino=hold.swap(control_mino)
                hold_on=True




if __name__=="__main__":#このプロシャージャがインポートされたものでなく直接呼び出されたときのみ下記を実行
    ai = AlienInvasion()
    ai.run_game()

