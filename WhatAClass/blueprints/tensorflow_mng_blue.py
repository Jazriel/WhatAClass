from flask import (Blueprint, flash, render_template, url_for,
                   redirect, request)
from flask_login import login_required, current_user

from paramiko import SSHClient, AutoAddPolicy
from werkzeug.utils import secure_filename
from os import path, mkdir
from glob import glob

from WhatAClass.forms import UploadForm, SelectDatasetForm
from WhatAClass.util import ssh_config


tensorflow_mng = Blueprint('tensorflow_mng', __name__)


@tensorflow_mng.route('/upload-dataset', methods=['GET', 'POST'])
@login_required
def upload_dataset():

    form = UploadForm()

    if request.method == 'POST':
        try:
            mkdir(path.join('/app/static/images', str(current_user.id)))
        except:
            pass
        # TODO technical debt move images path to env variable to reduce coupling
        filename, redir = save_file('/app/static/images', 'tensorflow_mng.upload_dataset')

        if filename is None:
            return redir
    return render_template('upload_ds.html', form=form)


@tensorflow_mng.route('/retrain', methods=['GET', 'POST'])
@login_required
def retrain():
    dataset_select = SelectDatasetForm()
    dataset_select.choice.choices = [datasets_to_encoded_pairs(split_zip(get_datasets()))]

    if request.method == 'POST':
        ssh = init_ssh()
        _, stdout, stderr = ssh.exec_command(
            'python3 '
            '/scripts/maybe_start_retrain.py'
            ' {} {} '.format(current_user.id, dataset_select.choice.data))
        output = stdout.read().decode()
        # TODO improve this and predict
        ssh.close()


@tensorflow_mng.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Page where users are going to upload files to get their predictions."""

    # TODO technical debt: refactor SSH out of the blueprints
    form = UploadForm()

    if request.method == 'POST':
        filename, redir = save_file('/app/static/images', 'tensorflow_mng.predict')

        if filename is None:
            return redir

        classes, probs, output, stderr = ssh_predict(filename)
        path.join('/app/static/images', filename)

        if len(classes) < 3 or len(probs) < 3:
            print(output)
            print(stderr.read().decode())
            return render_template('error.html')

        return render_template('predicted.html',
                               classes=classes,
                               probs=probs,
                               image_path=path.join('images', filename))

    return render_template('predict.html', form=form)


def ssh_predict(filename, layer='softmax:0'):
    ssh = init_ssh()
    _, stdout, stderr = ssh.exec_command(
        'python3 '
        '/scripts/run_inference.py'
        ' {} {} {} {} {}'.format(path.join('/images', filename),
                              '/graphs/inceptionv3_model.pb',
                              '/graphs/inceptionv3_labels.txt',
                              '/graphs/inceptionv3_label_map_proto.pbtxt',
                              layer))
    output = stdout.read().decode()
    pairs = output.split(';')
    classes = list()
    probs = list()
    for pair in pairs:
        if pair is not '':
            class_, prob = pair.split(':')
            classes.append(class_)
            probs.append(prob)
    ssh.close()
    return classes, probs, output, stderr


def init_ssh():
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(ssh_config['HOST'],
                port=int(ssh_config['PORT']),
                username=ssh_config['USER'],
                key_filename='/root/.ssh/id_rsa')
    return ssh


def save_file(path_, redir_target):
    """Standard file saving"""
    if 'file' not in request.files:
        flash('No file part')
        return None, redirect(url_for(redir_target))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return None, redirect(url_for(redir_target))

    filename = secure_filename(file.filename)
    file.save(path.join(path_, filename))
    return filename


def get_datasets():
    """Get all the datasets of the current user"""
    return glob(path.join('/app/static/images', str(current_user.id), '*.zip'))


def datasets_to_encoded_pairs(datasets):
    for dataset in datasets:
        encoded = dataset.encode()
        yield (encoded, encoded)


def split_zip(strings):
    for string in strings:
        yield string.split('.')[0]

