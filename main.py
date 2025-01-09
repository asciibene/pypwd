
# Password Manager
import os
import sys
import curses as nc
import _sha3

import hashlib


if __name__ == "main":
    proto_LoginData={"login":"","passwd":"","host":""}

    wrapper(main) 

def main(stdscr):
    menitm={"File": ["New Password","Exit"],"Database":["Save to Disk"]}
    ui=UI(menitm)
    db=PasswordDB()
    db.newlogindata()
    #main loop
    ui.draw()


class PasswordDB:
    filepath="./passwd.db"
    entries=[]
    
    def __init__(self):
        #Restore data from @filepath
        self.fh=open(self.filepath,"r")
        fdata=self.fh.read()
        flines=fdata.splitlines()
        entry={}
        i=0
        for l in flines:
            if l == "--------------------------------" and i==2:
                #Separator hit
                self.entries.append(entry)
                entry={}
            else:
                if i == 0:
                    
                elif i == 1:
                    pass
                elif i == 2:
                    pass
                    
                    
    
    def savetodisk_cleartext(self):
        """Dont Encrypt but Save the obj's entries into @filepath IN cleartext"""
        self.fh=open(self.filepath,"w")
        for e in entries:
            h = e["host"]
            self.fh.write(f"** {h} **")
            l = e["login"]
            self.fh.write(f"{l}")
            p = e["passwd"]
            self.fh.write(f"{p}")
            self.fh.write("--------------------------------")


    def newlogindata(self):
        """ldarray is login data array (proto_LoginData)"""
        in_h=input("Enter Host:")
        in_l = input("Enter login")
        in_p = input("Enter Pwd")
        self.entries.append({"host": in_h,"login": in_l,"passwd": in_p})
        self.savetodisk_cleartext()


class UI:
    drop_width = {}
    drop_xpos = {} 
    keybinds={}
    color_selected=2
    def __init__(self,itemlst):
        self.menu_items=itemlst
        self.keybinds={it[0]: it for it in self.menu_items}
        self.main_items=list(self.menu_items)
        for mainitem in self.main_items:
            self.drop_width[mainitem] = 0
            self.drop_xpos[mainitem] = 0
        #Figure out the dropdown top-left corner position along the x Axis
        #(Done easily by checking the position of item's first letter in the following string:
        self.menu_str = "   ".join(self.main_items)
        for mainitem in self.main_items:
            self.drop_xpos[mainitem] = self.menu_str.find(mainitem)
            for subitem in self.menu_items[mainitem]:
                if len(subitem)+1 > self.drop_width[mainitem]:
                    self.drop_width[mainitem] = len(subitem)+1

    def draw(self,stdscr):
        stdscr.addstr(0,0,self.menu_str,curses.A_STANDOUT)
    
    def dropdown(self,stdscr,mainitem):
        menuctrl=True
        selection_ypos=1
        selected_item=None
        
        # Take care of drawing the dropdown
        while menuctrl:
            stdscr.addstr(0,0,self.menu_str,curses.A_STANDOUT)
            stdscr.addstr(0,self.drop_xpos[mainitem],mainitem)
            ypos=1
            for subitem in self.menu_items[mainitem]:
                if ypos != selection_ypos:
                    stdscr.addstr(ypos,self.drop_xpos[mainitem],subitem.ljust(self.drop_width[mainitem]),curses.A_REVERSE)
                elif ypos == selection_ypos:
                    stdscr.addstr(ypos,self.drop_xpos[mainitem],subitem.ljust(self.drop_width[mainitem]),curses.color_pair(self.color_selected))
                ypos=ypos+1
            # Key bindings to react to input below...
            inkey=stdscr.getch()
            if inkey == curses.KEY_UP and selection_ypos > 1:
                selection_ypos=selection_ypos-1
            elif inkey==curses.KEY_DOWN and selection_ypos < len(self.menu_items[mainitem]):
                selection_ypos=selection_ypos+1
            elif inkey == curses.KEY_LEFT and self.main_items.index(mainitem) >= 1 :
                stdscr.clear()
                mainitem = self.main_items[self.main_items.index(mainitem)-1]
            elif inkey == curses.KEY_RIGHT and self.main_items.index(mainitem) < len(self.main_items)-1:
                stdscr.clear()
                mainitem = self.main_items[self.main_items.index(mainitem)+1]
            elif inkey==10: # key : ENTER
                selected_item=self.menu_items[mainitem][selection_ypos-1] 
                return selected_item
            stdscr.refresh()


