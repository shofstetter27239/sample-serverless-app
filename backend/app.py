#!/usr/bin/env python3
"""
example zappa flask sqlalchemy vue.js single page app backend
"""

import os
import logging
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, json, request
from flask_sqlalchemy import SQLAlchemy

# we need to instantiate the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# first, load your env file
# contains rds db connection vars
dotenv = load_dotenv(find_dotenv())


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


def build_response(resp_dict, status_code):
    """
    Used to add cors headers if needed
    """
    response = Response(json.dumps(resp_dict), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = \
        "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = \
        "POST,PUT,GET,OPTIONS,DELETE"
    return response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql+pymysql://{username}:{password}@{endpoint}:{port}/{db_name}"\
    .format(
        username=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
        endpoint=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        db_name=os.environ.get("DB_NAME"))
db = SQLAlchemy(app)


class RiskTypes(db.Model):
    """
    Table to hold risk types
    """
    __tablename__ = 'risk_types'
    rt_id = db.Column('rt_id', db.Integer, primary_key=True)
    risk_type_fields = db.relationship("RiskTypeFields")
    rt_meta = db.Column('rt_meta', db.JSON)

    def __repr__(self):
        return '<RiskTypes %r>' % self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'rt_id': self.rt_id,
            'rt_meta': self.rt_meta,
            'risk_type_fields': self.serialize_fields,
        }

    @property
    def serialize_fields(self):
        """
        Return object's relations in easily serializeable format.
        NB! Calls many2many's serialize property.
        """
        return [item.serialize for item in self.risk_type_fields]


class RiskTypeFields(db.Model):
    """
    Table to hold risk type data fields
    """
    __tablename__ = 'risk_type_fields'
    rtf_id = db.Column('rtf_id', db.Integer, primary_key=True)
    rt_id = db.Column('rt_id', db.ForeignKey('risk_types.rt_id'))
    rtf_meta = db.Column('rtf_meta', db.JSON)

    def __repr__(self):
        return '<RiskTypeFields %r>' % self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'rtf_id': self.rtf_id,
            'rtf_meta': self.rtf_meta,
        }


@app.route('/build', methods=["GET"])
def build():
    """
    initialize the database from the models
    """
    db.create_all()
    return "Models created!", 200


@app.route('/risk_types', methods=["GET", "POST", "OPTIONS"])
def risk_types():
    """
    fetch all risk types or insert a new one
    """
    if request.method == "GET":
        types = RiskTypes.query.all()
        return build_response({
            "risk_types": [rec.serialize for rec in types],
            "status": "success"}, 200)

    if request.method == "POST":
        post_data = request.get_json()
        risk_type = RiskTypes(rt_meta=post_data.get("rt_meta", ""))
        db.session.add(risk_type)
        db.session.commit()
        return build_response({
            "status": "success",
            "rt_id": risk_type.rt_id,
            "message": "Risk type added"}, 200)

    if request.method == "OPTIONS":
        return build_response({"status": "success"}, 200)


@app.route('/risk_types/<rt_id>',
           methods=["GET", "PUT", "DELETE", "OPTIONS"])
def single_risk_type(rt_id):
    """
    fetch/update/delete a single risk type
    """
    if request.method == "GET":
        risk_type = RiskTypes.query.get(int(rt_id))
        return build_response({
            "risk_type": risk_type.serialize,
            "status": "success"}, 200)

    if request.method == "PUT":
        post_data = request.get_json()
        risk_type = RiskTypes.query.get(int(rt_id))
        risk_type.rt_meta = post_data.get("rt_meta")
        db.session.commit()
        return build_response({
            "status": "success",
            "message": "Risk type updated"}, 200)

    if request.method == "DELETE":
        risk_type = RiskTypes.query.get(int(rt_id))
        db.session.delete(risk_type)
        db.session.commit()
        return build_response({
            "status": "success",
            "message": "Risk type removed"}, 200)

    if request.method == "OPTIONS":
        return build_response({"status": "success"}, 200)


@app.route('/risk_type_field/<rt_id>',
           methods=["GET", "POST", "OPTIONS"])
def risk_type_field(rt_id):
    """
    fetch all fields for a risk type or
    inserting a new field
    """
    if request.method == "GET":
        fields = RiskTypeFields.query\
            .filter_by(rt_id=int(rt_id)).all()
        return build_response({
            "risk_type_fields": [
                rec.serialize for rec in fields],
            "status": "success"}, 200)

    if request.method == "POST":
        post_data = request.get_json()
        field = RiskTypeFields(
            rt_id=rt_id,
            rtf_meta=post_data.get("rtf_meta", ""))
        db.session.add(field)
        db.session.commit()
        return build_response({
            "status": "success",
            "rtf_id": field.rtf_id,
            "message": "Field added!"}, 200)

    if request.method == "OPTIONS":
        return build_response({"status": "success"}, 200)


@app.route('/risk_type_field/<rtf_id>',
           methods=["GET", "PUT", "DELETE", "OPTIONS"])
def single_risk_type_field(rtf_id):
    """
    fetching/updating/deleting a single field
    """
    if request.method == "GET":
        field = RiskTypeFields.query.get(int(rtf_id))
        return build_response({
            "risk_type_field": field.serialize,
            "status": "success"}, 200)

    if request.method == "PUT":
        post_data = request.get_json()
        field = RiskTypeFields.query.get(int(rtf_id))
        field.rt_id = post_data.get("rt_id", "")
        field.rtf_meta = post_data.get("rtf_meta", "")
        db.session.commit()
        return build_response({
            "status": "success",
            "message": "Field updated!"}, 200)

    if request.method == "DELETE":
        field = RiskTypeFields.query.get(int(rtf_id))
        db.session.delete(field)
        db.session.commit()
        return build_response({
            "status": "success",
            "message": "Field removed!"}, 200)

    if request.method == "OPTIONS":
        return build_response({"status": "success"}, 200)


# here is how we are handling routing with flask:
@app.route('/')
def index():
    """
    The default index endpoint
    """
    return "Hello World!", 200


if __name__ == '__main__':
    app.run()
