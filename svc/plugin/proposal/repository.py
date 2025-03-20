from svc.utils.database import db
from .schema import InputProposal, Proposal

def create_proposal(proposal: InputProposal):
    db.proposal.insert_one(proposal.dict())

def find_proposals(company_id: str):
    return [Proposal(**p) for p in db.proposal.find({'consultancy_receiver': company_id})]