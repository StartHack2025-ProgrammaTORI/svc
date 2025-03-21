from svc.utils.database import db
from .schema import InputProposal, ProposalPopulated, Role
from bson import ObjectId  # Import ObjectId for querying by ID

def create_proposal(proposal: InputProposal):
    db.proposal.insert_one(proposal.dict())

def find_proposals(company_id: str, role: Role):
    pipeline = [
        {'$match': {'consultancy_receiver': company_id} if role == Role.RECEIVER else {'consultancy_provider': company_id}},
        {
            '$addFields': {
                'consultancy_receiver_obj': {'$toObjectId': '$consultancy_receiver'},
                'consultancy_provider_obj': {'$toObjectId': '$consultancy_provider'}
            }
        },
        {
            '$lookup': {
                'from': 'company',
                'localField': 'consultancy_receiver_obj',
                'foreignField': '_id',
                'as': 'consultancy_receiver'
            }
        },
        {'$unwind': '$consultancy_receiver'},
        {
            '$lookup': {
                'from': 'company',
                'localField': 'consultancy_provider_obj',
                'foreignField': '_id',
                'as': 'consultancy_provider'
            }
        },
        {'$unwind': '$consultancy_provider'},
        {
            '$project': {
                "_id": 1,
                "consultancy_receiver": 1,
                "consultancy_provider": 1,
                "status": 1,
                "reason_of_rejection": 1,
                "reason_of_match": 1,
                "created_at": 1
            }
        }
    ]
    data = db.proposal.aggregate(pipeline)
    return [ProposalPopulated(**p) for p in data]

def update_proposal_status(proposal_id: str, status: str):
    db.proposal.update_one(
        {'_id': ObjectId(proposal_id)}, 
        {'$set': {'status': status}}
    )