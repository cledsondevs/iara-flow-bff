from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Flow(db.Model):
    __tablename__ = 'flows'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    flow_data = db.Column(db.Text, nullable=False)  # JSON string
    status = db.Column(db.String(50), default='created')  # created, running, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, id, name, flow_data, description=None):
        self.id = id
        self.name = name
        self.description = description
        self.flow_data = json.dumps(flow_data) if isinstance(flow_data, dict) else flow_data
    
    def get_flow_data(self):
        return json.loads(self.flow_data)
    
    def set_flow_data(self, data):
        self.flow_data = json.dumps(data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'flow_data': self.get_flow_data(),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FlowExecution(db.Model):
    __tablename__ = 'flow_executions'
    
    id = db.Column(db.String(50), primary_key=True)
    flow_id = db.Column(db.String(50), db.ForeignKey('flows.id'), nullable=False)
    input_data = db.Column(db.Text)  # JSON string
    output_data = db.Column(db.Text)  # JSON string
    status = db.Column(db.String(50), default='running')  # running, completed, failed
    error_message = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    flow = db.relationship('Flow', backref=db.backref('executions', lazy=True))
    
    def __init__(self, id, flow_id, input_data=None):
        self.id = id
        self.flow_id = flow_id
        self.input_data = json.dumps(input_data) if isinstance(input_data, dict) else input_data
    
    def get_input_data(self):
        return json.loads(self.input_data) if self.input_data else {}
    
    def set_input_data(self, data):
        self.input_data = json.dumps(data)
    
    def get_output_data(self):
        return json.loads(self.output_data) if self.output_data else {}
    
    def set_output_data(self, data):
        self.output_data = json.dumps(data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'flow_id': self.flow_id,
            'input_data': self.get_input_data(),
            'output_data': self.get_output_data(),
            'status': self.status,
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

