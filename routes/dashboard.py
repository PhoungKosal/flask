from app import app, render_template

@app.route('/')
@app.route('/dashboard')
def dashboard():
    module = 'dashboard'
    return render_template('dashboard.html', module=module)
