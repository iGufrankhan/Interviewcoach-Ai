from fastapi import APIRouter, Request, Query
from interviewService.loader.get_data import InterviewDataLoader
from interviewService.QuestionGenService.Questiongen import QuestionGen
from interviewService.anwerService.AnwerListen import AnwerListen
from interviewService.Analyser.analysisanwer import AnalysisAnswer
from Models.resumeservice.resume_models import Resume_data
from Models.interviewservice.interview_models import InterviewSession
from Models.userReg.user import User
from utils.apierror import APIError
from utils.apiresponse import success_response, error_response
from utils.constant import GROQ_API_KEY
from interviewService.schema.interviewservice import StartInterviewRequest, SubmitAnswerRequest, SubmitInterviewRequest

router = APIRouter(
    prefix="/api/interview",
    tags=["interview"],
    responses={404: {"description": "Not found"}},
)


# ============= INTERVIEW ENDPOINTS =============

@router.post("/start")
async def start_interview(req: StartInterviewRequest, request: Request):
    user = request.state.user
    """Start a new interview session and generate 2 questions"""
    try:
        api_key = GROQ_API_KEY
        if not api_key:
            raise APIError(status_code=400, message="API key is required", error_code="MISSING_API_KEY")
        
        # Validate resume exists
        resume = await Resume_data.async_find_one(id=req.resume_id)
        if not resume:
            raise APIError(status_code=404, message=f"Resume with ID {req.resume_id} not found", error_code="RESUME_NOT_FOUND")
        
        # Generate questions from job description
        data_loader = InterviewDataLoader()
        context = data_loader.extract_job_info(req.job_description, api_key=api_key, resume_id=req.resume_id)
        
        question_gen = QuestionGen(api_key=api_key)
        questions = question_gen.generate_questions(context)
        
        # Create interview session
        user_obj = await User.async_find_one(email=user.email)
        interview = InterviewSession(
            user=user_obj,
            job_title=req.job_title,
            job_description=req.job_description,
            resume_id=req.resume_id,
            questions=questions
        )
        await interview.async_save()
        
        return success_response(
            message="Interview started",
            data={
                "session_id": str(interview.id),
                "questions": questions,
                "total_questions": len(questions)
            },
            status_code=201
        )
    
    except APIError:
        raise
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="START_INTERVIEW_ERROR",
            status_code=500
        )


@router.post("/submit-answer")
async def submit_answer(req: SubmitAnswerRequest, request: Request):
    """Submit an answer (audio or text) for current question"""
    user = request.state.user
    try:
        # Validate session exists and belongs to user
        interview = await db_find_one(InterviewSession, id=req.session_id)
        if not interview:
            raise APIError(status_code=404, message="Interview session not found", error_code="SESSION_NOT_FOUND")
        
        user_obj = await db_find_one(User, email=user.email)
        if interview.user != user_obj:
            raise APIError(status_code=403, message="Unauthorized", error_code="UNAUTHORIZED")
        
        # Handle audio input
        answer_text = request.answer
        if req.use_audio:
            try:
                audio_listener = AnwerListen()
                answer_text = audio_listener.listen()
                if not answer_text:
                    raise APIError(status_code=400, message="No audio captured", error_code="NO_AUDIO")
            except APIError as e:
                error_detail = e.detail.get("error") if isinstance(e.detail, dict) else str(e.detail)
                return error_response(
                    message=f"Audio failed: {error_detail}. Please type your answer.",
                    error_code="AUDIO_FAILED",
                    status_code=400
                )
        
        # Add answer to interview session
        current_answers_count = len(interview.answers)
        if current_answers_count >= len(interview.questions):
            raise APIError(status_code=400, message="All answers already submitted", error_code="ALL_ANSWERED")
        
        interview.answers.append(answer_text)
        await interview.async_save()
        
        return success_response(
            message=f"Answer {current_answers_count + 1} saved",
            data={
                "question_number": current_answers_count + 1,
                "total_questions": len(interview.questions),
                "remaining": len(interview.questions) - (current_answers_count + 1)
            },
            status_code=200
        )
    
    except APIError:
        raise
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="SUBMIT_ANSWER_ERROR",
            status_code=500
        )


@router.post("/submit")
async def submit_interview(req: SubmitInterviewRequest, request: Request):
    """Submit interview and analyze all answers, return score out of 10"""
    user = request.state.user
    try:
        interview = await InterviewSession.async_find_one(id=req.session_id)
        if not interview:
            raise APIError(status_code=404, message="Interview session not found", error_code="SESSION_NOT_FOUND")
        
        user_obj = await User.async_find_one(email=user.email)
        if interview.user != user_obj:
            raise APIError(status_code=403, message="Unauthorized", error_code="UNAUTHORIZED")
        
        # Check if all answers are provided
        if len(interview.answers) != len(interview.questions):
            raise APIError(
                status_code=400,
                message=f"Not all answers submitted. {len(interview.answers)}/{len(interview.questions)} answered",
                error_code="INCOMPLETE_ANSWERS"
            )
        
        # Analyze and score all answers
        api_key = GROQ_API_KEY
        analyzer = AnalysisAnswer(api_key)
        
        analysis_result = analyzer.batch_analyze_and_score(
            questions=interview.questions,
            answers=interview.answers,
            job_context=interview.job_description
        )
        
        # Save results to interview session
        interview.question_answers = analysis_result["question_answers"]
        interview.calculate_total_score()
        
        return success_response(
            message="Interview analyzed and scored",
            data={
                "session_id": str(interview.id),
                "total_score": analysis_result["total_score"],
                "score_out_of_10": analysis_result["total_score"],
                "percentage": analysis_result["percentage"],
                "average_per_question": analysis_result["average_score"],
                "question_answers": analysis_result["question_answers"]
            },
            status_code=200
        )
    
    except APIError:
        raise
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="SUBMIT_INTERVIEW_ERROR",
            status_code=500
        )


@router.get("/session/{session_id}")
async def get_interview_session(session_id: str, request: Request):
    """Get interview session details"""
    user = request.state.user
    try:
        interview = await InterviewSession.async_find_one(id=session_id)
        if not interview:
            raise APIError(status_code=404, message="Interview session not found", error_code="SESSION_NOT_FOUND")
        
        user_obj = await User.async_find_one(email=user.email)
        if interview.user != user_obj:
            raise APIError(status_code=403, message="Unauthorized", error_code="UNAUTHORIZED")
        
        return success_response(
            message="Interview session retrieved",
            data={
                "session_id": str(interview.id),
                "job_title": interview.job_title,
                "status": interview.status,
                "questions_count": len(interview.questions),
                "answers_count": len(interview.answers),
                "total_score": interview.total_score if interview.status == "completed" else None,
                "created_at": interview.created_at.isoformat(),
                "completed_at": interview.completed_at.isoformat() if interview.completed_at else None,
                "question_answers": interview.question_answers if interview.status == "completed" else []
            },
            status_code=200
        )
    
    except APIError:
        raise
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="GET_SESSION_ERROR",
            status_code=500
        )


@router.get("/sessions")
async def get_user_interviews(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (1-100)")
):
    """Get paginated interview sessions for user"""
    user = request.state.user
    try:
        user_obj = await User.async_find_one(email=user.email)
        
        total = await InterviewSession.async_count(user=user_obj)
        skip = (page - 1) * limit
        interviews = await InterviewSession.async_find(skip=skip, limit=limit, user=user_obj)
        
        interviews_list = [{
            "session_id": str(i.id),
            "job_title": i.job_title,
            "status": i.status,
            "total_score": i.total_score,
            "created_at": i.created_at.isoformat(),
            "completed_at": i.completed_at.isoformat() if i.completed_at else None
        } for i in interviews]
        
        return success_response(
            message="Interviews retrieved",
            data={
                "interviews": interviews_list,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": (total + limit - 1) // limit
                }
            },
            status_code=200
        )
    
    except Exception as e:
        return error_response(
            message=str(e),
            error_code="GET_INTERVIEWS_ERROR",
            status_code=500
        )


@router.post("/transcribe-audio")
async def transcribe_audio(req: dict, request: Request):
    """Transcribe audio blob to text
    
    Expected request body:
    {
        "audio_data": "base64_encoded_audio_string"
    }
    """
    user = request.state.user
    try:
        audio_data = req.get("audio_data")
        if not audio_data:
            raise APIError(
                status_code=400,
                message="audio_data is required",
                error_code="MISSING_AUDIO_DATA"
            )
        
        api_key = GROQ_API_KEY
        if not api_key:
            raise APIError(
                status_code=400,
                message="API key is required",
                error_code="MISSING_API_KEY"
            )
        
        # Import here to avoid circular imports
        from interviewService.anwerService.audio_transcriber import AudioTranscriber
        
        transcriber = AudioTranscriber(api_key=api_key)
        transcribed_text = transcriber.transcribe_audio(audio_data)
        
        return success_response(
            message="Audio transcribed successfully",
            data={
                "transcribed_text": transcribed_text
            },
            status_code=200
        )
    
    except APIError:
        raise
    except Exception as e:
        return error_response(
            message=f"Audio transcription failed: {str(e)}",
            error_code="TRANSCRIPTION_ERROR",
            status_code=500
        )
