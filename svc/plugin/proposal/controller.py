from fastapi import APIRouter, HTTPException, Depends
from svc.utils.userRecomendation import userRec
from svc.hook.auth.index import validate_token
from svc.utils.dataset import answers
from svc.plugin.question import repository as question_repository
from svc.plugin.consultant import repository as consultant_repository
from . import repository as repository_proposal
from .schema import InputProposal, Role

router = APIRouter(prefix="/proposals", tags=["proposals"])

@router.post("/{id}")
async def update_proposal(
    id: str,
    body: dict,
    role: Role,
    user: dict = Depends(validate_token)
    ):
    db_user = consultant_repository.get_user(user['uid'])
    my_company = consultant_repository.get_consultant(db_user['company'])
    proposal = repository_proposal.get_proposal(id)
    print("proposal:", proposal)
    if body['status'] == "REJECTED" and body['decision'] is not None:
        if str(my_company['_id']) == str(proposal['consultancy_receiver']['id']):
            consultant_repository.update_black_list(my_company['_id'], body['decision'], proposal['consultancy_provider'])
        if str(my_company['_id']) == str(proposal['consultancy_provider']['id']):
            consultant_repository.update_black_list(my_company['_id'], body['decision'], proposal['consultancy_receiver'])
    
    db_user = consultant_repository.get_user(user['uid'])
    repository_proposal.update_proposal_status(id, body['status'])
    proposals = repository_proposal.find_proposals(str(db_user['company']), role)
    return {"message": "Consultant created successfully", "data": proposals }

@router.get("")
async def get_proposals(role: Role, user: dict = Depends(validate_token)):
    db_user = consultant_repository.get_user(user['uid'])
    my_company = consultant_repository.get_consultant(db_user['company'])
    if my_company == None:
        return {"message": "Consultant not found", "data": [] }

    userRec.set_consultants(
        my_company['black_list_area'] if 'black_list_area' in my_company else [], 
        my_company['black_list_company'] if 'black_list_company' in my_company else [],
    )
    
    proposals = repository_proposal.find_proposals(str(db_user['company']), role)
    if len(proposals) == 0 and role == Role.RECEIVER:
        questions = question_repository.get_questions_and_answers(user['uid'])
        recomendations = userRec.find_best_match(questions)
        for recomendation in recomendations['consultants']:
            repository_proposal.create_proposal(
                InputProposal(
                    consultancy_receiver=str(my_company['_id']),
                    consultancy_provider=str(recomendation['_id']),
                    reason_of_match=recomendation['reason']
                )
            )
    proposals = repository_proposal.find_proposals(str(db_user['company']), role)
    return {"message": "Consultant created successfully", "data": proposals }
