from io import BytesIO
import base64
import PIL.Image
import PIL.ImageTk
import tkinter as tk
import copy

import resources

deer = PIL.Image.open(BytesIO(base64.decodebytes(resources.deer_sad)))
icon = PIL.Image.open(BytesIO(base64.decodebytes(resources.crown)))

class Piece:
    arr = []
    x = 0
    y = 0
    def __init__(self, _list, _x, _y):
        self.arr = _list
        self.x = _x
        self.y = _y

    def size(self):
        return len(self.arr)

    def __getitem__(self, key):
        return self.arr[key]

class point:
    x = 0
    y = 0
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

def print_piece(piece): # For debugging purposes only
    print("")
    for y in range(piece.y):
        for x in range(piece.x):
            cell = piece[x + piece.x*y]
            if cell != 0:
                print("# ", end = "")
            else:
                print(". ", end = "")
        print("")

def calculate_moves(points): # Calculates total possible moves
    total = 1
    for point in points:
        total = total * point.x * point.y
    return total

def accept_move(board, piece, x_offset, y_offset): # Applies piece to the board
    for y in range(piece.y):
        for x in range(piece.x):
            index = x + y*piece.x
            offset_index = (x + x_offset) + (y + y_offset)*board.x
            if piece[index] == 1:
                board.arr[offset_index] = 1*(board[offset_index] == 0)  # Needs modification in case of multiple shape implementation

def next_combination(pointlist, positions): # Modifies the move sequence to applie. Advances 1 iteration.
    for i in range(len(pointlist)):
        if i == 0:
            pointlist[i].x = (pointlist[i].x + 1) % positions[i].x
            if pointlist[i].x == 0:
                pointlist[i].y = (pointlist[i].y + 1) % positions[i].y
        else:
            for k in range(i):
                if pointlist[k].x == 0 and pointlist[k].y == 0:
                    pointlist[i].x = (pointlist[i].x + 1) % positions[i].x
                    if pointlist[i].x == 0:
                        pointlist[i].y = (pointlist[i].y + 1) % positions[i].y
                else:
                    break

def solver(pieces, board, solution_coords):
    solved = True

    positions = []
    for piece in pieces:
        x_positions = 1 + board.x - piece.x
        y_positions = 1 + board.y - piece.y
        positions.append(point(x_positions, y_positions))

    for i in range(len(positions)):
        solution_coords.append(point(0,0))
    
    movecount = calculate_moves(positions)

    num = 0
    while num < movecount:
        solved = True
        playboard = Piece(copy.copy(board.arr), board.x, board.y)

        for i in range(len(pieces)):
            accept_move(playboard, pieces[i], solution_coords[i].x, solution_coords[i].y)
        
        for k in range(board.size()):
            solved = solved * playboard[k]  # Needs modification in case of multiple shape implementation
        if solved:
            break

        next_combination(solution_coords, positions)

        num = num + 1
    if solved:
        return True
    else:
        return False

class GUI:
    boardpiece = Piece([0], 0, 0)
    bufferpiece = Piece([0], 0, 0)
    pieces = []
    piece_count = 0
    total_pieces = 0
    solution = []

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x620")
        self.root.title("Shapeshifter Solver")
        self.root.resizable(False, False)

        tkicon = PIL.ImageTk.PhotoImage(icon)
        self.root.iconphoto(True, tkicon)

        # Title
        self.titlelabel = tk.Label(self.root, text="Shapeshifter Solver", font=('Arial', 18))
        self.titlelabel.pack(padx=10, pady=10)

        self.contextlabel = tk.Label(self.root, text="Board starting state", font=('Arial', 16))
        self.contextlabel.pack()

        # Starting data
        self.dataFrame = tk.Frame(self.root)
        self.dataFrame.columnconfigure(0, weight=1)
        self.dataFrame.columnconfigure(1, weight=1)
        self.dataFrame.columnconfigure(2, weight=1)

        self.label1 = tk.Label(self.dataFrame, text="Width", font=('Arial', 16))
        self.label1.grid(row=0, column=0, sticky="we")
        self.textbox1 = tk.Text(self.dataFrame, height = 1, font=('Arial', 12))
        self.textbox1.grid(row=1, column=0, padx=30)
        self.textbox1.insert(tk.END, "0")
        self.label2 = tk.Label(self.dataFrame, text="Height", font=('Arial', 16))
        self.label2.grid(row=0, column=1, sticky="we")
        self.textbox2 = tk.Text(self.dataFrame, height = 1, font=('Arial', 12))
        self.textbox2.grid(row=1, column=1, padx=30)
        self.textbox2.insert(tk.END, "0")
        self.label3 = tk.Label(self.dataFrame, text="No. of pieces", font=('Arial', 16))
        self.label3.grid(row=0, column=2, sticky="we")
        self.textbox3 = tk.Text(self.dataFrame, height = 1, font=('Arial', 12))
        self.textbox3.grid(row=1, column=2, padx=30)
        self.textbox3.insert(tk.END, "0")
        self.dataFrame.pack(padx=100)
        self.textbox1.bind("<KeyRelease>", lambda event: self.create_buttons(self.boardpiece, w=int(self.textbox1.get('1.0', tk.END)), h=int(self.textbox2.get('1.0', tk.END))))
        self.textbox2.bind("<KeyRelease>", lambda event: self.create_buttons(self.boardpiece, w=int(self.textbox1.get('1.0', tk.END)), h=int(self.textbox2.get('1.0', tk.END))))

        # Sad Deer
        tkimage = PIL.ImageTk.PhotoImage(deer)
        
        # Create Canvas 
        self.canvas = tk.Canvas(self.root, width = 450, height = 450) 
        self.canvas.pack(fill = "both", expand = True) 
        # Display image 
        self.canvas.create_image(300, 200, image = tkimage) 

        # Button Grid
        self.btngridFrame = tk.Frame(self.canvas)

        self.bottom = tk.Frame(self.canvas)
        self.bottom.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        self.bottom.columnconfigure(0, weight=1, uniform="javier")
        self.bottom.columnconfigure(1, weight=1, uniform="javier")
        self.bottom.columnconfigure(2, weight=1, uniform="javier")

        self.button = tk.Button(self.bottom, text="Accept Board", font=('Arial', 16), command=self.next)
        self.button.grid(row=0, column=1, padx=30)
        
        self.RestartBtn = tk.Button(self.bottom, text="Restart", font=('Arial', 16), command=self.restart)
        self.RestartBtn.grid(row=0, column=2, padx=30)

        self.root.mainloop()

    def next(self):
        match self.button["text"]:
            case "Accept Board":
                if int(self.textbox3.get('1.0', tk.END)) > 0:
                    w = int(self.textbox1.get('1.0', tk.END))
                    h = int(self.textbox2.get('1.0', tk.END))
                    if w <= 15 and h <= 15 and w*h > 0:
                        self.total_pieces = int(self.textbox3.get('1.0', tk.END))
                        
                        # Clear the scene
                        for widget in self.dataFrame.winfo_children():
                            widget.destroy()
                        for widget in self.btngridFrame.winfo_children():
                            widget.destroy()
                        
                        # Set the scene
                        self.dataFrame.columnconfigure(0, weight=1)
                        self.dataFrame.columnconfigure(1, weight=1)
                        self.label1 = tk.Label(self.dataFrame, text="Width", font=('Arial', 16))
                        self.label1.grid(row=0, column=0, sticky="we")
                        self.textbox1 = tk.Text(self.dataFrame, height = 1, font=('Arial', 12))
                        self.textbox1.grid(row=1, column=0, padx=30)
                        self.label2 = tk.Label(self.dataFrame, text="Height", font=('Arial', 16))
                        self.label2.grid(row=0, column=1, sticky="we")
                        self.textbox2 = tk.Text(self.dataFrame, height = 1, font=('Arial', 12))
                        self.textbox2.grid(row=1, column=1, padx=30)
                        self.textbox1.delete(1.0, tk.END)
                        self.textbox2.delete(1.0, tk.END)
                        self.textbox1.insert(tk.END, "0")
                        self.textbox2.insert(tk.END, "0")
                        self.contextlabel["text"] = "Piece " + str(self.piece_count + 1)
                        self.button["text"] = "Next Piece"

                        # Bind command to Text widget
                        self.textbox1.bind("<KeyRelease>", lambda event: self.create_buttons(self.bufferpiece, w=int(self.textbox1.get('1.0', tk.END)), h=int(self.textbox2.get('1.0', tk.END))))
                        self.textbox2.bind("<KeyRelease>", lambda event: self.create_buttons(self.bufferpiece, w=int(self.textbox1.get('1.0', tk.END)), h=int(self.textbox2.get('1.0', tk.END))))
                else:
                    print("Number of pieces must be higher than 0")
            case "Next Piece":
                # Setting up the scene
                for widget in self.btngridFrame.winfo_children():
                    widget.destroy()
                
                self.textbox1.delete(1.0, tk.END)
                self.textbox2.delete(1.0, tk.END)
                self.textbox1.insert(tk.END, "0")
                self.textbox2.insert(tk.END, "0")

                self.pieces.append(Piece(copy.copy(self.bufferpiece.arr), self.bufferpiece.x, self.bufferpiece.y))

                self.piece_count = self.piece_count + 1
                self.contextlabel["text"] = "Piece " + str(self.piece_count + 1)
                
                # When the last piece is created
                if self.piece_count == self.total_pieces:
                    # Clear the scene
                    for widget in self.dataFrame.winfo_children():
                        widget.destroy()
                    for widget in self.btngridFrame.winfo_children():
                        widget.destroy()
                    
                    # Solving puzzle with given board and pieces
                    if solver(self.pieces, self.boardpiece, self.solution):
                        self.contextlabel["text"] = "Solution found!"
                        self.piece_count = 0

                        self.contextlabel2 = tk.Label(self.dataFrame, text="Move " + str(self.piece_count + 1) + ":", font=('Arial', 16))
                        self.contextlabel2.pack()

                        # Making the solution grid
                        self.btns = []
                        i = 0
                        for y in range(self.boardpiece.y):
                            for x in range(self.boardpiece.x):
                                color = "red" if (x == self.solution[self.piece_count].x and y == self.solution[self.piece_count].y) else "lightgray"
                                self.btns.append(tk.Button(self.btngridFrame, bg=color, width=3))
                                self.btns[i].grid(row=y, column=x, sticky="nsew")
                                i = i + 1
                        self.btngridFrame.pack(pady=10)
                        self.piece_count = self.piece_count + 1

                        self.button["text"] = "Next"
                    else:
                        self.contextlabel["text"] = "Solution not found"
                        self.button.destroy()

            case "Next":
                # Setting up the scene
                for widget in self.btngridFrame.winfo_children():
                    widget.destroy()

                self.contextlabel2["text"] = "Move " + str(self.piece_count + 1) + ":"

                # Making the solution grid
                self.btns = []
                i = 0
                for y in range(self.boardpiece.y):
                    for x in range(self.boardpiece.x):
                        color = "red" if (x == self.solution[self.piece_count].x and y == self.solution[self.piece_count].y) else "lightgray"
                        self.btns.append(tk.Button(self.btngridFrame, bg=color, width=3))
                        self.btns[i].grid(row=y, column=x, sticky="nsew")
                        i = i + 1
                self.btngridFrame.pack(pady=10)
                self.piece_count = self.piece_count + 1

                if self.piece_count == self.total_pieces:
                    self.button.destroy()

    def create_buttons(self, piece, w, h):
        # Clear the array and fill it with zeros
        piece.arr.clear()
        piece.x = w
        piece.y = h

        # Start button grid over
        for widget in self.btngridFrame.winfo_children():
            widget.destroy()
        # Create the new button grid
        self.btns = []
        if w <= 15 and h <= 15 and w*h > 0:
            i = 0
            for y in range(h):
                for x in range(w):
                    self.btns.append(tk.Button(self.btngridFrame, bg="lightgray", width=3))
                    self.btns[i]["command"] = lambda p = piece, b = self.btns[i], x=x, y=y: self.toggle_button(p, b, x, y)
                    self.btns[i].grid(row=y, column=x, sticky="nsew")
                    if self.button["text"] == "Accept Board":
                        piece.arr.append(1) # I chose that the winning state is a board full of 1s like a sillycoded dummy
                    else:
                        piece.arr.append(0)
                    i = i + 1
            
            self.btngridFrame.pack(pady=10)
        
    def toggle_button(self, piece, button, x, y):
        current_color = button.cget("bg")
        new_color = "red" if current_color == "lightgray" else "lightgray"
        button.config(bg=new_color)

        index = x + piece.x*y
        current_value = piece.arr[index]
        piece.arr[index] = 0 if current_value == 1 else 1

    def restart(self):
        self.boardpiece = Piece([0], 0, 0)
        self.bufferpiece = Piece([0], 0, 0)
        self.pieces = []
        self.piece_count = 0
        self.total_pieces = 0
        self.solution = []

        self.root.destroy()
        self.__init__()
        self.root.mainloop()

def main():
    GUI()

if __name__ == "__main__":
    main()
