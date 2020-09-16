import tkinter
import pickle as pkl
import re
import string


HEIGHT = 600
WIDTH = 900
topics = ['business', 'entertainment', 'sports',
          'health', 'life', 'travel', 'digital']
topic_dict = dict(enumerate(topics))


def load_model():
    with open("objects\\dtm_6.pkl", "rb") as infile:
        (count_vectorizer, dtm, label) = pkl.load(infile)
    with open("objects\\gnb_6.pkl", "rb") as infile:
        GNB = pkl.load(infile)
    return count_vectorizer, dtm, label, GNB


def clean_text(text):
    text = text.lower()  # lowercase
    text = re.sub('[%s]' % re.escape(string.punctuation),
                  '', text)  # remove punctuations
    text = re.sub('\w*\d\w*', '', text)  # Remove digits
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', ' ', text)
    text = re.sub('\s\s+', ' ', text)
    return text


def predict(text):
    text = clean_text(text)
    if text != " ":
        X_pred = count_vectorizer.transform([text]).toarray()
        y_pred = GNB.predict(X_pred)
        label['text'] = topic_dict[y_pred[0]]


def test_func():
    print("button clicked")


if __name__ == "__main__":
    count_vectorizer, dtm, label, GNB = load_model()
    root = tkinter.Tk()
    root.title("Vietnamese Article Topics Detector")

    canvas = tkinter.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tkinter.Frame(root, bg="white")
    frame.place(relheight=1, relwidth=1, relx=0, rely=0)

    grand_label = tkinter.Label(frame,
                                text="Vietnamese Article Topics Detector",
                                font=("Times New Roman", 20, 'bold', 'italic'),
                                bg="#a53e12",
                                fg="#f6d5b9")
    grand_label.place(relx=0, rely=0, relwidth=1, height=30)

    instruction = tkinter.Label(
        frame,
        text="Copy a Vietnamese article of your choice then paste it in the textbox below.")
    instruction.place(relwidth=0.8, relx=0.1, y=35)

    text = tkinter.Text(frame, bg="#f9f0e3")
    text.place(relwidth=0.8, height=400, relx=0.1, y=65)

    label = tkinter.Label(frame, width=20)
    label.place(relwidth=0.2, relx=0.4, y=500)

    button = tkinter.Button(frame, text="Predict topic",
                            command=lambda: predict(text.get(1.0, "end")))
    button.place(relwidth=0.1, relx=0.45, y=470)
    root.mainloop()
