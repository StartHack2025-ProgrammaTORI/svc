from fastapi import APIRouter, HTTPException, Depends
from svc.utils.userRecomendation import userRec
from svc.hook.auth.index import validate_token
from svc.utils.dataset import answers
from svc.plugin.question import repository as question_repository
from svc.plugin.consultant import repository as consultant_repository
from . import repository as repository_proposal
from .schema import InputProposal, Proposal

router = APIRouter(prefix="/proposals", tags=["proposals"])

@router.get("")
async def get_proposals(user: dict = Depends(validate_token)):
    db_user = consultant_repository.get_user(user['uid'])
    print("user: ", str(db_user['company']))
    my_company = consultant_repository.get_consultant(db_user['company'])
    print(my_company)
    proposals = repository_proposal.find_proposals(user['uid'])
    if len(proposals) == 0:
        questions = question_repository.get_questions_and_answers(user['uid'])
        recomendations = userRec.find_best_match(questions)
        for recomendation in recomendations:
            print("test: ", my_company, recomendation)
            repository_proposal.create_proposal(
                InputProposal(
                    consultancy_receiver=my_company['_id'],
                    consultancy_provider=recomendation['_id'],
                    reason_of_match=recomendation['reason']
                )
            )
    proposals = repository_proposal.find_proposals(user['uid'])
    return {"message": "Consultant created successfully", "data": proposals }
