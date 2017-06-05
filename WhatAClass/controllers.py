# -*- coding: utf-8 -*-
"""
    WhatAClass.controllers
    ~~~~~~~~~~~~~~~~~~~~~~

    The usual web-app architecture is the MVC
    (Model-View-Controller). This class implements
    the controllers of the architecture.

    The structure used was Blueprints for the app to
    be scalable (create a divisional or functional
    structure and distribute the work among the contributors).

    :author: Javier Martínez
"""

from flask import (Blueprint, flash, render_template, url_for,
                   redirect, request)
from flask_login import login_required

from paramiko import SSHClient, AutoAddPolicy
from werkzeug.utils import secure_filename
from os import path

from .forms import UploadForm
from .util import ssh_config

from .blueprints import index, user_mng




neuralnet_mng = Blueprint('neuralnet_mng', __name__)


@neuralnet_mng.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Page where users are going to upload files to get their predictions."""
    form = UploadForm()

    if request.method == 'POST':

        # Standard save file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('neuralnet_mng.fit'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('neuralnet_mng.fit'))

        filename = secure_filename(file.filename)
        file.save(path.join('/app/static/images', filename))

        # Start ssh
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ssh_config['HOST'],
                    port=int(ssh_config['PORT']),
                    username=ssh_config['USER'],
                    key_filename='/root/.ssh/id_rsa')

        _, stdout, stderr = ssh.exec_command(
            'python3 '
            '/scripts/run_inference.py'
            ' {} {} {} {}'.format(path.join('/images', filename),
                                  '/graphs/inceptionv3_model.pb',
                                  '/graphs/inceptionv3_labels.txt',
                                  '/graphs/inceptionv3_label_map_proto.pbtxt'))

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

        if len(classes) < 3 or len(probs) < 3:
            print(output)
            print(stderr.read().decode())
            return render_template('error.html')

        return render_template('fitted.html',
                               classes=classes,
                               probs=probs,
                               image_path=path.join('images', filename))

    return render_template('predict.html', form=form)

