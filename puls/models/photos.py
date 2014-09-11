# coding=utf-8
from __future__ import absolute_import, unicode_literals, division
from puls.models import on, has_triggers
from puls.helpers import resource
from puls.compat import str
from puls import app

import flask_wtf.file
import bson.objectid
import mongoengine as mge
import subprocess
import datetime
import werkzeug
import wtforms as wtf
import logging
import flask
import os


@has_triggers
class Photo(app.db.Document):
    filename = mge.StringField(required=False)
    format = mge.StringField(required=True)
    mime = mge.StringField(required=True)
    width = mge.IntField(required=True)
    height = mge.IntField(required=True)
    size = mge.IntField(required=True)

    # dates
    created = mge.DateTimeField(default=datetime.datetime.now)

    # useful properties
    @property
    def orig_path(self):
        return os.path.join("static", "photo", "orig", str(self.id))

    @property
    def web_path(self):
        return os.path.join("static", "photo", "web", "{0}.{1}".format(
            str(self.id), self.format))

    @property
    def thumb_path(self):
        return os.path.join("static", "photo", "thumb", "{0}.{1}".format(
            str(self.id), self.format))

    @property
    def paths(self):
        return self.orig_path, self.web_path, self.thumb_path

    @property
    def description(self):
        return "{width}x{height} {format} image".format(width=self.width,
                                                        height=self.height,
                                                        format=self.format)

    @property
    def thumb_url(self):
        return resource("photo/thumb/{0}.{1}".format(self.id, self.format))

    @property
    def web_url(self):
        return resource("photo/web/{0}.{1}".format(self.id, self.format))

    @property
    def orig_url(self):
        return flask.url_for("download_photo", id=str(self.id))

    @on(mge.signals.pre_delete)
    def delete_files(self):
        for filename in self.paths:
            try:
                os.unlink(filename)
            except EnvironmentError:
                # deleting is best effort only
                pass


class PhotoField(flask_wtf.file.FileField):
    """Holds a reference to a Photo object. """

    @classmethod
    def widget(cls, self, **kwargs):
        id = kwargs.pop("id", self.id)
        html =  "<input %s>" % wtf.widgets.html_params(
            name=self.name,
            type="file",
            **kwargs
        )
        if self.data:
            html += "<img %s>" % wtf.widgets.html_params(
                src=self.data.web_path,
                alt=self.data.description,
                class_="img-responsive img-rounded"
            )
            html += "<input %s>" % wtf.widgets.html_params(
                name=self.name,
                type="hidden",
                value=str(self.data.id)
            )
        return wtf.widgets.HTMLString("<div %s>%s</div>" % (
            wtf.widgets.html_params(id=id,
                                    class_="photo-widget"),
            html
        ))

    def process_data(self, value):
        # process initialization data
        if isinstance(value, Photo):
            self.data = value
        else:
            self.data = None

    def process_formdata(self, valuelist):
        if not valuelist:
            self.data = None
        elif isinstance(valuelist[0], werkzeug.FileStorage):
            self.data = self.process_upload(valuelist[0])
        else:
            # assume an existing photo id has been sent
            try:
                self.data = Photo.objects.get(id=str(valuelist[0]))
            except Photo.DoesNotExist:
                raise wtf.ValidationError("Invalid photo id.")

    def process_upload(self, input):
        # set default name from filename if non-existent
        secure_name = werkzeug.secure_filename(input.filename)
        photo = Photo(id=bson.objectid.ObjectId())

        # save the original file
        try:
            logging.info(photo.orig_path)
            input.save(photo.orig_path)
        except Exception:
            raise wtf.ValidationError("Unable to save image.")

        # attempt to generate thumbnail and web version
        try:
            identify = subprocess.Popen([
                app.config["IMAGEMAGICK_IDENTIFY"], photo.orig_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            out, err = identify.communicate()
            if identify.returncode != 0:
                logging.error("Unable to identify image")
                logging.debug(out)
                raise ValueError

            # get metadata
            pieces = str(out).split(" ")
            photo.format = pieces[1].lower()
            if photo.format == "jpg":
                photo.format = "jpeg"
            if photo.format not in ("jpeg", "gif"):
                photo.format = "png"

            photo.width, photo.height = map(int, pieces[2].split("x"))
            photo.mime = input.mimetype
            photo.size = os.stat(photo.orig_path).st_size

            # generate web version
            convert = subprocess.Popen([
                app.config["IMAGEMAGICK_CONVERT"], photo.orig_path,
                "-coalesce",
                "-resize", app.config["IMAGE_RESOLUTION"],
                photo.web_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            out, err = convert.communicate()
            if convert.returncode != 0:
                logging.error("Unable to generate web image")
                logging.info(out)
                raise ValueError

            convert = subprocess.Popen([
                app.config["IMAGEMAGICK_CONVERT"], photo.orig_path,
                "-coalesce",
                "-resize", app.config["THUMB_RESOLUTION"],
                photo.thumb_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)

            out, err = convert.communicate()
            if convert.returncode != 0:
                logging.error("Unable to generate thumb")
                logging.debug(out)
                raise ValueError

            # store the photo reference in the database
            photo.save()
            return photo
        except Exception:
            # delete temp file(s)
            photo.delete_files()
            raise wtf.ValidationError("Invalid or corrupt image.")
