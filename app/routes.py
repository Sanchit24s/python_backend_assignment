from flask import Blueprint, jsonify, request
from app.models import Retreat, Booking
from app import db
from app.utils import paginate_results
from sqlalchemy import or_

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Wellness Retreat API'}), 200

@bp.route('/retreats', methods=['GET'])
def get_retreats():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '')
    filter_param = request.args.get('filter', '')
    location = request.args.get('location', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_duration = request.args.get('min_duration', type=int)
    max_duration = request.args.get('max_duration', type=int)

    query = Retreat.query

    # Search
    if search:
        search_terms = search.split()
        search_filter = []
        for term in search_terms:
            search_filter.append(or_(
                Retreat.title.ilike(f'%{term}%'),
                Retreat.description.ilike(f'%{term}%'),
                Retreat.location.ilike(f'%{term}%')
            ))
        query = query.filter(or_(*search_filter))
    
    # Filter
    if filter_param:
        query = query.filter(or_(
            Retreat.title.ilike(f'%{filter_param}%'),
            Retreat.description.ilike(f'%{filter_param}%')
        ))
    
    # Location filter
    if location:
        query = query.filter(Retreat.location.ilike(f'%{location}%'))

    # Price range filter
    if min_price is not None:
        query = query.filter(Retreat.price >= min_price)
    if max_price is not None:
        query = query.filter(Retreat.price <= max_price)

    # Duration range filter
    if min_duration is not None:
        query = query.filter(Retreat.duration >= min_duration)
    if max_duration is not None:
        query = query.filter(Retreat.duration <= max_duration)

    retreats, pagination = paginate_results(query, page, per_page)
    
    return jsonify({
        'retreats': [
            {
                'id': retreat.id,
                'title': retreat.title,
                'description': retreat.description,
                'location': retreat.location,
                'price': retreat.price,
                'duration': retreat.duration,
                'capacity': retreat.capacity
            } for retreat in retreats
        ],
        #'pagination': pagination
    })

@bp.route('/retreats', methods=['POST'])
def create_retreat():
    data = request.json

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    # Validate required fields
    required_fields = ['title', 'description', 'location', 'price', 'duration', 'capacity']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Create new retreat
    new_retreat = Retreat(
        title=data['title'],
        description=data['description'],
        location=data['location'],
        price=float(data['price']),
        duration=int(data['duration']),
        capacity=int(data['capacity'])
    )

    try:
        db.session.add(new_retreat)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while creating the retreat', 'details': str(e)}), 500

    return jsonify({
        'message': 'Retreat created successfully',
        'retreat': {
            'id': new_retreat.id,
            'title': new_retreat.title,
            'description': new_retreat.description,
            'location': new_retreat.location,
            'price': new_retreat.price,
            'duration': new_retreat.duration,
            'capacity': new_retreat.capacity
        }
    }), 201

@bp.route('/book', methods=['POST'])
def book_retreat():
    data = request.json

    # Check if the retreat exists
    retreat = Retreat.query.get(data['retreat_id'])
    if not retreat:
        return jsonify({'error': 'Retreat not found'}), 404

    # Check if the user has already booked this retreat
    existing_booking = Booking.query.filter_by(
        user_id=data['user_id'],
        retreat_id=data['retreat_id']
    ).first()

    if existing_booking:
        return jsonify({'error': 'You have already booked this retreat'}), 400

    new_booking = Booking(
        user_id=data['user_id'],
        user_name=data['user_name'],
        user_email=data['user_email'],
        user_phone=data['user_phone'],
        retreat_id=data['retreat_id'],
        retreat_title=data['retreat_title'],
        retreat_location=data['retreat_location'],
        retreat_price=data['retreat_price'],
        retreat_duration=data['retreat_duration'],
        payment_details=data['payment_details']
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message': 'Booking created successfully'}), 201

@bp.route('/bookings', methods=['GET'])
def get_bookings():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)
    user_id = request.args.get('user_id', type=int)

    query = Booking.query

    if user_id:
        query = query.filter_by(user_id=user_id)

    bookings, pagination = paginate_results(query, page, per_page)

    return jsonify({
        'bookings': [
            {
                'id': booking.id,
                'user_id': booking.user_id,
                'user_name': booking.user_name,
                'user_email': booking.user_email,
                'user_phone': booking.user_phone,
                'retreat_id': booking.retreat_id,
                'retreat_title': booking.retreat_title,
                'retreat_location': booking.retreat_location,
                'retreat_price': booking.retreat_price,
                'retreat_duration': booking.retreat_duration,
                'payment_details': booking.payment_details,
                'booking_date': booking.booking_date.isoformat()
            } for booking in bookings
        ],
        # 'pagination': pagination
    }), 200