# -*- coding: utf-8 -*

@app.route('/home')
@login_required
def home():
    return render_template('home.html')
