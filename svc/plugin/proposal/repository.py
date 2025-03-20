from svc.utils.database import db
from .schema import InputProposal, Proposal
from bson import ObjectId  # Import ObjectId for querying by ID

def create_proposal(proposal: InputProposal):
    db.proposal.insert_one(proposal.dict())

def find_proposals(company_id: str):
    return [Proposal(**p) for p in db.proposal.find({'consultancy_receiver': company_id})]

def update_proposal_status(proposal_id: str, status: str):
    db.proposal.update_one(
        {'_id': ObjectId(proposal_id)}, 
        {'$set': {'status': status}}
    )