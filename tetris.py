from msvcrt import kbhit
from re import I
import sys
import pygame
import time
# -*- coding:utf-8 -*-
from pygame.locals import *
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

def spin_check(mino,well,after_fall_mino,):
    print(f"{mino}\n\n{well}\n\n{after_fall_mino}\m")

class Tetriminol:#操作ミノに関するクラス
    def __init__(self):
        self.rect_start_x=300
        self.rect_start_y=100
        self.rect_h=15
        self.rect_w=13
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
        self.key_down_r=False
        self.key_down_l=False
        self.key_down_d=False
        self.key_down_a=False
        self.key_down_up=False
        self.key_sensitivity=0
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

    def move(self,well,after_fall_mino):
            """キー入力の監視"""
            for event in  pygame.event.get():
                """event=キー入力などユーザーの操作"""
                if event.type == pygame.QUIT:#終了
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:#右移動
                        self.key_down_r=True
                    elif event.key == pygame.K_LEFT:#左移動
                        self.key_down_l=True
                    elif event.key == pygame.K_d:#左回転
                        self.key_down_d=True
                    elif event.key == pygame.K_a:#右回転
                        self.key_down_a == True
                    elif event.key == pygame.K_UP:#ハードドロップ
                        self.key_down_up=True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.key_down_r= False
                    elif event.key == pygame.K_LEFT:
                        self.key_down_l= False
                    elif event.key == pygame.K_d:
                        self.key_down_d = False
                    elif event.key == pygame.K_a:
                        self.key_down_a = False
                    elif event.key == pygame.K_UP:
                        self.key_down_up = False
            """キー入力に対応した操作ミノの動作"""
            #if self.key_sensitivity%2 == 0:
            if self.key_down_r == True:
                self.app_x=self.app_x+20
                self.spin(well,after_fall_mino,r_move=True)
            elif self.key_down_l == True:
                self.app_x=self.app_x-20
                self.spin(well,after_fall_mino,l_move=True)
            elif self.key_down_d == True:
                self.spin(well,after_fall_mino,+1)#＋1は右回転
            elif self.key_down_a == True:
                self.spin(well,after_fall_mino,-1)#-1は左回転
            elif self.key_down_up == True:
                    self.hard_dorp=True
            pygame.event.clear()
            #self.key_sensitivity=self.key_sensitivity+1
            return(self.hard_dorp)


    def move_check(self,mino,well):#ミノと壁が衝突するか判定
        flag = False #衝突判定用フラグ
        for i in mino:#動いている4つのミノが壁に接触しているか確認する
            if i.collidelist(well) != -1:#衝突したときにフラグをtrueに
                flag = True
        return(flag)


class Field_T(Tetriminol):#壁や落下後のテトリミノに関する処理
    def __init__(self):
        super().__init__()
        self.after_fall_mino=[]#落下後のミノを格納する
    def drow(self):#壁を描画
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(0,0,200,800)))#上の壁
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(400,0,200,800)))#左の壁
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(0,499,400,300)))#下の壁
        self.well.append(pygame.draw.rect(self.screen,(50,50,50),Rect(0,0,400,99)))#右の壁
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
        renzoku=0
        for i in range (0,len(self.after_fall_mino)):#pygameの四角形(rect)を格納したオブジェクトは個々の値を参照する際メソッドを使用するので、メソッド[.index]を併用できず個々の値から添え字を調べられないので、リストtopsに値を格納してから調べる
            tops.append(self.after_fall_mino[i].top)
        #print(tops.count(420))
        tops_loop=list(dict.fromkeys(tops))#重複要素を削除したループ用リストを作成
        for i in tops_loop:
            if tops.count(i)>=5:#同じ高さのブロックが10列並んだ時
                renzoku=renzoku+1
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

    def after_fall_mino_pass(self):#落下済みミノ渡し用
        return(self.after_fall_mino)
    def well_pass(self):#落下済みミノ渡し用
        return(self.well)

class Tetriminol_I(Tetriminol):#I型テトリミノ
    def __init__(self):
        super().__init__()
        self.rect_i_r=50
        self.rect_i_g=50
        self.rect_i_b=200
        self.spin_i=1

    def spin(self,well=[],after_fall_mino=[],spin_order=0,r_move=False,l_move=False):#I型テトリミノの描画
        self.mino=[]
        self.spin_pattern=self.spin_pattern+spin_order#spin_order+1で右回転,-1で左回転

        if self.spin_pattern >=2:
            self.spin_pattern=0
        if self.spin_pattern <=-1:
            self.spin_pattern=1

        if self.spin_pattern == 0:#I型テトリミノが縦方向の時のミノの配置
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x, self.rect_start_y+self.app_y,20,21)))
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x, self.rect_start_y+self.app_y+20,20,21)))
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x, self.rect_start_y+self.app_y+40,20,21)))
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x, self.rect_start_y+self.app_y+60,20,21)))

        else:#I型テトリミノが横方向の時のミノの配置
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x, self.rect_start_y+self.app_y,20,21)))
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x+20, self.rect_start_y+self.app_y,20,21)))
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x+40, self.rect_start_y+self.app_y,20,21)))
            self.mino.append(pygame.draw.rect(self.screen,(100,100,200),Rect(self.rect_start_x+self.app_x+60, self.rect_start_y+self.app_y,20,21)))

        if move_check(self.mino,well,after_fall_mino)==True:#ブロックが接触していた場合
            if  spin_order!=0:#回転指示が出ていれば回転前に
                self.spin_pattern=self.spin_pattern-spin_order
                if self.spin_pattern <=-1:
                    self.spin_pattern=1
                if self.spin_pattern >=2:
                    self.spin_pattern=0
            if r_move==True:#右移動指示が出ていれば
                self.app_x=self.app_x-20
            if l_move==True:
                self.app_x=self.app_x+20
        return()


class AlienInvasion:
    def __init__(self):
        """ゲームを初期化してゲームのリソースを作成する"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("エイリアン襲撃")
        self.bg_color = (230,230,100)

    def run_game(self):
        """ゲームのメインループを開始する"""
        x=0
        t=0
        y=0
        spin=0
        fall_flag=True#操作しているミノが落下済みまたはループ初回時かどうか
        control_mino=0
        fall_mino=[]
        fall_mino2=[]
        field=Field_T()
        sleep_time=0.3
        hard_drop_sleep=0.02
        while True:

            #画面の描写
            if fall_flag==True:
                control_mino=Tetriminol_I()
                fall_flag==False
                time.sleep(sleep_time*0.3)

            self.screen.fill(self.bg_color)#画面クリア
            #mino=control_mino.spin(300+x,100+y,spin)
            control_mino.spin()
            field.drow_fall_mino()
            well=field.drow()
            #spin=i.spin(300+x,y,spin)

            fall_flag=control_mino.mino_fall(well,field.after_fall_mino_pass())
            if fall_flag==True:
                fall_mino=control_mino.after_fall_minos_pass()
                #field.after_fall_mino_add(fall_mino[len(fall_mino)-4:])
                field.after_fall_mino_add(fall_mino)
                field.after_fall_mino_clear()

            t=t+1

            pygame.display.flip()#画面描画
            flag=control_mino.move(field.well_pass(),field.after_fall_mino_pass())#回転可能かどうか試す際に配置するミノを描画したくないので画面クリア直前に配置
            if flag==True:
                time.sleep(hard_drop_sleep)
            else:
                time.sleep(sleep_time)


if __name__=="__main__":#このプロシャージャがインポートされたものでなく直接呼び出されたときのみ下記を実行
    ai = AlienInvasion()
    ai.run_game()

