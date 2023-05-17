from flask import Flask, render_template, url_for, request, redirect
import script as s

app = Flask(__name__)

@app.route('/')
def home():
    return  redirect(url_for('WebScrapy_Home'))
@app.route('/WebScrapy_Home', methods=['GET','POST'])
def WebScrapy_Home():
    if request.method == 'POST':
        product = request.form['product']
        if product == '':
            product = 'error'
            return render_template('index.html', product = product)
        else:
             data_frame = s.get_data(product)

             return render_template('index.html',table=data_frame.to_html(header=True, index=False))
    return render_template('index.html', product = 'error')

@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)