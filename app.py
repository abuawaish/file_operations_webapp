from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from __file_operation import FileOperation
import os

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'files'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        filename = request.form['filename']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if filename in os.listdir(app.config['UPLOAD_FOLDER']):
                flash(f'File "{filename}" already exists.', 'primary')
            else:
                FileOperation(file_path)
                flash(f'File {filename} created!', 'success')
            return redirect(url_for('read', filename=filename))
        except Exception as e:
            flash(str(e), 'danger')
    return render_template('create.html')

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        filename = request.form['filename']
        content = request.form['content']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
                flash(f'File "{filename}" does not exist.', 'danger')
                return redirect(url_for('index'))
            else:
                file_op = FileOperation(file_path)
                file_op.write_file(content)
                flash('Content added!', 'success')
            return redirect(url_for('read', filename=filename))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('write.html')

@app.route('/read/<filename>')
def read(filename):
    try:
        file_path: str = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
            return render_template('index.html',message=flash(f'File "{filename}" does not exist.', 'danger'))
        else:
            file_op = FileOperation(file_path)
            content = file_op.read_file()
        return render_template('read.html', filename=filename, content=content)
    except Exception as e:
        return render_template('index.html', message=flash(f'Error reading file: {e}', 'danger'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    try:
        if request.method == 'POST':
            filename = request.form['filename']
            if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
                return render_template('index.html', message=flash(f'File "{filename}" does not exist.', 'danger'))
            else:
                line_number = int(request.form['line_number'])
                new_content = request.form['new_content']
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_op = FileOperation(file_path)
                result = file_op.update_file_content(line_number, new_content)
                flash(result, 'success' if 'updated' in result else 'danger')
                return redirect(url_for('read', filename=filename))
        return render_template('update.html')
    except Exception as e:
        return render_template('index.html', message=flash(f'Error updating file: {e}', 'danger'))

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    try:
        if request.method == 'POST':
            filename = request.form['filename']
            if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
                flash(f'File "{filename}" does not exist.', 'danger')
                return redirect(url_for('index'))
            else:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_op = FileOperation(file_path)
                result = file_op.clear_file_content()
                flash(result, 'success' if 'cleared' in result else 'danger')
            return redirect(url_for('read', filename=filename))
        return render_template('clear.html')
    except Exception as e:
        return render_template('index.html', message=flash(f'Error clearing file: {e}', 'danger'))


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    try:
        if request.method == 'POST':
            filename = request.form.get('filename', '').strip()
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    flash(f'File "{filename}" has been deleted successfully.', 'success')
                except Exception as e:
                    flash(f'Error deleting file: {str(e)}', 'danger')
            else:
                flash(f'File "{filename}" does not exist.', 'danger')

            return redirect(url_for('index'))
        return render_template('delete.html')
    except Exception as e:
        return render_template('index.html', message=flash(f'Error deleting file: {e}', 'danger'))

@app.route('/download/<filename>')
def download(filename):
    if filename not in os.listdir(app.config['UPLOAD_FOLDER']):
        return render_template('index.html', message=flash(f'File "{filename}" does not exist.', 'danger'))
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)