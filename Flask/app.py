from flask import Flask, render_template
from tkinter import *
import PIL
from PIL import ImageGrab
import model
import cv2


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home1.html')


@app.route('/intro')
def intro():
    return render_template('intro.html')


@app.route('/launch', methods=['GET', 'POST'])
def launch():
    class Main:
        def __init__(self, master):
            self.master = master
            self.res = ""
            self.pre = [None, None]
            self.bs = 4.5
            self.c = Canvas(self.master, bd=3, relief="ridge", width=400, height=400, bg='white')
            self.c.pack(side=LEFT)
            f1 = Frame(self.master, padx=5, pady=5)
            Label(f1, text="Maths Tutor for shape", fg="red", font=("", 15, "bold")).pack(pady=10)
            Label(f1, text="Draw a shape to get its formula", fg="red", font=("", 15)).pack()
            Label(f1, text="(Circle,Square,Triangle)", fg="red", font=("", 15)).pack()
            self.pr = Label(f1, text="Prediction: None", fg="red", font=("", 20, "bold"))
            self.pr.pack(pady=20)

            Button(f1, font=("", 15), fg="white", bg="red", text="Clear Canvas",
                   command=self.clear).pack(side=BOTTOM)

            f1.pack(side=RIGHT, fill=Y)
            self.c.bind("<Button-1>", self.putPoint)
            self.c.bind("<ButtonRelease-1>", self.getResult)
            self.c.bind("<B1-Motion>", self.paint)

        def getResult(self, e):
            x = self.master.winfo_rootx() + self.c.winfo_x()
            y = self.master.winfo_rooty() + self.c.winfo_y()
            x1 = x + self.c.winfo_width()
            y1 = y + self.c.winfo_height()
            img = PIL.ImageGrab.grab()
            img = img.crop((x, y, x1, y1))
            img.save("dist.png")
            pred = model.predict("dist.png")
            self.res = str(pred.argmax())
            self.pr['text'] = "Prediction: "
            if self.res == '0':
                self.pr['text'] = self.pr['text'] + "circle\nPerimeter formula: 2 × pi × radius\nArea formula: pi × radius^2"
            elif self.res == '1':
                self.pr['text'] = self.pr['text'] + "square\nPerimeter formula: 4 × side\nArea formula: side^2"
            elif self.res == '2':
                self.pr['text'] = self.pr['text'] + "triangle\nPerimeter formula: side1 + side2 + side3\nArea formula: base × height / 2"

            if self.res == '0':
                image = cv2.imread('circle.png')
                cv2.imshow('circle', image)
                cv2.waitKey(0)
                cv2.destroyWindow("circle")
            elif self.res == '1':
                image = cv2.imread('square.png')
                cv2.imshow('square', image)
                cv2.waitKey(0)
                cv2.destroyWindow("square")
            else:
                image = cv2.imread('triangle.png')
                cv2.imshow('triangle', image)
                cv2.waitKey(0)
                cv2.destroyWindow("triangle")

        def clear(self):
            self.c.delete('all')

        def putPoint(self, e):
            self.c.create_oval(e.x - self.bs, e.y - self.bs, e.x + self.bs, e.y + self.bs,
                               outline='black', fill='black')
            self.pre = [e.x, e.y]

        def paint(self, e):
            self.c.create_line(self.pre[0], self.pre[1], e.x, e.y, width=self.bs * 2,
                               fill='black', capstyle=ROUND,
                               smooth=TRUE)

            self.pre = [e.x, e.y]


    if __name__ == "__main__":
        root = Tk()
        Main(root)
        root.title('Digit Classifier')
        root.resizable(0, 0)
        root.mainloop()

    return render_template("home1.html")


if __name__ == "__main__":
    app.run(debug=False)
