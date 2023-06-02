from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building


from model.kahans import Kahans

kahan_api = Blueprint('kahan_api', __name__,
                   url_prefix='/api/kahan')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(kahan_api)

class KahanApi:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            song = body.get('song')
            if song is None or len(song) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            tID = body.get('tID')
            if tID is None or len(tID) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            rID = body.get('rID')
            if rID is None:
                return {'message': f'you have never played this game!'}, 210
            

            ''' #1: Key code block, setup USER OBJECT '''
            ko = Kahans(song=song, 
                      tID=tID,
                      rID=rID)
            
            ''' Additional garbage error checking '''
            # set password if provided
        
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            kahan = ko.create()
            # success returns json of user
            if kahan:
                return jsonify(kahan.read())
            # failure returns error
            return {'message': f'Processed {song}, format error'}, 210

    class _Read(Resource):
        def get(self):
            kahans = Kahans.query.all()    # read/extract all users from database
            json_ready = [kahan.read() for kahan in kahans]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
    
        
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
