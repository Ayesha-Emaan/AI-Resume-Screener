from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from algorithms import process_resumes
import os
from config import Config  # Add this import

app = Flask(__name__)
app.config.from_object(Config)  # Load configuration

# Ensure upload folder exists at startup
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'resumes' not in request.files:
        flash('No files selected', 'error')
        return redirect(request.url)
    
    files = request.files.getlist('resumes')
    if not files or all(file.filename == '' for file in files):
        flash('No files selected', 'error')
        return redirect(request.url)
    
    for file in files:
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    flash('Resumes uploaded successfully', 'success')
    return redirect(url_for('select_job'))

@app.route('/select_job')
def select_job():
    return render_template('job_selection.html')

@app.route('/process', methods=['POST'])
def process():
    job_description = request.form.get('job_description', '')
    algorithm = request.form.get('algorithm', 'default')
    
    if not job_description.strip():
        flash('Please enter a job description', 'error')
        return redirect(url_for('select_job'))
    
    try:
        results = process_resumes(
            app.config['UPLOAD_FOLDER'],
            job_description,
            algorithm.lower()
        )
        return render_template('results.html', results=results, algorithm=algorithm.capitalize())
    except Exception as e:
        flash(f'Error processing resumes: {str(e)}', 'error')
        return redirect(url_for('select_job'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

from app import app  # Import your Flask app instance

if __name__ == '__main__':
    app.run(port=5501)


