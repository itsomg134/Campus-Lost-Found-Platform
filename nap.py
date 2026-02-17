from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

# Database Models
class Item(db.Model):
    """Item model for lost and found items"""
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # student, teacher, staff
    type = db.Column(db.String(10), nullable=False)  # lost, found
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    status = db.Column(db.String(20), default='active')  # active, returned, claimed
    contact_info = db.Column(db.String(100))  # Optional contact information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert item to dictionary for JSON responses"""
        return {
            'id': self.id,
            'role': self.role,
            'role_display': self.get_role_display(),
            'type': self.type,
            'type_display': 'LOST' if self.type == 'lost' else 'FOUND',
            'name': self.name,
            'description': self.description,
            'location': self.location or 'Not specified',
            'status': self.status,
            'contact_info': self.contact_info,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'time_ago': self.get_time_ago()
        }
    
    def get_role_display(self):
        """Get display name for role"""
        roles = {
            'student': 'Student',
            'teacher': 'Teacher',
            'staff': 'Staff'
        }
        return roles.get(self.role, self.role.capitalize())
    
    def get_time_ago(self):
        """Get human-readable time difference"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"

class User(db.Model):
    """User model for future authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()
    
    # Add sample data if database is empty
    if Item.query.count() == 0:
        sample_items = [
            Item(
                role='student',
                type='lost',
                name='Engineering Drawing Set',
                description='Includes compass, rulers, drawing pens. Lost in drafting room.',
                location='Drafting Room 302',
                contact_info='student@email.com'
            ),
            Item(
                role='teacher',
                type='found',
                name='Laser Presenter',
                description='Black, Logitech R400, found on podium',
                location='Multimedia Classroom 204',
                contact_info='faculty@email.com'
            ),
            Item(
                role='staff',
                type='lost',
                name='Two-way Radio',
                description='Security model H8, lost near gymnasium',
                location='Gymnasium West Entrance',
                contact_info='security@email.com'
            ),
            Item(
                role='student',
                type='found',
                name='AirPods Charging Case',
                description='Just the case, no earphones, has sticker on it',
                location='Library 2nd Floor',
                contact_info='library@email.com'
            ),
            Item(
                role='teacher',
                type='lost',
                name='Teaching USB Drive',
                description='32GB silver SanDisk, contains course materials',
                location='Admin Building Copy Room',
                contact_info='teacher@email.com'
            ),
            Item(
                role='staff',
                type='found',
                name='Tool Kit',
                description='Sata 12-piece set, left outside pump house',
                location='Maintenance Building 101',
                contact_info='maintenance@email.com'
            )
        ]
        
        for item in sample_items:
            db.session.add(item)
        
        db.session.commit()

# Routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    """Get all items with optional role filter"""
    role = request.args.get('role', 'all')
    item_type = request.args.get('type', 'all')  # lost, found, or all
    
    query = Item.query.filter_by(status='active')
    
    if role and role != 'all':
        query = query.filter_by(role=role)
    
    if item_type and item_type != 'all':
        query = query.filter_by(type=item_type)
    
    items = query.order_by(Item.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items', methods=['POST'])
def create_item():
    """Create a new item report"""
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Item name is required'}), 400
        
        new_item = Item(
            role=data.get('role', 'student'),
            type=data.get('type', 'lost'),
            name=data['name'],
            description=data.get('description', ''),
            location=data.get('location', ''),
            contact_info=data.get('contact_info', ''),
            status='active'
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify(new_item.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Get a single item by ID"""
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an item"""
    item = Item.query.get_or_404(item_id)
    data = request.json
    
    if 'status' in data:
        item.status = data['status']
    if 'description' in data:
        item.description = data['description']
    if 'location' in data:
        item.location = data['location']
    
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics for dashboard"""
    total_active = Item.query.filter_by(status='active').count()
    total_returned = Item.query.filter_by(status='returned').count()
    
    # Category counts
    books_count = Item.query.filter(
        Item.name.ilike('%book%') | 
        Item.name.ilike('%textbook%') |
        Item.name.ilike('%notebook%')
    ).filter_by(status='active').count()
    
    electronics_count = Item.query.filter(
        Item.name.ilike('%phone%') | 
        Item.name.ilike('%laptop%') | 
        Item.name.ilike('%charger%') |
        Item.name.ilike('%calculator%') |
        Item.name.ilike('%airpods%') |
        Item.name.ilike('%usb%')
    ).filter_by(status='active').count()
    
    lost_count = Item.query.filter_by(type='lost', status='active').count()
    found_count = Item.query.filter_by(type='found', status='active').count()
    
    return jsonify({
        'active': total_active,
        'returned': total_returned,
        'books': books_count,
        'electronics': electronics_count,
        'lost': lost_count,
        'found': found_count
    })

@app.route('/api/search', methods=['GET'])
def search_items():
    """Search items by keyword"""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    items = Item.query.filter(
        (Item.name.ilike(f'%{query}%') | 
         Item.description.ilike(f'%{query}%') |
         Item.location.ilike(f'%{query}%')) &
        (Item.status == 'active')
    ).order_by(Item.created_at.desc()).all()
    
    return jsonify([item.to_dict() for item in items])

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    """Render item detail page"""
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)

@app.route('/api/items/<int:item_id>/claim', methods=['POST'])
def claim_item(item_id):
    """Mark item as claimed/returned"""
    item = Item.query.get_or_404(item_id)
    item.status = 'returned'
    db.session.commit()
    return jsonify({'message': 'Item marked as returned', 'item': item.to_dict()})

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)