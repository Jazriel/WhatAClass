# -*- coding: utf-8 -*-
"""
    WhatAClass.blueprints.tensorflow_mng_blue
    ~~~~~~~~~~~~~~~~~~~~~~
    Blueprint that communicates with a tensorflow instance via SSH.


    :author: Javier Martínez
"""

from flask import (Blueprint, flash, render_template, url_for,
                   redirect, request)
from flask_login import login_required, current_user
from flask_babel import gettext as _

from paramiko import SSHClient, AutoAddPolicy
from werkzeug.utils import secure_filename
from os import path, mkdir
from glob import glob

from ..forms import UploadForm, SelectDatasetForm, SelectUploadForm
from ..utils import ssh_config


tensorflow_mng = Blueprint('tensorflow_mng', __name__)


@tensorflow_mng.route('/upload-dataset', methods=['GET', 'POST'])
@login_required
def upload_dataset():
    """Page where users upload datasets to be able to fit the model later"""
    form = UploadForm()

    if request.method == 'POST':
        print('Uploading dataset')
        try:
            mkdir(path.join('/app/static/images', str(current_user.id)))
        except FileExistsError:
            pass
        # TODO technical debt move images path to env variable to reduce coupling
        try:
            save_file(path.join('/app/static/images', str(current_user.id)))
            print('Saved dataset')
            flash(_('Dataset successfully saved.'))
            return redirect(url_for('tensorflow_mng.retrain'))
        except NotSavedError:
            flash(_('There was an error while saving the dataset, please try again.'))
            return redirect(url_for('tensorflow_mng.upload_dataset'))

    return render_template('tensorflow_mng/upload_ds.html', form=form)


@tensorflow_mng.route('/retrain', methods=['GET', 'POST'])
@login_required
def retrain():
    """Page where users are going to retrain the model to fit their dataset."""
    dataset_select = SelectDatasetForm()

    if request.method == 'POST':
        print('Remote command: python3 /scripts/maybe_start_retrain.py {} {} '.format(current_user.id, dataset_select.choice.data))

        ssh = init_ssh()
        ssh_client, stdout, stderr = ssh.exec_command(
            'python3 '
            '/scripts/maybe_start_retrain.py'
            ' {} {} '.format(current_user.id, dataset_select.choice.data))
        output = stdout.read().decode()
        err = stderr.read().decode()
        ssh.close()

        print('The output from the worker was: ' + output)
        print('The stderr was: ' + err)

        if 'True' in output:
            flash(_('Retrain started.'))
            return render_template('tensorflow_mng/retrain.html', form=dataset_select, datasets=list(get_datasets()))
        else:
            flash(_('A model was already trained or queued to train with that dataset.'))
            return render_template('tensorflow_mng/retrain.html', form=dataset_select, datasets=list(get_datasets()))

    return render_template('tensorflow_mng/retrain.html', form=dataset_select, datasets=list(get_datasets()))


@tensorflow_mng.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Page where users are going to upload files to get their predictions on the default model."""

    # TODO technical debt: refactor SSH out of the blueprints
    form = UploadForm()

    if request.method == 'POST':
        try:
            filename = save_file('/app/static/images')
        except NotSavedError:
            return redirect(url_for('tensorflow_mng.predict'))

        print('Saved: ', filename)

        classes, probs, output, stderr = ssh_predict(filename)

        print('Classes: ', classes, '; Probs', probs)
        
        if len(classes) < 3 or len(probs) < 3:
            print(output)
            print(stderr.read().decode())
            return render_template('error.html')

        return render_template('tensorflow_mng/predicted.html',
                               classes=classes,
                               probs=probs,
                               image_path=path.join('images', filename))

    return render_template('tensorflow_mng/predict.html', form=form)


@tensorflow_mng.route('/select-predict', methods=['GET', 'POST'])
@login_required
def select_predict():
    """Page where users are going to upload files to get their predictions on their models."""

    # TODO technical debt: refactor SSH out of the blueprints
    select_upload_form = SelectUploadForm()

    if request.method == 'POST':
        try:
            filename = save_file('/app/static/images')
        except NotSavedError as e:
            flash(_('There was a problem saving the file: ' + str(e)))
            return redirect(url_for('tensorflow_mng.select_predict'))

        print('Saved: ', filename)

        graph_path='/images/{}/{}/out_graph.pb'.format(current_user.id, select_upload_form.choice.data)
        label_path='/images/{}/{}/out_labels.txt'.format(current_user.id, select_upload_form.choice.data)

        classes, probs, output, stderr = ssh_predict(filename,
                                                     graph_path=graph_path,
                                                     label_path=label_path,
                                                     layer='final_result:0',
                                                     label_map_path='')

        print('Classes: ', classes, '; Probs', probs)

        if len(classes) < 2 or len(probs) < 2:
            print(output)
            print(stderr.read().decode())
            return render_template('error.html')

        return render_template('tensorflow_mng/predicted-custom.html',
                               classes=classes,
                               probs=probs,
                               image_path=path.join('images', filename))

    return render_template('tensorflow_mng/select-predict.html',
                           sel_up_form=select_upload_form,
                           datasets=list(get_trained_models()))


def ssh_predict(filename,
                graph_path='/graphs/inceptionv3_model.pb',
                label_path='/graphs/inceptionv3_labels.txt',
                layer='softmax:0',
                label_map_path='/graphs/inceptionv3_label_map_proto.pbtxt'):
    ssh = init_ssh()
    _, stdout, stderr = ssh.exec_command(
        'python3 '
        '/scripts/run_inference.py'
        ' {} {} {} {} {} '.format(path.join('/images', filename),
                                  graph_path,
                                  label_path,
                                  layer,
                                  label_map_path))
    output = stdout.read().decode()
    print(output)
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


def save_file(path_):
    """Standard file saving"""
    print('Saving file')
    if 'file' not in request.files:
        print('No file part')
        raise NotSavedError

    file = request.files['file']

    if file.filename == '':
        print('No selected file')
        raise NotSavedError

    filename = secure_filename(file.filename)
    file.save(path.join(path_, filename))
    return filename



def get_datasets():
    """Get all the datasets of the current user"""
    for dataset in glob(path.join('/app/static/images', str(current_user.id), '*.zip')):
        yield dataset.split('/')[-1].split('.zip')[0]

def get_trained_models():
    """Get all trained models of the current user"""
    for model_path in glob(path.join('/app/static/images', str(current_user.id), '**', 'out_graph.pb')):
        yield model_path.split('/')[-2]

class NotSavedError(RuntimeError):
    pass

